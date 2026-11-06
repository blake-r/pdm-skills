from .base import *


class HadiCanvas(PptxSpec):
    @property
    def rel(self):
        return "product-validation/hadi-canvas/hadi-canvas.pptx"

    example = {"text": {
        "title": "FreshDrop, slow slot booking, 1–30 September 2026",
        "problem": "Slot booking fails in 38% of sessions; 22% of buyers leave at the slot step (July analytics)",
        "hypothesis": "If 2-hour slots are shown on the first screen, slot-to-order rises from 61% to 70%, because buyers stop scrolling",
        "experiment": "2-hour slots on the home screen for 2 weeks in 2 districts, 50% of traffic",
        "metrics": "Slot-to-order at 70% or more confirms; below 65% drops the idea",
        "period1": "Week 1", "period2": "Week 2", "period3": "Week 3",
        "metric1": "Slot-to-order, %", "metric2": "Slot errors, %", "metric3": "Orders in test districts",
        "m1_p1": "61%", "m1_p2": "66%", "m1_p3": "71%",
        "m2_p1": "38%", "m2_p2": "24%", "m2_p3": "15%",
        "m3_p1": "1,140", "m3_p2": "1,620", "m3_p3": "1,980",
        "subresults": "Week 2: 2-hour slots picked 3 times more often; errors fell after the map fix",
        "results": "Confirmed: 71% in week 3 (target 70%). Decision: roll out to all Moscow districts from 1 October",
    }}

    def draw(self, prs, slide):
        header(slide, "HADI CANVAS · HYPOTHESIS TESTING CYCLE", "{{title: whose product, which problem, cycle dates}}")
        sh = slide.shapes
        x0, w, gap = 0.5, 2.97, 0.15
        lanes = [
            ("Problem", "problem", "the problem and its measured size"),
            ("Hypothesis", "hypothesis", "hypothesis: change, effect and reason"),
            ("Action · experiment", "experiment", "what is tested, where and for how long"),
            ("Metrics", "metrics", "success and failure thresholds"),
        ]
        for i, (tag, key, hint) in enumerate(lanes):
            x = x0 + i * (w + gap)
            kind = MSO_SHAPE.CHEVRON if i else MSO_SHAPE.PENTAGON
            text(box(sh, x, 1.3, w + (0.1 if i < 3 else 0), 0.45, fill=INK, line=None, kind=kind), tag,
                 size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, 1.85, w, 2.2), f"{{{{{key}: {hint}}}}}", size=11)

        label(sh, 0.5, 4.2, 6.5, 0.35, "Data · by period", size=12, bold=True)
        tbl = sh.add_table(4, 4, Inches(0.5), Inches(4.6), Inches(6.5), Inches(2.6)).table
        tbl.columns[0].width = Inches(2.0)
        for c in range(1, 4):
            tbl.columns[c].width = Inches(1.5)
        cells = [["Metric"] + [f"{{{{period{c}: period {c}}}}}" for c in range(1, 4)]]
        cells += [[f"{{{{metric{r}: metric {r}}}}}"] + [f"{{{{m{r}_p{c}: value}}}}" for c in range(1, 4)]
                  for r in range(1, 4)]
        for r, row in enumerate(cells):
            for c, value in enumerate(row):
                cell = tbl.cell(r, c)
                cell.text = ""
                tf = cell.text_frame
                tf.word_wrap = True
                run = tf.paragraphs[0].add_run()
                run.text = value
                run.font.size, run.font.name = Pt(10), FONT
                run.font.bold = r == 0 or c == 0
                run.font.color.rgb = WHITE if r == 0 else INK
                cell.fill.solid()
                cell.fill.fore_color.rgb = INK if r == 0 else (ACCENT_BG if c == 0 else WHITE)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE

        for x, pw, name, key, hint, fill in [
            (7.2, 2.75, "Insights · interim", "subresults", "interim findings from the test", None),
            (10.1, 2.73, "Outcome and decision", "results", "outcome and the decision taken", ACCENT_BG),
        ]:
            label(sh, x, 4.2, pw, 0.35, name, size=12, bold=True)
            text(box(sh, x, 4.6, pw, 2.6, fill=fill), f"{{{{{key}: {hint}}}}}", size=10)


class ExperimentCard(PptxSpec):
    @property
    def rel(self):
        return "product-validation/experiment-card/experiment-card.pptx"

    example = {"text": {
        "title": "FreshDrop express slots, test 1–14 September 2026",
        "question": "Does showing 2-hour slots on the home screen raise slot-to-order conversion?",
        "hypothesis": "Buyers abandon because the slot picker sits two taps deep",
        "right_if": "Slot-to-order rises from 61% to 70% or more in 2 weeks, in 2 districts with 50% of traffic",
        "people": "New and returning buyers in Khimki and Mytishchi, about 9,000 sessions",
        "materials": "Home screen mockup, A/B flag, 40,000 RUB for push messages",
        "procedure": "2 weeks, 50/50 split by user ID, 9,000 sessions, checked daily",
        "observations": "Variant: 70.4% slot-to-order vs control 61.2%; errors 15% vs 27%",
        "conclusion": "Validated: roll out to all Moscow districts from 1 October",
        "validated": "✓",
        "invalidated": "",
        "uncertain": "",
    }}

    def draw(self, prs, slide):
        header(slide, "EXPERIMENT CARD", "{{title: product, what we are testing, dates}}")
        sh = slide.shapes

        def field(x, y, w, h, tag, key, hint, fill=None, tag_color=INK):
            box(sh, x, y, w, h, fill=fill)
            label(sh, x + 0.04, y + 0.03, w - 0.08, 0.3, tag, size=10, bold=True, color=tag_color)
            text(box(sh, x, y + 0.3, w, h - 0.3, line=None), f"{{{{{key}: {hint}}}}}", size=10)

        lx, rx, w, g = 0.5, 6.78, 6.05, 0.1
        y = 1.3
        for h, tag, key, hint in [
            (1.1, "1 Our question is", "question", "the question the test answers"),
            (1.2, "2 Our hypothesis is", "hypothesis", "the hypothesis we test"),
            (1.2, "3 We are right if", "right_if", "the result that confirms the hypothesis"),
        ]:
            field(lx, y, w, h, tag, key, hint)
            y += h + g
        hw = (w - g) / 2
        field(lx, y, hw, 7.2 - y, "4 People", "people", "who is in the test and sample size")
        field(lx + hw + g, y, hw, 7.2 - y, "Materials", "materials", "what we need: assets, budget, tools")

        y = 1.3
        for h, tag, key, hint in [
            (1.95, "5 Our procedure is", "procedure", "test design: split, duration, checks"),
            (1.95, "6 Our observations were", "observations", "what we measured, with figures"),
        ]:
            field(rx, y, w, h, tag, key, hint)
            y += h + g
        field(rx, y, w, 7.2 - y - 0.75, "7 Our hypothesis was", "conclusion", "the conclusion and the next step",
              fill=ACCENT_BG, tag_color=ACCENT)
        vy, vw = 7.2 - 0.65, (w - 2 * g) / 3
        for i, (tag, key, fill, color) in enumerate([
            ("Validated", "validated", GOOD_BG, GOOD),
            ("Invalidated", "invalidated", BAD_BG, BAD),
            ("Uncertain", "uncertain", None, MUTED),
        ]):
            x = rx + i * (vw + g)
            box(sh, x, vy, vw, 0.65, fill=fill, line=color)
            label(sh, x + 0.04, vy + 0.02, vw - 0.08, 0.28, tag, size=9, bold=True, color=color)
            text(box(sh, x, vy + 0.28, vw, 0.35, line=None), f"{{{{{key}: ✓}}}}", size=11, bold=True,
                 color=color, align=PP_ALIGN.CENTER)


