from .base import *


# ---------------------------------------------------------------- five whys

class FiveWhys(PptxSpec):
    @property
    def rel(self):
        return "product-analysis/five-whys/five-whys.pptx"

    example = {"text": {
        "title": "Checkout outage, 14 March 2026: 52 min, 1 140 orders lost",
        "problem": "Checkout returned errors for 52 min on 14 March (18:10–19:02); 1 140 orders were not paid",
        "why_1": "The payment service stopped answering after a spike in timeouts",
        "why_2": "Retries had no limit, so the request queue filled up in 9 minutes",
        "why_3": "A config change raised the payment timeout from 2 s to 30 s",
        "why_4": "The change went live without a load test, as a \"minor\" edit",
        "why_5": "Nothing defines which settings are risky, so \"minor\" is judged by the author",
        "root_cause": "Config changes of payment settings skip load-test review; there is no list of risky settings",
        "countermeasure": "Every payment setting needs review and a load test. Owner: Platform lead, by 1 April",
        "check": "No checkout error rate above 1% for 4 weeks after the change; reported weekly",
    }}

    def draw(self, prs, slide):
        header(slide, "5 WHYS · FIVE WHYS", "{{title: what is analysed, event, date, scale}}")
        hints = [
            ("Problem", "{{problem: observed problem, with date and figures}}"),
            ("Why 1", "{{why_1: cause of the problem}}"),
            ("Why 2", "{{why_2: cause of why 1}}"),
            ("Why 3", "{{why_3: cause of why 2}}"),
            ("Why 4", "{{why_4: cause of why 3}}"),
            ("Why 5", "{{why_5: cause of why 4}}"),
        ]
        y, bh, gap = 1.3, 0.72, 0.33
        for i, (tag, token) in enumerate(hints):
            shapes = slide.shapes
            group = None
            if i >= 4:
                group = slide.shapes.add_group_shape()
                group.name = f"optional_level_{i}"
                shapes = group.shapes
            if i > 0:
                arrow = box(shapes, 1.05, y - gap + 0.03, 0.3, gap - 0.06, fill=LINE, line=None, kind=MSO_SHAPE.DOWN_ARROW)
                label(shapes, 1.4, y - gap - 0.01, 1.2, gap, "why?", size=10, color=MUTED, anchor=MSO_ANCHOR.MIDDLE)
            is_problem = i == 0
            text(box(shapes, 0.5, y, 1.4, bh, fill=INK if is_problem else ACCENT_BG, line=None),
                 tag, size=11, bold=True, color=WHITE if is_problem else ACCENT, anchor=MSO_ANCHOR.MIDDLE)
            text(box(shapes, 1.9, y, 6.6, bh), token, size=12, anchor=MSO_ANCHOR.MIDDLE)
            y += bh + gap

        x, w = 8.95, 3.9
        panels = [
            ("Root cause", "{{root_cause: process or condition that can change}}", ACCENT, 1.3, 1.7),
            ("Countermeasure", "{{countermeasure: what we change, owner and date}}", INK, 3.15, 1.9),
            ("How we will check", "{{check: metric showing the problem is gone}}", INK, 5.2, 1.85),
        ]
        for tag, token, color, py, ph in panels:
            label(slide.shapes, x, py, w, 0.35, tag, size=12, bold=True, color=color)
            body = box(slide.shapes, x, py + 0.35, w, ph - 0.35, fill=ACCENT_BG if color == ACCENT else None,
                       line=ACCENT if color == ACCENT else LINE)
            text(body, token, size=12)


# ---------------------------------------------------------------- cohort analysis

class CohortAnalysis(XlsxSpec):
    @property
    def rel(self):
        return "product-analysis/cohort-analysis/cohort-analysis.xlsx"

    example = {"text": {
        "title": "FreshDrop app, cohorts by first order month, Jan–Jun 2026, data as of 1 July 2026",
        "metric": "buyers who placed an order in the month",
        "normalization": "share of cohort size",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.formatting.rule import ColorScaleRule
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.utils import get_column_letter
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        periods, cohorts = 13, 24
        first, last = 6, 6 + cohorts - 1
        last_col = get_column_letter(2 + periods)
        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        thin = Side(style="thin", color="C9CED6")

        data = wb.active
        data.title = "Data"
        table = wb.create_sheet("Cohorts")

        data["A1"] = "Cohort Analysis: {{title: product, cohort attribute and metric}}"
        data["A2"], data["B2"] = "Metric:", "{{metric: what the cells count, e.g. buyers, orders}}"
        data["A3"], data["B3"] = "Normalisation:", "{{normalization: share of cohort size or index}}"
        table["A1"] = "=Data!A1"
        table["A2"], table["B2"] = "Metric:", "=Data!B2"
        table["A3"], table["B3"] = "Normalisation:", "=Data!B3"
        for ws in (data, table):
            ws["A1"].font = Font(name=FONT, bold=True, size=14)
            ws.merge_cells(f"A1:{last_col}1")
            for r in (2, 3):
                ws[f"A{r}"].font = muted
                ws[f"B{r}"].font = bold
                ws.merge_cells(f"B{r}:{last_col}{r}")
        table["A4"] = "The index is also shown in percent: 180% = 1.80 of period 0. Colour: green — above, red — below (excluding period 0)."
        for ws in (data, table):
            ws["A4"].font = muted

        headers = [("Cohort", "Entry period: month, week or year of the first action.", 16),
                   ("Cohort size", "Customers, or amount, that entered the cohort in period 0.", 19)]
        headers += [(f"Period {k}", "Metric value in this period since the cohort start; period 0 is the entry."
                     if k == 0 else f"Metric value {k} period(s) after entry.", 10) for k in range(periods)]
        for ws in (data, table):
            for i, (title, hint, width) in enumerate(headers, start=1):
                c = ws.cell(5, i, title)
                c.font, c.fill = bold, head_fill
                c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center" if i > 1 else "left")
                c.border = Border(bottom=thin)
                if ws is data:
                    c.comment = Comment(hint, "pdm-skills", width=260, height=90)
                ws.column_dimensions[c.column_letter].width = width
            ws.row_dimensions[5].height = 30
            ws.freeze_panes = "C6"

        for r in range(first, last + 1):
            for c in range(1, 3 + periods):
                data.cell(r, c).font = regular
            table.cell(r, 1, f'=IF(Data!A{r}="","",Data!A{r})').font = bold
            table.cell(r, 2, f'=IF(Data!B{r}="","",Data!B{r})').font = muted
            for k in range(periods):
                col = get_column_letter(3 + k)
                base = f"Data!$B{r}"
                f = (f'=IF(Data!{col}{r}="","",IF(Data!$B$3="index to period 0",'
                     f'IF(Data!$C{r}="","",Data!{col}{r}/Data!$C{r}),'
                     f'IF({base}="","",Data!{col}{r}/{base})))')
                cell = table.cell(r, 3 + k, f)
                cell.number_format = "0.0%"
                cell.font = regular
                cell.alignment = Alignment(horizontal="center")
        table.conditional_formatting.add(
            f"D{first}:{last_col}{last}",
            ColorScaleRule(start_type="min", start_color="F8D7D7", mid_type="percentile", mid_value=50,
                           mid_color="FFF6D5", end_type="max", end_color="CDEBD6"))
        data.column_dimensions["A"].width = table.column_dimensions["A"].width = 16
        data.column_dimensions["B"].width = table.column_dimensions["B"].width = 19

        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"Data!$A${first}")
        dv_n = DataValidation(type="list", formula1='"share of cohort size,index to period 0"', allow_blank=True,
                              errorStyle="warning", showErrorMessage=True,
                              error="Normalisation: \"share of cohort size\" or \"index to period 0\"")
        dv_n.add("B3")
        dv_v = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                              errorStyle="warning", showErrorMessage=True, error="Metric values cannot be negative")
        dv_v.add(f"B{first}:{last_col}{last}")
        for dv in (dv_n, dv_v):
            data.add_data_validation(dv)
        wb.active = 1


