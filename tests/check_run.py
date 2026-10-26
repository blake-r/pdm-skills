# /// script
# requires-python = ">=3.10"
# dependencies = ["python-pptx>=1.0"]
# ///
"""Mechanical part of the run checklist for a pdm-brief run. No LLM, no network.

Usage (from the repository root):
    uv run tests/check_run.py <run folder>

The run folder holds the output of one pdm-brief run: deck.pptx and brief.md.
Checks (numbers refer to the run checklist in tests/README.md):
  1. the deck has a title slide, a sources slide and an assumptions slide;
  2. check_pptx.py reports no problems and no {{ token is left;
  3. brief.md exists and is not empty;
  4. when brief.md cites web sources (a link), it contains a four-digit year and,
     if written in English, names a source tier (official / corporate / other);
     a brief in another language is checked for the year only;
  5. the assumptions slide has no unfilled token.
What needs reading (invented numbers, Selection-table fit, order of questions)
stays with the human or model reviewer: see the rubric in tests/scenarios.md.

Exits with 0 when every check passes, with 1 otherwise.
"""

import re
import subprocess
import sys
from pathlib import Path

from pptx import Presentation

ROOT = Path(__file__).resolve().parent.parent
MARKERS = {
    "title": "DECK · TITLE",
    "sources": "SOURCES AND DATA",
    "assumptions": "ASSUMPTIONS",
}


def slide_texts(deck):
    for slide in Presentation(deck).slides:
        yield [sh.text_frame.text for sh in slide.shapes if sh.has_text_frame]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        sys.exit(2)
    run = Path(args[0])
    problems = []

    deck = run / "deck.pptx"
    brief = run / "brief.md"
    if not deck.is_file():
        problems.append(f"missing {deck}")
    if not brief.is_file():
        problems.append(f"missing {brief}")
    if problems:
        print("\n".join("FAIL: " + p for p in problems))
        sys.exit(1)

    slides = list(slide_texts(deck))
    heads = [" ".join(t) for t in slides]
    for name, marker in MARKERS.items():
        if not any(marker in h for h in heads):
            problems.append(f"no {name} slide (marker '{marker}')")
    if len(slides) < 4:
        problems.append(f"only {len(slides)} slides: expected title, tool slide(s), sources, assumptions")

    left = [i for i, h in enumerate(heads, 1) if "{{" in h]
    if left:
        problems.append(f"template tokens left on slides {left}")

    r = subprocess.run(["uv", "run", "scripts/check_pptx.py", str(deck)], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        problems.append("check_pptx.py: " + (r.stdout + r.stderr).strip().replace("\n", " | "))

    text = brief.read_text(encoding="utf-8")
    if not text.strip():
        problems.append("brief.md is empty")
    elif "http" in text and not re.search(r"\b(19|20)\d\d\b", text):
        problems.append("brief.md has no year: facts need an edition or reading date")
    elif "http" in text and len(re.findall(r"[А-Яа-яЁё]", text)) < 50 and not re.search(r"official|corporate|other", text, re.I):
        problems.append("brief.md names no source tier (official / corporate / other)")

    for i, h in enumerate(heads, 1):
        if MARKERS["assumptions"] in h and "{{" in h:
            problems.append(f"assumptions slide {i} has an unfilled token")

    for p in problems:
        print("FAIL:", p)
    if problems:
        sys.exit(1)
    print(f"run ok: {len(slides)} slides, brief.md {len(text.split())} words")


if __name__ == "__main__":
    main()
