# /// script
# requires-python = ">=3.10"
# dependencies = ["python-pptx>=1.0"]
# ///
"""Rough layout check of a filled deck. No rendering: estimates from the text and the boxes.

Usage:
    uv run check_pptx.py DECK.pptx

Reports, one line per problem, and exits with 1 if there are any:
- a shape that extends beyond the slide edges;
- text that probably does not fit its box (estimated lines x line height);
- a word longer than a line of its box, which breaks in the middle;
- a template token ({{key}}) left in the text.

The estimate is coarse: it uses the average glyph width of the text's font size
(wider for bold), the same rule as fill_pptx.py. Treat each report as a
place to look, not as proof. Slides are not rendered or viewed.
"""

import sys
import textwrap

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

TOKEN = "{{"
DEFAULT_PT = 18
GLYPH = 0.52          # average glyph width, share of the font size (Arial, mixed Latin and Cyrillic)
GLYPH_BOLD = 0.58
LINE = 1.2            # line height, share of the font size
INSET_W, INSET_H = 14, 7.2   # default text box insets, pt


def iter_shapes(shapes):
    for shape in shapes:
        yield shape
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from iter_shapes(shape.shapes)


def frame_font(tf):
    for p in tf.paragraphs:
        for r in p.runs:
            if r.text.strip():
                size = r.font.size.pt if r.font.size else DEFAULT_PT
                return size, bool(r.font.bold)
    return DEFAULT_PT, False


def estimate(tf, width_pt, height_pt):
    """Return (height needed in pt, longest word, its line length) for the frame, paragraph by paragraph."""
    needed = 0.0
    longest, longest_per_line, longest_size = "", 1, DEFAULT_PT
    for p in tf.paragraphs:
        size, bold = DEFAULT_PT, False
        for r in p.runs:
            if r.text.strip():
                size = r.font.size.pt if r.font.size else DEFAULT_PT
                bold = bool(r.font.bold)
                break
        glyph = GLYPH_BOLD if bold else GLYPH
        per_line = max(1, int(width_pt / (size * glyph)))
        lines = len(textwrap.wrap(p.text, per_line, break_long_words=True)) or 1
        needed += lines * size * LINE
        for w in p.text.split():
            if len(w) > len(longest):
                longest, longest_per_line, longest_size = w, per_line, size
    return needed, longest, longest_per_line, longest_size


def check_deck(path):
    prs = Presentation(path)
    sw, sh = prs.slide_width, prs.slide_height
    problems = []
    for n, slide in enumerate(prs.slides, start=1):
        for shape in iter_shapes(slide.shapes):
            name = f"slide {n}, {shape.name!r}"
            if shape.left is not None and shape.width is not None:
                if shape.left < 0 or shape.top < 0 or shape.left + shape.width > sw or shape.top + shape.height > sh:
                    problems.append(f"{name}: extends beyond the slide edge")
            frames = []
            if shape.has_text_frame:
                frames.append(shape.text_frame)
            if getattr(shape, "has_table", False) and shape.has_table:
                frames += [c.text_frame for row in shape.table.rows for c in row.cells]
            for tf in frames:
                text = tf.text
                if TOKEN in text:
                    problems.append(f"{name}: template token left in text: {text[:60]!r}")
                if not text.strip() or not shape.width or not shape.height:
                    continue
                width_pt = shape.width / 12700 - INSET_W
                height_pt = shape.height / 12700 - INSET_H
                if tf._txBody.bodyPr.get("vert", "").startswith("vert"):  # rotated text runs along the height
                    width_pt, height_pt = shape.height / 12700 - INSET_W, shape.width / 12700 - INSET_H
                needed, longest, per_line, size = estimate(tf, width_pt, height_pt)
                if len(longest) > per_line:
                    problems.append(
                        f"{name}: word {longest!r} is longer than a line ({per_line} chars at {size:g} pt) and will break mid-word"
                    )
                if needed > height_pt:
                    problems.append(
                        f"{name}: text needs about {needed:.0f} pt, the box holds {height_pt:.0f} pt; text may overflow"
                    )
    return problems


def main():
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        sys.exit(2)
    problems = check_deck(sys.argv[1])
    if not problems:
        print("ok: no layout problems found by the estimate")
        return
    for p in problems:
        print(p)
    sys.exit(1)


if __name__ == "__main__":
    main()