# ---------------------------------------------------------------- rfm

class RfmAnalysis(XlsxSpec):
    @property
    def rel(self):
        return "product-analysis/rfm-analysis/rfm-analysis.xlsx"

    example = {"text": {
        "title": "FreshDrop buyers, 12 months to 1 September 2026",
        "actions": "R5 F5 M5: loyalty offer, free express slot",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.formatting.rule import ColorScaleRule
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        input_fill = PatternFill("solid", fgColor="FFF6D5")
        thin = Side(style="thin", color="C9CED6")

        ws = wb.active
        ws.title = "Customers"
        ws["A1"] = "RFM Analysis: {{title: customer base, period and calculation date}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:I1")

        ws["A2"] = "Scale thresholds (3 — best, 1 — worst):"
        ws["A2"].font = muted
        scales = [
            (3, "R, days since last purchase", "3 — at most", 30, "2 — at most", 90, "otherwise 1 (churn)",
             "Recency thresholds, in days since the last purchase."),
            (4, "F, orders in the period", "3 — at least", 4, "2 — at least", 2, "otherwise 1 (one-off)",
             "Orders in the analysis period."),
            (5, "M, purchase amount in the period", "3 — at least", 20000, "2 — at least", 5000, "otherwise 1",
             "Purchase amount in the base currency, same period."),
        ]
        for r, name, l3, v3, l2, v2, rest, hint in scales:
            ws.cell(r, 1, name).font = bold
            ws.cell(r, 1).comment = Comment(hint, "pdm-skills", width=260, height=80)
            ws.cell(r, 2, l3).font = muted
            ws.cell(r, 2).alignment = Alignment(shrink_to_fit=True)
            ws.cell(r, 3, v3).font = bold
            ws.cell(r, 4, l2).font = muted
            ws.cell(r, 4).alignment = Alignment(shrink_to_fit=True)
            ws.cell(r, 5, v2).font = bold
            ws.cell(r, 6, rest).font = muted
            for c in (3, 5):
                ws.cell(r, c).fill = input_fill
                ws.cell(r, c).number_format = "#,##0"

        headers = [
            ("Customer", "Customer ID or name, one per row.", 31),
            ("Days since last purchase", "How many days passed from the last purchase to the calculation date.", 16),
            ("Orders", "The customer's number of orders in the analysis period.", 11),
            ("Purchase amount", "The customer's purchase amount in the analysis period.", 16),
            ("R", "Calculated automatically from the thresholds in row 3.", 9),
            ("F", "Calculated automatically from the thresholds in row 4.", 16),
            ("M", "Calculated automatically from the thresholds in row 5.", 9),
            ("RFM", "R-F-M code, e.g. 3-3-2.", 9),
            ("Segment", "Calculated automatically from R and F: recency × frequency.", 26),
        ]
        hr = 7
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(hr, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left" if i in (1, 9) else "center")
            c.border = Border(bottom=thin)
            c.comment = Comment(hint, "pdm-skills", width=240, height=70)
            ws.column_dimensions[c.column_letter].width = width
        ws.row_dimensions[hr].height = 46

        first, last = hr + 1, hr + 300
        for r in range(first, last + 1):
            ws.cell(r, 5, f'=IF(B{r}="","",IF(B{r}<=$C$3,3,IF(B{r}<=$E$3,2,1)))')
            ws.cell(r, 6, f'=IF(C{r}="","",IF(C{r}>=$C$4,3,IF(C{r}>=$E$4,2,1)))')
            ws.cell(r, 7, f'=IF(D{r}="","",IF(D{r}>=$C$5,3,IF(D{r}>=$E$5,2,1)))')
            ws.cell(r, 8, f'=IF(E{r}="","",E{r}&"-"&F{r}&"-"&G{r})')
            ws.cell(r, 9, f'=IF(E{r}="","",CHOOSE(E{r},"Churned","Dormant","Recent")&", "&CHOOSE(F{r},"one-off","medium","frequent"))')
            for c in range(1, 10):
                ws.cell(r, c).font = regular
                if 5 <= c <= 8:
                    ws.cell(r, c).alignment = Alignment(horizontal="center")
            ws.cell(r, 4).number_format = "#,##0"
        ws.freeze_panes = f"B{first}"
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"Customers!$A${first}")
        dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                            errorStyle="warning", showErrorMessage=True, error="The value cannot be negative")
        dv.add(f"B{first}:D{last}")
        for ref in ("C3:C5", "E3:E5"):
            dv.add(ref)
        ws.add_data_validation(dv)

        grid = wb.create_sheet("Segments")
        grid["A1"] = "=Customers!A1"
        grid["A1"].font = Font(name=FONT, bold=True, size=14)
        grid.merge_cells("A1:E1")
        grid["A2"].font = muted
        grid.column_dimensions["A"].width = 30
        for col in "BCDE":
            grid.column_dimensions[col].width = 20
        grid_last = hr + 5000

        def block(top, caption, fmt, value):
            grid.cell(top, 1, caption).font = bold
            for j, title in enumerate(["Frequent (F = 3)", "Medium (F = 2)", "One-off (F = 1)", "Total"], start=2):
                c = grid.cell(top, j, title)
                c.font, c.fill = bold, head_fill
                c.alignment = Alignment(horizontal="center")
            rows = [("Bought recently (R = 3)", 3), ("Dormant (R = 2)", 2), ("Churned (R = 1)", 1)]
            for i, (name, rv) in enumerate(rows, start=1):
                r = top + i
                grid.cell(r, 1, name).font = bold
                for j, fv in enumerate((3, 2, 1), start=2):
                    c = grid.cell(r, j, value(rv, fv))
                    c.number_format, c.font = fmt, regular
                    c.alignment = Alignment(horizontal="center")
                c = grid.cell(r, 5, f"=SUM(B{r}:D{r})")
                c.number_format, c.font = fmt, bold
                c.alignment = Alignment(horizontal="center")
            grid.conditional_formatting.add(
                f"B{top + 1}:D{top + 3}",
                ColorScaleRule(start_type="min", start_color="FFFFFF", end_type="max", end_color="9DC3F5"))

        block(4, "Customers", "#,##0",
              lambda rv, fv: f"=COUNTIFS(Customers!$E${first}:$E${grid_last},{rv},Customers!$F${first}:$F${grid_last},{fv})")
        block(10, "Purchase amount", "#,##0",
              lambda rv, fv: f"=SUMIFS(Customers!$D${first}:$D${grid_last},Customers!$E${first}:$E${grid_last},{rv},"
                             f"Customers!$F${first}:$F${grid_last},{fv})")
        grid["A18"] = "Actions per cell:"
        grid["A18"].font = bold
        grid["A19"] = "{{actions: one action per cell}}"
        grid["A19"].alignment = Alignment(wrap_text=True, vertical="top")
        grid.merge_cells("A19:E27")
        grid["A16"].font = muted