class ValidationBoard(PptxSpec):
    @property
    def rel(self):
        return "product-validation/validation-board/validation-board.pptx"

    example = {"text": {
        "title": "FreshDrop, product team, August–September 2026",
        "customer_0": "Busy Moscow buyers",
        "customer_1": "Office workers in the centre",
        "customer_2": "Families with 2+ kids",
        "customer_3": "Families with 2+ kids in 2 districts",
        "customer_4": "Families, 2 districts, weekly box",
        "problem_0": "Groceries take too long to order",
        "problem_1": "Slots are hard to pick after work",
        "problem_2": "No time for a weekly shop",
        "problem_3": "Weekly shop from a saved list",
        "problem_4": "Saved list and fixed slot",
        "solution_0": "Express 30-minute delivery",
        "solution_1": "One-tap slot choice",
        "solution_2": "Family weekly box",
        "solution_3": "Weekly box with fixed slot",
        "solution_4": "2-district pilot, 9,000 sessions",
        "assumptions": "Families pay 10% more for a fixed slot and order at least 3 times a month",
        "riskiest": "Families will commit to a fixed weekly slot before they pay for it",
        "method": "12 interviews and a landing page with weekly box pre-orders",
        "criterion": "At least 5% of landing visitors pre-order before we build",
        "results": "Landing: 500 visits, 31 pre-orders (6.2%); 9 of 12 interviewees said yes",
        "invalidated": "No: the weekly box assumption held, so no pivot",
        "validated": "✓ Weekly box goes to build; next step is a 2-district pilot from 1 November",
    }}

    def draw(self, prs, slide):
        header(slide, "VALIDATION BOARD", "{{title: product, who is testing, dates}}")
        sh = slide.shapes

        def field(x, y, w, h, tag, key, hint, fill=None, tag_color=INK, size=10):
            box(sh, x, y, w, h, fill=fill, line=tag_color if fill else LINE)
            label(sh, x + 0.04, y + 0.03, w - 0.08, 0.3, tag, size=10, bold=True, color=tag_color)
            text(box(sh, x, y + 0.3, w, h - 0.3, line=None), f"{{{{{key}: {hint}}}}}", size=size)

        label(sh, 0.5, 1.2, 6, 0.32, "Hypothesis pivots · track pivots", size=12, bold=True)
        rows = [("Customer", "customer", "customer segment"), ("Problem", "problem", "problem to solve"),
                ("Solution", "solution", "solution tried")]
        cols = ["Start", "Pivot 1", "Pivot 2", "Pivot 3", "Pivot 4"]
        tbl = sh.add_table(4, 6, Inches(0.5), Inches(1.55), Inches(12.33), Inches(2.4)).table
        tbl.columns[0].width = Inches(1.78)
        for c in range(1, 6):
            tbl.columns[c].width = Inches(2.11)
        tbl.rows[0].height = Inches(0.36)
        for r in range(1, 4):
            tbl.rows[r].height = Inches(0.68)
        cells = [[""] + cols]
        for tag, key, hint in rows:
            cells.append([tag] + [f"{{{{{key}_{c}: {hint}}}}}" for c in range(5)])
        for r, row in enumerate(cells):
            for c, value in enumerate(row):
                cell = tbl.cell(r, c)
                cell.text = ""
                tf = cell.text_frame
                tf.word_wrap = True
                run = tf.paragraphs[0].add_run()
                run.text = value
                run.font.size, run.font.name = Pt(10), FONT
                run.font.bold = r == 0 or c == 0
                run.font.color.rgb = WHITE if r == 0 else INK
                cell.fill.solid()
                cell.fill.fore_color.rgb = INK if r == 0 else (ACCENT_BG if c == 0 else WHITE)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE if r == 0 or c == 0 else MSO_ANCHOR.TOP

        y0 = 4.15
        label(sh, 0.5, y0, 6, 0.32, "Experiment · design experiments", size=12, bold=True)
        y1, bottom = y0 + 0.4, 7.2
        field(0.5, y1, 2.75, bottom - y1, "Core assumptions", "assumptions",
              "what must be true for the hypothesis")
        fx, fw, fh = 3.35, 3.4, (bottom - y1 - 0.1) / 3
        for i, (tag, key, hint, fill, color) in enumerate([
            ("Riskiest", "riskiest", "the assumption to test first", ACCENT_BG, ACCENT),
            ("Method", "method", "test method used", None, INK),
            ("Minimum success criterion", "criterion", "success number set in advance", None, INK),
        ]):
            field(fx, y1 + i * (fh + 0.05), fw, fh, tag, key, hint, fill=fill, tag_color=color)
        ax = fx + fw + 0.1
        text(box(sh, ax, y1 + 0.75, 1.55, 1.15, fill=LINE, line=None, kind=MSO_SHAPE.RIGHT_ARROW),
             "Get out of the building", size=9, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        rx = ax + 1.65
        rw = 12.83 - rx
        field(rx, y1, rw, 1.55, "Results", "results", "people reached and what they said and did")
        vw = (rw - 0.1) / 2
        vy = y1 + 1.65
        for i, (tag, key, hint, fill, color) in enumerate([
            ("Invalidated", "invalidated", "outcome and what we change", BAD_BG, BAD),
            ("Validated", "validated", "outcome and the next step", GOOD_BG, GOOD),
        ]):
            field(rx + i * (vw + 0.1), vy, vw, bottom - vy, tag, key, hint, fill=fill, tag_color=color)


class AbTesting(XlsxSpec):
    @property
    def rel(self):
        return "product-validation/ab-testing/ab-testing.xlsx"

    example = {"text": {
        "title": "FreshDrop checkout, one-tap slot choice, 1–14 September 2026",
        "hypothesis": "if the slot is chosen on the first screen, the order rate will grow, because fewer taps are needed",
        "metric": "order conversion from the cart",
        "guardrails": "average check, cancellations, courier complaints",
        "audience": "app users, split by user ID, 50/50, excluding staff accounts",
        "duration": "about 2 weeks: 38,000 users in total",
        "decision_rule": "better: conversion up and average check flat; worse or not proven: keep the old flow",
        "baseline": "4.2%",
        "mde": "5%",
        "daily": "2,700",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "A-B"
        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        section = Font(name=FONT, bold=True, size=12, color="2F6FDE")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        input_fill = PatternFill("solid", fgColor="FFF7E0")
        thin = Side(style="thin", color="C9CED6")
        wrap = Alignment(wrap_text=True, vertical="top")

        ws["A1"] = "A/B Testing: {{title: product, what is compared, test dates}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:I1")

        ws["A2"] = "Plan"
        ws["A2"].font = section
        plan = [
            ("Hypothesis", "{{hypothesis: expected change and its reason}}"),
            ("Primary metric", "{{metric: primary metric the decision is based on}}"),
            ("Guardrail metrics", "{{guardrails: metrics that must not get worse}}"),
            ("Who is in the test", "{{audience: randomization unit, variant shares, exclusions}}"),
            ("Duration and size", "{{duration: users and whole weeks of the test}}"),
            ("Decision rule", "{{decision_rule: actions for better, worse and not proven}}"),
        ]
        for i, (lab, tok) in enumerate(plan, start=3):
            ws.cell(i, 1, lab).font = bold
            c = ws.cell(i, 2, tok)
            c.font, c.alignment = regular, wrap
            ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=9)
            ws.row_dimensions[i].height = 30

        ws["A10"], ws["B10"] = "Significance level α", 0.05
        ws["A11"], ws["B11"] = "Power 1 − β", 0.8
        for c in ("B10", "B11"):
            ws[c].fill, ws[c].number_format = input_fill, "0%"
        for c in ("A10", "A11"):
            ws[c].font = muted
        ws["C10"] = "the probability of seeing a difference that is not there; usually 5%"
        ws["C11"] = "the probability of noticing a difference if it exists; usually 80%"
        for c in ("C10", "C11"):
            ws[c].font = muted

        ws["A12"] = "Results — the first row is always the control (A)"
        ws["A12"].font = section
        headers = [
            ("Variant", "The variant name. The first row is the control, the current version.", 30),
            ("Users", "How many units of split fell into the variant over the whole test.", 14),
            ("Conversions", "How many of them performed the target action of the primary metric.", 13),
            ("Conversion rate", "Calculated automatically: conversions / users.", 12),
            ("Difference vs A, rel.", "Calculated automatically: how much higher or lower the variant's conversion rate is than the control, as a percentage of the control.", 14),
            ("p-value", "Calculated automatically: a two-sided two-proportion z-test against the control. Below α — the difference is significant.", 11),
            ("95% CI of difference, from", "Calculated automatically: the lower bound of the confidence interval of the conversion difference, in percentage points. The level is 1 − α.", 14),
            ("95% CI of difference, to", "Calculated automatically: the upper bound of the confidence interval of the conversion difference, in percentage points.", 14),
            ("Conclusion", "Calculated automatically from α: \"better than A\", \"worse than A\" or \"difference not proven\". Decide by the rule in the plan.", 22),
        ]
        hr = 13
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(hr, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            c.comment = Comment(hint, "pdm-skills", width=260, height=110)
            ws.column_dimensions[c.column_letter].width = width
        ws.row_dimensions[hr].height = 44
        ws.column_dimensions["J"].width = 4

        f, last = 14, 18
        for r in range(f, last + 1):
            ws.cell(r, 4, f'=IF(OR(B{r}="",C{r}="",B{r}=0),"",C{r}/B{r})').number_format = "0.00%"
            if r > f:
                se_pool = (f"SQRT(((C{r}+$C${f})/(B{r}+$B${f}))*(1-(C{r}+$C${f})/(B{r}+$B${f}))*(1/B{r}+1/$B${f}))")
                se_diff = f"SQRT(D{r}*(1-D{r})/B{r}+$D${f}*(1-$D${f})/$B${f})"
                z = f"NORMSINV(1-$B$10/2)"
                ok = f'OR(D{r}="",$D${f}="")'
                ws.cell(r, 5, f'=IF(OR({ok},$D${f}=0),"",D{r}/$D${f}-1)').number_format = "+0.0%;-0.0%;0.0%"
                ws.cell(r, 6, f'=IF({ok},"",2*(1-NORMSDIST(ABS(D{r}-$D${f})/{se_pool})))').number_format = "0.000"
                ws.cell(r, 7, f'=IF({ok},"",D{r}-$D${f}-{z}*{se_diff})').number_format = "+0.00%;-0.00%"
                ws.cell(r, 8, f'=IF({ok},"",D{r}-$D${f}+{z}*{se_diff})').number_format = "+0.00%;-0.00%"
                ws.cell(r, 9, f'=IF(F{r}="","",IF(F{r}<$B$10,IF(D{r}>$D${f},"better than A","worse than A"),"difference not proven"))')
            else:
                for c in range(5, 10):
                    ws.cell(r, c, "—" if c == 9 else "")
                ws.cell(r, 9, '=IF(B14="","","control")')
            ws.cell(r, 10, f'=IF(B{r}="","",(B{r}-SUM($B${f}:$B${last})/COUNT($B${f}:$B${last}))^2'
                           f'/(SUM($B${f}:$B${last})/COUNT($B${f}:$B${last})))')
            ws.cell(r, 10).font = Font(name=FONT, size=8, color="FFFFFF")
            for c in range(1, 10):
                ws.cell(r, c).font = regular
                if c >= 4:
                    ws.cell(r, c).fill = calc_fill
            ws.cell(r, 2).number_format = ws.cell(r, 3).number_format = "#,##0"
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'A-B'!$A${f}")

        ws["A19"] = "Split skew (SRM), p"
        ws["A19"].font = muted
        ws["B19"] = f'=IF(COUNT(B{f}:B{last})<2,"",CHIDIST(SUM(J{f}:J{last}),COUNT(B{f}:B{last})-1))'
        ws["B19"].number_format, ws["B19"].fill = "0.000", calc_fill
        ws["C19"] = (f'=IF(B19="","",IF(B19<0.001,"users were not split evenly — the results cannot be trusted, '
                     f'look for a split error","the split is fine (for equal shares)"))')
        ws["C19"].font = muted

        ws["A21"] = "Sample size"
        ws["A21"].font = section
        calc = [
            ("Baseline conversion", "{{baseline: current conversion of the primary metric}}", "0.00%", True),
            ("Minimum detectable effect, rel.", "{{mde: difference to detect, % of baseline}}", "0.0%", True),
            ("Needed per variant", "=IF(OR(B22=\"\",B23=\"\",ISTEXT(B22),ISTEXT(B23)),\"\",ROUNDUP((NORMSINV(1-B10/2)+NORMSINV(B11))^2"
                                 "*(B22*(1-B22)+B22*(1+B23)*(1-B22*(1+B23)))/(B22*B23)^2,0))", "#,##0", False),
            ("Variants in the test", 2, "0", True),
            ("Users per day, total", "{{daily: randomization units entering per day}}", "#,##0", True),
            ("Days", "=IF(OR(B24=\"\",B26=\"\",ISTEXT(B26)),\"\",ROUNDUP(B24*B25/B26,0))", "0", False),
            ("Whole weeks", "=IF(B27=\"\",\"\",MAX(1,ROUNDUP(B27/7,0)))", "0", False),
        ]
        for i, (lab, val, fmt, is_input) in enumerate(calc, start=22):
            ws.cell(i, 1, lab).font = muted
            c = ws.cell(i, 2, val)
            c.number_format, c.fill = fmt, input_fill if is_input else calc_fill
            c.font = regular
        ws["C28"] = "the test runs for whole weeks: weekday and weekend behaviour differ"
        ws["C28"].font = muted

        for rng, lo, hi, msg in [("B10", 0.001, 0.2, "α — from 0.1% to 20%"), ("B11", 0.5, 0.99, "Power — from 50% to 99%")]:
            dv = DataValidation(type="decimal", operator="between", formula1=str(lo), formula2=str(hi), allow_blank=True,
                                errorStyle="warning", showErrorMessage=True, error=msg)
            dv.add(rng)
            ws.add_data_validation(dv)
        ws.freeze_panes = "A14"


class AaTesting(XlsxSpec):
    @property
    def rel(self):
        return "product-validation/aa-testing/aa-testing.xlsx"

    example = {"text": {
        "title": "FreshDrop split system, 1–5 August 2026",
        "goal": "the split system and the significance calculation after the update",
        "metric": "order conversion from the cart",
        "audience": "app users, split by user ID, 50/50",
        "runs": "10 re-splits of history, 4 days each; no live traffic",
        "decision_rule": "if more than 5% of runs are significant, fix the split before the next test",
    }}

    def draw(self, wb):
        from openpyxl.chart import BarChart, Reference
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "A-A"
        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        section = Font(name=FONT, bold=True, size=12, color="2F6FDE")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        input_fill = PatternFill("solid", fgColor="FFF7E0")
        thin = Side(style="thin", color="C9CED6")
        wrap = Alignment(wrap_text=True, vertical="top")

        ws["A1"] = "A/A Testing: {{title: product, what is being checked, dates}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:K1")

        ws["A2"] = "Plan"
        ws["A2"].font = section
        plan = [
            ("What we check", "{{goal: what is checked and what changed}}"),
            ("Metric", "{{metric: metric compared in the runs}}"),
            ("Who is in the test", "{{audience: randomization unit, group shares, exclusions}}"),
            ("Runs", "{{runs: number of runs and duration of each}}"),
            ("Decision rule", "{{decision_rule: actions for too many significant runs or skewed split}}"),
        ]
        for i, (lab, tok) in enumerate(plan, start=3):
            ws.cell(i, 1, lab).font = bold
            c = ws.cell(i, 2, tok)
            c.font, c.alignment = regular, wrap
            ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=11)
            ws.row_dimensions[i].height = 30

        ws["A9"], ws["B9"] = "Significance level α", 0.05
        ws["A10"], ws["B10"] = "Planned share of group A", 0.5
        for c in ("B9", "B10"):
            ws[c].fill, ws[c].number_format = input_fill, "0%"
        ws["A9"].font = ws["A10"].font = muted
        ws["C9"] = "the same level as in future tests; usually 5%"
        ws["C10"] = "the share of users the system should send to A"
        ws["C9"].font = ws["C10"].font = muted

        f, prepared, last = 25, 100, 1000
        I = f"I{f}:I{last}"
        J = f"J{f}:J{last}"
        ws["A12"] = "Summary across all runs"
        ws["A12"].font = section
        summary = [
            ("Runs", f"=COUNT({I})", "0"),
            ("Significant at α", f"=SUMPRODUCT(ISNUMBER({I})*({I}<B9))", "0"),
            ("Share significant", "=IF(B13=0,\"\",B14/B13)", "0.0%"),
            ("p that this many significant results are chance", "=IF(B13=0,\"\",IF(B14=0,1,1-BINOMDIST(B14-1,B13,B9,TRUE)))", "0.000"),
            ("Runs with split skew", f"=SUMPRODUCT(ISNUMBER({J})*({J}<0.001))", "0"),
            ("Uniformity of p-values, p", "=IF(B13<20,\"\",CHIDIST(SUMPRODUCT((O14:O23-B13/10)^2)/(B13/10),9))", "0.000"),
        ]
        for i, (lab, formula, fmt) in enumerate(summary, start=13):
            ws.cell(i, 1, lab).font = muted
            c = ws.cell(i, 2, formula)
            c.number_format, c.fill, c.font = fmt, calc_fill, regular
        ws["C15"] = "=IF(B15=\"\",\"\",\"expected about \"&TEXT(B9,\"0%\"))"
        ws["C16"] = ("=IF(B16=\"\",\"\",IF(B16<0.05,\"more significant results than chance gives — look for an error in the split, "
                     "the metric or the calculation\",\"within chance\"))")
        ws["C17"] = ("=IF(B13=0,\"\",IF(B17=0,\"the split is fine\",IF(1-BINOMDIST(B17-1,B13,0.001,TRUE)<0.01,\"more skews than chance gives — look for a split error\",\"a single skew in the series — within chance\")))")
        ws["C18"] = ("=IF(B13<20,\"at least 20 runs are needed, 100 is better\",IF(B18<0.01,\"the p-values are not uniformly distributed — "
                     "the significance calculation does not suit the metric\",\"the p-values are uniformly distributed\"))")
        for r in range(15, 19):
            ws.cell(r, 3).font = muted
            ws.cell(r, 3).alignment = Alignment(horizontal="left")
            ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=11)
        ws["A20"], ws["A20"].font = "Conclusion", bold
        ws["B20"] = ("=IF(B13=0,\"\",IF(OR(AND(B17>0,1-BINOMDIST(MAX(B17,1)-1,B13,0.001,TRUE)<0.01),AND(B16<>\"\",B16<0.05),AND(B18<>\"\",B18<0.01)),"
                     "\"the system is wrong — do not trust tests until it is fixed\","
                     "IF(B13<20,\"no errors visible, but too few runs\",\"the system is fine — tests can be launched\")))")
        ws["B20"].font = bold
        ws["B20"].alignment = Alignment(horizontal="left")
        ws.merge_cells("B20:K20")

        ws["N12"] = "p-value histogram"
        ws["N12"].font = section
        ws.merge_cells("N12:P12")
        ws["N13"], ws["O13"] = "from", "runs"
        ws["N13"].font = ws["O13"].font = bold
        for k in range(10):
            r = 14 + k
            ws.cell(r, 14, k / 10).number_format = "0.0"
            hi = "<=" if k == 9 else "<"
            ws.cell(r, 15, f"=SUMPRODUCT(ISNUMBER({I})*({I}>=N{r})*({I}{hi}N{r}+0.1))").fill = calc_fill
            ws.cell(r, 14).font = ws.cell(r, 15).font = regular
        ws.column_dimensions["N"].width = 6
        ws.column_dimensions["O"].width = 10
        chart = BarChart()
        chart.type = "col"
        chart.title = "p-values by bin: with a healthy system the bars are roughly equal"
        chart.add_data(Reference(ws, min_col=15, min_row=13, max_row=23), titles_from_data=True)
        chart.set_categories(Reference(ws, min_col=14, min_row=14, max_row=23))
        chart.legend = None
        chart.y_axis.title = "runs"
        chart.x_axis.title = "p-value from"
        chart.x_axis.delete = False
        chart.y_axis.delete = False
        chart.gapWidth = 20
        chart.height, chart.width = 7, 13
        ws.add_chart(chart, "Q12")

        ws["A23"] = "Runs — one row per test or re-split"
        ws["A23"].font = section
        headers = [
            ("Run", "The name or date of the run. One row for a single test.", 18),
            ("Users A", "How many units of split fell into group A.", 13),
            ("Conversions A", "How many of them performed the target action.", 12),
            ("Users B", "How many units of split fell into group B.", 13),
            ("Conversions B", "How many of them performed the target action.", 12),
            ("Conversion rate A", "Calculated automatically.", 11),
            ("Conversion rate B", "Calculated automatically.", 11),
            ("Difference B vs A, rel.", "Calculated automatically. The groups see the same thing, so the difference is only noise.", 13),
            ("p-value", "Calculated automatically: a two-sided two-proportion z-test. Below α in about α of runs is normal.", 10),
            ("Split, p", "Calculated automatically: whether the share of A matches the planned one. Below 0.001 — split skew, a system error.", 11),
            ("Conclusion", "Calculated automatically: \"split skew\", \"significant — false positive\" or \"no difference\".", 32),
        ]
        hr = f - 1
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(hr, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            c.comment = Comment(hint, "pdm-skills", width=260, height=110)
            ws.column_dimensions[c.column_letter].width = width
        ws.column_dimensions["A"].width = 38
        ws.row_dimensions[hr].height = 44

        for r in range(f, f + prepared):
            ok = f"OR(B{r}=\"\",C{r}=\"\",D{r}=\"\",E{r}=\"\",B{r}=0,D{r}=0)"
            pool = f"(C{r}+E{r})/(B{r}+D{r})"
            ws.cell(r, 6, f"=IF({ok},\"\",C{r}/B{r})").number_format = "0.00%"
            ws.cell(r, 7, f"=IF({ok},\"\",E{r}/D{r})").number_format = "0.00%"
            ws.cell(r, 8, f"=IF(OR({ok},C{r}=0),\"\",G{r}/F{r}-1)").number_format = "+0.0%;-0.0%;0.0%"
            ws.cell(r, 9, f"=IF(OR({ok},C{r}+E{r}=0,C{r}+E{r}=B{r}+D{r}),\"\","
                          f"2*(1-NORMSDIST(ABS(G{r}-F{r})/SQRT({pool}*(1-{pool})*(1/B{r}+1/D{r})))))").number_format = "0.000"
            ws.cell(r, 10, f"=IF(OR(B{r}=\"\",D{r}=\"\",B{r}+D{r}=0),\"\","
                           f"2*(1-NORMSDIST(ABS(B{r}-(B{r}+D{r})*$B$10)/SQRT((B{r}+D{r})*$B$10*(1-$B$10)))))").number_format = "0.000"
            ws.cell(r, 11, f"=IF(J{r}=\"\",\"\",IF(J{r}<0.001,\"split skew\",IF(I{r}=\"\",\"\","
                           f"IF(I{r}<$B$9,\"significant — false positive\",\"no difference\"))))")
            for c in range(1, 12):
                ws.cell(r, c).font = regular
                if c >= 6:
                    ws.cell(r, c).fill = calc_fill
            ws.cell(r, 11).alignment = Alignment(horizontal="left")
            for c in (2, 3, 4, 5):
                ws.cell(r, c).number_format = "#,##0"
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'A-A'!$A${f}")

        for rng, lo, hi, msg in [("B9", 0.001, 0.2, "α — from 0.1% to 20%"), ("B10", 0.01, 0.99, "Share — from 1% to 99%")]:
            dv = DataValidation(type="decimal", operator="between", formula1=str(lo), formula2=str(hi), allow_blank=True,
                                errorStyle="warning", showErrorMessage=True, error=msg)
            dv.add(rng)
            ws.add_data_validation(dv)
        ws.freeze_panes = f"A{f}"


class PrototypingProcess(PptxSpec):
    @property
    def rel(self):
        return "product-validation/prototyping-process/prototyping-process.pptx"

    example = {"text": {
        "title": "FreshDrop express slots, test 1–14 September 2026",
        "hypothesis": "If buyers see 2-hour slots on the first screen, they book one in under a minute, because the picker stops being hidden",
        "question": "Will 8 of 10 buyers find and pick a slot without help in under 60 seconds?",
        "scope": "Home screen, slot picker, cart and checkout for 3 scenarios; payment is only drawn",
        "participants": "8 Moscow buyers who ordered in the last 30 days, recruited by SMS",
        "tasks": "Order milk and bread for tomorrow evening, choose a slot, pay",
        "observe": "Where they hesitate on the picker, which button they tap first, what they expect",
        "findings": "7 of 8 booked a slot, median time 52 s; 3 missed the picker on the first screen",
        "sketch": "", "mockup": "", "clickable": "✓", "wizard": "", "live": "",
        "go": "", "iterate": "✓", "drop": "",
        "next": "Move 2-hour slots to the first screen; retest with 6 buyers on 20 September",
    }}

    def draw(self, prs, slide):
        header(slide, "PROTOTYPING PROCESS · TESTING A SOLUTION WITH A PROTOTYPE", "{{title: product, what is being tested, dates}}")
        sh = slide.shapes

        def field(x, y, w, h, tag, key, hint, fill=None, tag_color=INK):
            box(sh, x, y, w, h, fill=fill)
            label(sh, x + 0.04, y + 0.03, w - 0.08, 0.3, tag, size=10, bold=True, color=tag_color)
            text(box(sh, x, y + 0.3, w, h - 0.3, line=None), hint, size=10)

        def mark(x, y, w, tag, key, fill, color):
            box(sh, x, y, w, 0.42, fill=fill, line=color)
            label(sh, x + 0.04, y + 0.04, w - 1.4, 0.34, tag, size=9, bold=True, color=color, anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x + w - 1.35, y + 0.04, 1.3, 0.34, line=None), "{{%s}}" % key, size=10, bold=True,
                 color=color, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        x0, w, gap, top, bottom = 0.5, 2.97, 0.15, 1.85, 7.2
        for i, tag in enumerate(["1 Hypothesis", "2 Prototype", "3 Test", "4 Decision"]):
            x = x0 + i * (w + gap)
            kind = MSO_SHAPE.CHEVRON if i else MSO_SHAPE.PENTAGON
            text(box(sh, x, 1.3, w + (0.1 if i < 3 else 0), 0.45, fill=INK, line=None, kind=kind), tag,
                 size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        x = x0
        field(x, top, w, 2.5, "Hypothesis", "hypothesis", "{{hypothesis: expected user behaviour and its reason}}")
        field(x, top + 2.6, w, bottom - top - 2.6, "What the prototype must show", "question",
              "{{question: question whose answer changes the decision}}")

        x = x0 + (w + gap)
        label(sh, x, top, w, 0.3, "Fidelity", size=10, bold=True)
        for k, (tag, key) in enumerate([
            ("Sketch, paper", "sketch"),
            ("Screen mockup", "mockup"),
            ("Clickable mockup", "clickable"),
            ("Human simulation", "wizard"),
            ("On real data", "live"),
        ]):
            mark(x, top + 0.35 + k * 0.5, w, tag, key, None, ACCENT)
        y = top + 0.35 + 5 * 0.5 + 0.05
        field(x, y, w, bottom - y, "What is in the prototype", "scope", "{{scope: screens and scenario steps; what is only drawn}}")

        x = x0 + 2 * (w + gap)
        field(x, top, w, 1.55, "Participants", "participants", "{{participants: who, how many, how selected}}")
        field(x, top + 1.65, w, 1.9, "Tasks", "tasks", "{{tasks: what we ask them to do, without hints}}")
        field(x, top + 3.65, w, bottom - top - 3.65, "What we observe", "observe", "{{observe: where they get stuck and what they expected}}")

        x = x0 + 3 * (w + gap)
        field(x, top, w, 2.3, "What we found", "findings", "{{findings: facts and figures: successes, mistakes}}",
              fill=ACCENT_BG, tag_color=ACCENT)
        y = top + 2.4
        for k, (tag, key, fill, color) in enumerate([
            ("Go", "go", GOOD_BG, GOOD),
            ("Iterate", "iterate", None, MUTED),
            ("Drop", "drop", BAD_BG, BAD),
        ]):
            mark(x, y + k * 0.5, w, tag, key, fill, color)
        y += 3 * 0.5 + 0.05
        field(x, y, w, bottom - y, "What we change and what next", "next", "{{next: changes to the solution and the next test}}")


class FakeDoorTest(PptxSpec):
    @property
    def rel(self):
        return "product-validation/fake-door-test/fake-door-test.pptx"

    example = {"text": {
        "title": "FreshDrop, express slot button in the app, 1–7 September 2026",
        "hypothesis": "buyers in Moscow who order weekly need express slots; at least 8% will tap the button",
        "element": "bottom of the cart: «Express slot: 149 rub»; the same text as the real feature",
        "stub": "«Express slots are coming in October. Leave an email and we will tell you first.»",
        "audience": "Moscow app users with 2+ orders in 3 months, half of them, 7 days",
        "threshold": "build from 5% click-through; drop below 2%; set on 1 September, before launch",
        "result": "click-through 4.1% overall, Moscow weekly buyers 5.8%; effect on orders not measured",
        "decision": "build the slot picker; email everyone who clicked when it launches",
        "g1": "Moscow, weekly buyers",
        "g2": "Moscow, all buyers",
        "g3": "Saint Petersburg",
        "g4": "Students",
        "v1": "2,310",
        "v2": "1,870",
        "v3": "940",
        "v4": "1,120",
        "a1": "118",
        "a2": "74",
        "a3": "31",
        "a4": "52",
        "r1": "5.1%",
        "r2": "4.0%",
        "r3": "3.3%",
        "r4": "4.6%",
    }}

    def draw(self, prs, slide):
        s = slide.shapes
        A = MSO_ANCHOR.MIDDLE
        header(slide, "FAKE DOOR TEST", "{{title: feature, product, and test dates}}")
        x0, W, gap = 0.5, 12.33, 0.165

        text(box(s, x0, 1.2, 2.0, 0.55, fill=ACCENT, line=None), "Hypothesis", size=12, bold=True, color=WHITE, anchor=A)
        text(box(s, 2.5, 1.2, W - 2.0, 0.55, fill=ACCENT_BG),
             "{{hypothesis: segment, need, and share who will click}}", size=11, anchor=A)

        cw = (W - 2 * gap) / 3
        cols = [("Interface element", "element", "{{element: where it sits and what it is called}}"),
                ("Stub after the click", "stub", "{{stub: what the person who clicked sees}}"),
                ("Audience and duration", "audience", "{{audience: who was shown it, share of users, days}}")]
        for i, (nm, k, h) in enumerate(cols):
            x = x0 + i * (cw + gap)
            text(box(s, x, 1.9, cw, 0.32, fill=INK, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
            text(box(s, x, 2.22, cw, 0.78), h, size=10, anchor=A)

        label(s, x0, 3.05, W, 0.3, "Reaction: click-through share", size=11, bold=True, color=ACCENT)
        widths = [6.33, 2.0, 2.0, 2.0]
        heads = ["Segment or variant", "Saw", "Clicked", "Click-through share"]
        xs = [x0]
        for w in widths[:-1]:
            xs.append(xs[-1] + w)
        for x, w, hd in zip(xs, widths, heads):
            text(box(s, x, 3.35, w, 0.32, fill=ACCENT, line=WHITE), hd, size=10, bold=True, color=WHITE, anchor=A)
        ry, rh = 3.67, 0.4
        hints = [("g", ["{{g%d: segment or text variant}}" % n for n in range(1, 5)]), ("v", ["{{v%d: number of views}}" % n for n in range(1, 5)]), ("a", ["{{a%d: number of clicks}}" % n for n in range(1, 5)]), ("r", ["{{r%d: share}}" % n for n in range(1, 5)])]
        for n in range(1, 5):
            for j, (x, w) in enumerate(zip(xs, widths)):
                k, h = hints[j]
                cell = text(box(s, x, ry + (n - 1) * rh, w, rh), h[n - 1],
                            size=10, anchor=A, align=PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER)
                if j:
                    cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.02)

        y = 5.4
        blocks = [("Threshold and volume", "threshold", "{{threshold: build and drop shares, views needed}}", INK, None),
                  ("What the reaction showed", "result", "{{result: share by segment, effect, what was not measured}}", INK, None),
                  ("Decision", "decision", "{{decision: next step, and what clickers are told}}", GOOD, GOOD_BG)]
        for i, (nm, k, h, c, bg) in enumerate(blocks):
            x = x0 + i * (cw + gap)
            text(box(s, x, y, cw, 0.34, fill=c, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
            text(box(s, x, y + 0.34, cw, 1.5, fill=bg), h, size=10)


class LandingPageTest(PptxSpec):
    @property
    def rel(self):
        return "product-validation/landing-page-test/landing-page-test.pptx"

    example = {"text": {
        "title": "FreshDrop express slots, Moscow, 1–10 September 2026",
        "hypothesis": "we believe busy families will want fixed express slots; the sign-up rate at 10% will confirm it, because our surveys show slot misses",
        "page": "headline «Fixed slot, no missed courier», price 149 rub, button «Choose a slot»",
        "traffic": "Moscow families, targeted ads in messenger; 4,200 people saw it",
        "action": "leave an email to get the early access link",
        "s1": "visit the page", "s2": "click «Choose a slot»", "s3": "leave an email", "s4": "confirm the plan",
        "n1": "4,200", "n2": "610", "n3": "205", "n4": "48",
        "p1": "—", "p2": "14.5%", "p3": "33.6%", "p4": "23.4%",
        "t1": "100%", "t2": "14.5%", "t3": "4.9%", "t4": "1.1%",
        "threshold": "strong at 5% or more leave an email; we need 4,000 visitors",
        "result": "4,200 views, 610 clicks, 48 plans; buyers said the price is clear",
        "decision": "build the early access flow in the app; change the price block for the second test",
    }}

    def draw(self, prs, slide):
        s = slide.shapes
        A = MSO_ANCHOR.MIDDLE
        header(slide, "LANDING PAGE / PRESENTATION / CONTACT COLLECTION", "{{title: idea, audience and test dates}}")
        x0, W, gap = 0.5, 12.33, 0.165

        text(box(s, x0, 1.2, 2.0, 0.55, fill=ACCENT, line=None), "Hypothesis", size=12, bold=True, color=WHITE, anchor=A)
        text(box(s, 2.5, 1.2, W - 2.0, 0.55, fill=ACCENT_BG),
             "{{hypothesis: belief, audience and confirming criterion}}", size=11, anchor=A)

        cw = (W - 2 * gap) / 3
        cols = [("Page or presentation", "page", "page contents"),
                ("Where visitors come from", "traffic", "channel and audience of visitors"),
                ("Target action", "action", "action we ask for")]
        for i, (nm, k, h) in enumerate(cols):
            x = x0 + i * (cw + gap)
            text(box(s, x, 1.9, cw, 0.32, fill=INK, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
            text(box(s, x, 2.22, cw, 0.78), "{{%s: %s}}" % (k, h), size=10, anchor=A)

        label(s, x0, 3.05, W, 0.3, "Visitor reaction steps", size=11, bold=True, color=ACCENT)
        widths = [6.33, 2.0, 2.0, 2.0]
        heads = ["Step (from the view to the most costly action)", "Number of people", "To previous step", "To views"]
        xs = [x0]
        for w in widths[:-1]:
            xs.append(xs[-1] + w)
        for x, w, hd in zip(xs, widths, heads):
            text(box(s, x, 3.35, w, 0.32, fill=ACCENT, line=WHITE), hd, size=10, bold=True, color=WHITE, anchor=A)
        ry, rh = 3.67, 0.4
        hints = [("s", "step, what people did"), ("n", "number of people"), ("p", "share, %"), ("t", "share, %")]
        for n in range(1, 5):
            for j, (x, w) in enumerate(zip(xs, widths)):
                k, h = hints[j]
                cell = text(box(s, x, ry + (n - 1) * rh, w, rh), "{{%s%d: %s}}" % (k, n, h),
                            size=10, anchor=A, align=PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER)
                if j:
                    cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.02)

        y = 5.4
        blocks = [("Threshold and volume", "threshold", "conversion threshold and visitor count", INK, None),
                  ("What the reaction showed", "result", "figures by step and what we learned", INK, None),
                  ("Decision", "decision", "next step: build, change or stop", GOOD, GOOD_BG)]
        for i, (nm, k, h, c, bg) in enumerate(blocks):
            x = x0 + i * (cw + gap)
            text(box(s, x, y, cw, 0.34, fill=c, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
            text(box(s, x, y + 0.34, cw, 1.5, fill=bg), "{{%s: %s}}" % (k, h), size=10)


class MinimumViableProduct(PptxSpec):
    @property
    def rel(self):
        return "product-validation/minimum-viable-product/minimum-viable-product.pptx"

    example = {"text": {
        "title": "FreshDrop weekly plan, 20 families, September 2026",
        "hypothesis": "families with 2+ children in Moscow pay for a fixed slot, because they miss the courier now",
        "assumption": "families will pay 149 rub for a slot; if not, nothing else matters",
        "real": "a paid slot order in the app",
        "manual": "the team books slots by hand in a spreadsheet; the ops lead confirms each order",
        "skip": "the weekly plan, the loyalty points and the SMS reminders",
        "metric": "share of paid slot orders; confirmed at 8% of cart checkouts",
        "sample": "120 families in 2 districts; 3 weeks",
        "cost": "budget 300,000 rub; 2 people for 3 weeks",
        "result": "41 paid orders (6.1%); feedback: «the slot is what I need»; the 8% target was not reached",
        "decision": "change the price to 129 rub and repeat for 2 weeks; decision on 1 October 2026",
    }}

    def draw(self, prs, slide):
        s = slide.shapes
        header(slide, "MINIMUM VIABLE PRODUCT", "{{title: what we test, on whom and when}}")
        A = MSO_ANCHOR.MIDDLE
        x0, wl, xv = 0.5, 2.0, 2.5
        wv = 12.83 - xv

        def row(y, h, name, key, hint, fill=None, bg=ACCENT_BG, size=11):
            text(box(s, x0, y, wl, h, fill=fill or ACCENT, line=None), name, size=12, bold=True, color=WHITE, anchor=A)
            text(box(s, xv, y, wv, h, fill=bg), "{{%s: %s}}" % (key, hint), size=size, anchor=A)

        row(1.2, 0.55, "Hypothesis", "hypothesis", "audience, need and reason")
        row(1.8, 0.55, "Risky\nassumption", "assumption", "riskiest assumption to test", fill=BAD, bg=BAD_BG)

        # form of MVP
        y = 2.45
        label(s, x0, y, 12.33, 0.3, "MVP form", size=11, bold=True, color=ACCENT)
        cw, gap = 4.0, 0.165
        cols = [("Real for the user", GOOD, GOOD_BG, "real", "what the user gets"),
                ("Done manually", ACCENT, ACCENT_BG, "manual", "what the team does by hand"),
                ("Not building", MUTED, RGBColor(0xF1, 0xF2, 0xF4), "skip", "features left out")]
        for i, (nm, c, bg, k, h) in enumerate(cols):
            x = x0 + i * (cw + gap)
            text(box(s, x, y + 0.32, cw, 0.34, fill=c, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
            text(box(s, x, y + 0.66, cw, 0.8, fill=bg), "{{%s: %s}}" % (k, h), size=10, anchor=A)

        # measurement
        y = 4.05
        label(s, x0, y, 12.33, 0.3, "How we measure", size=11, bold=True, color=ACCENT)
        items = [("Metric and success threshold", "metric", "metric and success threshold"),
                 ("Sample and duration", "sample", "sample size and duration"),
                 ("Costs", "cost", "budget and people involved")]
        for i, (nm, k, h) in enumerate(items):
            x = x0 + i * (cw + gap)
            text(box(s, x, y + 0.32, cw, 0.34, fill=INK, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
            text(box(s, x, y + 0.66, cw, 0.7, fill=None), "{{%s: %s}}" % (k, h), size=10, anchor=A)

        row(5.5, 0.6, "Result", "result", "measured result and quotes", fill=INK, bg=WHITE, size=10)
        row(6.2, 0.75, "Decision", "decision", "decision taken and its date", fill=GOOD, bg=GOOD_BG, size=10)


class PackagingOfferTest(PptxSpec):
    @property
    def rel(self):
        return "product-validation/packaging-offer-test/packaging-offer-test.pptx"

    example = {"text": {
        "title": "FreshDrop family box, offer test on 2 product pages, September 2026",
        "hypothesis": "families with children in Moscow need a weekly box, and the offer will attract at least 5% of visitors",
        "audience": "families in 3 Moscow districts: online ads and a shelf card in 2 shops",
        "pack": "a shelf card and a box insert with «Fixed slot, dinner on time»",
        "action": "clicks «Get the box» and leaves a phone number",
        "o1": "«Fixed slot, no missed courier»", "o2": "«Weekly box: 10 items for 2 children»",
        "o3": "«Dinner in 40 minutes»", "o4": "«Order once, eat all week»",
        "v1": "3,100", "v2": "2,980", "v3": "3,020", "v4": "2,940",
        "a1": "92", "a2": "146", "a3": "71", "a4": "58",
        "r1": "3.0%", "r2": "4.9%", "r3": "2.4%", "r4": "2.0%",
        "threshold": "strong at 4% or more; 3,000 views per variant needed",
        "result": "variant 1 converts 4.9%, variant 3 converts 2.0%; Moscow families beat the other groups",
        "decision": "test the box in 5 stores; drop the variant 3 offer",
    }}

    def draw(self, prs, slide):
        s = slide.shapes
        A = MSO_ANCHOR.MIDDLE
        header(slide, "AD / BROCHURE / PACKAGING · OFFER TEST", "{{title: idea, audience and test dates}}")
        x0, W, gap = 0.5, 12.33, 0.165

        text(box(s, x0, 1.2, 2.0, 0.55, fill=ACCENT, line=None), "Hypothesis", size=12, bold=True, color=WHITE, anchor=A)
        text(box(s, 2.5, 1.2, W - 2.0, 0.55, fill=ACCENT_BG),
             "{{hypothesis: audience, need and expected reaction}}", size=11, anchor=A)

        cw = (W - 2 * gap) / 3
        cols = [("Audience and channel", "audience", "audience and channel"),
                ("Packaging", "pack", "packaging contents"),
                ("Non-binding action", "action", "action we ask for")]
        for i, (nm, k, h) in enumerate(cols):
            x = x0 + i * (cw + gap)
            text(box(s, x, 1.9, cw, 0.32, fill=INK, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
            text(box(s, x, 2.22, cw, 0.78), "{{%s: %s}}" % (k, h), size=10, anchor=A)

        label(s, x0, 3.05, W, 0.3, "Offer variants and reaction", size=11, bold=True, color=ACCENT)
        widths = [6.33, 2.0, 2.0, 2.0]
        heads = ["Offer (wording on the packaging)", "Shown", "Showed interest", "Conversion"]
        xs = [x0]
        for w in widths[:-1]:
            xs.append(xs[-1] + w)
        for x, w, hd in zip(xs, widths, heads):
            text(box(s, x, 3.35, w, 0.32, fill=ACCENT, line=WHITE), hd, size=10, bold=True, color=WHITE, anchor=A)
        ry, rh = 3.67, 0.4
        hints = [("o", "offer text, variant"), ("v", "views, count"), ("a", "responses, count"), ("r", "share, %")]
        for n in range(1, 5):
            for j, (x, w) in enumerate(zip(xs, widths)):
                k, h = hints[j]
                cell = text(box(s, x, ry + (n - 1) * rh, w, rh), "{{%s%d: %s}}" % (k, n, h),
                            size=10, anchor=A, align=PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER)
                if j:
                    cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.02)

        y = 5.4
        blocks = [("Threshold and volume", "threshold", "threshold and views needed", INK, None),
                  ("What the reaction showed", "result", "figures by variant and audience", INK, None),
                  ("Decision", "decision", "next step and the variant kept", GOOD, GOOD_BG)]
        for i, (nm, k, h, c, bg) in enumerate(blocks):
            x = x0 + i * (cw + gap)
            text(box(s, x, y, cw, 0.34, fill=c, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
            text(box(s, x, y + 0.34, cw, 1.5, fill=bg), "{{%s: %s}}" % (k, h), size=10)


class PhysicalModeling(PptxSpec):
    @property
    def rel(self):
        return "product-validation/physical-modeling/physical-modeling.pptx"

    example = {"text": {
        "title": "FreshDrop courier bag, insulated, 3 variants",
        "hypothesis": "a bag with a separate cold compartment keeps food cold for 40 minutes for the courier on the route",
        "model": "a foam mock-up of the bag, 30 × 40 cm, built in our office",
        "people": "5 couriers and 2 shop staff, tested on the route",
        "term": "12–26 September 2026; 2 fix cycles",
        "sc1": "courier takes a 4-stop route with hot and cold orders",
        "sc2": "courier takes a 4-stop route with hot and cold orders",
        "sc3": "courier takes a 4-stop route with hot and cold orders",
        "cr1": "food stays at 4 °C or lower for 40 minutes",
        "cr2": "food stays at 4 °C or lower for 40 minutes",
        "cr3": "food stays at 4 °C or lower for 40 minutes",
        "ra1": "6 °C after 40 minutes in 3 of 5 tests",
        "ra2": "6 °C after 40 minutes in 3 of 5 tests",
        "ra3": "6 °C after 40 minutes in 3 of 5 tests",
        "ch1": "thicker inner wall, cold pack moved to the side",
        "ch2": "thicker inner wall, cold pack moved to the side",
        "ch3": "thicker inner wall, cold pack moved to the side",
        "rb1": "4 °C after 40 minutes in 5 of 5 tests",
        "rb2": "4 °C after 40 minutes in 5 of 5 tests",
        "rb3": "4 °C after 40 minutes in 5 of 5 tests",
        "decision": "criteria met on 2 of 3 variants; move the second variant to production; revisit the handle",
    }}

    def draw(self, prs, slide):
        s = slide.shapes
        A = MSO_ANCHOR.MIDDLE
        header(slide, "PHYSICAL MODELING", "{{title: solution and where we model it}}")
        x0, W, gap = 0.5, 12.33, 0.165

        text(box(s, x0, 1.2, 2.0, 0.55, fill=ACCENT, line=None), "Hypothesis", size=12, bold=True, color=WHITE, anchor=A)
        text(box(s, 2.5, 1.2, W - 2.0, 0.55, fill=ACCENT_BG),
             "{{hypothesis: solution feature under test, and users}}", size=11, anchor=A)

        cw = (W - 2 * gap) / 3
        for i, (nm, k, h) in enumerate([
                ("Model", "model", "what we build and its size"),
                ("Participants", "people", "who takes part"),
                ("Term", "term", "dates and number of fix cycles")]):
            x = x0 + i * (cw + gap)
            text(box(s, x, 1.9, cw, 0.32, fill=INK, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
            text(box(s, x, 2.22, cw, 0.8), "{{%s: %s}}" % (k, h), size=10)

        cols = [("Scenario", "sc", "situation the participant goes through", 2.9),
                ("Criterion", "cr", "pass or fail threshold", 2.4),
                ("Run 1", "ra", "result of the first run", 2.2),
                ("Fix", "ch", "change made after the run", 2.5),
                ("Run 2", "rb", "result of the second run", 2.33)]
        y = 3.2
        x = x0
        for nm, k, h, w in cols:
            text(box(s, x, y, w, 0.32, fill=ACCENT, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
            for n in range(3):
                text(box(s, x, y + 0.32 + n * 0.58, w, 0.58), "{{%s%d: %s}}" % (k, n + 1, h), size=9, anchor=A)
            x += w
        y = 5.5
        text(box(s, x0, y, W, 0.34, fill=GOOD, line=None), "Decision", size=11, bold=True, color=WHITE, anchor=A)
        text(box(s, x0, y + 0.34, W, 1.3, fill=GOOD_BG),
             "{{decision: result against criteria and next step}}", size=10)


class PilotProject(PptxSpec):
    @property
    def rel(self):
        return "product-validation/pilot-project/pilot-project.pptx"

    example = {"text": {
        "title": "FreshDrop reminder pilot, 2 districts, 50 buyers, 1–21 September 2026",
        "hypothesis": "buyers in the pilot districts get a fixed slot delivery in time; the reminder lowers missed slots",
        "trial": "one key feature: the reminder 15 minutes before the slot; the rest done by hand",
        "people": "50 buyers from 2 districts, chosen at random among weekly buyers",
        "term": "1–21 September 2026; a free slot for each participant",
        "criteria": "missed slots below 5% (from 14%), by 21 September; the team lead decides",
        "numbers": "share of participants who kept the slot, and orders per week",
        "feedback": "«I stopped calling the shop», three people asked for the reminder on all orders",
        "decision": "scale to all of Moscow if missed slots fall by 20%; otherwise rework the reminder time and repeat",
    }}

    def draw(self, prs, slide):
        s = slide.shapes
        A = MSO_ANCHOR.MIDDLE
        header(slide, "PILOT PROJECT / SAMPLE", "{{title: idea, participants and test dates}}")
        x0, W, gap = 0.5, 12.33, 0.165

        text(box(s, x0, 1.2, 2.0, 0.55, fill=ACCENT, line=None), "Hypothesis", size=12, bold=True, color=WHITE, anchor=A)
        text(box(s, 2.5, 1.2, W - 2.0, 0.55, fill=ACCENT_BG),
             "{{hypothesis: group, benefit and trial solution}}", size=11, anchor=A)

        cw = (W - 2 * gap) / 3

        def row(y, hh, items, headfill=INK):
            for i, (nm, k, h) in enumerate(items):
                x = x0 + i * (cw + gap)
                text(box(s, x, y, cw, 0.32, fill=headfill, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
                text(box(s, x, y + 0.32, cw, hh), "{{%s: %s}}" % (k, h), size=10)

        row(1.9, 1.0, [
            ("Trial solution", "trial", "trial solution and its main feature"),
            ("Participants", "people", "participants: who and how chosen"),
            ("Term and conditions", "term", "dates and conditions for participants")])
        row(3.3, 1.2, [
            ("Criteria and threshold", "criteria", "criteria, threshold and who decides"),
            ("Result: figures", "numbers", "measured figures"),
            ("Result: feedback", "feedback", "participant quotes and requests")], headfill=ACCENT)

        y = 5.2
        text(box(s, x0, y, W, 0.34, fill=GOOD, line=None), "Decision", size=11, bold=True, color=WHITE, anchor=A)
        text(box(s, x0, y + 0.34, W, 1.4, fill=GOOD_BG),
             "{{decision: scale, rework or stop, and on what basis}}",
             size=10)


class SingleFeaturePrototype(PptxSpec):
    @property
    def rel(self):
        return "product-validation/single-feature-prototype/single-feature-prototype.pptx"

    example = {"text": {
        "title": "FreshDrop reminder, concierge test with 10 buyers, August 2026",
        "hypothesis": "if a buyer gets a reminder before the slot, then missed slots fall, which the share of kept slots will confirm, because our data shows misses",
        "need": "a buyer needs a fixed slot; the test is a manual slot booking by chat",
        "approach": "Concierge: the team books the slots by hand for 10 buyers",
        "behind": "ops books the slot, the courier is told by the app team; the log is a shared sheet",
        "m1": "need solved: slot reminder",
        "m2": "need solved: weekly plan",
        "m3": "need solved: fast checkout",
        "m4": "need solved: cheap delivery",
        "t1": "≥ 70% of users",
        "t2": "≥ 70%",
        "t3": "≥ 50%",
        "t4": "≥ 30%",
        "f1": "8 of 10",
        "f2": "6 of 10",
        "f3": "4 of 10",
        "f4": "3 of 10",
        "c1": "keep, build",
        "c2": "build later",
        "c3": "drop",
        "c4": "drop",
        "group": "10 buyers from Moscow, chosen from the survey, 14 days",
        "result": "9 of 10 kept their slot; 2 asked for the evening slot; ops spent 25 minutes per order",
        "decision": "automate the reminder first; stop the manual slot booking after 1 month",
    }}

    def draw(self, prs, slide):
        s = slide.shapes
        A = MSO_ANCHOR.MIDDLE
        header(slide, "SINGLE-FEATURE PROTOTYPE · CONCIERGE / WIZARD OF OZ / SOMEONE ELSE'S PRODUCT", "{{title: feature, product and test dates}}")
        x0, W, gap = 0.5, 12.33, 0.165

        text(box(s, x0, 1.2, 2.0, 0.55, fill=ACCENT, line=None), "Hypothesis", size=12, bold=True, color=WHITE, anchor=A)
        text(box(s, 2.5, 1.2, W - 2.0, 0.55, fill=ACCENT_BG),
             "{{hypothesis: role, solution and expected result}}", size=10, anchor=A)

        cw = (W - 2 * gap) / 3
        cols = [("Need and feature", "need", "user need and feature"),
                ("Approach and what the customer sees", "approach", "what the customer sees"),
                ("Behind the scenes", "behind", "what the team does behind the scenes")]
        for i, (nm, k, h) in enumerate(cols):
            x = x0 + i * (cw + gap)
            text(box(s, x, 1.9, cw, 0.32, fill=INK, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
            text(box(s, x, 2.22, cw, 0.9), "{{%s: %s}}" % (k, h), size=10, anchor=A)

        label(s, x0, 3.2, W, 0.3, "Success criteria", size=11, bold=True, color=ACCENT)
        widths = [4.33, 2.0, 2.0, 4.0]
        heads = ["Indicator", "Threshold", "Fact", "Conclusion"]
        xs = [x0]
        for w in widths[:-1]:
            xs.append(xs[-1] + w)
        for x, w, hd in zip(xs, widths, heads):
            text(box(s, x, 3.5, w, 0.32, fill=ACCENT, line=WHITE), hd, size=10, bold=True, color=WHITE, anchor=A)
        ry, rh = 3.82, 0.36
        hints = [("m", "success indicator"), ("t", "threshold"), ("f", "fact"), ("c", "conclusion")]
        for n in range(1, 5):
            for j, (x, w) in enumerate(zip(xs, widths)):
                k, h = hints[j]
                text(box(s, x, ry + (n - 1) * rh, w, rh), "{{%s%d: %s}}" % (k, n, h),
                     size=10, anchor=A, align=PP_ALIGN.LEFT if j in (0, 3) else PP_ALIGN.CENTER)

        y = 5.4
        blocks = [("Participants and duration", "group", "participants and test length", INK, None),
                  ("What the run showed", "result", "figures and what they showed", INK, None),
                  ("Decision", "decision", "decision and next step", GOOD, GOOD_BG)]
        for i, (nm, k, h, c, bg) in enumerate(blocks):
            x = x0 + i * (cw + gap)
            text(box(s, x, y, cw, 0.34, fill=c, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
            text(box(s, x, y + 0.34, cw, 1.5, fill=bg), "{{%s: %s}}" % (k, h), size=10)


class SoftLaunch(PptxSpec):
    @property
    def rel(self):
        return "product-validation/soft-launch/soft-launch.pptx"

    example = {"text": {
        "title": "FreshDrop express slots, 2 districts of Moscow, 1 September 2026",
        "hypothesis": "buyers in 2 districts get a fixed slot from the app; we test value and the price of the slot",
        "packaging": "the 149 rub slot price and the reminder; no TV or outdoor ads",
        "audience": "Moscow districts Basmanny and Tverskoy; buyers with 2+ orders a month",
        "term": "1–28 September 2026; no paid advertising",
        "criteria": "repeat order within 14 days 35%+, conversion 5%+, margin 80 rub per order",
        "numbers": "repeat orders 38%, conversion 5.6%, margin 92 rub: all above threshold",
        "feedback": "«The reminder is what made me order again»; 6 of 10 interviews repeat the same praise",
        "decision": "scale to 6 districts if the margin holds for 4 weeks; otherwise shut down and move buyers to the standard slots",
    }}

    def draw(self, prs, slide):
        s = slide.shapes
        A = MSO_ANCHOR.MIDDLE
        header(slide, "SOFT LAUNCH", "{{title: idea, districts and launch date}}")
        x0, W, gap = 0.5, 12.33, 0.165

        text(box(s, x0, 1.2, 2.0, 0.55, fill=ACCENT, line=None), "Hypothesis", size=12, bold=True, color=WHITE, anchor=A)
        text(box(s, 2.5, 1.2, W - 2.0, 0.55, fill=ACCENT_BG),
             "{{hypothesis: value, business model or both}}", size=11, anchor=A)

        cw = (W - 2 * gap) / 3

        def row(y, hh, items, headfill=INK):
            for i, (nm, k, h) in enumerate(items):
                x = x0 + i * (cw + gap)
                text(box(s, x, y, cw, 0.32, fill=headfill, line=None), nm, size=11, bold=True, color=WHITE, anchor=A)
                text(box(s, x, y + 0.32, cw, hh), "{{%s: %s}}" % (k, h), size=10)

        row(1.9, 1.0, [
            ("Packaging: what differs", "packaging", "what differs in the offer"),
            ("Audience and market", "audience", "audience and market"),
            ("Term and conditions", "term", "dates and conditions")])
        row(3.3, 1.2, [
            ("Criteria and threshold", "criteria", "criteria and threshold"),
            ("Result: figures", "numbers", "measured figures"),
            ("Result: feedback", "feedback", "customer quotes and feedback")], headfill=ACCENT)

        y = 5.2
        text(box(s, x0, y, W, 0.34, fill=GOOD, line=None), "Decision", size=11, bold=True, color=WHITE, anchor=A)
        text(box(s, x0, y + 0.34, W, 1.4, fill=GOOD_BG),
             "{{decision: scale, stop or repeat, and on what basis}}",
             size=10)


class PreMortem(PptxSpec):
    @property
    def rel(self):
        return "product-validation/pre-mortem/pre-mortem.pptx"

    example = {"text": {
        "title": "Client of a subscription-app consultancy, new subscription tier, pre-mortem before launch (2025)",
        "scenario": "The new subscription tier has been launched and has failed",
        "r1": "Existing customers feel cheated when new customers get a better deal",
        "r2": "N/A", "r3": "N/A", "r4": "N/A", "r5": "N/A", "r6": "N/A",
        "a1": "Position the existing tier, not only the new one; add a feature to the higher tier against cannibalization; tell existing customers first; brief support",
        "a2": "N/A", "a3": "N/A", "a4": "N/A", "a5": "N/A", "a6": "N/A",
        "decision": "Launch the tier with the four changes (the risk could not be removed: the tier had to offer more value). Outcome reported: fewer complaints than expected, MRR up",
    }}

    def draw(self, prs, slide):
        header(slide, "PRE-MORTEM · PROSPECTIVE HINDSIGHT",
               "{{title: project, plan under review, date of the session}}")
        sh = slide.shapes
        left, full, g = 0.5, 12.33, 0.1
        label(sh, left, 1.3, 2.2, 0.5, "Imagined failure", size=11, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(box(sh, left + 2.3, 1.3, full - 2.3, 0.5, fill=BAD_BG, line=None),
             "{{scenario: the failure the team is told to assume has happened}}",
             size=12, bold=True, color=BAD, anchor=MSO_ANCHOR.MIDDLE)
        tbl = sh.add_table(7, 3, Inches(left), Inches(2.0), Inches(full), Inches(3.9)).table
        for c, w in enumerate([0.5, 5.4, 6.43]):
            tbl.columns[c].width = Inches(w)
        rows = [["#", "Reasons it failed", "Change to the plan"]]
        rows += [[str(i), f"{{{{r{i}: reason for the failure}}}}", f"{{{{a{i}: change to the plan against it}}}}"]
                 for i in range(1, 7)]
        for r, row in enumerate(rows):
            tbl.rows[r].height = Inches(0.4 if r == 0 else 0.58)
            for c, value in enumerate(row):
                cell = tbl.cell(r, c)
                cell.text = ""
                tf = cell.text_frame
                tf.word_wrap = True
                run = tf.paragraphs[0].add_run()
                run.text = value
                run.font.size, run.font.name = Pt(10), FONT
                run.font.bold = r == 0 or c == 0
                run.font.color.rgb = WHITE if r == 0 else INK
                cell.fill.solid()
                cell.fill.fore_color.rgb = INK if r == 0 else (ACCENT_BG if c == 0 else WHITE)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        label(sh, left, 6.05, 2.2, 1.0, "Decision", size=12, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(box(sh, left + 2.3, 6.05, full - 2.3, 1.0, fill=ACCENT_BG, line=None),
             "{{decision: decision on the plan after the session}}", size=11, anchor=MSO_ANCHOR.MIDDLE)
