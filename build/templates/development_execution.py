from .base import *


# ---------------------------------------------------------------- retrospective

class RetrospectiveMeeting(PptxSpec):
    @property
    def rel(self):
        return "development-execution/retrospective-meeting/retrospective-meeting.pptx"

    example = {"text": {
        "title": "Delivery team, 1–14 March 2026",
        "good": "Daily stand-ups kept blockers visible (+5); couriers app shipped on time (+3)",
        "bad": "Test environment was down for 3 days (+4); requirements changed twice after sprint start (+2)",
        "improve": "Book the test environment in advance (+4); write acceptance criteria before the sprint (+2)",
        "actions": "1. Agree a test-environment booking with QA: Ivan, by 20 March. 2. Add a Definition of Ready check to planning: Anna, by 27 March. Check: no environment downtime in the next sprint",
    }}

    def draw(self, prs, slide):
        header(slide, "RETROSPECTIVE", "{{title: team and period}}")
        cols = [
            ("What went well", "What's good?", GOOD, GOOD_BG,
             "{{good: what went well, one item per line}}"),
            ("What went badly", "What's bad?", BAD, BAD_BG,
             "{{bad: what got in the way, facts only}}"),
            ("How to improve", "How to improve?", ACCENT, ACCENT_BG,
             "{{improve: improvement ideas, one per line}}"),
        ]
        x, w, gap = 0.5, 3.95, 0.225
        for title, original, color, bg, token in cols:
            head = box(slide.shapes, x, 1.3, w, 0.6, fill=color, line=None)
            text(head, title, size=14, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            p = head.text_frame.add_paragraph()
            r = p.add_run()
            r.text = original
            r.font.size, r.font.name, r.font.color.rgb = Pt(10), FONT, WHITE
            text(box(slide.shapes, x, 1.9, w, 3.35, fill=bg, line=None), token, size=12)
            x += w + gap
        label(slide.shapes, 0.5, 5.4, 12.3, 0.35, "Actions before the next retrospective", size=12, bold=True, color=INK)
        text(box(slide.shapes, 0.5, 5.75, 12.3, 1.45),
             "{{actions: 1–3 actions with owner, date and check}}",
             size=12)


class TeamCanvas(PptxSpec):
    @property
    def rel(self):
        return "development-execution/team-canvas/team-canvas.pptx"

    example = {"text": {
        "title": "Delivery team, 6 people, 10 September 2026: reset after the release",
        "people": "Olga, product lead: slot picker; Dmitry, mobile lead: app; Anna, QA; Ilya, analyst",
        "common_goals": "Slot-to-order conversion 70% by 1 November; weekly-order retention 40% by Q1 2027",
        "personal_goals": "Olga: own the slot picker roadmap; Dmitry: cut app start time to 2 seconds",
        "values": "Buyers first: a late courier is our bug; ship small and check the data",
        "needs": "Olga needs weekly slot data; Anna needs test devices and 2 days before each release",
        "rules": "Stand-up at 10:00; decisions in the Thursday review; Friday release only after QA sign-off",
        "strengths": "Dark-store ops know-how, 2 years of slot data, a fast mobile release pipeline",
        "weaknesses": "Olga: too many tests in parallel; Dmitry: decisions not written down",
        "purpose": "Every Moscow buyer gets their slot on time",
    }}

    def draw(self, prs, slide):
        header(slide, "TEAM CANVAS", "{{title: team, date and occasion of the session}}")
        sh = slide.shapes
        # coordinates follow the original canvas (theteamcanvas.com), px of a 2000-px-wide image
        x0, y0, sx, sy = 0.5, 1.25, 12.33 / 1885, 5.5 / 1102
        X = lambda px: x0 + (px - 60) * sx
        Y = lambda py: y0 + (py - 228) * sy

        def block(l, t, r, b, tag, key, hint, agreed, tr=None, tl=None):
            fill = ACCENT_BG if agreed else WHITE
            box(sh, X(l), Y(t), X(r) - X(l), Y(b) - Y(t), fill=fill)
            left, right = X(tl or l), X(tr or r)
            label(sh, left + 0.06, Y(t) + 0.03, right - left - 0.12, 0.28, tag, size=10, bold=True, color=INK)
            tb = label(sh, left + 0.02, Y(t) + 0.3, right - left - 0.04, Y(b) - Y(t) - 0.34,
                       hint, size=9)
            return tb

        block(60, 228, 472, 1010, "1 · People and roles", "people", "{{people: name, role; who is responsible for what}}", True)
        block(472, 228, 1003, 602, "2 · Common goals", "common_goals",
              "{{common_goals: what we want to achieve together}}", True, tr=840)
        block(472, 602, 1003, 1010, "3 · Personal goals", "personal_goals",
              "{{personal_goals: goal, [name]: what each person wants for themselves}}", False, tr=850)
        block(1003, 228, 1533, 602, "5 · Values", "values", "{{values: principles the team stands for}}",
              True, tl=1160)
        block(1003, 602, 1533, 1010, "8 · Needs and expectations", "needs",
              "{{needs: needs of each person and team support}}", False, tl=1160)
        block(1533, 228, 1945, 1010, "9 · Rules & Activities", "rules",
              "{{rules: working rules: communication, decisions, rituals}}", True)
        block(60, 1010, 1003, 1330, "6 · Strengths and assets", "strengths",
              "{{strengths: skills and resources for the goals}}", False)
        block(1003, 1010, 1945, 1330, "7 · Weaknesses & Development Areas", "weaknesses",
              "{{weaknesses: own weaknesses and what holds the team back}}", False)
        hx, hy, hw, hh = 850, 430, 300, 290
        heart = box(sh, X(hx), Y(hy), hw * sx, hh * sy, fill=ACCENT, line=None, kind=MSO_SHAPE.HEART, name="Purpose")
        tb = text(heart, "{{purpose: why we do this, beyond the common goal}}", size=9, color=WHITE,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        tb.text_frame.margin_left = tb.text_frame.margin_right = Inches(0.25)
        tb.text_frame.margin_top = Inches(0.15)
        label(sh, X(hx), Y(hy) - 0.32, hw * sx, 0.32, "4 · Purpose", size=10, bold=True, color=ACCENT,
              align=PP_ALIGN.CENTER)
        ly = Y(1330) + 0.12
        box(sh, 0.5, ly + 0.07, 0.22, 0.16, fill=ACCENT_BG)
        label(sh, 0.75, ly, 4.2, 0.3, "agreed by the whole team", size=9, color=MUTED)
        box(sh, 3.3, ly + 0.07, 0.22, 0.16, fill=WHITE)
        label(sh, 3.55, ly, 4.0, 0.3, "each person can fill in for themselves", size=9, color=MUTED)
        label(sh, 6.9, ly, 5.93, 0.42, "After the Team Canvas by A. Ivanov and D. Voloshchuk, CC BY-SA 4.0",
              size=9, color=MUTED, align=PP_ALIGN.RIGHT)


class Sprint(XlsxSpec):
    @property
    def rel(self):
        return "development-execution/sprint/sprint.xlsx"

    example = {"text": {
        "title": "FreshDrop team, sprint 14, 3–14 August 2026",
        "goal": "ship the express slot reminder to 50% of buyers",
        "product_goal": "cut missed express slots from 22% to 10%",
        "unit": "story points",
        "review": "reminder demo to 6 buyers; decided to add an SMS fallback in sprint 15",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Sprint"

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        thin = Side(style="thin", color="C9CED6")

        def note(cell, hint, height=100):
            return comment(cell, hint, height=height, width=260)

        def dv_list(sheet, values, ref):
            dv = DataValidation(type="list", formula1=f'"{values}"', allow_blank=True, errorStyle="warning",
                                showErrorMessage=True, error=f"Values: {values}")
            dv.add(ref)
            sheet.add_data_validation(dv)

        def dv_number(sheet, *refs):
            dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                                errorStyle="warning", showErrorMessage=True, error="A non-negative number")
            for ref in refs:
                dv.add(ref)
            sheet.add_data_validation(dv)

        ws["A1"] = "Sprint: {{title: team, sprint number, start and end dates}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:I1")
        top = [
            (2, "Sprint goal:", "{{goal: sprint goal and why it matters now}}", bold, 32),
            (3, "Product goal:", "{{product_goal: what the sprint leads towards}}", regular, 18),
        ]
        for r, name, token, font, height in top:
            ws.cell(r, 1, name).font = muted
            c = ws.cell(r, 3, token)
            c.font = font
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.merge_cells(f"C{r}:I{r}")
            ws.row_dimensions[r].height = height
        ws["A4"] = "Sprint limit:"
        ws["A4"].font = muted
        ws["C4"].font, ws["C4"].fill = bold, calc_fill
        note(ws["C4"], "How much the team is ready to take, in the units of the \"Estimate\" column: capacity accounting for time off "
                       "and the results of past sprints. A guide, not a hard limit.")
        ws["D4"] = "{{unit: estimate unit}}"
        ws["D4"].font = muted
        ws.merge_cells("D4:E4")
        ws["F4"] = "Goal achieved:"
        ws["F4"].font = muted
        ws["G4"].font, ws["G4"].fill = bold, calc_fill
        note(ws["G4"], "Filled in at the sprint review: yes, partly or no.")
        dv_list(ws, "yes,partly,no", "G4")
        ws["A5"] = "Review outcome:"
        ws["A5"].font = muted
        ws["C5"] = "{{review: what was shown and decided next}}"
        ws["C5"].alignment = Alignment(wrap_text=True, vertical="top")
        ws["C5"].font = regular
        ws.merge_cells("C5:I5")
        ws.row_dimensions[5].height = 32

        headers = [
            ("#", "Calculated automatically.", 5),
            ("Item", "An item from the product's shared work list, taken into the sprint. The most important at the top.", 40),
            ("For the goal", "\"yes\" — the item is needed for the sprint goal. The other items are done if there is capacity.", 9),
            ("How we will do it", "The plan: subtasks or steps to a finished result.", 34),
            ("Who", "Who takes the item. The team distributes the work itself.", 14),
            ("Estimate", "An estimate by those who will do the work, in the units from row 4.", 9),
            ("Source", "\"planned\" — taken at planning; \"added\" — came in during the sprint.", 11),
            ("Done", "\"yes\" — the item meets the team's definition of done. Filled in at the end of the sprint.", 9),
            ("What next", "For unfinished items: return to the shared list, carry over to the next sprint, cancel — and why.", 28),
        ]
        hr = 7
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(hr, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            note(c, hint)
            ws.column_dimensions[c.column_letter].width = width
        ws.column_dimensions["A"].width = 16
        ws.row_dimensions[hr].height = 30

        first, last = hr + 1, hr + 50
        for r in range(first, last + 1):
            ws.cell(r, 1, f'=IF(B{r}="","",COUNTA($B${first}:B{r}))').fill = calc_fill
            for c in range(1, 10):
                ws.cell(r, c).font = regular
                ws.cell(r, c).alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = ws.cell(first, 3)
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'Sprint'!$B${first}")

        rng = lambda col: f"${col}${first}:${col}${last}"
        ws["K7"] = "Sprint results"
        ws["K7"].font, ws["K7"].fill = bold, head_fill
        ws["L7"].fill = head_fill
        ws.column_dimensions["K"].width = 34
        ws.column_dimensions["L"].width = 12
        stats = [
            ("Items", f'=COUNTA({rng("B")})', "0", "How many items are in the sprint."),
            ("Of them for the goal", f'=COUNTIF({rng("C")},"yes")', "0",
             "Zero — there is no goal, the sprint became a task list. All — the goal most likely just restates the items."),
            ("Taken at planning", f'=SUMIF({rng("G")},"planned",{rng("F")})', "0.0", "The sum of estimates of \"planned\" items."),
            ("Load vs limit", '=IF(OR($C$4="",$C$4=0),"",L10/$C$4)', "0%",
             "What was taken at planning divided by the limit. Above 100% — the team promises more than it has delivered before."),
            ("Added during the sprint", f'=SUMIF({rng("G")},"added",{rng("F")})', "0.0",
             "Work that arrived after planning. Its volume hints at how much reserve to leave."),
            ("Not done", f'=SUMPRODUCT(({rng("B")}<>"")*({rng("H")}<>"yes"),{rng("F")})', "0.0",
             "The sum of estimates of items without \"yes\" in the \"Done\" column."),
            ("Share unfinished", '=IF(L10+L12=0,"",L13/(L10+L12))', "0%",
             "Not done divided by everything taken and added."),
            ("Goal items not done", f'=SUMPRODUCT(({rng("C")}="yes")*({rng("H")}<>"yes"))', "0",
             "More than zero at the end of the sprint — the goal is at risk, even if the rest is done."),
        ]
        for i, (name, formula, fmt, hint) in enumerate(stats, start=8):
            a = ws.cell(i, 11, name)
            a.font = regular
            note(a, hint, 90)
            b = ws.cell(i, 12, formula)
            b.font, b.fill = bold, calc_fill
            b.number_format = fmt

        dv_list(ws, "yes,no", f"C{first}:C{last}")
        dv_list(ws, "planned,added", f"G{first}:G{last}")
        dv_list(ws, "yes,no", f"H{first}:H{last}")
        dv_number(ws, f"F{first}:F{last}", "C4")

        hs = wb.create_sheet("History")
        hs["A1"] = "Sprint history"
        hs["A1"].font = Font(name=FONT, bold=True, size=14)
        hs["A2"].font = muted
        hhead = [
            ("Sprint", "Number or dates.", 14),
            ("Sprint goal", "The goal statement.", 40),
            ("Goal achieved", "yes, partly or no.", 12),
            ("Limit", "The limit the team agreed on at planning.", 9),
            ("Taken", "Taken at planning, in estimate units.", 9),
            ("Added", "Added during the sprint, including growth of estimates.", 11),
            ("Not done", "Removed from the sprint or not brought to done by its end.", 11),
            ("Done", "Calculated automatically: taken + added − not done.", 10),
            ("Share unfinished", "Calculated automatically: not done / (taken + added).", 14),
            ("All done", "Calculated automatically: \"yes\" if not done is 0.", 11),
        ]
        for i, (title, hint, width) in enumerate(hhead, start=1):
            c = hs.cell(4, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            note(c, hint, 70)
            hs.column_dimensions[c.column_letter].width = width
        hs.row_dimensions[4].height = 30
        h1, h2 = 5, 30
        for r in range(h1, h2 + 1):
            for c in range(1, 11):
                hs.cell(r, c).font = regular
                hs.cell(r, c).alignment = Alignment(wrap_text=True, vertical="top")
            done = hs.cell(r, 8, f'=IF(OR(E{r}="",G{r}=""),"",E{r}+N(F{r})-G{r})')
            done.fill, done.number_format = calc_fill, "0.0"
            g = hs.cell(r, 9, f'=IF(OR(E{r}="",G{r}=""),"",IF(E{r}+N(F{r})=0,"",G{r}/(E{r}+N(F{r}))))')
            g.fill, g.number_format = calc_fill, "0%"
            hs.cell(r, 10, f'=IF(OR(E{r}="",G{r}=""),"",IF(G{r}=0,"yes","no"))').fill = calc_fill
        dv_list(hs, "yes,partly,no", f"C{h1}:C{h2}")
        dv_number(hs, f"D{h1}:G{h2}")
        hs["L4"] = "Over the last 10 sprints"
        hs["L4"].font, hs["L4"].fill = bold, head_fill
        hs["M4"].fill = head_fill
        hs.column_dimensions["L"].width = 34
        hs.column_dimensions["M"].width = 10
        hist = [
            ("Sprints in history", f"=COUNTA(A{h1}:A{h2})", "0", "How many sprints are recorded."),
            ("Goal achieved", f'=COUNTIF(C{h1}:C{h2},"yes")', "0", "In how many sprints the goal was fully achieved."),
            ("Everything taken was done", f'=COUNTIF(J{h1}:J{h2},"yes")', "0",
             "The benchmark of M. Cohn as retold by Rosbank: in 8 of the last 10 sprints the team did everything it promised."),
        ]
        for i, (name, formula, fmt, hint) in enumerate(hist, start=5):
            a = hs.cell(i, 12, name)
            a.font = regular
            note(a, hint, 90)
            b = hs.cell(i, 13, formula)
            b.font, b.fill = bold, calc_fill
            b.number_format = fmt
        hs["L9"].font = muted
        hs.freeze_panes = "B5"


class StandUpMeeting(PptxSpec):
    @property
    def rel(self):
        return "development-execution/stand-up-meeting/stand-up-meeting.pptx"

    example = {"text": {
        "title": "Delivery team, 6 people, agreed 1 September 2026",
        "purpose": "slot reminders live for 50% of buyers; progress checked every day",
        "when": "10:00 every day, video call link pinned in the team chat",
        "length": "Limit 15 minutes; actual average 11 minutes",
        "people": "6 people: 4 developers, QA and the product lead",
        "facilitator": "Scrum master Ilya; the role rotates each sprint",
        "agenda": "By board: blocked cards first, then cards in review, then the rest by priority",
        "prep": "Each person moves their cards on the board by 09:50 and marks blockers",
        "offline": "Topics over 2 minutes go offline; the people involved stay after the call",
        "outcome": "Plan for the day and help requests, recorded in the team chat",
        "check": "Length measured weekly; usefulness asked in the retro, reviewed each sprint",
        "decision": "From 1 October: a 15-minute cap, blockers first, and no status round",
    }}

    def draw(self, prs, slide):
        header(slide, "STAND-UP MEETING · STAND-UP AGREEMENT",
               "{{title: team, size and date of the agreement}}")
        sh = slide.shapes
        left, full, g = 0.5, 12.33, 0.1

        def block(x, y, w, h, tag, key, hint, fill=WHITE, line=LINE, size=10):
            tb = text(box(sh, x, y, w, h, fill=fill, line=line), hint, size=size)
            tb.text_frame.margin_top = Inches(0.36)
            label(sh, x + 0.08, y + 0.03, w - 0.16, 0.32, tag, size=10, bold=True, color=INK)

        tb = text(box(sh, left, 1.25, full, 0.6, fill=ACCENT_BG, line=None),
                  "Sprint goal: {{purpose: goal the progress is checked against}}",
                  size=11, anchor=MSO_ANCHOR.MIDDLE)
        tb.text_frame.margin_left = Inches(1.6)
        label(sh, left + 0.1, 1.25, 1.4, 0.6, "Why", size=12, bold=True, anchor=MSO_ANCHOR.MIDDLE)

        y1, h1 = 1.95, 1.3
        qw = (full - 3 * g) / 4
        for i, (tag, key, hint) in enumerate([
            ("When and where", "when", "{{when: time, place or link}}"),
            ("Length", "length", "{{length: limit in minutes and actual average}}"),
            ("Who", "people", "{{people: who takes part and how many}}"),
            ("Facilitator", "facilitator", "{{facilitator: who leads and how the role rotates}}"),
        ]):
            block(left + i * (qw + g), y1, qw, h1, tag, key, hint)

        y2, h2 = y1 + h1 + g, 2.0
        lw = 5.6
        block(left, y2, lw, h2, "Order of discussion", "agenda",
              "{{agenda: order of topics: by board or by person}}",
              fill=ACCENT_BG, line=None)
        rw = (full - lw - 2 * g) / 2
        block(left + lw + g, y2, rw, h2, "Preparation", "prep", "{{prep: what each person does before the meeting}}")
        block(left + lw + g + rw + g, y2, rw, h2, "What we take offline", "offline",
              "{{offline: how long discussions are moved, and who stays}}")

        y3, h3 = y2 + h2 + g, 1.55
        tw = (full - 2 * g) / 3
        block(left, y3, tw, h3, "Meeting outcome", "outcome", "{{outcome: day plan and help requests: where recorded}}")
        block(left + tw + g, y3, tw, h3, "How we check the format", "check",
              "{{check: how the format is checked, and when}}")
        block(left + 2 * (tw + g), y3, tw, h3, "Decision", "decision", "{{decision: format change, date and reason}}",
              fill=ACCENT_BG, line=None)


class KanbanBoard(PptxSpec):
    @property
    def rel(self):
        return "development-execution/kanban-board/kanban-board.pptx"

    example = {"text": {
        "title": "FreshDrop mobile team: delivery board for the buyer app, September 2026",
        "c1": "Backlog",
        "c2": "Ready",
        "c3": "In progress",
        "c4": "Code review",
        "c5": "QA",
        "c6": "Done",
        "w1": "—",
        "w2": "8",
        "w3": "4",
        "w4": "3",
        "w5": "3",
        "w6": "—",
        "x1": "Story has criteria and design",
        "x2": "Developer has capacity, WIP below limit",
        "x3": "PR opened, tests pass",
        "x4": "2 approvals, CI green",
        "x5": "Checked on staging, no open bugs",
        "x6": "Released to all Moscow users",
        "bounds": "Started when a card leaves Ready; finished in Done; lead time counted from creation",
        "lanes": "Expedite lane for production bugs, one card at a time; features and QA bugs in standard lanes",
        "blocked": "Red flag with reason and owner; the team lead removes it by the next stand-up",
        "replenish": "Every Monday product adds up to 10 cards to Backlog; the team pulls 8 into Ready",
        "metrics": "WIP 14 on average; throughput 9 cards a week; median cycle time 3.1 days; oldest card 6 days (checked daily)",
        "sle": "85% of cards done in 5 days or faster; July: 78%",
        "decision": "Code review is the bottleneck: cards wait 1.8 days. From 1 October: pair review for cards over 3 files; check the wait time in 2 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "KANBAN BOARD · BOARD AND FLOW RULES",
               "{{title: team, what work goes through the board, date}}")
        sh = slide.shapes
        left, full, g = 0.5, 12.33, 0.1
        lw, n = 1.55, 6
        gx = left + lw + g
        cw = (left + full - gx) / n
        rows = [
            ("Column", "c", ["{{c1: stage name}}", "{{c2: stage name}}", "{{c3: stage name}}", "{{c4: stage name}}", "{{c5: stage name}}", "{{c6: stage name}}"], 0.42),
            ("WIP limit", "w", ["{{w1: cards at once}}", "{{w2: cards at once}}", "{{w3: cards at once}}", "{{w4: cards at once}}", "{{w5: cards at once}}", "{{w6: cards at once}}"], 0.42),
            ("Can pull on when", "x", ["{{x1: exit rule for the stage}}", "{{x2: exit rule for the stage}}", "{{x3: exit rule for the stage}}", "{{x4: exit rule for the stage}}", "{{x5: exit rule for the stage}}", "{{x6: exit rule for the stage}}"], 1.1),
        ]
        y = 1.25
        for tag, key, hint, h in rows:
            label(sh, left, y, lw, h, tag, size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
            for i in range(n):
                fill, line, color, bold = WHITE, LINE, INK, False
                if key == "c":
                    fill, line, color, bold = ACCENT, None, WHITE, True
                elif key == "w":
                    fill, line = ACCENT_BG, None
                text(box(sh, gx + i * cw + 0.03, y, cw - 0.06, h, fill=fill, line=line),
                     hint[i], size=9, bold=bold, color=color,
                     anchor=MSO_ANCHOR.TOP if key == "x" else MSO_ANCHOR.MIDDLE)
            y += h + 0.06

        def block(x, y, w, h, tag, key, hint, fill=WHITE, line=LINE, size=10):
            tb = text(box(sh, x, y, w, h, fill=fill, line=line), hint, size=size)
            tb.text_frame.margin_top = Inches(0.36)
            label(sh, x + 0.08, y + 0.03, w - 0.16, 0.32, tag, size=10, bold=True, color=INK)

        y1, h1 = y + 0.1, 1.5
        qw = (full - 3 * g) / 4
        for i, (tag, key, hint) in enumerate([
            ("Start and finish", "bounds", "{{bounds: column where work starts, column where it ends}}"),
            ("Lanes and urgent", "lanes", "{{lanes: lanes and classes of work, expedite rules}}"),
            ("Blockers", "blocked", "{{blocked: how blocked work is marked and unblocked}}"),
            ("Replenishment", "replenish", "{{replenish: work entering the first column: when, how much}}"),
        ]):
            block(left + i * (qw + g), y1, qw, h1, tag, key, hint)

        y2, h2 = y1 + h1 + g, 1.75
        mw = 4.3
        block(left, y2, mw, h2, "Flow metrics", "metrics",
              "{{metrics: flow metrics: values, period, where we look}}")
        sw = 2.9
        block(left + mw + g, y2, sw, h2, "Expected lead time", "sle", "{{sle: service level: share of cards and days}}")
        block(left + mw + sw + 2 * g, y2, full - mw - sw - 2 * g, h2, "Bottleneck and decision", "decision",
              "{{decision: bottleneck and decision, and how it is checked}}",
              fill=ACCENT_BG, line=None)