class AbcdxSegmentation(XlsxSpec):
    @property
    def rel(self):
        return "product-analysis/abcdx-segmentation/abcdx-segmentation.xlsx"

    example = {"text": {
        "title": "FreshDrop, September 2026 orders, gross margin as revenue",
        "criteria_a": "weekly buyers with 2+ orders a month in 3–4 categories, almost never contact support",
        "strategy_a": "priority courier slots, referral bonus, features for their requests",
        "criteria_b": "buy 2–3 times a month, pay for delivery, but leave when the slot is late",
        "strategy_b": "fix slot reliability, lower the free delivery threshold",
        "criteria_c": "one-off orders of 1–2 items, small check, long chats about refunds",
        "strategy_c": "automate refunds and chat replies, promo by email only",
        "criteria_d": "sign up for the free promo, leave after the first box, never pay for delivery",
        "strategy_d": "no paid acquisition, minimal service",
        "criteria_x": "Moscow families with children, ready to pay for a weekly box but need a bulk-size product",
        "strategy_x": "test a family box with a 2-week pilot before building it",
        "decision": "focus on segments A and D; test a cheaper delivery plan for B; stop paid push to X",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        seg_fill = {"A": "E8F5EC", "B": "E8F5EC", "C": "F3F4F6", "D": "FBEAEA", "X": "FFF6D5"}
        thin = Side(style="thin", color="C9CED6")

        def head(ws, r, items):
            for i, (title, hint, width) in enumerate(items, start=1):
                c = ws.cell(r, i, title)
                c.font, c.fill = bold, head_fill
                c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left" if i == 1 else "center")
                c.border = Border(bottom=thin)
                if hint:
                    c.comment = Comment(hint, "pdm-skills", width=260, height=90)
                if width:
                    ws.column_dimensions[c.column_letter].width = width
            ws.row_dimensions[r].height = 46

        ws = wb.active
        ws.title = "Customers"
        ws["A1"] = "ABCDX segmentation: {{title: product, period and what counts as revenue}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:G1")
        ws["A2"].font = muted
        hr = 4
        head(ws, hr, [
            ("Customer", "Customer ID or name, one per row.", 28),
            ("Revenue or margin for the period", "Revenue or margin of the customer in the analysis period.", 16),
            ("Purchases", "Number of purchases or payments in the period.", 11),
            ("Cycle, days", "Days from first contact to first payment. May be left empty for B2C.", 13),
            ("Support requests", "How many requests and questions the customer raised in the period.", 14),
            ("Segment", "A, B, C, D or X — per the criteria on the \"Segments\" sheet.", 11),
            ("Why this segment", "Which criterion decided it: one short phrase.", 40),
        ])
        first, last = hr + 1, hr + 300
        for r in range(first, last + 1):
            for c in range(1, 8):
                ws.cell(r, c).font = regular
            ws.cell(r, 2).number_format = "#,##0"
            ws.cell(r, 6).alignment = Alignment(horizontal="center")
        ws.freeze_panes = f"B{first}"
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"Customers!$A${first}")
        num = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                             errorStyle="warning", showErrorMessage=True, error="The value cannot be negative")
        num.add(f"B{first}:E{last}")
        seg = DataValidation(type="list", formula1='"A,B,C,D,X"', allow_blank=True,
                             errorStyle="warning", showErrorMessage=True, error="Segment must be one of the letters A, B, C, D, X")
        seg.add(f"F{first}:F{last}")
        ws.add_data_validation(num)
        ws.add_data_validation(seg)

        sm = wb.create_sheet("Segments")
        sm["A1"] = "=Customers!A1"
        sm["A1"].font = Font(name=FONT, bold=True, size=14)
        sm.merge_cells("A1:I1")
        sm["A2"].font = muted
        head(sm, 4, [
            ("Segment", None, 12),
            ("Criteria: who these customers are", "How the segment's customers differ: need, context, objections.", 38),
            ("Customers", None, 11), ("Share of customers", None, 11),
            ("Revenue", None, 14), ("Share of revenue", None, 11),
            ("Requests", None, 13), ("Share of requests", None, 13),
            ("Strategy", "What we do with the segment.", 38),
        ])
        rng = lambda col: f"Customers!${col}${first}:${col}${hr + 5000}"
        for i, letter in enumerate("ABCDX"):
            r = 5 + i
            sm.cell(r, 1, letter).font = Font(name=FONT, bold=True, size=14)
            sm.cell(r, 2, "{{criteria_%s: who these customers are}}" % letter.lower())
            sm.cell(r, 3, f'=COUNTIF({rng("F")},"{letter}")')
            sm.cell(r, 4, f"=IF($C$10=0,\"\",C{r}/$C$10)")
            sm.cell(r, 5, f'=SUMIF({rng("F")},"{letter}",{rng("B")})')
            sm.cell(r, 6, f"=IF($E$10=0,\"\",E{r}/$E$10)")
            sm.cell(r, 7, f'=SUMIF({rng("F")},"{letter}",{rng("E")})')
            sm.cell(r, 8, f"=IF($G$10=0,\"\",G{r}/$G$10)")
            sm.cell(r, 9, "{{strategy_%s: what we do with the segment}}" % letter.lower())
            for c in range(1, 10):
                cell = sm.cell(r, c)
                cell.fill = PatternFill("solid", fgColor=seg_fill[letter])
                cell.border = Border(bottom=thin)
                cell.alignment = Alignment(wrap_text=True, vertical="top", horizontal="center" if 3 <= c <= 8 or c == 1 else "left")
                if c > 1:
                    cell.font = regular
            for c in (4, 6, 8):
                sm.cell(r, c).number_format = "0%"
            for c in (5,):
                sm.cell(r, c).number_format = "#,##0"
            sm.row_dimensions[r].height = 58
        sm.cell(10, 1, "Total").font = bold
        for c in (3, 5, 7):
            cell = sm.cell(10, c, f"=SUM({sm.cell(5, c).column_letter}5:{sm.cell(9, c).column_letter}9)")
            cell.font, cell.alignment = bold, Alignment(horizontal="center")
            cell.number_format = "#,##0"
        sm.cell(11, 1, "A + B").font = bold
        sm.cell(12, 1, "C + D").font = bold
        for r, (x, y) in ((11, (5, 6)), (12, (7, 8))):
            for c in (4, 6, 8):
                col = sm.cell(5, c).column_letter
                cell = sm.cell(r, c, f"=IF(${sm.cell(10, c - 1).column_letter}$10=0,\"\",{col}{x}+{col}{y})")
                cell.number_format, cell.font = "0%", bold
                cell.alignment = Alignment(horizontal="center")
        sm["B11"] = "share of the best segments"
        sm["B12"] = "share of the weak segments: if requests here exceed revenue, support is working for them"
        for ref in ("B11", "B12"):
            sm[ref].font = muted
            sm[ref].alignment = Alignment(wrap_text=True, vertical="top")
        sm.row_dimensions[12].height = 46

        sm["A14"] = "Customer requests by segment"
        sm["A14"].font = bold
        sm["C14"].font = muted
        head(sm, 15, [
            ("Request or problem", "The topic of requests or a feature request. One topic per row.", None),
            (None, None, None),
            ("From A and B", "How many requests on the topic came from A and B customers.", None),
            ("From C and D", "How many requests on the topic came from C and D customers.", None),
            ("Share of A and B", None, None),
            ("Total", None, None),
        ])
        sm.cell(15, 2).fill = head_fill
        for r in range(16, 26):
            sm.merge_cells(start_row=r, start_column=1, end_row=r, end_column=2)
            cell = sm.cell(r, 5, f'=IF(C{r}+D{r}=0,"",C{r}/(C{r}+D{r}))')
            cell.number_format = "0%"
            sm.cell(r, 6, f'=IF(C{r}+D{r}=0,"",C{r}+D{r})')
            for c in (1, 3, 4, 5, 6):
                sm.cell(r, c).font = regular
                if c > 1:
                    sm.cell(r, c).alignment = Alignment(horizontal="center")
        sm.merge_cells("A15:B15")
        sm["A26"] = "Decision: {{decision: segments in focus and first actions}}"
        sm["A26"].font = bold
        sm["A26"].alignment = Alignment(wrap_text=True, vertical="top")
        sm.merge_cells("A26:I29")
        wb.active = 1


