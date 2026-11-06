from .base import *


# ---------------------------------------------------------------- pdm-brief deck slides

class IntakeTitle(PptxSpec):
    @property
    def rel(self):
        return "pdm-brief/title.pptx"

    def draw(self, prs, slide):
        label(slide.shapes, 0.5, 0.3, 12.3, 0.35, "DECK · TITLE", size=12, bold=True, color=ACCENT)
        text(box(slide.shapes, 0.5, 2.2, 12.3, 1.6), "{{title: the task in one line}}",
             size=34, bold=True, anchor=MSO_ANCHOR.BOTTOM)
        box(slide.shapes, 0.5, 3.95, 2.4, 0.06, fill=ACCENT, line=None)
        text(box(slide.shapes, 0.5, 4.2, 12.3, 0.8), "{{subtitle: audience and the decision the deck prepares}}", size=16)
        label(slide.shapes, 0.5, 6.2, 6.0, 0.35, "Date", size=11, bold=True, color=MUTED)
        text(box(slide.shapes, 0.5, 6.5, 6.0, 0.45), "{{date: date of the deck}}", size=12)


class IntakeSources(PptxSpec):
    @property
    def rel(self):
        return "pdm-brief/sources.pptx"

    def draw(self, prs, slide):
        header(slide, "SOURCES AND DATA", "{{title: what the deck rests on}}")
        cols = [
            ("Official", "Regulator or government; with edition and date", ACCENT, ACCENT_BG,
             "{{sources_official: act or page, edition date, date read, what it confirms}}"),
            ("Corporate", "Company's own site; facts about that company only", INK, None,
             "{{sources_corporate: page, date read, what it confirms}}"),
            ("Other", "News, blogs, aggregators; leads, not confirmation", MUTED, None,
             "{{sources_other: outlet, date, what it says, not confirmed}}"),
        ]
        x, w, gap = 0.5, 3.95, 0.225
        for title, sub, color, bg, token in cols:
            head = box(slide.shapes, x, 1.3, w, 0.6, fill=color, line=None)
            text(head, title, size=14, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            p = head.text_frame.add_paragraph()
            r = p.add_run()
            r.text = sub
            r.font.size, r.font.name, r.font.color.rgb = Pt(10), FONT, WHITE
            text(box(slide.shapes, x, 1.9, w, 3.2, fill=bg, line=LINE), token, size=11)
            x += w + gap
        label(slide.shapes, 0.5, 5.3, 6.0, 0.35, "Data used", size=12, bold=True, color=INK)
        text(box(slide.shapes, 0.5, 5.65, 6.0, 1.45, line=None),
             "{{data_used: local files and data with dates; the ticket or brief as a source}}", size=11)
        label(slide.shapes, 6.8, 5.3, 6.0, 0.35, "Not confirmed", size=12, bold=True, color=BAD)
        text(box(slide.shapes, 6.8, 5.65, 6.0, 1.45, line=None),
             "{{not_confirmed: facts without an official source, and why}}", size=11)


class IntakeConclusions(PptxSpec):
    @property
    def rel(self):
        return "pdm-brief/conclusions.pptx"

    def draw(self, prs, slide):
        header(slide, "CONCLUSIONS", "{{title: the answer in one line}}")
        rows = [
            ("Decision", "{{decision: what to do, by whom, by when}}", ACCENT_BG, ACCENT, 1.3, 1.25),
            ("Why", "{{why: the two or three facts that decide it, with tier and date}}", None, INK, 2.7, 1.55),
            ("Risks and assumptions", "{{risks: the weakest assumptions and how to check them}}", None, INK, 4.4, 1.45),
            ("Open questions", "{{open_questions: what must be settled before the next step, and who settles it}}",
             None, INK, 6.0, 1.15),
        ]
        for tag, token, bg, color, y, h in rows:
            head = box(slide.shapes, 0.5, y, 2.8, h, fill=color if bg is None else bg, line=None)
            text(head, tag, size=13, bold=True, color=WHITE if bg is None else ACCENT, anchor=MSO_ANCHOR.MIDDLE)
            text(box(slide.shapes, 3.45, y, 9.38, h, line=LINE), token, size=12, anchor=MSO_ANCHOR.MIDDLE)


class IntakeAssumptions(PptxSpec):
    @property
    def rel(self):
        return "pdm-brief/assumptions.pptx"

    def draw(self, prs, slide):
        header(slide, "ASSUMPTIONS", "{{title: what was taken as given without the PM's answer}}")
        cols = [
            ("Not answered", "Question the PM did not settle", ACCENT, ACCENT_BG,
             "{{questions: each open question, one per line}}"),
            ("Assumed instead", "What the deck takes as true until checked", INK, None,
             "{{assumptions: the assumption behind each question, same order}}"),
            ("Who confirms", "Owner and the moment it must be settled", MUTED, None,
             "{{confirm: owner and by when, same order}}"),
        ]
        x, w, gap = 0.5, 3.95, 0.225
        for title, sub, color, bg, token in cols:
            head = box(slide.shapes, x, 1.3, w, 0.6, fill=color, line=None)
            text(head, title, size=14, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            p = head.text_frame.add_paragraph()
            r = p.add_run()
            r.text = sub
            r.font.size, r.font.name, r.font.color.rgb = Pt(10), FONT, WHITE
            text(box(slide.shapes, x, 1.9, w, 4.3, fill=bg, line=LINE), token, size=11)
            x += w + gap
        label(slide.shapes, 0.5, 6.35, 12.33, 0.3,
              "Each assumption stays in the deck until its owner confirms or rejects it", size=10, color=MUTED)
