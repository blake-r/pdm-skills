from .base import *


class DefinitionOfDone(PptxSpec):
    @property
    def rel(self):
        return "development-handoff/definition-of-done/definition-of-done.pptx"

    example = {"text": {
        "title": "Delivery team, FreshDrop app, agreed 1 September 2026",
        "scope": "all user stories in the app; done = live for buyers and the support team knows it",
        "k1": "Code merged to main, build green",
        "k2": "Unit tests cover new logic at 80%+",
        "k3": "Reviewed and approved by 2 developers",
        "k4": "Passes QA on staging, no open bugs",
        "k5": "Works on iOS and Android, last 2 versions",
        "k6": "Accessibility check passed",
        "k7": "Analytics events tracked",
        "k8": "Support has a reply template",
        "h1": "CI pipeline; the author checks before merge",
        "h2": "coverage report in CI; reviewer checks the diff",
        "h3": "GitHub approvals; reviewer lists risks in the PR",
        "h4": "QA lead signs the ticket; 0 open bugs of any severity",
        "h5": "device farm run; QA lead checks the release notes",
        "h6": "designer runs the checklist; screen reader test on the main flow",
        "h7": "analyst checks the events in the dashboard within 24 hours",
        "h8": "support lead checks the help center article before release",
        "auto": "Build, unit tests, lint and the release checklist in Jira block the merge by themselves",
        "fail": "Back to In progress; a part can ship behind a feature flag if the rest is green",
        "review": "Every 2 sprints in the retro; the team lead makes the edits, the team votes",
        "agreed": "Mobile team lead, QA lead and product owner; based on the company engineering standard",
        "decision": "From 1 October for all stories; we add the accessibility check and drop the manual smoke test",
    }}

    def draw(self, prs, slide):
        header(slide, "DEFINITION OF DONE · DEFINITION OF DONE AGREEMENT",
               "{{title: team, product and date of the agreement}}")
        sh = slide.shapes
        left, full, g = 0.5, 12.33, 0.1

        def block(x, y, w, h, tag, key, hint, fill=WHITE, line=LINE, size=10):
            tb = text(box(sh, x, y, w, h, fill=fill, line=line), hint, size=size)
            tb.text_frame.margin_top = Inches(0.36)
            label(sh, x + 0.08, y + 0.03, w - 0.16, 0.32, tag, size=10, bold=True, color=INK)

        tb = text(box(sh, left, 1.25, full, 0.55, fill=ACCENT_BG, line=None),
                  "{{scope: work covered and what done means}}",
                  size=11, anchor=MSO_ANCHOR.MIDDLE)
        tb.text_frame.margin_left = Inches(1.6)
        label(sh, left + 0.1, 1.25, 1.4, 0.55, "Applies to", size=12, bold=True, anchor=MSO_ANCHOR.MIDDLE)

        cw1, cw2 = 3.3, 4.5
        x2 = left + cw1 + g
        y = 1.9
        for x, w, tag in [(left, cw1, "Done criterion"), (x2, cw2, "How we check and who")]:
            text(box(sh, x, y, w, 0.3, fill=ACCENT, line=None), tag, size=10, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
        y += 0.35
        rh = 0.42
        for i in range(8):
            text(box(sh, left, y, cw1, rh, fill=WHITE, line=LINE), "{{k%d: criterion, checkable yes or no}}" % (i + 1),
                 size=9, bold=True, anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x2, y, cw2, rh, fill=WHITE, line=LINE),
                 "{{h%d: how it is checked and by whom}}" % (i + 1), size=9, anchor=MSO_ANCHOR.MIDDLE)
            y += rh + 0.05
        ybot = y

        rx = left + cw1 + cw2 + 2 * g
        rw = left + full - rx
        rbh = (ybot - 1.9 - 2 * g) / 3
        for i, (tag, key, hint) in enumerate([
            ("Automatic checks", "auto", "{{auto: what blocks release by itself}}"),
            ("Criteria not met", "fail", "{{fail: where work goes back, and what may ship}}"),
            ("How we review", "review", "{{review: review frequency, triggers and editors}}"),
        ]):
            block(rx, 1.9 + i * (rbh + g), rw, rbh, tag, key, hint)

        y3 = ybot + g - 0.05
        h3 = 7.3 - y3
        hw = (full - g) / 2
        block(left, y3, hw, h3, "Who agreed", "agreed", "{{agreed: roles that accepted, and standard}}")
        block(left + hw + g, y3, hw, h3, "Decision", "decision", "{{decision: from which date, what changes, and why}}",
              fill=ACCENT_BG, line=None)