# ---------------------------------------------------------------- AARRR

class AarrrMetrics(PptxSpec):
    @property
    def rel(self):
        return "product-analysis/aarrr-metrics/aarrr-metrics.pptx"

    example = {"text": {
        "title": "FreshDrop, July–August 2026 cohorts, weekly active buyers",
        "acquisition": "6,200 new installs in July: 58% referral, 42% paid ads; CAC 1,150 RUB",
        "activation": "38% of new buyers place a first order within 3 days",
        "retention": "41% of first-time buyers order again within 30 days",
        "referral": "12% of buyers invite a friend; 1 in 4 invitees orders",
        "revenue": "2,450 RUB average spend per buyer per month",
        "acquisition_compare": "July target 6,000 installs; CAC target 1,000 RUB",
        "activation_compare": "target 55%; June cohort 36%",
        "retention_compare": "June cohort 37%; target 45%",
        "referral_compare": "June 9%; target 15%",
        "revenue_compare": "June 2,310 RUB; target 2,600 RUB",
        "bottleneck": "activation: 38% of new users make a first order; benchmark 55%; the address step loses most users",
        "decision": "simplify the address form and show the delivery time before sign-up; check activation after 4 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "AARRR METRICS · PIRATE METRICS", "{{title: product, period and funnel question}}")
        sh = slide.shapes
        label(sh, 2.75, 1.3, 3.6, 0.3, "Metric and value", size=11, bold=True, color=MUTED)
        label(sh, 6.45, 1.3, 2.6, 0.3, "Compared with", size=11, bold=True, color=MUTED)
        stages = [
            ("Acquisition", "Acquisition", "acquisition"),
            ("Activation", "Activation", "activation"),
            ("Retention", "Retention", "retention"),
            ("Referral", "Referral", "referral"),
            ("Revenue", "Revenue", "revenue"),
        ]
        top, h, gap = 1.65, 0.98, 0.1
        for i, (en, ru, key) in enumerate(stages):
            y = top + i * (h + gap)
            inset = i * 0.12
            stage = box(sh, 0.5 + inset, y, 2.1 - 2 * inset, h, fill=ACCENT_BG, line=None, kind=MSO_SHAPE.RECTANGLE)
            text(stage, en, size=13, bold=True, color=ACCENT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, 2.75, y, 3.6, h), "{{%s: metric and value of the stage}}" % key, size=11, anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, 6.45, y, 2.6, h), "{{%s_compare: target, previous period or benchmark}}" % key,
                 size=10, color=MUTED, anchor=MSO_ANCHOR.MIDDLE)
        x, w = 9.25, 3.6
        panels = [
            ("Bottleneck", "{{bottleneck: stage losing most users, and why}}", 1.3, 2.3),
            ("Decision", "{{decision: what we change, metric to verify it, date}}", 3.7, 3.4),
        ]
        for tag, token, py, ph in panels:
            label(sh, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            text(box(sh, x, py + 0.35, w, ph - 0.35), token, size=11)


# ---------------------------------------------------------------- frequency / adoption analysis

class FrequencyAdoptionAnalysis(PptxSpec):
    @property
    def rel(self):
        return "product-analysis/frequency-adoption-analysis/frequency-adoption-analysis.pptx"

    example = {
        "text": {
            "title": "FreshDrop features, 1 August–31 August 2026, 12,400 active buyers",
            "method": "base: buyers with 1+ order in the period; a use is any feature tap; a 30-day window",
            "decision": "develop the slot picker; engage people with a reminder for the rarely used replacement feature; remove the old coupon screen",
            "checks": "rare but critical: refunds; hard to find: express slots; needs replacement: manual cart edit",
        },
        "charts": {"features": {"points": [
            {"label": "Feature X", "x": 80, "y": 16},
            {"label": "Feature Y", "x": 70, "y": 4},
            {"label": "Feature Z", "x": 20, "y": 13},
            {"label": "Feature W", "x": 12, "y": 3},
        ]}},
    }

    def draw(self, prs, slide):
        header(slide, "FREQUENCY / ADOPTION ANALYSIS", "{{title: product, period and base of active customers}}")
        zones = [(25, 19.2, "Special · decide"), (75, 19.2, "Core · develop"),
                 (25, 0.8, "Unneeded · drop"), (75, 0.8, "Utility · automate")]
        features = [("{{feature: feature name}}", 50, 10)]
        data = XyChartData()
        series = [("Adoption boundary", [(50, 0), (50, 20)]), ("Frequency boundary", [(0, 10), (100, 10)])]
        series += [(name, [(x, y)]) for x, y, name in zones]
        series += [(name, [(x, y)]) for name, x, y in features]
        for name, pts in series:
            ser = data.add_series(name)
            for x, y in pts:
                ser.add_data_point(x, y)
        frame = slide.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER, Inches(0.4), Inches(1.3),
                                       Inches(8.6), Inches(5.9), data)
        frame.name = "features"
        chart = frame.chart
        ids = {}
        for el in chart._chartSpace.xpath(".//c:axId | .//c:crossAx"):
            el.set("val", str(ids.setdefault(el.get("val"), 510000 + len(ids))))
        chart.has_legend = False
        chart.font.name, chart.font.size = FONT, Pt(11)
        chart.font.color.rgb = INK
        all_series = list(chart.plots[0].series)
        for ser in all_series[:2]:
            ser.marker.style = XL_MARKER_STYLE.NONE
            ser.format.line.color.rgb = MUTED
            ser.format.line.width = Pt(1.25)
            ser.smooth = False


        for i, ser in enumerate(all_series[2:6]):
            ser.marker.style = XL_MARKER_STYLE.NONE
            ser.format.line.fill.background()
            name_label(ser, XL_LABEL_POSITION.CENTER, 12, True, GOOD if i == 1 else (BAD if i == 2 else MUTED))
        for ser in all_series[6:]:
            ser.format.line.fill.background()
            ser.marker.style = XL_MARKER_STYLE.CIRCLE
            ser.marker.size = 11
            ser.marker.format.fill.solid()
            ser.marker.format.fill.fore_color.rgb = ACCENT
            ser.marker.format.line.color.rgb = WHITE
            name_label(ser, XL_LABEL_POSITION.ABOVE, 11, False, INK)
        for axis, title, top, step, fmt in (
                (chart.category_axis, "Adoption: % of active customers →", 100, 25, '0"%"'),
                (chart.value_axis, "Frequency: uses per customer who adopted the feature per period →", 20, 5, "0")):
            axis.minimum_scale, axis.maximum_scale, axis.major_unit = 0, top, step
            axis.has_major_gridlines = False
            axis.format.line.color.rgb = LINE
            axis.tick_labels.font.size = Pt(10)
            axis.tick_labels.font.color.rgb = MUTED
            axis.tick_labels.number_format, axis.tick_labels.number_format_is_linked = fmt, False
            axis.has_title = True
            axis.axis_title.text_frame.text = title
            r = axis.axis_title.text_frame.paragraphs[0].runs[0]
            r.font.size, r.font.bold, r.font.name = Pt(11), False, FONT
            r.font.color.rgb = MUTED

        x, w = 9.25, 3.6
        panels = [
            ("How it was counted", "{{method: base, period and what counts as use}}", 1.3, 1.75),
            ("Decisions by zone", "{{decision: what we develop, engage, automate or remove}}", 3.15, 2.2),
            ("Check before deciding", "{{checks: critical, hard-to-find and replaced features}}", 5.45, 1.75),
        ]
        for tag, token, py, ph in panels:
            label(slide.shapes, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            text(box(slide.shapes, x, py + 0.35, w, ph - 0.35), token, size=11)


# ---------------------------------------------------------------- feedback matrix

class FeedbackMatrix(PptxSpec):
    @property
    def rel(self):
        return "product-analysis/feedback-matrix/feedback-matrix.pptx"

    example = {"text": {
        "title": "FreshDrop: 412 feedback items, Jun–Aug 2026",
        "advice": "Delivery map: praised, but needs live courier position (96 customers)",
        "compliment": "Fast refunds: «money back in a day» (140 customers)",
        "critique": "Slot picker: hard to find the next free slot (58 customers)",
        "suggestion": "Dark theme: asked often, annoying but usable (22 customers)",
        "scope": "Jun–Aug 2026, 412 statements; «needs fixing» = mentioned by 20+ customers",
        "decision": "Fix the slot picker by 30 Sep (owner: Anna). Accumulate dark theme. Reply to all critiques within 2 days",
    }}

    def draw(self, prs, slide):
        header(slide, "FEEDBACK MATRIX", "{{title: product, period and feedback channels}}")
        sh = slide.shapes
        left, top, cw, ch, gap = 0.95, 1.7, 3.95, 2.7, 0.1
        for i, head in enumerate(("Needs fixing", "Does not need fixing")):
            label(sh, left + i * (cw + gap), 1.3, cw, 0.35, head, size=12, bold=True, color=MUTED, align=PP_ALIGN.CENTER)
        for j, head in enumerate(("Positive tone", "Negative tone")):
            side = box(sh, 0.4, top + j * (ch + gap), 0.45, ch, fill=None, line=None)
            side.text_frame._txBody.bodyPr.set("vert", "vert270")
            text(side, head, size=12, bold=True, color=MUTED, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        cells = [
            (0, 0, "Advice · take into improvements", "{{advice: topic, gist and number of customers}}", ACCENT),
            (1, 0, "Compliment · keep", "{{compliment: topic, gist and number of customers}}", GOOD),
            (0, 1, "Critique · fix first", "{{critique: topic, gist and number of customers}}", BAD),
            (1, 1, "Suggestion · accumulate", "{{suggestion: topic, gist and number of customers}}", MUTED),
        ]
        for i, j, tag, token, color in cells:
            x, y = left + i * (cw + gap), top + j * (ch + gap)
            box(sh, x, y, cw, ch, fill=None, line=color)
            label(sh, x + 0.12, y + 0.08, cw - 0.24, 0.35, tag, size=12, bold=True, color=color)
            text(box(sh, x + 0.12, y + 0.45, cw - 0.24, ch - 0.55, fill=None, line=None), token, size=11)
        x, w = 9.25, 3.6
        panels = [
            ("Feedback and criterion", "{{scope: period, channels and the fix criterion}}", 1.3, 1.95),
            ("Decision", "{{decision: what we fix, accumulate and how we reply}}", 3.4, 3.7),
        ]
        for tag, token, py, ph in panels:
            label(sh, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            text(box(sh, x, py + 0.35, w, ph - 0.35), token, size=11)


class ForcesOfProgress(PptxSpec):
    @property
    def rel(self):
        return "product-analysis/forces-of-progress/forces-of-progress.pptx"

    example = {"text": {
        "title": "Switch from supermarket shopping to FreshDrop: 52 interviews, May 2026",
        "current": "Supermarket visits and a paper list",
        "new": "FreshDrop app with next-day delivery",
        "push": "Queues and no time to shop: 64% of switchers",
        "pull": "Delivery in 2 hours and lower prices: 58%",
        "habit": "Habit of checking produce in person: 41%",
        "anxiety": "Fear of wrong items and bad produce: 35%",
        "balance": "Push and pull outweigh habit and anxiety: 52% of trial users switched within 2 weeks",
        "decision": "Weaken anxiety with a produce guarantee; expect 60% switch rate; check in 4 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "FORCES OF PROGRESS", "{{title: which switch and its data source}}")
        sh = slide.shapes
        for x, tag, token in ((0.5, "Current solution", "{{current: what the customer uses now}}"),
                              (7.1, "New solution", "{{new: what the customer switches to}}")):
            box(sh, x, 1.4, 2.0, 5.6, fill=ACCENT_BG, line=None)
            label(sh, x + 0.05, 1.5, 1.9, 0.6, tag, size=13, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
            text(box(sh, x + 0.05, 2.1, 1.9, 4.8, line=None), token, size=11, align=PP_ALIGN.CENTER)
        forces = [
            (2.65, 1.4, "→ Push", "{{push: unsatisfying factors, with shares}}", GOOD),
            (4.85, 1.4, "→ Pull", "{{pull: what the new solution promises, with shares}}", GOOD),
            (2.65, 4.6, "← Habit", "{{habit: what holds them, with shares}}", BAD),
            (4.85, 4.6, "← Anxiety", "{{anxiety: what they fear, with shares}}", BAD),
        ]
        for x, y, tag, token, color in forces:
            box(sh, x, y, 2.1, 2.4, line=color)
            label(sh, x + 0.08, y + 0.06, 1.95, 0.35, tag, size=12, bold=True, color=color)
            tb = text(box(sh, x + 0.08, y + 0.45, 1.95, 1.9, line=None), token, size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(5)
        arrow = box(sh, 2.65, 3.92, 4.3, 0.56, fill=LINE, line=None, kind=MSO_SHAPE.RIGHT_ARROW)
        text(arrow, "Switch", size=10, bold=True, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
        x, w = 9.3, 3.55
        panels = [
            ("Balance of forces", "{{balance: which forces outweigh, and switch data}}", 1.4, 2.4),
            ("What we move and how we check", "{{decision: which force we change and how we check}}", 4.0, 3.0),
        ]
        for tag, token, py, ph in panels:
            label(sh, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            tb = text(box(sh, x, py + 0.35, w, ph - 0.35), token, size=11)
            tb.text_frame.paragraphs[0].space_after = Pt(5)


class CustomerProfile(PptxSpec):
    @property
    def rel(self):
        return "product-analysis/customer-profile/customer-profile.pptx"

    example = {"text": {
        "title": "FreshDrop profile: busy family buyer, 30–40, with 2+ children",
        "about": "34, marketing manager, two kids; spends about 60 000 a month on groceries; orders weekly",
        "context": "Orders on the phone during the evening commute, for the whole week ahead",
        "value": "Wants reliable slots and fresh produce; success means a complete order on time",
        "problems": "Missing items and late couriers after 21:00; loses about 40 minutes a week to fixing orders",
        "persona": "Olga: plans the family week in one order",
        "sources": "18 interviews (May 2026) and analytics of 2 400 orders",
        "implications": "Fix missing items first; no extra categories for her; check on-time rate every week",
    }}

    def draw(self, prs, slide):
        header(slide, "CUSTOMER PROFILE", "{{title: product and the segment the profile is for}}")
        sh = slide.shapes
        left, top, cw, ch, gap = 0.5, 1.3, 4.15, 2.85, 0.1
        cells = [
            (0, 0, "About", "{{about: who they are, age, role, spending, habits}}"),
            (1, 0, "Context", "{{context: how, where and with what they use it}}"),
            (0, 1, "Value", "{{value: what matters and how they judge success}}"),
            (1, 1, "Problems", "{{problems: obstacles and losses for the customer}}"),
        ]
        for i, j, tag, token in cells:
            x, y = left + i * (cw + gap), top + j * (ch + gap)
            box(sh, x, y, cw, ch, line=BAD if i == 1 and j == 1 else LINE)
            ly = y + 0.06 if j == 0 else y + ch - 0.41
            label(sh, x + 0.1, ly, cw - 0.2, 0.35, tag, size=12, bold=True, color=BAD if i == 1 and j == 1 else ACCENT,
                  align=PP_ALIGN.LEFT if i == 0 else PP_ALIGN.RIGHT)
            tx = x + 0.1 if i == 0 else x + 1.05
            tb = text(box(sh, tx, y + 0.45 if j == 0 else y + 0.1, cw - 1.15, ch - 0.55, line=None), token, size=11)
            tb.text_frame.paragraphs[0].space_after = Pt(4)
        d = 2.1
        cx, cy = left + cw + gap / 2 - d / 2, top + ch + gap / 2 - d / 2
        circle = box(sh, cx, cy, d, d, fill=ACCENT_BG, line=ACCENT, kind=MSO_SHAPE.OVAL)
        text(circle, "{{persona: persona name, one phrase about them}}", size=10, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        x, w = 9.25, 3.6
        panels = [
            ("Data", "{{sources: sources, sample size and date}}", 1.3, 2.2),
            ("Takeaway for the product", "{{implications: problems we solve and what to check}}", 3.7, 3.35),
        ]
        for tag, token, py, ph in panels:
            label(sh, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            tb = text(box(sh, x, py + 0.35, w, ph - 0.35), token, size=11)
            tb.text_frame.paragraphs[0].space_after = Pt(4)


class CustomerJourneyMap(PptxSpec):
    @property
    def rel(self):
        return "product-analysis/customer-journey-map/customer-journey-map.pptx"

    example = {"text": {
        "title": "FreshDrop app, Moscow family buyer, first weekly shop",
        "actor": "Busy parent, Moscow: full weekly shop before 21:00",
        "stage1": "Browse the catalog", "stage2": "Build the cart", "stage3": "Choose a slot",
        "stage4": "Pay and track the courier", "stage5": "Rate and reorder",
        "goals1": "Find milk and eggs fast", "goals2": "Add 15–20 items without losing track",
        "goals3": "Get a slot after work", "goals4": "Know when the courier arrives", "goals5": "Reorder the same basket",
        "touch1": "Search, category tabs", "touch2": "Cart, promo code field", "touch3": "Slot picker, 2-hour windows",
        "touch4": "Map with courier, push alerts", "touch5": "Order history, repeat button",
        "exp1": "Search misses «kefir»: 3 of 10 give up", "exp2": "Total hidden until checkout",
        "exp3": "Only 2 slots left by 19:00: 22% drop", "exp4": "Courier status lags by 10 minutes",
        "exp5": "Reorder hidden in profile: 6 of 10 never find it",
        "ins1": "Add search synonyms for dairy", "ins2": "Show the total in the cart",
        "ins3": "Open 2 more evening slots", "ins4": "Live courier map on the order page",
        "ins5": "Put reorder on the home screen",
        "decision": "Bottleneck: evening slots after 18:00 (22% drop). Test 2 extra slots in 3 Moscow districts from 1 November; check slot-to-order conversion on 15 November.",
    }}

    def draw(self, prs, slide):
        header(slide, "CUSTOMER JOURNEY MAP", "{{title: product, customer type and scenario}}")
        sh = slide.shapes
        rows = [
            ("Goals and expectations", "goals", "what they want and expect"),
            ("Touchpoints and scenarios", "touch", "where they meet the company, what they do"),
            ("Experience and problems", "exp", "what they feel, where it is hard; source"),
            ("Insights and opportunities", "ins", "what follows and what to improve"),
        ]
        n = 5
        left, top, hw, cw, hh, rh = 0.5, 1.3, 1.5, 1.75, 0.6, 1.28
        label(sh, left, top - 0.15, hw, hh + 0.2, "{{actor: customer type and their goal}}", size=9, color=MUTED, anchor=MSO_ANCHOR.MIDDLE)
        for k in range(n):
            x = left + hw + k * cw
            head = box(sh, x, top, cw - 0.05, hh, fill=ACCENT_BG, line=None, kind=MSO_SHAPE.CHEVRON if k else MSO_SHAPE.PENTAGON)
            text(head, "{{stage%d: customer action at this stage}}" % (k + 1), size=10, bold=True, color=ACCENT,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            head.text_frame.margin_left = head.text_frame.margin_right = Inches(0.02)
        for j, (tag, key, hint) in enumerate(rows):
            y = top + hh + 0.1 + j * rh
            color = BAD if key == "exp" else (GOOD if key == "ins" else INK)
            label(sh, left, y, hw - 0.05, rh - 0.05, tag, size=11, bold=True, color=color, anchor=MSO_ANCHOR.MIDDLE)
            for k in range(n):
                x = left + hw + k * cw
                tb = text(box(sh, x, y, cw - 0.05, rh - 0.05, line=BAD if key == "exp" else LINE),
                          "{{%s%d: %s}}" % (key, k + 1, hint), size=9)
                tb.text_frame.paragraphs[0].space_after = Pt(2)
        x, w = 10.9, 1.95
        label(sh, x, top, w, hh, "Decision", size=12, bold=True, color=INK, anchor=MSO_ANCHOR.MIDDLE)
        tb = text(box(sh, x, top + hh + 0.1, w, 4 * rh - 0.05),
                  "{{decision: bottleneck, test, metric and check date}}", size=10)
        tb.text_frame.paragraphs[0].space_after = Pt(4)


class BuyerPersona(PptxSpec):
    @property
    def rel(self):
        return "product-analysis/buyer-persona/buyer-persona.pptx"

    example = {"text": {
        "title": "FreshDrop, busy families with children, Moscow, interviews August 2026",
        "persona": "Olga, mother of two, 38, 12 interviews",
        "quote": "«If the slot is gone, I order from the shop next door.»",
        "goals": "Dinner on the table without a trip to the shop, around the kids' schedule",
        "personal": "Less guilt about shopping; one fixed slot she can plan her evening around",
        "management": "Household budget: keeps the monthly grocery spend under 25,000 RUB",
        "criteria": "1) a fixed slot; 2) fresh produce; 3) prices within 5% of the store",
        "barriers": "Fear of substitutions; card-only payment; a slot that is not reliable",
        "approval": "She decides alone; her partner checks the monthly bill",
        "budget": "Household grocery budget of 25,000 RUB a month, paid by her card",
        "alternatives": "The shop next door with a queue; a rival app with 2-hour slots; skipping the order",
        "decision": "put the slot guarantee first, remove the card-only barrier, hand the family plan to sales; review 1 November 2026",
    }}

    def draw(self, prs, slide):
        header(slide, "BUYER PERSONA",
               "{{title: company or product, buyer segment, interview date}}")
        sh = slide.shapes
        # role and basis
        box(sh, 0.5, 1.25, 6.05, 0.83, fill=ACCENT_BG, line=ACCENT)
        label(sh, 0.56, 1.26, 5.9, 0.3, "Persona", size=10, bold=True, color=ACCENT)
        text(box(sh, 0.56, 1.56, 5.93, 0.5, line=None),
             "{{persona: role and number of interviews}}", size=10)
        box(sh, 6.78, 1.25, 6.05, 0.83)
        label(sh, 6.84, 1.26, 5.9, 0.3, "Buyer's words", size=10, bold=True, color=ACCENT)
        text(box(sh, 6.84, 1.56, 5.93, 0.5, line=None),
             "{{quote: verbatim quote that shows the decision}}", size=10)

        blocks = [
            ("Company goals", "goals", "{{goals: result the organization needs}}"),
            ("Personal motivation", "personal", "{{personal: what the choice gives the buyer personally}}"),
            ("Management motivation", "management", "{{management: what matters to whoever signs or approves}}"),
            ("Decision criteria", "criteria", "{{criteria: main criteria and their meaning}}"),
            ("Barriers to purchase", "barriers", "{{barriers: fears and objections that stop buying}}"),
            ("Approval process", "approval", "{{approval: approval steps and who takes part}}"),
            ("Budget", "budget", "{{budget: which budget pays and who owns it}}"),
            ("Alternatives", "alternatives", "{{alternatives: what they buy instead, and why}}"),
        ]
        x0, y0, w, h, gx, gy = 0.5, 2.18, 6.05, 0.92, 0.23, 0.08
        for i, (tag, key, hint) in enumerate(blocks):
            col, row = i % 2, i // 2
            x, y = x0 + col * (w + gx), y0 + row * (h + gy)
            key_block = key == "criteria" or key == "barriers"
            box(sh, x, y, w, h, fill=ACCENT_BG if key_block else None, line=ACCENT if key_block else LINE)
            label(sh, x + 0.06, y + 0.02, w - 0.12, 0.3, tag, size=10, bold=True, color=ACCENT)
            text(box(sh, x + 0.06, y + 0.32, w - 0.12, h - 0.35, line=None), hint, size=10)

        y = y0 + 4 * (h + gy)
        box(sh, 0.5, y, 12.33, 7.2 - y, fill=ACCENT_BG, line=ACCENT)
        label(sh, 0.56, y + 0.02, 12.2, 0.3, "Decision", size=10, bold=True, color=ACCENT)
        text(box(sh, 0.56, y + 0.32, 12.21, 7.2 - y - 0.35, line=None),
             "{{decision: messages first, barriers to remove, review date}}", size=10)
