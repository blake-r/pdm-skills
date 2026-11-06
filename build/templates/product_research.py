from .base import *


class StakeholdersMatrix(PptxSpec):
    @property
    def rel(self):
        return "product-research/stakeholders-matrix/stakeholders-matrix.pptx"

    example = {"text": {
        "title": "Express pilot in Moscow: stakeholders, July 2026",
        "keep_satisfied": "head of finance: approves the budget, sees little of daily work",
        "manage_closely": "ops director: runs couriers; reviews the pilot every week",
        "monitor": "local media: low impact; coverage checked monthly",
        "keep_informed": "couriers: routes change; told by push and at the weekly meeting",
        "decision": "ops director decides; finance signs off the budget",
        "result": "pilot routes approved 1 July; courier churn checked after 6 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "STAKEHOLDERS MATRIX", "{{title: product, project or decision, date}}")
        sh = slide.shapes
        # Influence of the stakeholder on the product runs up, the product's impact on the stakeholder runs right
        mx, my, mw, mh = 0.95, 1.35, 7.9, 5.5
        cw, ch = mw / 2, mh / 2

        def cell(col, row, tag, key, hint, fill=WHITE, tag_color=INK):
            x, y = mx + col * cw, my + row * ch
            tb = text(box(sh, x, y, cw, ch, fill=fill), f"{{{{{key}: {hint}}}}}", size=10)
            tb.text_frame.margin_top = Inches(0.4)
            label(sh, x + 0.06, y + 0.05, cw - 0.12, 0.3, tag, size=11, bold=True, color=tag_color)

        cell(0, 0, "Keep satisfied", "keep_satisfied",
             "role and influence on the product")
        cell(1, 0, "Manage closely", "manage_closely",
             "role and involvement in the pilot",
             fill=ACCENT_BG, tag_color=ACCENT)
        cell(0, 1, "Monitor", "monitor", "role, influence and impact")
        cell(1, 1, "Keep informed", "keep_informed",
             "role and what changes for them")
        ax = label(sh, 0.2, my, 0.35, mh, "Stakeholder's influence on the product →", size=10, color=MUTED,
                   align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        ax.text_frame._txBody.bodyPr.set("vert", "vert270")
        ax.text_frame.margin_left = ax.text_frame.margin_right = 0
        label(sh, mx - 0.6, my, 0.55, 0.3, "high", size=9, color=MUTED, align=PP_ALIGN.RIGHT)
        label(sh, mx - 0.6, my + mh - 0.3, 0.55, 0.3, "low", size=9, color=MUTED, align=PP_ALIGN.RIGHT)
        label(sh, mx, my + mh + 0.03, mw, 0.3, "Product's impact on the stakeholder →", size=10, color=MUTED, align=PP_ALIGN.CENTER)
        label(sh, mx, my + mh + 0.03, 0.8, 0.3, "low", size=9, color=MUTED)
        label(sh, mx + mw - 0.8, my + mh + 0.03, 0.8, 0.3, "high", size=9, color=MUTED, align=PP_ALIGN.RIGHT)

        px, pw = 9.2, 3.63
        for y, h, name, key, hint in [
            (my, 2.55, "Decision", "decision", "who decides and who signs off"),
            (my + 2.95, 2.55, "Result", "result", "result with dates and checks"),
        ]:
            label(sh, px, y - 0.07, pw, 0.37, name, size=12, bold=True)
            text(box(sh, px, y + 0.3, pw, h - 0.3), f"{{{{{key}: {hint}}}}}", size=10)


class KanoModel(XlsxSpec):
    @property
    def rel(self):
        return "product-research/kano-model/kano-model.xlsx"

    example = {"text": {
        "title": "FreshDrop app, 240 buyers surveyed, 24 August 2026, online form",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.formatting.rule import FormulaRule
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Kano"
        ev = wb.create_sheet("Evaluation table")

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        thin = Side(style="thin", color="C9CED6")

        ws["A1"] = "Kano Model: {{title: product, who was surveyed, how many people, when}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws["A2"].font = Font(name=FONT, size=11, color="6B7280")
        ws.merge_cells("A1:M1")
        ws.merge_cells("A2:M2")

        headers = [
            ("Feature", "product property as the user sees it", 36),
            ("A\nattractive", "Attractive: delights if present, does not upset if absent.", 11),
            ("O\none-dimensional", "One-dimensional: the better it is done, the happier people are; if absent, they are unhappy.", 11),
            ("M\nmust-be", "Must-be: not noticed if present, strongly dissatisfying if absent.", 13),
            ("I\nindifferent", "Indifferent: people do not care whether it is there or not.", 12),
            ("R\nreverse", "Reverse: unhappy if present, happy if absent.", 10),
            ("Q\nquestionable", "Questionable: the answers contradict each other, the question was misunderstood.", 12),
            ("Decision", "decision on the feature and why", 40),
            ("Answers", "sum of answers B to G", 10),
            ("Category", "category with the most answers", 22),
            ("Category\nby most answers", "A+O+M vs I+R+Q category rule", 16),
            ("Better", "share of A and O answers", 10),
            ("Worse", "negative share of O and M answers", 10),
        ]
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(3, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            c.comment = Comment(hint, "pdm-skills", width=260, height=110)
            ws.column_dimensions[c.column_letter].width = width
        ws.row_dimensions[3].height = 46

        names = ["A · attractive", "O · one-dimensional", "M · must-be", "I · indifferent", "R · reverse", "Q · questionable"]
        first, last = 4, 53
        for r in range(first, last + 1):
            rng = f"B{r}:G{r}"
            ws.cell(r, 9, f'=IF(COUNT({rng})=0,"",SUM({rng}))')
            pick = " ".join(f'IF(MAX({rng})={chr(66 + k)}{r},"{names[k]}",' for k in range(6)) + '""' + ")" * 6
            ws.cell(r, 10, f'=IF(I{r}="","",IF(COUNTIF({rng},MAX({rng}))>1,"tie",{pick}))'.replace(", IF", ",IF"))
            pick3 = lambda cols: " ".join(f'IF(MAX({",".join(c + str(r) for c in cols)})={c}{r},"{names[ord(c) - 66]}",' for c in cols) + '""' + ")" * len(cols)
            ws.cell(r, 11, f'=IF(I{r}="","",IF(B{r}+C{r}+D{r}>E{r}+F{r}+G{r},{pick3("CBD")},{pick3("EFG")}))'.replace(", IF", ",IF"))
            base = f"(B{r}+C{r}+D{r}+E{r})"
            ws.cell(r, 12, f'=IF(OR(I{r}="",{base}=0),"",(B{r}+C{r})/{base})').number_format = "0.00"
            ws.cell(r, 13, f'=IF(OR(I{r}="",{base}=0),"",-(C{r}+D{r})/{base})').number_format = "0.00"
            for c in range(1, 14):
                ws.cell(r, c).font = regular
            ws.cell(r, 8).alignment = Alignment(wrap_text=True, vertical="top")
        ws.conditional_formatting.add(f"J{first}:J{last}", FormulaRule(
            formula=[f'J{first}="tie"'], font=Font(color="C63D3D", bold=True)))
        ws.freeze_panes = "B4"
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text="Kano!$A$4")
        dv = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                            error="The number of respondents must be a whole number, at least 0", showErrorMessage=True)
        dv.add(f"B{first}:G{last}")
        ws.add_data_validation(dv)

        ev["A1"] = "Kano evaluation table: answer to the functional question × answer to the dysfunctional question"
        ev["A1"].font = Font(name=FONT, bold=True, size=12)
        ev["A2"] = ("Functional: \"If the product has X, how would you feel about it?\" "
                    "Dysfunctional: \"If the product does not have X, how would you feel about it?\"")
        ev["A2"].font = Font(name=FONT, size=10, color="6B7280")
        answers = ["I like it", "I expect it", "I am neutral", "I can tolerate it", "I dislike it"]
        grid = ["QAAAO", "RIIIM", "RIIIM", "RIIIM", "RRRRQ"]
        ev.cell(4, 1, "X present ↓ / X absent →").font = bold
        for j, a in enumerate(answers):
            c = ev.cell(4, 2 + j, a)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, horizontal="center")
            ev.column_dimensions[c.column_letter].width = 16
            rc = ev.cell(5 + j, 1, a)
            rc.font, rc.fill = bold, head_fill
            for k, v in enumerate(grid[j]):
                cc = ev.cell(5 + j, 2 + k, v)
                cc.font, cc.alignment = regular, Alignment(horizontal="center")
                cc.border = Border(left=thin, right=thin, top=thin, bottom=thin)
        ev.column_dimensions["A"].width = 22
        ev.row_dimensions[4].height = 32
        for i, n in enumerate(names):
            ev.cell(11 + i, 1, n).font = regular


class PerceptualMap(PptxSpec):
    @property
    def rel(self):
        return "product-research/perceptual-map/perceptual-map.pptx"

    example = {"text": {
        "title": "Grocery delivery apps in Moscow: 300 buyers, August 2026",
        "x_axis": "Price: from cheap (left) to premium (right), 1–10",
        "y_axis": "Speed: slow (bottom) to fast (top)",
        "scope": "ratings of 300 buyers, August 2026; circle size = market share",
        "gap": "fast and premium: no strong brand; buyers say they would pay for it",
        "decision": "move FreshDrop to fast, mid-price; message «delivery in 2 hours»",
        "result": "message tested in 2 districts from 1 September; share checked after 6 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "PERCEPTUAL MAP", "{{title: market, who was asked, when}}")
        data = XyChartData()
        series = [("Midpoint X", [(5.5, 1), (5.5, 10)]), ("Midpoint Y", [(1, 5.5), (10, 5.5)]),
                  ("Brand A", [(7.5, 8)]), ("Brand B", [(3, 7)]), ("Brand C", [(4, 3)]), ("Our product", [(6.5, 4)])]
        for name, pts in series:
            ser = data.add_series(name)
            for x, y in pts:
                ser.add_data_point(x, y)
        cx, cy, cw, chh = 0.9, 1.3, 7.9, 5.45
        frame = slide.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER, Inches(cx), Inches(cy), Inches(cw), Inches(chh), data)
        frame.name = "map"
        chart = frame.chart
        ids = {}
        for el in chart._chartSpace.xpath(".//c:axId | .//c:crossAx"):
            el.set("val", str(ids.setdefault(el.get("val"), 500000 + len(ids))))
        chart.has_legend = False
        chart.font.name, chart.font.size = FONT, Pt(11)
        chart.font.color.rgb = INK
        all_series = list(chart.plots[0].series)
        for ser in all_series[:2]:
            ser.marker.style = XL_MARKER_STYLE.NONE
            ser.format.line.color.rgb = LINE
            ser.format.line.width = Pt(1.25)
            ser.smooth = False
        for ser in all_series[2:]:
            ser.format.line.fill.background()
            ser.marker.style = XL_MARKER_STYLE.CIRCLE
            ser.marker.size = 22
            ser.marker.format.fill.solid()
            ser.marker.format.fill.fore_color.rgb = ACCENT
            ser.marker.format.line.color.rgb = WHITE
            dls = DataLabels(ser._element.get_or_add_dLbls())
            dls.show_series_name, dls.show_value, dls.show_category_name = True, False, False
            dls.position = XL_LABEL_POSITION.RIGHT
            dls.font.size, dls.font.name = Pt(11), FONT
            dls.font.color.rgb = INK
        for axis in (chart.category_axis, chart.value_axis):
            axis.minimum_scale, axis.maximum_scale, axis.major_unit = 1, 10, 1
            axis.has_major_gridlines = False
            axis.format.line.color.rgb = LINE
            axis.tick_labels.font.size = Pt(10)
            axis.tick_labels.font.color.rgb = MUTED
        text(box(slide.shapes, cx, cy + chh + 0.02, cw, 0.4, line=None),
             "{{x_axis: horizontal axis: from what to what}}", size=11, color=MUTED, align=PP_ALIGN.CENTER)
        ax = text(box(slide.shapes, 0.3, cy, 0.5, chh, line=None),
                  "{{y_axis: vertical axis: from what to what}}", size=11, color=MUTED,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        ax.text_frame._txBody.bodyPr.set("vert", "vert270")

        x, w = 9.25, 3.6
        panels = [
            ("Data", "{{scope: data source, sample and circle size}}", 1.3, 1.3),
            ("Open position", "{{gap: empty position and whether buyers need it}}", 2.75, 1.35),
            ("Decision", "{{decision: where we move the product and how}}", 4.25, 1.35),
            ("Result", "{{result: result with dates and checks}}", 5.75, 1.35),
        ]
        for tag, token, py, ph in panels:
            label(slide.shapes, x, py - 0.05, w, 0.37, tag, size=12, bold=True, color=INK)
            text(box(slide.shapes, x, py + 0.32, w, ph - 0.32), token, size=10)


class EmpathyMap(PptxSpec):
    @property
    def rel(self):
        return "product-research/empathy-map/empathy-map.pptx"

    example = {"text": {
        "title": "Parents who order groceries online: 12 interviews, May 2026",
        "who": "Olga, 34, marketing manager, two kids, evening commute",
        "need_to_do": "plan the family week, choose a slot, know the order will be on time",
        "see": "rival apps with cheap offers; friends posting about fresh deliveries",
        "say": "«I never know if the slot will be on time»",
        "do": "checks the app 5 times a day; calls support when late",
        "hear": "friends recommend cheaper rivals; news about courier shortages",
        "pains": "late deliveries, missed items, wasted evenings",
        "gains": "time for family, fresh food, peace of mind",
        "think_feel": "wants a weekly plan she does not have to check",
        "decision": "add a delivery-time guarantee to the slot picker; product lead decides",
        "result": "guarantee shown in the slot picker from 1 July; complaints checked after 4 weeks",
    }}

    def draw(self, prs, slide):
        # Layout follows Dave Gray's Empathy Map Canvas (2017): goal on top, a big head in the middle
        # holding thoughts and feelings, observable sectors around it, numbered in the intended order
        header(slide, "EMPATHY MAP", "{{title: who was studied, how and when}}")
        sh = slide.shapes
        x0, y0, x1, y1 = 0.5, 1.3, 9.0, 7.2
        cx, cy, r = 4.75, 4.45, 1.9
        d = r * 0.7071
        ul, ur, ll, lr = (cx - d, cy - d), (cx + d, cy - d), (cx - d, cy + d), (cx + d, cy + d)

        box(sh, x0, y0, x1 - x0, y1 - y0)
        emu = lambda pt: (int(Inches(pt[0])), int(Inches(pt[1])))
        ff = sh.build_freeform(*emu((x0, y0)))
        ff.add_line_segments([emu((x1, y0)), emu(ur), emu(ul)], close=True)
        goal = ff.convert_to_shape()
        goal.fill.solid()
        goal.fill.fore_color.rgb = ACCENT_BG
        goal.line.color.rgb = LINE
        goal.shadow.inherit = False

        def line(a, b):
            return connector(sh, a, b, width=1)

        line((cx, y0), (cx, cy - r))
        line((x0, y1), ll)
        line((x1, y1), lr)
        line((cx + r, cy), (x1, cy))
        box(sh, cx - r, cy - r, 2 * r, 2 * r, fill=WHITE, kind=MSO_SHAPE.OVAL, line=INK)

        def cell(x, y, w, h, tag, key, hint, tag_color=INK):
            label(sh, x, y, w, 0.3, tag, size=11, bold=True, color=tag_color)
            text(box(sh, x, y + 0.28, w, h - 0.28, line=None), f"{{{{{key}: {hint}}}}}", size=10)

        cell(2.05, 1.36, 2.6, 1.05, "1 Who", "who", "name, age, role and situation",
             tag_color=ACCENT)
        cell(4.85, 1.36, 2.9, 1.05, "2 What they need to do", "need_to_do",
             "the job they are trying to do", tag_color=ACCENT)
        cell(6.75, 3.0, 2.2, 1.4, "3 See", "see", "what they see in the market")
        cell(6.75, 4.55, 2.2, 1.3, "4 Say", "say", "what they say out loud")
        cell(3.1, 6.4, 3.3, 0.78, "5 Do", "do", "observable actions and habits")
        cell(0.6, 3.2, 2.2, 2.4, "6 Hear", "hear", "what they hear from others")
        label(sh, cx - 1.8, cy - r + 0.3, 3.6, 0.3, "7 Think and feel", size=11, bold=True,
              align=PP_ALIGN.CENTER)
        line((cx, cy - r + 0.68), (cx, cy + 0.85))
        cell(cx - 1.5, cy - r + 0.68, 1.45, 2.1, "Pains", "pains", "frustrations and obstacles")
        cell(cx + 0.05, cy - r + 0.68, 1.45, 2.1, "Gains", "gains", "wants and measures of success")
        text(box(sh, cx - 1.3, cy + 0.9, 2.6, 0.75, line=None),
             "{{think_feel: thoughts and feelings that drive behaviour}}", size=10, align=PP_ALIGN.CENTER)

        px, pw = 9.25, 3.6
        for y, h, name, key, hint in [
            (1.3, 2.75, "Decision", "decision", "what we change and who decides"),
            (4.45, 2.75, "Result", "result", "result with dates and checks"),
        ]:
            label(sh, px, y - 0.07, pw, 0.37, name, size=12, bold=True)
            text(box(sh, px, y + 0.3, pw, h - 0.3), f"{{{{{key}: {hint}}}}}", size=10)


class JobsToBeDone(PptxSpec):
    @property
    def rel(self):
        return "product-research/jobs-to-be-done/jobs-to-be-done.pptx"

    example = {"text": {
        "title": "FreshDrop, families who plan the week: 18 interviews, May 2026",
        "job1": "Get groceries for the week",
        "job2": "Find a slot that fits",
        "job3": "Reorder the usual basket",
        "job1_when": "Sunday evening, fridge nearly empty",
        "job1_want": "order the full weekly list in one go",
        "job1_so_that": "the family eats well all week",
        "job1_solution": "weekly list from last order; 2-hour slots",
        "job2_when": "Tuesday, after the school run",
        "job2_want": "pick a window within 2 hours",
        "job2_so_that": "I am home for the courier",
        "job2_solution": "slot picker shows free windows first",
        "job3_when": "milk runs out in the morning",
        "job3_want": "repeat last week's basket in 2 taps",
        "job3_so_that": "I save 15 minutes",
        "job3_solution": "one-tap reorder on the home screen",
        "who": "families with children in Moscow; 18 interviews, May 2026",
        "result": "slot picker on the first screen from 1 July; reorder rate checked after 4 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "JOBS-TO-BE-DONE", "{{title: whose product, who was studied, how and when}}")
        sh = slide.shapes
        x0, y0, w, gap = 0.5, 1.3, 2.75, 0.08
        rows = [
            ("When", "when", "situation in which the job arises", 1.2, WHITE, INK),
            ("I want to", "want", "what the person wants to do", 1.2, WHITE, INK),
            ("So that", "so_that", "which outcome they need", 1.2, WHITE, INK),
            ("What we did", "solution", "what we changed for this job", 1.45, ACCENT_BG, ACCENT),
        ]
        for i in range(3):
            n = i + 1
            x = x0 + i * (w + gap)
            text(box(sh, x, y0, w, 0.45, fill=INK, line=None), f"{{{{job{n}: job name}}}}",
                 size=11, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            y = y0 + 0.5
            for tag, key, hint, h, fill, tag_color in rows:
                box(sh, x, y, w, h, fill=fill)
                label(sh, x + 0.04, y + 0.03, w - 0.08, 0.3, tag, size=10, bold=True, color=tag_color)
                text(box(sh, x, y + 0.3, w, h - 0.3, line=None), f"{{{{job{n}_{key}: {hint}}}}}", size=10)
                y += h + 0.05

        px, pw = 9.25, 3.6
        for y, h, name, key, hint in [
            (1.3, 2.75, "Who and where the data is from", "who", "who was studied, where and when"),
            (4.45, 2.75, "Result", "result", "result with dates and checks"),
        ]:
            label(sh, px, y - 0.07, pw, 0.37, name, size=12, bold=True)
            text(box(sh, px, y + 0.3, pw, h - 0.3), f"{{{{{key}: {hint}}}}}", size=10)


class CustomerSurvey(PptxSpec):
    @property
    def rel(self):
        return "product-research/customer-survey/customer-survey.pptx"

    example = {"text": {
        "title": "FreshDrop team, buyers in Moscow, 3–10 August 2026",
        "hypothesis": "buyers who miss a slot would pay for a reminder; the reminder feature depends on the answer",
        "audience": "buyers with 2+ orders in the last 3 months; 1,800 invited, screening: 1 order a week or more",
        "channel": "email and push; 412 answered (23%); trial run with 20 people",
        "q1": "Do you order groceries online? («Yes» / «No»)",
        "q2": "How often do you miss a delivery slot?",
        "q3": "How much would you pay for a fixed slot, rub?",
        "q4": "Which reminder time do you prefer?",
        "a1": "Yes: 91% (n=412)",
        "a2": "Once a month or more: 38%",
        "a3": "median 150 rub",
        "a4": "15 minutes before: 61%",
        "c1": "most buyers order online",
        "c2": "missed slots are common",
        "c3": "a fixed slot is worth paying for",
        "c4": "a reminder 15 minutes before wins",
        "gaps": "no answers from non-app buyers; no data on the 18–25 group",
        "decision": "build the reminder first; add a slot guarantee to the next release",
        "check": "reminder opened by 40% of users in 2 weeks; missed slots down by a fifth",
    }}

    def draw(self, prs, slide):
        header(slide, "CUSTOMER SURVEY · SURVEY PLAN AND RESULTS",
               "{{title: who ran the survey, whom, when}}")
        sh = slide.shapes
        top = [
            ("Hypothesis and decision", "{{hypothesis: what we test, and the decision it drives}}"),
            ("Whom we survey (screening)", "{{audience: screening condition and people invited}}"),
            ("Channel and collection", "{{channel: how it was sent, answers, trial run}}"),
        ]
        w, gap = 4.0, 0.165
        for i, (tag, token) in enumerate(top):
            x = 0.5 + i * (w + gap)
            text(box(sh, x, 1.25, w, 0.32, fill=ACCENT, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, 1.57, w, 0.85), token, size=10)
        cols = [("Question (closed or open)", "q", 4.2, INK, ["{{q1: exact wording}}", "{{q2: exact wording}}", "{{q3: exact wording}}", "{{q4: exact wording}}"]),
                ("Answers (shares, number of respondents)", "a", 4.0, INK, ["{{a1: shares or 'not in the source'}}", "{{a2: shares or 'not in the source'}}", "{{a3: shares or 'not in the source'}}", "{{a4: shares or 'not in the source'}}"]),
                ("Conclusion", "c", 3.8, BAD, ["{{c1: what follows from the answers}}", "{{c2: what follows from the answers}}", "{{c3: what follows from the answers}}", "{{c4: what follows from the answers}}"])]
        x = 0.5
        for tag, key, cw, color, hint in cols:
            text(box(sh, x, 2.55, cw, 0.32, fill=color, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            for r in range(4):
                text(box(sh, x, 2.87 + r * 0.58, cw, 0.58), hint[r], size=10)
            x += cw + 0.15
        panels = [
            ("What the data does not show", "{{gaps: what is unknown: respondents, groups, caveats}}", BAD, BAD_BG),
            ("Decision", "{{decision: what we change as a result}}", GOOD, GOOD_BG),
            ("Decision check", "{{check: how we check it by behavior, and when}}", INK, None),
        ]
        for i, (tag, token, color, fill) in enumerate(panels):
            px = 0.5 + i * (w + gap)
            text(box(sh, px, 5.2, w, 0.32, fill=color, line=None), tag, size=12, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, px, 5.52, w, 1.6, fill=fill), token, size=11)


class DiaryStudy(PptxSpec):
    @property
    def rel(self):
        return "product-research/diary-study/diary-study.pptx"

    example = {"text": {
        "title": "FreshDrop team, weekly shopping of families, Moscow, August 2026",
        "question": "how families plan and change the weekly order, and what makes them cancel",
        "sample": "14 families, 2 children each on average; 7 days; 2 dropouts",
        "entry": "event-based: an entry after each order; messenger photos of the fridge",
        "a1": "Tue 19:10: opened the app, searched «milk», gave up",
        "a2": "Thu 18:40: ordered by phone, asked for the 19:00 slot",
        "a3": "Sat 10:20: planned the week in the messenger",
        "t1": "«I always lose the slot, it is annoying»",
        "t2": "«The phone is easier, I trust the operator»",
        "t3": "«Relief when the courier calls»",
        "c1": "the family plans on Sunday; the slot is the trigger",
        "c2": "phone ordering is the fallback for missed slots",
        "c3": "weekend planning is the habit to support",
        "interview": "what we clarified: the weekly plan is made on Sunday; cancellation is the fear of a missed slot",
        "gaps": "dropout after day 3 for 2 families; some entries are late",
        "decision": "build the reminder and the weekly plan; test with 50 families",
    }}

    def draw(self, prs, slide):
        header(slide, "DIARY STUDY · DIARY STUDY LOG",
               "{{title: who ran the study, whom, where, year}}")
        sh = slide.shapes
        top = [
            ("Research question", "{{question: what we want to learn about behavior}}"),
            ("Participants and duration", "{{sample: people, group, days, dropout}}"),
            ("Entry: type and medium", "{{entry: entry type and medium}}"),
        ]
        w, gap = 4.0, 0.165
        for i, (tag, token) in enumerate(top):
            x = 0.5 + i * (w + gap)
            text(box(sh, x, 1.25, w, 0.32, fill=ACCENT, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, 1.57, w, 0.8), token, size=10)
        cols = [("Entry: what they did (day, time)", "a", 4.2, INK,
                 ["{{a1: action, place, method; verbatim or 'not in the source'}}", "{{a2: action, place, method; verbatim or 'not in the source'}}", "{{a3: action, place, method; verbatim or 'not in the source'}}"]),
                ("Entry: what they thought and felt", "t", 3.6, INK,
                 ["{{t1: participant's words or 'not in the source'}}", "{{t2: participant's words or 'not in the source'}}", "{{t3: participant's words or 'not in the source'}}"]),
                ("Researcher's conclusion", "c", 4.2, BAD,
                 ["{{c1: what this means, in the researcher's view}}", "{{c2: what this means, in the researcher's view}}", "{{c3: what this means, in the researcher's view}}"])]
        x = 0.5
        for tag, key, cw, color, hint in cols:
            text(box(sh, x, 2.5, cw, 0.32, fill=color, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            for r in range(3):
                text(box(sh, x, 2.82 + r * 0.72, cw, 0.72), hint[r], size=10)
            x += cw + 0.15
        panels = [
            ("Closing interview", "{{interview: what was clarified in the interview}}", INK, None),
            ("Data gaps and risks", "{{gaps: dropout, missing entries, distortions}}", BAD, BAD_BG),
            ("Decision and check", "{{decision: what we change and how we check it}}", GOOD, GOOD_BG),
        ]
        for i, (tag, token, color, fill) in enumerate(panels):
            px = 0.5 + i * (w + gap)
            text(box(sh, px, 5.1, w, 0.32, fill=color, line=None), tag, size=12, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, px, 5.42, w, 1.8, fill=fill), token, size=11)


class ExpertInterview(PptxSpec):
    @property
    def rel(self):
        return "product-research/expert-interview/expert-interview.pptx"

    example = {"text": {
        "title": "FreshDrop team, 6 experts from logistics and retail, 20 August 2026",
        "hypothesis": "courier delays are caused by the slot model, not by the route; the slot decision depends on it",
        "experts": "2 former courier managers, 2 category managers, 2 logistics analysts; 6 people",
        "format": "interview, 60 minutes each; led by the product lead, notes by the analyst",
        "q1": "How long does a courier wait at a slot in a dense district?",
        "q2": "Where does a late delivery start: in the slot or in the route?",
        "q3": "What would you fix first in a delivery service?",
        "q4": "What do buyers complain about most?",
        "a1": "«12–15 min» (former courier manager)",
        "a2": "«The slot, the route is fine» (logistics analyst)",
        "a3": "«Slots first» (category manager)",
        "a4": "«Late courier, then no call» (category manager)",
        "c1": "waiting is the main cost",
        "c2": "the slot causes the delay",
        "c3": "the slot model comes first",
        "c4": "calls matter as much as time",
        "gaps": "no experts from the Saint Petersburg market; numbers are from memory",
        "decision": "fix the slot model before the route algorithm",
        "check": "fewer late deliveries in the pilot districts over 4 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "EXPERT INTERVIEW · EXPERT INTERVIEW PLAN AND RESULTS",
               "{{title: who ran it, with whom, when}}")
        sh = slide.shapes
        top = [
            ("Hypothesis and decision", "{{hypothesis: what we test, and the decision it drives}}"),
            ("Experts (roles)", "{{experts: roles, how each knows consumers, count}}"),
            ("Format and collection", "{{format: interview or workshop; who led and took notes}}"),
        ]
        w, gap = 4.0, 0.165
        for i, (tag, token) in enumerate(top):
            x = 0.5 + i * (w + gap)
            text(box(sh, x, 1.25, w, 0.32, fill=ACCENT, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, 1.57, w, 0.85), token, size=10)
        cols = [("Question to the expert", "q", 4.2, INK, ["{{q1: exact wording or 'not in the source'}}", "{{q2: exact wording or 'not in the source'}}", "{{q3: exact wording or 'not in the source'}}", "{{q4: exact wording or 'not in the source'}}"]),
                ("Answer or summary (role)", "a", 4.0, INK, ["{{a1: what was said and by which role, or authors' summary}}", "{{a2: what was said and by which role, or authors' summary}}", "{{a3: what was said and by which role, or authors' summary}}", "{{a4: what was said and by which role, or authors' summary}}"]),
                ("Conclusion", "c", 3.8, BAD, ["{{c1: what follows from the answers}}", "{{c2: what follows from the answers}}", "{{c3: what follows from the answers}}", "{{c4: what follows from the answers}}"])]
        x = 0.5
        for tag, key, cw, color, hint in cols:
            text(box(sh, x, 2.55, cw, 0.32, fill=color, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            for r in range(4):
                text(box(sh, x, 2.87 + r * 0.58, cw, 0.58), hint[r], size=10)
            x += cw + 0.15
        panels = [
            ("What the data does not show", "{{gaps: what is unknown: participants, verbatim answers, caveats}}", BAD, BAD_BG),
            ("Decision", "{{decision: what we change as a result}}", GOOD, GOOD_BG),
            ("Decision check", "{{check: how we check it with consumers, and when}}", INK, None),
        ]
        for i, (tag, token, color, fill) in enumerate(panels):
            px = 0.5 + i * (w + gap)
            text(box(sh, px, 5.2, w, 0.32, fill=color, line=None), tag, size=12, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, px, 5.52, w, 1.6, fill=fill), token, size=11)


class FieldResearch(PptxSpec):
    @property
    def rel(self):
        return "product-research/field-research/field-research.pptx"

    example = {"text": {
        "title": "FreshDrop team, 3 families observed at home, Moscow, August 2026",
        "hypothesis": "at home the family plans the order on the phone during dinner prep and loses the slot when they forget",
        "setting": "3 homes, 2 visits each, 1.5 hours per visit",
        "role": "passive, with clarifying questions; partial immersion",
        "patterns": "all 3 families plan on the phone during cooking; 2 of 3 check the slot after work",
        "refuted": "the family does not compare prices; they choose by habit",
        "decision": "build the reminder into the cooking time; test with 10 families",
        "f1": "Tue 19:10: opened the app, typed «milk», gave up on the slot",
        "f2": "Tue 19:40: called the shop, ordered by phone",
        "f3": "Wed 07:30: checked the slot on the way to work",
        "q1": "«I just want it to come when I am home»",
        "q2": "«The slot is always gone by the evening»",
        "q3": "«I forgot again, the courier left»",
        "i1": "the family plans around the slot, not the price",
        "i2": "the phone is the planning tool at dinner prep",
        "i3": "missed slots push the family back to the shop",
    }}

    def draw(self, prs, slide):
        header(slide, "FIELD RESEARCH · FIELD OBSERVATION LOG",
               "{{title: who observed, where, whom, year}}")
        sh = slide.shapes
        top = [
            ("Hypothesis", "{{hypothesis: in situation X the person does Y because Z}}"),
            ("Place, people, time", "{{setting: where, whom, visits and hours}}"),
            ("Observer's role", "{{role: passive or with questions; full or partial}}"),
        ]
        w, gap = 4.0, 0.165
        for i, (tag, token) in enumerate(top):
            x = 0.5 + i * (w + gap)
            text(box(sh, x, 1.25, w, 0.32, fill=ACCENT, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, 1.57, w, 0.8), token, size=10)
        cols = [("Observation (fact only)", "f", 4.2, INK),
                ("The person's words", "q", 3.6, INK),
                ("Interpretation", "i", 4.2, BAD)]
        x = 0.5
        for tag, key, cw, color in cols:
            text(box(sh, x, 2.5, cw, 0.32, fill=color, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            hints = {"f": ["{{f%d: what they did, where, in what order}}" % n for n in range(1, 4)],
                     "q": ["{{q%d: verbatim or 'not in the source'}}" % n for n in range(1, 4)],
                     "i": ["{{i%d: why, in the observer's view}}" % n for n in range(1, 4)]}
            for r in range(3):
                text(box(sh, x, 2.82 + r * 0.72, cw, 0.72), hints[key][r], size=10)
            x += cw + 0.15
        panels = [
            ("Repeats across visits", "{{patterns: what repeated, and how many people}}", INK, None),
            ("Not confirmed", "{{refuted: what did not match, or stayed unclear}}", BAD, BAD_BG),
            ("Decision and check", "{{decision: what we change, and how we check it}}", GOOD, GOOD_BG),
        ]
        for i, (tag, token, color, fill) in enumerate(panels):
            px = 0.5 + i * (w + gap)
            text(box(sh, px, 5.1, w, 0.32, fill=color, line=None), tag, size=12, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, px, 5.42, w, 1.8, fill=fill), token, size=11)


class InDepthInterview(XlsxSpec):
    @property
    def rel(self):
        return "product-research/in-depth-interview/in-depth-interview.xlsx"

    example = {"text": {
        "title": "FreshDrop, ordering habits of families, August 2026, 8 interviews",
        "hypothesis": "parents who order weekly plan the order on Sunday because the slot is fixed",
        "who": "8 weekly buyers from Moscow, found through the app survey; 45 minutes each",
        "goal": "learn how the weekly order is planned and what breaks it; the slot choice decision depends on it",
        "t1": "Weekly planning", "c1": "when the order is planned and by whom",
        "q1": "Tell me about the last time you planned the week's groceries.", "f1": "Which day? Did you check the fridge first?",
        "t2": "Slot choice", "c2": "how the delivery slot is picked and how often it is full",
        "q2": "Walk me through the last slot you booked.", "f2": "Was there a slot you wanted and could not get? What did you do?",
        "t3": "Lost orders", "c3": "orders dropped or moved to a shop",
        "q3": "Tell me about the last time an order fell through.", "f3": "How much did it cost you in time and money? Where did you buy instead?",
        "t4": "Payment", "c4": "which payment method is used and why",
        "q4": "Tell me about the last time you paid for an order in the app.", "f4": "Did you try to pay another way? Was the card form a problem?",
        "t5": "Willingness to pay", "c5": "whether a fixed slot is worth money, by past behaviour",
        "q5": "Tell me about a time you paid extra for a delivery.", "f5": "What did you pay? Would you pay again next week?",
        "findings": "6 of 8 plan on Sunday; 5 lost a slot in the last month; separately, 2 said they would pay more for a fixed slot (opinion only)",
        "decision": "hypothesis confirmed; build the slot reminder and test it with 50 buyers",
        "gaps": "no buyers from outside the Moscow ring road; no answers from non-weekly buyers",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Interview"

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        thin = Side(style="thin", color="C9CED6")
        wrap = Alignment(wrap_text=True, vertical="top")

        def note(cell, hint, height=100):
            return comment(cell, hint, height=height, width=260)

        def dv_list(values, ref):
            dv = DataValidation(type="list", formula1=f'"{values}"', allow_blank=True, errorStyle="warning",
                                showErrorMessage=True, error=f"Values: {values}")
            dv.add(ref)
            ws.add_data_validation(dv)

        def header_cell(r, c, title, hint, width=None):
            cell = ws.cell(r, c, title)
            cell.font, cell.fill = bold, head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="center")
            cell.border = Border(bottom=thin)
            note(cell, hint, 110)
            if width:
                ws.column_dimensions[cell.column_letter].width = width

        ws["A1"] = "Depth interview: {{title: research topic, segment and date}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:H1")

        top = [
            (2, "Hypothesis:", "{{hypothesis: the statement we test}}", bold),
            (3, "Respondents:", "{{who: who and how many, how selected, interview length}}", regular),
            (4, "Goal:", "{{goal: learning goal and the decision behind it}}", regular),
        ]
        for r, name, token, font in top:
            ws.cell(r, 1, name).font = muted
            c = ws.cell(r, 2, token)
            c.font, c.alignment = font, wrap
            ws.merge_cells(f"B{r}:H{r}")
            ws.row_dimensions[r].height = 32

        # guide
        ws["A6"] = "Interview guide"
        ws["A6"].font = bold
        gh = 7
        header_cell(gh, 1, "№", "Theme number. The answer log refers to the question by it.", 14)
        header_cell(gh, 2, "Theme", "Short name of a block of the conversation, for example \"payment method\", \"last time they refused\".", 22)
        header_cell(gh, 3, "What we check", "Which part of the hypothesis the theme covers. Without it the question is not needed.", 24)
        header_cell(gh, 4, "Main question", "Open question about a concrete past case: \"Tell me about the last time when...\". "
                           "Not \"did you like it\" and not \"would you...\".", 44)
        header_cell(gh, 5, "Follow-ups", "Nested questions: when it was, how much time and money it took, what they did next. "
                           "Probing \"tell me more\" prompts are not written in advance.", 36)
        for i in range(1, 6):
            r = gh + i
            ws.cell(r, 1, i).font = bold
            ws.cell(r, 1).alignment = wrap
            for c, (key, hint) in [(2, ("t", "theme name")), (3, ("c", "what exactly we check")),
                                   (4, ("q", "main question about a past case")), (5, ("f", "follow-up questions"))]:
                cell = ws.cell(r, c, f"{{{{{key}{i}: {hint}}}}}")
                cell.font, cell.alignment = regular, wrap
            ws.row_dimensions[r].height = 46

        # conclusions
        concl = [
            (14, "Findings:", "{{findings: repeated cases and separate opinions}}"),
            (15, "Decision:", "{{decision: decision taken, hypothesis confirmed or not}}"),
            (16, "What is missing:", "{{gaps: what was not clarified, uncovered roles, open numbers}}"),
        ]
        for r, name, token in concl:
            ws.cell(r, 1, name).font = muted
            c = ws.cell(r, 2, token)
            c.font, c.alignment = regular, wrap
            ws.merge_cells(f"B{r}:H{r}")
            ws.row_dimensions[r].height = 46

        # log
        ws["A18"] = "Answer log: one row is one record from an interview"
        ws["A18"].font = bold
        hr = 19
        cols = [
            ("Respondent", "Respondent code (R1, R2...), not a name. One row is one record; a respondent has many.", 14),
            ("Role", "Respondent's job title or role: roles are recorded separately, they have different emphases.", 22),
            ("Theme (no.)", "Theme number from the guide or its name; for something unexpected, \"outside the guide\".", 24),
            ("What happened", "Fact: when, what they did, how much time and money it took. Only what the person said, without your assessment.", 44),
            ("Quote", "Respondent's exact phrase. If it was not recorded verbatim, leave it empty instead of paraphrasing. Empty = no data: do not write placeholders.", 36),
            ("Signal", "Time or money spent on a solution, strong emotion (irritation, relief). "
                       "A sign that the problem is real.", 26),
            ("Data type", "Fact from the past, opinion or intention (\"we would...\", \"I usually...\"), idea or request (a request to add a feature), "
                           "compliment. Facts weigh more than the rest. Empty = no data: do not write placeholders.", 22),
            ("What it means", "Your interpretation, separate from the facts: which part of the hypothesis it confirms, refutes or leaves open.", 36),
        ]
        for i, (t, h, w) in enumerate(cols, start=1):
            header_cell(hr, i, t, h, w)
        ws.row_dimensions[hr].height = 34

        first, last = hr + 1, hr + 100
        for r in range(first, last + 1):
            for c in range(1, 9):
                ws.cell(r, c).font = regular
                ws.cell(r, c).alignment = wrap
        ws.freeze_panes = None
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'Interview'!$A${first}")
        dv_list("fact from the past,opinion or intention,idea or request,compliment", f"G{first}:G{last}")

        rng = lambda col: f"${col}${first}:${col}${last}"
        ws.column_dimensions["I"].width = 3
        ws.column_dimensions["J"].width = 34
        ws.column_dimensions["K"].width = 12
        ws["J7"] = "Totals"
        ws["J7"].font, ws["J7"].fill = bold, head_fill
        ws["K7"].fill = head_fill
        stats = [
            ("Records", f'=COUNTA({rng("D")})', "0", "How many records are in the log."),
            ("Respondents", f'=SUMPRODUCT(({rng("A")}<>"")/COUNTIF({rng("A")},{rng("A")}&""))', "0",
             "How many different codes are in the first column."),
            ("Facts from the past", f'=COUNTIF({rng("G")},"fact from the past")', "0", "Records where the person described a case, not an opinion."),
            ("Opinions and intentions", f'=COUNTIF({rng("G")},"opinion or intention")', "0", "Words about the future and \"usually\": weak data."),
            ("Ideas and requests", f'=COUNTIF({rng("G")},"idea or request")', "0", "Feature requests: find out the motive, do not just fulfil them."),
            ("Compliments", f'=COUNTIF({rng("G")},"compliment")', "0", "Praise is not evidence. A growing share is a warning sign."),
            ("Share of facts", '=IF(K8=0,"",K10/K8)', "0%",
             "Facts divided by records. A low share means the interview came down to opinions; it is not a market estimate."),
            ("Records without a quote", f'=SUMPRODUCT(({rng("D")}<>"")*({rng("E")}=""))', "0",
             "Records with an empty quote: check that the wording was not made up."),
            ("Records without a type", f'=SUMPRODUCT(({rng("D")}<>"")*({rng("G")}=""))', "0", "Should be 0: a record without a type cannot be weighed."),
        ]
        for i, (name, formula, fmt, hint) in enumerate(stats, start=8):
            a = ws.cell(i, 10, name)
            a.font = regular
            note(a, hint, 90)
            b = ws.cell(i, 11, formula)
            b.font, b.fill = bold, calc_fill
            b.number_format = fmt


class JtbdInterview(PptxSpec):
    @property
    def rel(self):
        return "product-research/jtbd-interview/jtbd-interview.pptx"

    example = {"text": {
        "title": "FreshDrop, supermarket to delivery, Moscow, Aug 2026",
        "t1": "after a long queue at the shop on a Saturday",
        "t2": "read reviews of delivery services during the evening",
        "t3": "a friend recommended a delivery service with a fixed slot",
        "t4": "compared three apps, checked slot times and the price of delivery",
        "t5": "the first free delivery offer",
        "t6": "chose FreshDrop for the fixed slot and the reminder",
        "t7": "first weekly order went well; the courier was on time; expectations matched",
        "push": "waiting in queues on Saturday cost 2 hours a week",
        "pull": "a fixed slot and a reminder before the courier comes",
        "anxiety": "fear the courier will be late and the food will not arrive in time",
        "habit": "the family is used to shopping on the way home from work",
        "insights": "the job is a dinner on time for the family; the slot is what buyers pay for",
        "decision": "build the reminder and the slot guarantee; check it by the share of weekly orders",
    }}

    def draw(self, prs, slide):
        header(slide, "JTBD INTERVIEW · PURCHASE TIMELINE AND FORCES OF CHOICE",
               "{{title: who, which purchase, date}}")
        sh = slide.shapes
        marks = [
            ("First thought", "{{t1: first thought, when and why}}"),
            ("Passive looking", "{{t2: what they noticed and read}}"),
            ("Event 1", "{{t3: what pushed them to look}}"),
            ("Active looking", "{{t4: alternatives compared, workarounds}}"),
            ("Event 2", "{{t5: last nudge before the decision}}"),
            ("Decision", "{{t6: what they chose and when}}"),
            ("Use", "{{t7: first use, against expectations}}"),
        ]
        w, gap, y = 1.7, 0.07, 1.3
        for i, (tag, token) in enumerate(marks):
            x = 0.5 + i * (w + gap)
            text(box(sh, x, y, w, 0.4, fill=ACCENT, line=None), tag, size=11, bold=True, color=WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, y + 0.4, w, 1.85), token, size=10)
        forces = [
            ("→ Push", "{{push: what was wrong with the old way}}", GOOD),
            ("→ Pull", "{{pull: what the new option promised}}", GOOD),
            ("← Anxiety", "{{anxiety: what they feared about the new option}}", BAD),
            ("← Habit", "{{habit: what kept them with the old way}}", BAD),
        ]
        fw, fg, fy = 3.0, 0.107, 3.7
        for i, (tag, token, color) in enumerate(forces):
            x = 0.5 + i * (fw + fg)
            box(sh, x, fy, fw, 1.7, line=color)
            label(sh, x + 0.05, fy + 0.03, fw - 0.1, 0.35, tag, size=12, bold=True, color=color)
            text(box(sh, x + 0.05, fy + 0.4, fw - 0.1, 1.25, line=None), token, size=10)
        panels = [
            (0.5, "What the interviews showed", "{{insights: repeated findings, job and open points}}", INK, None),
            (6.75, "Decision", "{{decision: what we change and the check metric}}", GOOD, GOOD_BG),
        ]
        for x, tag, token, color, fill in panels:
            text(box(sh, x, 5.55, 6.08, 0.32, fill=color, line=None), tag, size=12, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, 5.87, 6.08, 1.4, fill=fill), token, size=11)


class ProblemInterviewScript(XlsxSpec):
    @property
    def rel(self):
        return "product-research/problem-interview-script/problem-interview-script.xlsx"

    example = {"text": {
        "title": "FreshDrop, busy families, Moscow, August 2026",
        "person": "parents with 2+ children who order food weekly",
        "problem": "the courier comes late and the slot is lost; the order is cancelled and the family eats out",
        "cause": "slots are fixed by the shop, not by the family; no reminder",
        "motivation": "a dinner on time; the metric is orders delivered in the slot, target 90%",
        "metric": "share of orders delivered in the chosen slot",
        "hypothesis": "families lose a slot about once a month and want a reminder",
        "who": "12 parents, interviewer and note-taker from the product team",
        "extra": "they plan the week on Sunday; they check the app three times a week",
        "general": "busy, two incomes, shop by phone and by app",
        "context": "they keep a list in a messenger and call the shop when a slot is missed",
        "values": "time with the children; food that is healthy and fresh",
        "pains": "a missed slot is the worst part of the week; the courier does not call",
        "decision": "hypothesis confirmed for 9 of 12 parents; build the reminder first",
        "gaps": "no answers from parents who order only once a month",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Script"

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        thin = Side(style="thin", color="C9CED6")
        wrap = Alignment(wrap_text=True, vertical="top")

        def note(cell, hint, height=100):
            return comment(cell, hint, height=height, width=260)

        def header_cell(r, c, title, hint, width=None):
            cell = ws.cell(r, c, title)
            cell.font, cell.fill = bold, head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="center")
            cell.border = Border(bottom=thin)
            note(cell, hint, 120)
            if width:
                ws.column_dimensions[cell.column_letter].width = width

        ws["A1"] = "Problem interview script: {{title: segment and problem, date}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:H1")

        # Step 1: hypothesis
        top = [
            (2, "Person (who has it):", "{{person: segment that has the problem}}"),
            (3, "Problem (what):", "{{problem: behavior and blocker metric}}"),
            (4, "Cause (why):", "{{cause: possible causes of the problem}}"),
            (5, "Motivation (what for):", "{{motivation: desired result and goal metric}}"),
            (6, "Common metric:", "{{metric: one metric for the blocker and goal}}"),
            (7, "Hypothesis:", "{{hypothesis: problem hypothesis in one sentence}}"),
            (8, "Interview:", "{{who: respondents, count, interviewer and note-taker}}"),
        ]
        for r, name, token in top:
            ws.cell(r, 1, name).font = muted
            c = ws.cell(r, 2, token)
            c.font, c.alignment = (bold if r == 7 else regular), wrap
            ws.merge_cells(f"B{r}:H{r}")
            ws.row_dimensions[r].height = 32

        # Step 2: script and answers
        ws["A10"] = "Script"
        ws["A10"].font = bold
        hr = 11
        cols = [
            ("№", "Order of questions: left to right, top to bottom.", 6),
            ("Block", "Script block: behavior, problem, goal, solution or closing.", 16),
            ("Question type", "For example: general about behavior, example, frequency, tools, emotions, presence of a blocker, impact on the goal, "
                            "current solution, \"magic wand\", reverse question.", 24),
            ("Checks", "Part of the hypothesis: Behavior, Blocker metric, Motivation or Cause. A question without a hypothesis part is not needed.", 18),
            ("Question (hypothesis check)", "Open question about a use case, for example \"When was the last time you ___? Can you give an example?\". "
                                           "Do not put the answer in the question.", 44),
            ("Follow-up (new knowledge)", "Question from the new-knowledge flow if the answer did not match the hypothesis: \"Why is ___ important to you?\", \"Who else faces this?\".", 36),
            ("Respondent answer", "Notes on what they answered. No answer: leave it empty; do not write placeholders, they are counted as an answer.", 40),
            ("Matches hypothesis", "Lowercase: yes, no or partially. Assessment of the answer; empty = not yet assessed: do not write placeholders.", 18),
        ]
        for i, (t, h, w) in enumerate(cols, start=1):
            header_cell(hr, i, t, h, w)
        ws.row_dimensions[hr].height = 34

        first, last = hr + 1, hr + 30
        for r in range(first, last + 1):
            for c in range(1, 9):
                ws.cell(r, c).font = regular
                ws.cell(r, c).alignment = wrap
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'Script'!$A${first}")
        dv = DataValidation(type="list", formula1='"yes,no,partially"', allow_blank=True, errorStyle="warning",
                            showErrorMessage=True, error="Values: yes, no, partially")
        dv.add(f"H{first}:H{last}")
        ws.add_data_validation(dv)

        # Steps 3-4: extra hypotheses, persona, decision (below the 30 script rows)
        base = last + 2
        blocks = [
            ("Extra hypotheses:", "{{extra: additional hypotheses about the persona}}"),
            ("General features:", "{{general: how the persona behaves in general}}"),
            ("Context:", "{{context: how the persona copes now}}"),
            ("Values and goals:", "{{values: what they strive for and value}}"),
            ("Pains and difficulties:", "{{pains: confirmed problems, what hurts most}}"),
            ("Decision:", "{{decision: outcome for the hypothesis and next step}}"),
            ("What is missing:", "{{gaps: what is not clarified, missing answers}}"),
        ]
        ws.cell(base - 1, 1, "Results: persona description in four parts and the decision").font = bold
        for i, (name, token) in enumerate(blocks):
            r = base + i
            ws.cell(r, 1, name).font = muted
            c = ws.cell(r, 2, token)
            c.font, c.alignment = regular, wrap
            ws.merge_cells(f"B{r}:H{r}")
            ws.row_dimensions[r].height = 40

        # totals
        rng = lambda col: f"${col}${first}:${col}${last}"
        ws.column_dimensions["I"].width = 3
        ws.column_dimensions["J"].width = 30
        ws.column_dimensions["K"].width = 12
        ws["J11"] = "Answer totals"
        ws["J11"].font, ws["J11"].fill = bold, head_fill
        ws["K11"].fill = head_fill
        stats = [
            ("Questions with an answer", f'=COUNTA({rng("G")})', "0", "How many rows have notes on the answer."),
            ("Matched", f'=COUNTIF({rng("H")},"yes")', "0", "Answers that confirm the hypothesis."),
            ("Did not match", f'=COUNTIF({rng("H")},"no")', "0", "Answers that refute the hypothesis: see the new-knowledge flow."),
            ("Partially", f'=COUNTIF({rng("H")},"partially")', "0", "Partial match."),
            ("Answers without assessment", f'=SUMPRODUCT(({rng("G")}<>"")*({rng("H")}=""))', "0",
             "There is an answer but no \"matches\" assessment. Should be 0 after review."),
        ]
        for i, (name, formula, fmt, hint) in enumerate(stats, start=12):
            a = ws.cell(i, 10, name)
            a.font = regular
            note(a, hint, 80)
            b = ws.cell(i, 11, formula)
            b.font, b.fill = bold, calc_fill
            b.number_format = fmt
