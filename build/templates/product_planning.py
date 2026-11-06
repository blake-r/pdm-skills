from .base import *


# ---------------------------------------------------------------- rice

class RiceScoring(XlsxSpec):
    @property
    def rel(self):
        return "product-planning/rice-scoring/rice-scoring.xlsx"

    example = {
        "text": {"title": "FreshDrop backlog for Q3 2026, 6 initiatives", "reach_period": "quarter"},
        "rows": [
            ["Express checkout with saved cards", 12000, 2, 0.8, 2],
            ["Substitutes for out-of-stock items", 30000, 1, 0.8, 3],
            ["Loyalty points for weekly orders", 8000, 2, 0.5, 4],
            ["Dark mode in the app", 40000, 0.25, 1, 1],
            ["Delivery slot reminders by push", 25000, 1, 0.8, 1],
            ["Live chat with couriers", 6000, 1, 0.5, 3],
        ],
    }

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "RICE"
        scales = wb.create_sheet("Scales")

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        thin = Side(style="thin", color="C9CED6")

        ws["A1"] = "RICE Scoring: {{title: what is prioritised, product and period}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws["A2"] = "Reach is counted per: {{reach_period: reporting period for all rows}}"
        ws["A2"].font = Font(name=FONT, size=11, color="6B7280")
        ws.merge_cells("A1:G1")
        ws.merge_cells("A2:G2")

        headers = [
            ("Initiative", "Initiative: one feature or hypothesis per row", 42),
            ("Reach", "Reach: users affected in the period, as a number"
                              "", 16),
            ("Impact", "Impact: effect on the target metric per user, see the Scales sheet"
                                 "", 16),
            ("Confidence", "Confidence: how well the estimates are backed by data"
                                         "", 18),
            ("Effort", "Effort: person-months for the whole team"
                                      "", 18),
            ("RICE\nScore", "Calculated automatically: Reach × Impact × Confidence ÷ Effort.", 14),
            ("Rank", "Calculated automatically: rank by RICE Score, 1 — first to work on.", 10),
        ]
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(3, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            c.comment = Comment(hint, "pdm-skills", width=260, height=110)
            ws.column_dimensions[c.column_letter].width = width
        ws.row_dimensions[3].height = 34

        first, last = 4, 33
        for r in range(first, last + 1):
            ws.cell(r, 6, f'=IF(OR(B{r}="",C{r}="",D{r}="",E{r}="",E{r}=0),"",B{r}*C{r}*D{r}/E{r})').number_format = "#,##0.00"
            ws.cell(r, 7, f'=IF(F{r}="","",RANK(F{r},$F:$F))')
            ws.cell(r, 4).number_format = "0%"
            ws.cell(r, 2).number_format = "#,##0"
            for c in range(1, 8):
                ws.cell(r, c).font = regular
        ws.freeze_panes = "A4"
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text="RICE!$A$4")
        scales["A1"] = "RICE scales (after Sean McBride, Intercom)"
        scales["A1"].font = Font(name=FONT, bold=True, size=12)
        scales["A2"], scales["B2"] = "Impact", "Value"
        scales["D2"], scales["E2"] = "Confidence", "Value"
        for c in ("A2", "B2", "D2", "E2"):
            scales[c].font = bold
        for i, (v, t) in enumerate([(3, "massive"), (2, "high"), (1, "medium"), (0.5, "low"), (0.25, "minimal")], 3):
            scales.cell(i, 1, v).font = regular
            scales.cell(i, 2, t).font = regular
        for i, (v, t) in enumerate([(1, "high"), (0.8, "medium"), (0.5, "low")], 3):
            scales.cell(i, 4, v).number_format = "0%"
            scales.cell(i, 5, t).font = regular
        scales.column_dimensions["B"].width = 16
        scales.column_dimensions["D"].width = 14
        scales.column_dimensions["E"].width = 14

        dv_i = DataValidation(type="list", formula1="=Scales!$A$3:$A$7", allow_blank=True, errorStyle="warning",
                              error="Impact: 3, 2, 1, 0.5 or 0.25", showErrorMessage=True)
        dv_c = DataValidation(type="decimal", operator="between", formula1="0", formula2="1",
                              allow_blank=True, errorStyle="warning", showErrorMessage=True,
                              error="Confidence: 100%, 80% or 50%; below 50% is a blind bet")
        dv_e = DataValidation(type="decimal", operator="greaterThan", formula1="0", allow_blank=True,
                              error="Effort must be a positive number (usually person-months)", showErrorMessage=True)
        dv_i.add(f"C{first}:C{last}")
        dv_c.add(f"D{first}:D{last}")
        dv_e.add(f"E{first}:E{last}")
        for dv in (dv_i, dv_c, dv_e):
            ws.add_data_validation(dv)


class IceScoring(XlsxSpec):
    @property
    def rel(self):
        return "product-planning/ice-scoring/ice-scoring.xlsx"

    example = {
        "text": {"title": "FreshDrop onboarding ideas, target: weekly orders", "method": "average"},
        "rows": [
            ["Show delivery time on the product card", 7, 8, 9],
            ["One-tap reorder of the last basket", 8, 7, 7],
            ["Free delivery banner above the threshold", 6, 5, 9],
            ["Search with product photos", 7, 4, 3],
            ["Referral bonus for the first order", 9, 3, 6],
        ],
    }

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "ICE"

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        thin = Side(style="thin", color="C9CED6")

        ws["A1"] = "ICE Scoring: {{title: what is prioritised, product and target metric}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:F1")
        ws["A2"] = "Calculation method:"
        ws["A2"].font = muted
        ws["B2"] = "{{method: scoring method, average or product}}"
        ws["B2"].font = bold
        ws.merge_cells("B2:F2")

        headers = [
            ("Idea", "Idea: one hypothesis or feature per row", 44),
            ("Impact", "Impact: 1–10, how far the idea moves weekly orders"
                                 "", 14),
            ("Confidence", "Confidence: 1–10, how well the evidence backs the estimate"
                                         "", 16),
            ("Ease", "Ease: 1–10, 10 = easiest to build"
                                "", 14),
            ("ICE", "ICE: calculated automatically, average of the three scores", 12),
            ("Rank", "Calculated automatically: rank by ICE, 1 — first to work on.", 10),
        ]
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(3, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            c.comment = Comment(hint, "pdm-skills", width=260, height=110)
            ws.column_dimensions[c.column_letter].width = width
        ws.row_dimensions[3].height = 34

        first, last = 4, 33
        for r in range(first, last + 1):
            ws.cell(r, 5, f'=IF(OR(B{r}="",C{r}="",D{r}=""),"",'
                          f'IF($B$2="product",B{r}*C{r}*D{r},(B{r}+C{r}+D{r})/3))').number_format = "[<=10]0.0;#,##0"
            ws.cell(r, 6, f'=IF(E{r}="","",RANK(E{r},$E:$E))')
            for c in range(1, 7):
                ws.cell(r, c).font = regular
            ws.cell(r, 1).alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = "A4"
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text="ICE!$A$4")
        dv_m = DataValidation(type="list", formula1='"average,product"', allow_blank=True, errorStyle="warning",
                              error="Method: \"average\" or \"product\"", showErrorMessage=True)
        dv_m.add("B2")
        dv_s = DataValidation(type="decimal", operator="between", formula1="1", formula2="10", allow_blank=True,
                              errorStyle="warning", showErrorMessage=True, error="ICE scores are from 1 to 10")
        dv_s.add(f"B{first}:D{last}")
        for dv in (dv_m, dv_s):
            ws.add_data_validation(dv)


# ---------------------------------------------------------------- impact / effort

class ImpactEffortMatrix(PptxSpec):
    @property
    def rel(self):
        return "product-planning/impact-effort-matrix/impact-effort-matrix.pptx"

    example = {
        "text": {
            "title": "FreshDrop: 4 ideas for the Q3 goal of +10% weekly orders",
            "scales": "Metric: weekly orders per user. Impact 0–10: change in orders. Effort 0–10: team weeks, 10 = the largest",
            "decision": "Now: delivery time on the card (2 weeks). Plan: search with photos as a project. Postpone: dark mode",
            "rejected": "Courier chat: high effort, low gain, rejected for Q3",
        },
        "charts": {"matrix": {"points": [
            {"label": "Delivery time on card", "x": 2, "y": 8},
            {"label": "Search with photos", "x": 7, "y": 7},
            {"label": "Dark mode", "x": 3, "y": 3},
            {"label": "Courier chat", "x": 8, "y": 2},
        ]}},
    }

    def draw(self, prs, slide):
        header(slide, "IMPACT / EFFORT MATRIX", "{{title: product, goal and the set of ideas}}")
        quadrants = [(2.5, 9.55, "Quick wins · 1st priority"), (7.5, 9.55, "Major projects"),
                     (2.5, 0.45, "Fill-ins · 3rd priority"), (7.5, 0.45, "Thankless tasks · do not take")]
        ideas = [("{{idea: idea name}}", 5, 5)]
        data = XyChartData()
        series = [("Effort boundary", [(5, 0), (5, 10)]), ("Impact boundary", [(0, 5), (10, 5)])]
        series += [(name, [(x, y)]) for x, y, name in quadrants]
        series += [(name, [(x, y)]) for name, x, y in ideas]
        for name, pts in series:
            ser = data.add_series(name)
            for x, y in pts:
                ser.add_data_point(x, y)
        frame = slide.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER, Inches(0.4), Inches(1.3),
                                       Inches(8.6), Inches(5.9), data)
        frame.name = "matrix"
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
            ser.format.line.color.rgb = MUTED
            ser.format.line.width = Pt(1.25)
            ser.smooth = False


        for i, ser in enumerate(all_series[2:6]):
            ser.marker.style = XL_MARKER_STYLE.NONE
            ser.format.line.fill.background()
            name_label(ser, XL_LABEL_POSITION.CENTER, 12, True, GOOD if i == 0 else (BAD if i == 3 else MUTED))
        for ser in all_series[6:]:
            ser.format.line.fill.background()
            ser.marker.style = XL_MARKER_STYLE.CIRCLE
            ser.marker.size = 11
            ser.marker.format.fill.solid()
            ser.marker.format.fill.fore_color.rgb = ACCENT
            ser.marker.format.line.color.rgb = WHITE
            name_label(ser, XL_LABEL_POSITION.RIGHT, 11, False, INK)
        for axis, title in ((chart.category_axis, "Implementation effort (Effort), 0–10 →"),
                            (chart.value_axis, "Business impact (Impact), 0–10 →")):
            axis.minimum_scale, axis.maximum_scale, axis.major_unit = 0, 10, 1
            axis.has_major_gridlines = False
            axis.format.line.color.rgb = LINE
            axis.tick_labels.font.size = Pt(10)
            axis.tick_labels.font.color.rgb = MUTED
            axis.has_title = True
            axis.axis_title.text_frame.text = title
            r = axis.axis_title.text_frame.paragraphs[0].runs[0]
            r.font.size, r.font.bold, r.font.name = Pt(11), False, FONT
            r.font.color.rgb = MUTED

        x, w = 9.25, 3.6
        panels = [
            ("Goal and scales", "{{scales: metric and meaning of the 0–10 scales}}", 1.3, 1.75),
            ("What we take on", "{{decision: what we do now, plan and postpone}}", 3.15, 2.2),
            ("What we do not take and why", "{{rejected: ideas not taken, with reasons}}", 5.45, 1.75),
        ]
        for tag, token, py, ph in panels:
            label(slide.shapes, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            text(box(slide.shapes, x, py + 0.35, w, ph - 0.35), token, size=11)


# ---------------------------------------------------------------- cost / benefit

class CostBenefitAnalysis(PptxSpec):
    @property
    def rel(self):
        return "product-planning/cost-benefit-analysis/cost-benefit-analysis.pptx"

    example = {
        "text": {
            "title": "Weekly slots for couriers: 3 options compared over 3 years",
            "assumptions": "3 years by quarter; benefit = saved courier hours and fewer late orders; discount rate 12%",
            "totals": "A: payback 9 months, ratio 2.4, net 14 M. B: payback 15 months, ratio 1.8. C: no payback, ratio 0.7",
            "decision": "Launch option A in Q4. Revisit C if courier shortage exceeds 20% in two cities",
        },
        "charts": {"ratio": {
            "categories": ["Period 1", "Period 2", "Period 3", "Period 4", "Period 5"],
            "series": [{"name": "Break-even (1.0)", "values": [1, 1, 1, 1, 1]},
                       {"name": "Option A", "values": [0.4, 0.9, 1.3, 1.6, 1.8]},
                       {"name": "Option B", "values": [0.8, 1.1, 1.2, 1.2, 1.1]},
                       {"name": "Option C", "values": [0.1, 0.4, 0.9, 1.4, 1.9]}],
        }},
    }

    def draw(self, prs, slide):
        from pptx.enum.chart import XL_LEGEND_POSITION
        from pptx.enum.dml import MSO_LINE_DASH_STYLE

        header(slide, "COST / BENEFIT ANALYSIS", "{{title: product, decision and the options compared}}")
        data = CategoryChartData()
        data.categories = ["Period 1", "Period 2", "Period 3", "Period 4", "Period 5"]
        data.add_series("Break-even (1.0)", [1, 1, 1, 1, 1])
        data.add_series("{{option_a: option name}}", [0, 0, 0, 0, 0])
        data.add_series("{{option_b: option name}}", [0, 0, 0, 0, 0])
        data.add_series("{{option_c: option name}}", [0, 0, 0, 0, 0])
        frame = slide.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.4), Inches(1.3),
                                       Inches(8.6), Inches(5.9), data)
        frame.name = "ratio"
        chart = frame.chart
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(11)
        chart.font.name, chart.font.size = FONT, Pt(11)
        chart.font.color.rgb = INK
        colors = [MUTED, ACCENT, RGBColor(0xE0, 0x8A, 0x1E), GOOD, RGBColor(0x8E, 0x44, 0xAD)]
        for i, ser in enumerate(chart.plots[0].series):
            ser.smooth = False
            ser.format.line.color.rgb = colors[i]
            ser.format.line.width = Pt(1.5 if i == 0 else 2.5)
            if i == 0:
                ser.format.line.dash_style = MSO_LINE_DASH_STYLE.DASH
                ser.marker.style = XL_MARKER_STYLE.NONE
            else:
                ser.marker.style = XL_MARKER_STYLE.CIRCLE
                ser.marker.size = 7
                ser.marker.format.fill.solid()
                ser.marker.format.fill.fore_color.rgb = colors[i]
                ser.marker.format.line.color.rgb = WHITE
        va = chart.value_axis
        va.minimum_scale, va.maximum_scale, va.major_unit = 0, 2.0, 0.5
        va.has_major_gridlines = True
        va.major_gridlines.format.line.color.rgb = RGBColor(0xEC, 0xEE, 0xF1)
        va.tick_labels.number_format, va.tick_labels.number_format_is_linked = "0.0", False
        for axis, title in ((chart.category_axis, "Time →"),
                            (va, "Cumulative benefits / cumulative costs")):
            axis.format.line.color.rgb = LINE
            axis.tick_labels.font.size = Pt(10)
            axis.tick_labels.font.color.rgb = MUTED
            axis.has_title = True
            axis.axis_title.text_frame.text = title
            r = axis.axis_title.text_frame.paragraphs[0].runs[0]
            r.font.size, r.font.bold, r.font.name = Pt(11), False, FONT
            r.font.color.rgb = MUTED

        x, w = 9.25, 3.6
        panels = [
            ("Assumptions", "{{assumptions: horizon, benefits, costs and discount rate}}", 1.3, 1.75),
            ("Totals by option", "{{totals: payback, ratio and net benefit per option}}", 3.05, 1.95),
            ("Decision", "{{decision: what we launch, postpone or close, revisit condition}}", 5.0, 2.2),
        ]
        for tag, token, py, ph in panels:
            label(slide.shapes, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            text(box(slide.shapes, x, py + 0.35, w, ph - 0.35), token, size=11)


class ValuePropositionCanvas(PptxSpec):
    @property
    def rel(self):
        return "product-planning/value-proposition-canvas/value-proposition-canvas.pptx"

    example = {"text": {
        "title": "FreshDrop, busy families with children in Moscow",
        "products": "express slots, a weekly plan, replacement of out-of-stock items",
        "gain_creators": "a fixed slot saves 30 minutes a week; the weekly plan removes repeat orders",
        "pain_relievers": "a reminder 15 minutes before the slot; replacement chosen by the buyer",
        "gains": "a dinner on the table at 19:00; no extra trips to the shop",
        "pains": "missed courier, wrong item, waiting for a slot that is always full",
        "jobs": "plan the weekly shop; get the food home on time",
        "segment": "families with 2+ children, Moscow; 14 interviews and 300 survey answers, August 2026; survey date 20 August",
        "fit": "covered: missed courier, slot availability; not covered: price of the express slot (buyers say it is high)",
        "decision": "launch the weekly plan for families; do not cut the express price yet; check repeat orders in 6 weeks",
    }}

    def draw(self, prs, slide):
        from pptx.enum.shapes import MSO_CONNECTOR
        header(slide, "VALUE PROPOSITION CANVAS", "{{title: product and customer segment}}")
        sh = slide.shapes

        def line(x1, y1, x2, y2, color=LINE):
            return connector(sh, (x1, y1), (x2, y2), color=color, width=1.25)

        def block(x, y, w, h, tag, token, color, align=PP_ALIGN.LEFT, th=0.32):
            label(sh, x, y, w, th, tag, size=11, bold=True, color=color, align=align)
            tb = text(box(sh, x, y + th, w, h - th, line=None), token, size=10, align=align)
            tb.text_frame.paragraphs[0].space_after = Pt(3)

        top, side = 1.75, 4.3
        label(sh, 0.5, 1.3, side, 0.4, "Value proposition", size=12, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
        box(sh, 0.5, top, side, side, line=ACCENT)
        line(1.95, top, 1.95, top + side, ACCENT)
        line(1.95, top + side / 2, 0.5 + side, top + side / 2, ACCENT)
        block(0.55, top + 0.08, 1.35, side - 0.15, "Products and services",
              "{{products: what we offer, products and services}}", ACCENT, th=0.55)
        block(2.0, top + 0.08, 2.75, side / 2 - 0.12, "+ Gain creators",
              "{{gain_creators: how the product delivers the gains}}", GOOD)
        block(2.0, top + side / 2 + 0.06, 2.75, side / 2 - 0.12, "− Pain relievers",
              "{{pain_relievers: how the product removes the pains}}", BAD)

        cx0 = 5.5
        label(sh, cx0, 1.3, side, 0.4, "Customer segment", size=12, bold=True, color=INK, align=PP_ALIGN.CENTER)
        box(sh, cx0, top, side, side, line=INK, kind=MSO_SHAPE.OVAL)
        mid_x, mid_y = cx0 + side * 0.62, top + side / 2
        line(mid_x, top + 0.02, mid_x, top + side - 0.02, INK)
        line(cx0 + 0.02, mid_y, mid_x, mid_y, INK)
        block(cx0 + 0.55, top + 0.45, mid_x - cx0 - 0.6, side / 2 - 0.5, "+ Gains",
              "{{gains: what the customer wants to achieve}}", GOOD, PP_ALIGN.CENTER)
        block(cx0 + 0.55, mid_y + 0.06, mid_x - cx0 - 0.6, side / 2 - 0.5, "− Pains",
              "{{pains: what gets in the way and annoys}}", BAD, PP_ALIGN.CENTER)
        block(mid_x + 0.05, top + 1.1, side * 0.38 - 0.25, side - 2.2, "Jobs",
              "{{jobs: what the customer is trying to do}}", INK, PP_ALIGN.CENTER)
        arrow = box(sh, 0.5 + side + 0.08, mid_y - 0.25, cx0 - 0.5 - side - 0.16, 0.5, fill=LINE, line=None,
                    kind=MSO_SHAPE.LEFT_RIGHT_ARROW)
        label(sh, 0.5, top + side + 0.1, side * 2 + 0.7, 0.4, "{{segment: who the customer is, data source and date}}",
              size=10, color=MUTED, align=PP_ALIGN.CENTER)
        x, w = 10.1, 2.75
        panels = [
            ("Fit", "{{fit: pains and gains covered, and not covered}}", 1.3, 2.55),
            ("Decision and check", "{{decision: what we do, skip and check}}", 4.0, 2.55),
        ]
        for tag, token, py, ph in panels:
            label(sh, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            tb = text(box(sh, x, py + 0.35, w, ph - 0.35), token, size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(4)


class SixThinkingHats(PptxSpec):
    @property
    def rel(self):
        return "product-planning/six-thinking-hats/six-thinking-hats.pptx"

    example = {"text": {
        "title": "Launch express delivery in Kazan? Six hats session, 12 June 2026",
        "white": "3 pilot zones: 17% fewer late orders; no cost data for Kazan yet",
        "red": "Team is excited; support is worried about courier shortage",
        "black": "Couriers may run out at peak hours; margin could drop below 5%",
        "yellow": "Average order up 18% in pilot zones; loyal buyers get faster delivery",
        "green": "Start in 2 districts; add a surge fee at peak hours",
        "blue": "Question set by Anna; 6 hats in 45 minutes; facilitated by Ivan",
        "order": "White, red, black, yellow, green, blue: 6 minutes each; 9 participants",
        "decision": "Pilot in 2 districts from 1 July. Stop if margin is below 5% after 6 weeks. Owner: Anna",
    }}

    def draw(self, prs, slide):
        header(slide, "SIX THINKING HATS", "{{title: the question the group is discussing}}")
        sh = slide.shapes
        hats = [
            ("White · facts", "{{white: what is known and missing, with source}}", RGBColor(0x9C, 0xA3, 0xAF)),
            ("Red · feelings", "{{red: feelings of participants and customers}}", RGBColor(0xC6, 0x3D, 0x3D)),
            ("Black · risks", "{{black: what could go wrong, and why}}", INK),
            ("Yellow · benefits", "{{yellow: benefits and why they are realistic}}", RGBColor(0xD9, 0xA4, 0x06)),
            ("Green · ideas", "{{green: new options and refinements}}", GOOD),
            ("Blue · process", "{{blue: question, discussion course, facilitator}}", ACCENT),
        ]
        left, top, cw, ch, gap = 0.5, 1.35, 2.85, 2.75, 0.12
        for k, (tag, token, color) in enumerate(hats):
            i, j = k % 3, k // 3
            x, y = left + i * (cw + gap), top + j * (ch + gap)
            box(sh, x, y, cw, ch, line=color)
            box(sh, x, y, cw, 0.08, fill=color, line=None)
            label(sh, x + 0.08, y + 0.14, cw - 0.16, 0.35, tag, size=12, bold=True, color=color)
            tb = text(box(sh, x + 0.08, y + 0.5, cw - 0.16, ch - 0.58, line=None), token, size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(3)
        x, w = 9.35, 3.5
        panels = [
            ("Order and participants", "{{order: hat sequence, time for each, participants}}", 1.35, 2.0),
            ("Decision", "{{decision: what was decided, owner, date and check}}", 3.55, 3.4),
        ]
        for tag, token, py, ph in panels:
            label(sh, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            tb = text(box(sh, x, py + 0.35, w, ph - 0.35), token, size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(4)


class ScamperMethod(PptxSpec):
    @property
    def rel(self):
        return "product-planning/scamper-method/scamper-method.pptx"

    example = {"text": {
        "title": "Cut delivery cost per order for Moscow buyers, FreshDrop",
        "s": "Replace the paper receipt with an SMS link; swap cold packs for insulated bags",
        "c": "Combine pickups from two dark stores into one courier batch",
        "a": "Adapt the parcel-locker idea: pickup points at metro exits",
        "m": "Modify the courier route: loops of 4 stops at most",
        "p": "Use dark-store couriers for evening restaurant pickups",
        "e": "Drop the call-before-delivery step: 14% of orders wait for it",
        "r": "Let the courier choose the drop order, not the dispatcher",
        "shortlist": "Two ideas passed: batch pickups (Combine) and route rebuild (Modify). Criterion: saves 10+ minutes per trip",
        "decision": "Test batch pickups in 2 districts from 1 July; check idle time per courier after 4 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "SCAMPER · IDEA GENERATION", "{{title: what we improve and for whom}}")
        sh = slide.shapes
        rows = [
            ("S", "Substitute", "What to replace: a step, channel, material, participant?", "s"),
            ("C", "Combine", "What can be combined with something else?", "c"),
            ("A", "Adapt", "What can be borrowed from another industry or product?", "a"),
            ("M", "Modify", "What to enlarge, shrink, or change in its properties?", "m"),
            ("P", "Put to another use", "Where else and for whom can this be used?", "p"),
            ("E", "Eliminate", "What can be removed without losing the essence?", "e"),
            ("R", "Reverse, rearrange", "What can be swapped around or done the opposite way?", "r"),
        ]
        left, top, rh = 0.5, 1.35, 0.8
        for k, (letter, name, q, key) in enumerate(rows):
            y = top + k * rh
            text(box(sh, left, y, 0.6, rh - 0.06, fill=ACCENT_BG, line=None), letter, size=20, bold=True, color=ACCENT,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            label(sh, left + 0.65, y, 2.4, 0.3, name, size=11, bold=True)
            label(sh, left + 0.65, y + 0.28, 2.4, rh - 0.34, q, size=9, color=MUTED)
            tb = text(box(sh, left + 3.1, y, 5.6, rh - 0.06), "{{%s: ideas for this question}}" % key, size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(2)
        x, w = 9.35, 3.5
        panels = [
            ("Selection", "{{shortlist: ideas that passed and the criterion}}", 1.35, 2.3),
            ("Decision and check", "{{decision: what we do first, check, metric and deadline}}", 3.85, 1.9 + 1.2),
        ]
        for tag, token, py, ph in panels:
            label(sh, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            tb = text(box(sh, x, py + 0.35, w, ph - 0.35), token, size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(4)


class HeartMetrics(PptxSpec):
    @property
    def rel(self):
        return "product-planning/heart-metrics/heart-metrics.pptx"

    example = {"text": {
        "title": "FreshDrop checkout redesign: HEART metrics for Q3 2026",
        "h_goal": "Buyers find checkout clear and fair",
        "h_signal": "Score 4+ of 5 in the post-order survey",
        "h_metric": "CSAT after checkout: 3.9 (target 4.2)",
        "e_goal": "Buyers add more items per order",
        "e_signal": "Use of cart reorder and substitutions",
        "e_metric": "Items per order: 11.2 (Q2: 10.4)",
        "a_goal": "New buyers complete the first order",
        "a_signal": "First order within 7 days of install",
        "a_metric": "2,100 new buyers a month, 31% convert",
        "r_goal": "Buyers come back for a second week",
        "r_signal": "Repeat order within 14 days",
        "r_metric": "Retention D14: 36% (target 40%)",
        "t_goal": "Pay without errors or retries",
        "t_signal": "Checkout completion, failed payments",
        "t_metric": "Completion 87%; failed payments 4.2%",
        "focus": "Chosen: Happiness and Task success. Engagement postponed: no baseline data yet",
        "decision": "Task success target: 92% of orders with no support contact. Checked weekly by Lena",
    }}

    def draw(self, prs, slide):
        header(slide, "HEART · USER EXPERIENCE METRICS", "{{title: product or feature and what we change}}")
        sh = slide.shapes
        rows = [
            ("H", "Happiness", "User satisfaction", "h"),
            ("E", "Engagement", "Depth of use", "e"),
            ("A", "Adoption", "New users", "a"),
            ("R", "Retention", "Users who stay", "r"),
            ("T", "Task success", "Efficiency, errors", "t"),
        ]
        left, top, hh, rh = 0.5, 1.3, 0.4, 1.04
        cols = [("Goal", "goal", "what we want to achieve for the user", 2.55),
                ("Signal", "signal", "which action or attitude will show it", 2.55),
                ("Metric", "metric", "how it is counted, period, current value", 2.55)]
        x0 = left + 2.05
        x = x0
        for name, _, _, w in cols:
            label(sh, x, top, w, hh, name, size=12, bold=True, color=INK)
            x += w + 0.05
        for k, (letter, en, ru, key) in enumerate(rows):
            y = top + hh + k * rh
            text(box(sh, left, y, 0.5, rh - 0.06, fill=ACCENT_BG, line=None), letter, size=20, bold=True, color=ACCENT,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            label(sh, left + 0.55, y + 0.05, 1.45, 0.3, en, size=11, bold=True)
            label(sh, left + 0.55, y + 0.35, 1.45, 0.3, ru, size=9, color=MUTED)
            x = x0
            for ci, (_, ck, hint, w) in enumerate(cols):
                tb = text(box(sh, x, y, w, rh - 0.06), "{{%s_%s: %s}}" % (key, ck, hint), size=9)
                tb.text_frame.paragraphs[0].space_after = Pt(2)
                x += w + 0.05
        x, w = 10.4, 2.45
        panels = [
            ("In focus", "{{focus: chosen categories and why}}", 1.3, 2.4),
            ("Decision", "{{decision: what was decided, check order, deadline}}", 3.85, 2.75),
        ]
        for tag, token, py, ph in panels:
            label(sh, x, py, w, 0.4, tag, size=12, bold=True, color=INK)
            tb = text(box(sh, x, py + 0.4, w, ph - 0.4), token, size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(4)


class MetricPyramid(PptxSpec):
    @property
    def rel(self):
        return "product-planning/metric-pyramid/metric-pyramid.pptx"

    example = {"text": {
        "title": "FreshDrop: weekly orders and profit, Q3 2026",
        "nsm": "Weekly orders per active buyer = orders ÷ buyers; now 1.8",
        "key1": "Active buyers: 12,400 in August",
        "key2": "Orders per buyer: 1.8 a week",
        "key3": "Average basket: 1,850 RUB",
        "pulse1": "Weekly open rate 64%; slot picked in 58% of orders",
        "pulse2": "Cart abandon rate 28%; substitutions accepted in 71% of orders",
        "pulse3": "Repeat order within 14 days: 46%; NPS 41",
        "traction": "Week-4 retention, basket size and delivery time drive weekly orders most",
        "decision": "Bet on basket size: test «buy 3, get 1 free». Check weekly orders every Monday",
    }}

    def draw(self, prs, slide):
        header(slide, "METRIC PYRAMID", "{{title: product and the main goal}}")
        sh = slide.shapes
        area_l, area_w = 0.5, 9.3
        # North Star
        nw = 3.6
        nx = area_l + (area_w - nw) / 2
        label(sh, nx, 1.25, nw, 0.3, "North Star — the value metric", size=11, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
        tb = text(box(sh, nx, 1.55, nw, 1.0, fill=ACCENT_BG, line=ACCENT), "{{nsm: metric, formula and current value}}",
                  size=11, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # Key metrics
        kw, gap = 2.7, 0.6
        kx0 = area_l + (area_w - 3 * kw - 2 * gap) / 2
        ky = 3.25
        label(sh, area_l, ky + 1.0, area_w, 0.3, "Key — key metrics",
              size=10, color=MUTED, align=PP_ALIGN.CENTER)
        for i in range(3):
            x = kx0 + i * (kw + gap)
            ln = sh.add_connector(1, Inches(nx + nw / 2), Inches(2.55), Inches(x + kw / 2), Inches(ky))
            ln.line.color.rgb = LINE
            text(box(sh, x, ky, kw, 1.0), "{{key%d: metric and value}}" % (i + 1), size=10, bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            if i < 2:
                label(sh, x + kw, ky + 0.2, gap, 0.6, "×", size=20, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
            tb = text(box(sh, x, ky + 1.3, kw, 1.45, line=LINE), "{{pulse%d: user behaviour metrics for this key}}" % (i + 1), size=9)
            tb.text_frame.paragraphs[0].space_after = Pt(2)
        label(sh, area_l, ky + 2.8, area_w, 0.3, "Pulse — user behaviour metrics under the key ones", size=10, color=MUTED, align=PP_ALIGN.CENTER)
        x, w = 10.1, 2.75
        panels = [
            ("Traction", "{{traction: key metrics that influence the goal most}}", 1.25, 2.2),
            ("Decision", "{{decision: which metric we bet on, levers and check}}", 3.6, 2.85),
        ]
        for tag, token, py, ph in panels:
            label(sh, x, py, w, 0.4, tag, size=12, bold=True, color=INK)
            tb = text(box(sh, x, py + 0.4, w, ph - 0.4), token, size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(4)


class TheoryOfInventiveProblemSolving(PptxSpec):
    @property
    def rel(self):
        return "product-planning/theory-of-inventive-problem-solving/theory-of-inventive-problem-solving.pptx"

    example = {"text": {
        "title": "Slots must be short to be convenient, but couriers need long windows",
        "element": "Length of the delivery window",
        "need_a": "a slot the buyer can book within 1 hour (benefit X: convenience)",
        "need_not_a": "a window of 3+ hours for couriers (benefit Y: efficient routes)",
        "ikr": "slots are short for buyers and long for couriers, at no extra cost",
        "resources": "order history by hour, courier GPS data, 6 dark stores",
        "principle": "separation in time: short slots at peak hours, long windows at night",
        "solution": "Separate short slots for regulars, long windows for new users (segmentation in time)",
        "check": "Late deliveries 4% → 2.5% after 3 weeks in two districts; rollout from 1 October",
    }}

    def draw(self, prs, slide):
        header(slide, "TRIZ · RESOLVING A CONTRADICTION", "{{title: the problem in one phrase}}")
        sh = slide.shapes
        left, top = 0.5, 1.3
        label(sh, left, top, 9.2, 0.35, "Contradiction", size=12, bold=True, color=INK)
        text(box(sh, left, top + 0.4, 9.2, 0.75, fill=ACCENT_BG, line=None), "{{element: element or parameter in dispute}}",
             size=12, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        cw = 4.5
        for i, (tag, key, hint, fill, line, col) in enumerate([
            ("It must be A", "need_a", "{{need_a: what it must be, with its benefit}}", GOOD_BG, GOOD, GOOD),
            ("It must be not-A", "need_not_a", "{{need_not_a: what it must be, with its benefit}}", BAD_BG, BAD, BAD),
        ]):
            x = left + i * (cw + 0.2)
            label(sh, x, top + 1.3, cw, 0.3, tag, size=11, bold=True, color=col)
            tb = text(box(sh, x, top + 1.6, cw, 1.1, fill=fill, line=line), hint, size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(2)
        blocks = [
            ("Ideal final result", "ikr", "{{ikr: the ideal result, with no harm or cost}}"),
            ("Resources", "resources", "{{resources: what is already available}}"),
            ("Resolution principle", "principle", "{{principle: principle used to resolve it}}"),
        ]
        bw = (9.2 - 0.4) / 3
        for i, (tag, key, hint) in enumerate(blocks):
            x = left + i * (bw + 0.2)
            label(sh, x, top + 2.9, bw, 0.3, tag, size=11, bold=True, color=INK)
            tb = text(box(sh, x, top + 3.2, bw, 1.6), hint, size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(2)
        x, w = 10.0, 2.85
        panels = [
            ("Solution", "{{solution: what was done to get both}}", 1.3, 2.6),
            ("Check", "{{check: how it was checked, result and deadline}}", 4.05, 2.45),
        ]
        for tag, token, py, ph in panels:
            label(sh, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            tb = text(box(sh, x, py + 0.4, w, ph - 0.4), token, size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(4)


class MorphologicalAnalysis(PptxSpec):
    @property
    def rel(self):
        return "product-planning/morphological-analysis/morphological-analysis.pptx"

    example = {"text": {
        "title": "Pickup point for groceries: options for a 2026 pilot in 3 districts",
        "prop1": "Pickup place", "prop2": "Ordering", "prop3": "Payment", "prop4": "Courier", "prop5": "Notification",
        "v1_1": "metro exit kiosk", "v1_2": "courier hand-off", "v1_3": "locker", "v1_4": "store counter",
        "v2_1": "order 2 hours ahead", "v2_2": "order at the kiosk", "v2_3": "app pickup in 15 min", "v2_4": "next-day pickup",
        "v3_1": "card at order", "v3_2": "cash at kiosk", "v3_3": "pay in app", "v3_4": "bank link",
        "v4_1": "own courier", "v4_2": "partner fleet", "v4_3": "taxi", "v4_4": "bike",
        "v5_1": "push", "v5_2": "SMS", "v5_3": "email", "v5_4": "in-app",
        "excluded": "Locker + night pickup dropped: couriers cannot reach lockers after 22:00",
        "combos": "option A = 1.1 + 2.3 + 3.2 (kiosk, metro, app pickup)",
        "decision": "Option A: kiosk at metro exits, app pickup. Chosen for cost; check pickups per day after 6 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "MORPHOLOGICAL ANALYSIS", "{{title: the object and goal of the option search}}")
        sh = slide.shapes
        left, top = 0.5, 1.3
        pw, vw, gap, rh = 1.9, 1.7, 0.1, 0.62
        label(sh, left, top, pw, 0.3, "Property", size=11, bold=True, color=INK)
        label(sh, left + pw + gap, top, 4 * vw + 3 * gap, 0.3, "Values", size=11, bold=True, color=INK)
        for r in range(5):
            y = top + 0.35 + r * (rh + gap)
            text(box(sh, left, y, pw, rh, fill=ACCENT_BG, line=None), "{{prop%d: name of the property}}" % (r + 1),
                 size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
            for c in range(4):
                x = left + pw + gap + c * (vw + gap)
                text(box(sh, x, y, vw, rh), "{{v%d_%d: value of property %d}}" % (r + 1, c + 1, r + 1), size=9,
                     anchor=MSO_ANCHOR.MIDDLE)
        y = top + 0.35 + 5 * (rh + gap) + 0.1
        label(sh, left, y, 9.2, 0.3, "Discarded values and why", size=11, bold=True, color=INK)
        tb = text(box(sh, left, y + 0.35, 9.2, 1.05, fill=BAD_BG, line=None),
                  "{{excluded: discarded values or combinations, and why}}", size=10)
        tb.text_frame.paragraphs[0].space_after = Pt(2)
        x, w = 10.0, 2.85
        panels = [
            ("Combinations", "{{combos: combinations of values, one per row}}", 1.3, 2.9),
            ("Decision", "{{decision: chosen combination, reason and check}}", 4.35, 2.15),
        ]
        for tag, token, py, ph in panels:
            label(sh, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            tb = text(box(sh, x, py + 0.4, w, ph - 0.4), token, size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(4)


class ProjectCanvas(PptxSpec):
    @property
    def rel(self):
        return "product-planning/project-canvas/project-canvas.pptx"

    example = {"text": {
        "title": "Dark store in Kazan, project 2026",
        "motivation": "Kazan orders grew 40% in a year; the nearest store is 25 minutes away",
        "participants": "ops team, courier partner, city council, landlord",
        "goals": "80% of Kazan orders delivered within 1 hour; 3 000 orders a week by Q4",
        "users": "buyers in Kazan's 5 central districts",
        "benefits": "groceries within 1 hour, fresh produce, lower delivery fee",
        "activities": "lease site, fit out cold rooms, hire 20 pickers, set up routes",
        "deliverables": "working dark store, pickers' schedule, KPI dashboard",
        "risks": "rent may rise 15%; winter courier shortage; 6-month lease option",
        "milestones": "lease signed 1 Nov; fit-out 1 Dec – 15 Jan; launch 1 Feb 2027",
        "constraints": "fire code limits night work; budget capped at 45 M",
        "scope": "in: 5 districts, groceries only. Out: alcohol, pharmacy",
        "project_end": "two months at the KPI, or a stop decision after the pilot",
    }}

    def draw(self, prs, slide):
        header(slide, "PROJECT CANVAS", "{{title: project name}}")
        sh = slide.shapes
        left, full = 0.5, 12.33

        def block(x, y, w, h, tag, key, hint, fill=WHITE, line=LINE, size=9):
            tb = text(box(sh, x, y, w, h, fill=fill, line=line), hint, size=size)
            tf = tb.text_frame
            tf.margin_top = Inches(0.36)
            tf.paragraphs[0].space_after = Pt(2)
            label(sh, x + 0.08, y + 0.04, w - 0.16, 0.28, tag, size=10, bold=True, color=INK)

        def strip(y, h, tag, key, hint):
            tb = text(box(sh, left, y, full, h, fill=ACCENT_BG, line=None), hint, size=10,
                      anchor=MSO_ANCHOR.MIDDLE)
            tb.text_frame.margin_left = Inches(2.1)
            label(sh, left + 0.1, y, 1.9, h, tag, size=11, bold=True, color=INK, anchor=MSO_ANCHOR.MIDDLE)

        strip(1.25, 0.62, "Motivation", "motivation", "{{motivation: why the project is needed}}")
        y, h, cw, g = 1.97, 2.55, 2.39, 0.095
        xs = [left + i * (cw + g) for i in range(5)]
        block(xs[0], y, cw, h, "Participants", "participants", "{{participants: who takes part}}")
        block(xs[1], y, cw, h, "Goals", "goals", "{{goals: measurable project goals}}")
        block(xs[2], y, cw, h / 2 - 0.05, "Users", "users", "{{users: who the users are}}", fill=ACCENT_BG, line=None)
        block(xs[2], y + h / 2 + 0.05, cw, h / 2 - 0.05, "User benefits", "benefits",
              "{{benefits: what users gain}}", fill=ACCENT_BG, line=None)
        block(xs[3], y, cw, h, "Activities", "activities", "{{activities: main activities}}")
        block(xs[4], y, cw, h, "Deliverables", "deliverables", "{{deliverables: what the project delivers}}")
        y2, h2 = y + h + 0.1, 1.9
        qw = (full - 3 * g) / 4
        for i, (tag, key, hint) in enumerate([
            ("Risks", "risks", "{{risks: main risks}}"),
            ("Milestones", "milestones", "{{milestones: key dates}}"),
            ("Constraints", "constraints", "{{constraints: limits on the project}}"),
            ("Scope", "scope", "{{scope: what is in and out}}"),
        ]):
            block(left + i * (qw + g), y2, qw, h2, tag, key, hint)
        strip(y2 + h2 + 0.1, 0.55, "Project end", "project_end", "{{project_end: when the project ends}}")


class FeatureCanvas(PptxSpec):
    @property
    def rel(self):
        return "product-planning/feature-canvas/feature-canvas.pptx"

    example = {"text": {
        "title": "Express slot reminder",
        "idea": "push reminder 15 minutes before the express slot the buyer booked",
        "why": "buyers forget slots; 22% of express orders are missed",
        "context": "evening, when buyers plan the next day; couriers already have the route",
        "value": "the order arrives on time without checking the app",
        "restrictions": "iOS push permission is needed; no SMS budget",
        "problems": "missed express slots; cancelled orders",
        "affected": "about 40 000 buyers a month who book express",
        "behavior": "buyers set phone alarms or call support to confirm the slot",
        "capabilities": "push system, slot data, courier ETA",
        "tasks": "turn reminders on or off; change the slot from the reminder",
        "awareness": "prompt at checkout; reminders list in the profile",
        "support": "wrong time zone, no push permission; FAQ and chat link",
        "goals": "cut missed express slots from 22% to 10%",
        "success": "missed slots under 10% for 4 weeks; 70% reminder open rate",
        "activities": "build push reminder, link slot data, test with 5% of buyers",
    }}

    def draw(self, prs, slide):
        header(slide, "FEATURE CANVAS", "{{title: the feature or idea}}")
        sh = slide.shapes
        # coordinates follow the original canvas image (1024 px wide), scaled onto the slide
        x0, y0, sx, sy = 0.5, 1.25, 12.33 / 985, 5.95 / 635

        def block(px, py, pw, ph, tag, key, hint, fill=WHITE):
            x, y, w, h = x0 + (px - 20) * sx, y0 + (py - 52) * sy, pw * sx, ph * sy
            tb = text(box(sh, x, y, w, h, fill=fill), f"{{{{{key}: {hint}}}}}", size=8)
            tb.text_frame.margin_top = Inches(0.3)
            label(sh, x + 0.06, y + 0.03, w - 0.12, 0.26, tag, size=9, bold=True, color=INK)

        for args in [
            (20, 52, 200, 223, "Idea description", "idea", "the idea in 2–3 sentences"),
            (20, 275, 200, 412, "Why?", "why", "why it matters to customers and business"),
            (220, 52, 220, 296, "Contextual situations", "context", "situations where the need arises"),
            (220, 348, 220, 152, "Value proposition", "value", "what customers get and why they choose it"),
            (220, 500, 220, 187, "Restrictions and Limitations", "restrictions", "what prevents solving the problems"),
            (440, 52, 220, 148, "Problems to solve", "problems", "customer and business problems solved"),
            (440, 200, 220, 148, "Affected customers", "affected", "whom it concerns, how often, how critical"),
            (440, 348, 220, 152, "Current behavior and habits", "behavior", "how customers cope now, what they use"),
            (440, 500, 220, 187, "Capabilities", "capabilities", "existing assets that help solve the problems"),
        ]:
            block(*args)
        for args in [
            (664, 52, 341, 155, "Customers tasks", "tasks", "what customers will do with the feature"),
            (664, 207, 170, 123, "Awareness", "awareness", "how customers learn about the feature"),
            (834, 207, 171, 123, "Support needed", "support", "where customers need help, possible errors"),
            (664, 330, 170, 202, "Business goals", "goals", "why the business should release the feature"),
            (834, 330, 171, 202, "Success criteria", "success", "how we know the feature is useful"),
            (664, 532, 341, 155, "Key activities", "activities", "minimum work and tasks to deliver"),
        ]:
            block(*args, fill=ACCENT_BG)
        box(sh, x0 + (660 - 20) * sx, y0, 0.03, 5.95, fill=INK, line=None)


class ImpactMapping(PptxSpec):
    @property
    def rel(self):
        return "product-planning/impact-mapping/impact-mapping.pptx"

    example = {"text": {
        "title": "FreshDrop: weekly orders from families, 2026",
        "goal": "Grow weekly orders by 10% in Q3 2026",
        "metric": "weekly orders per buyer: 1.8 → 2.0 by 30 September",
        "actor1": "Regular buyers",
        "actor2": "New families",
        "actor3": "Couriers",
        "impact1_1": "Orders weekly",
        "impact1_2": "Adds a second order",
        "impact2_1": "Books express slots",
        "impact2_2": "Books on time",
        "impact3_1": "Fewer missed items",
        "impact3_2": "Faster picking",
        "deliv1_1": "Weekly reminder",
        "deliv1_2": "Ratings after each order",
        "deliv2_1": "Express slot banner",
        "deliv2_2": "Push 15 min before slot",
        "deliv3_1": "Live stock picking",
        "deliv3_2": "Courier ETA alerts",
    }}

    def draw(self, prs, slide):
        from pptx.enum.shapes import MSO_CONNECTOR
        header(slide, "IMPACT MAPPING", "{{title: product or initiative}}")
        sh = slide.shapes
        cols = [(0.5, 2.3), (3.25, 2.3), (6.0, 3.0), (9.45, 3.38)]
        for (x, w), tag in zip(cols, ["Why? Goal", "Who? Actors", "How? Impacts", "What? Deliverables"]):
            label(sh, x, 1.25, w, 0.32, tag, size=11, bold=True, color=ACCENT)
        top, rh, gap = 1.65, 0.82, 0.1
        rows = [top + i * (rh + gap) for i in range(6)]
        mid = lambda y, h=rh: y + h / 2

        def line(x1, y1, x2, y2):
            return connector(sh, (x1, y1), (x2, y2))

        gx, gw = cols[0]
        gy, gh = rows[1], 2 * rh + gap
        ax, aw = cols[1]
        ix, iw = cols[2]
        dx, dw = cols[3]
        for a in range(3):
            ay = rows[2 * a]
            ah = 2 * rh + gap
            line(gx + gw, mid(gy, gh), ax, mid(ay, ah))
            for k in range(2):
                y = rows[2 * a + k]
                line(ax + aw, mid(ay, ah), ix, mid(y))
                line(ix + iw, mid(y), dx, mid(y))
        text(box(sh, gx, gy, gw, gh, fill=ACCENT), "{{goal: the business goal}}", size=11, bold=True,
             color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        label(sh, gx, rows[3] + 0.05, gw, 0.28, "Goal metric", size=10, bold=True, color=INK)
        tb = text(box(sh, gx, rows[3] + 0.35, gw, 1.5, fill=ACCENT_BG, line=None),
                  "{{metric: measure, now → target, deadline}}", size=9)
        for a in range(3):
            ay = rows[2 * a]
            text(box(sh, ax, ay, aw, 2 * rh + gap, fill=ACCENT_BG, line=None), f"{{{{actor{a + 1}: who influences the goal}}}}",
                 size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
            for k in range(2):
                y = rows[2 * a + k]
                n = f"{a + 1}_{k + 1}"
                text(box(sh, ix, y, iw, rh, fill=WHITE), f"{{{{impact{n}: how the actor's behaviour changes}}}}", size=9,
                     anchor=MSO_ANCHOR.MIDDLE)
                text(box(sh, dx, y, dw, rh, fill=WHITE), f"{{{{deliv{n}: deliverable that causes the impact}}}}", size=9,
                     anchor=MSO_ANCHOR.MIDDLE)


class LeanUxCanvas(PptxSpec):
    @property
    def rel(self):
        return "product-planning/lean-ux-canvas/lean-ux-canvas.pptx"

    example = {"text": {
        "title": "FreshDrop express slots, iteration 2",
        "problem": "buyers miss the 2-hour slot and wait a day",
        "outcomes": "express share of orders from 8% to 15% in 8 weeks",
        "users": "busy families with 2+ children, weekly orders",
        "benefits": "an order in 2 hours without planning; 2 orders a week instead of 1",
        "solutions": "express slot banner, push reminder before the slot, one-tap reorder",
        "hypotheses": "we believe express share will rise if families get a push reminder, because they forget slots",
        "riskiest": "families will book express slots at night",
        "experiment": "push test for 2 weeks on 20% of users; success if express share grows by 5 points",
    }}

    def draw(self, prs, slide):
        header(slide, "LEAN UX CANVAS", "{{title: initiative · iteration}}")
        sh = slide.shapes
        # coordinates follow the original v2 canvas image (2000 px wide), scaled onto the slide
        x0, y0, sx, sy = 0.5, 1.25, 12.33 / 1880, 5.95 / 1112

        def block(px, py, pw, ph, tag, key, hint, fill=WHITE, size=9):
            x, y, w, h = x0 + (px - 60) * sx, y0 + (py - 138) * sy, pw * sx, ph * sy
            tb = text(box(sh, x, y, w, h, fill=fill), f"{{{{{key}: {hint}}}}}", size=size)
            tb.text_frame.margin_top = Inches(0.34)
            tb.text_frame.paragraphs[0].space_after = Pt(2)
            label(sh, x + 0.06, y + 0.04, w - 0.12, 0.28, tag, size=10, bold=True, color=INK)

        for args in [
            (60, 138, 695, 352, "1 · Business problem", "problem", "business problem solved"),
            (1245, 138, 695, 352, "2 · Business outcomes", "outcomes", "business outcome and its metric"),
            (60, 490, 695, 413, "3 · Users", "users", "primary users and customers"),
            (1245, 490, 695, 413, "4 · User outcomes and benefits", "benefits",
             "user benefits and behaviour change"),
            (755, 138, 490, 765, "5 · Solutions", "solutions", "solutions for business and users"),
        ]:
            block(*args)
        for args in [
            (60, 903, 695, 347, "6 · Hypotheses", "hypotheses",
             "hypothesis linking outcome, users and feature"),
            (755, 903, 490, 347, "7 · What to learn first", "riskiest", "riskiest assumption to test"),
            (1245, 903, 695, 347, "8 · The minimum work to learn it", "experiment", "experiment and its result"),
        ]:
            block(*args, fill=ACCENT_BG)


class ElevatorPitch(PptxSpec):
    @property
    def rel(self):
        return "product-planning/elevator-pitch/elevator-pitch.pptx"

    example = {"text": {
        "title": "FreshDrop pitch for store partners, investor meeting, 10 September 2026",
        "target": "busy families in new Moscow districts",
        "need": "need groceries for the week without a shop trip",
        "product": "FreshDrop",
        "category": "grocery delivery app",
        "benefit": "delivers a complete order in 2 hours",
        "alt": "supermarket delivery slots that are booked a day ahead",
        "diff": "picks live stock, so no item is missing",
        "spoken": "We bring the week's groceries in 2 hours, and every item on the list is in stock. Families in new districts order in 3 taps.",
        "check": "Tested on 6 parents: 5 retold it correctly; the question was about refunds",
        "decision": "Keep the 2-hour line; add refund terms to the deck. Investor meeting: next step is a pilot budget review",
    }}

    def draw(self, prs, slide):
        header(slide, "ELEVATOR PITCH · GEOFFREY MOORE'S POSITIONING TEMPLATE",
               "{{title: product, audience, purpose of the pitch, date}}")
        rows = [
            ("For", "{{target: target customers: who exactly}}"),
            ("who", "{{need: the customer's need or opportunity}}"),
            ("the", "{{product: product name}}"),
            ("is a", "{{category: product category}}"),
            ("that", "{{benefit: key benefit, a compelling reason to buy}}"),
            ("Unlike", "{{alt: main competing alternative}}"),
            ("our product", "{{diff: main difference from the alternative}}"),
        ]
        y0, rh, gap = 1.3, 0.72, 0.1
        for i, (en, token) in enumerate(rows):
            y = y0 + i * (rh + gap)
            text(box(slide.shapes, 0.5, y, 1.5, rh, fill=ACCENT, line=None), en, size=11, bold=True,
                 color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            text(box(slide.shapes, 2.0, y, 5.9, rh), token, size=11, anchor=MSO_ANCHOR.MIDDLE)
        x, w = 8.2, 4.63
        bottom = y0 + 7 * (rh + gap) - gap
        panels = [
            ("Spoken, 30 seconds", "{{spoken: the pitch in plain words}}", INK, ACCENT_BG, 1.9),
            ("Check", "{{check: who heard it and how they responded}}", INK, None, 1.65),
        ]
        y = y0
        for tag, token, color, fill, h in panels:
            text(box(slide.shapes, x, y, w, 0.32, fill=color, line=None), tag, size=12, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(slide.shapes, x, y + 0.32, w, h - 0.32, fill=fill), token, size=11)
            y += h + 0.1
        text(box(slide.shapes, x, y, w, 0.32, fill=GOOD, line=None), "Decision", size=12, bold=True, color=WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
        text(box(slide.shapes, x, y + 0.32, w, bottom - y - 0.32, fill=GOOD_BG),
             "{{decision: decision on the pitch, and its basis}}", size=11)


class Storytelling(PptxSpec):
    @property
    def rel(self):
        return "product-planning/storytelling/storytelling.pptx"

    example = {"text": {
        "title": "FreshDrop CEO pitch to the board, 15 September 2026",
        "audience": "board members; they worry about margin; they have tried a price cut before; if nothing changes, churn grows",
        "a1": "in 2026 a missed slot costs a family an evening",
        "b1": "a dinner on time with one tap in the app",
        "a2": "couriers come in a 2-hour window and families wait at home",
        "b2": "a fixed slot and a reminder 15 minutes before",
        "a3": "the shop is out of stock for the items on the list",
        "b3": "the family orders the same basket in one tap",
        "a4": "the slot is gone when they check at 19:00",
        "b4": "the courier calls at the wrong time",
        "a5": "the slot is booked on the first tap",
        "b5": "the courier calls 15 minutes before",
        "ask": "approve the slot pilot budget of 4 million rub by 1 October 2026",
        "bliss": "every family gets dinner on time and the courier never misses a slot",
        "decision": "the board is to decide on the pilot; the story lacks the margin numbers for the second year",
    }}

    def draw(self, prs, slide):
        s = slide.shapes
        header(slide, "STORYTELLING · PRESENTATION SPARKLINE (DUARTE)", "{{title: speaker, audience and date}}")
        text(box(s, 0.5, 1.15, 1.9, 0.5, fill=ACCENT, line=None), "Audience", size=12, bold=True, color=WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 2.4, 1.15, 10.43, 0.5, fill=ACCENT_BG, line=None),
             "{{audience: audience, concerns and history}}",
             size=11, anchor=MSO_ANCHOR.MIDDLE)
        label(s, 0.5, 1.7, 1.9, 1.0, "Story line\nabove: \"what could be\",\nbelow: \"what is\"", size=10, bold=True,
              anchor=MSO_ANCHOR.MIDDLE)
        cd = CategoryChartData()
        cd.categories = [f"beat {i}" for i in range(1, 9)]
        cd.add_series("Story", [0, 1, 0, 1, 0, 1, 0, 1])
        frame = s.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(2.4), Inches(1.7), Inches(10.43), Inches(1.0), cd)
        frame.name = "sparkline"
        ch = frame.chart
        ch.has_legend = False
        ch.has_title = False
        ch.font.size, ch.font.name = Pt(9), FONT
        ser = ch.plots[0].series[0]
        ser.smooth = False
        ser.format.line.color.rgb, ser.format.line.width = ACCENT, Pt(2.5)
        ser.marker.format.fill.solid()
        ser.marker.format.fill.fore_color.rgb = ACCENT
        va = ch.value_axis
        va.minimum_scale, va.maximum_scale, va.major_unit = 0, 1, 1
        va.has_major_gridlines = False
        va.tick_labels.number_format = '"could be";;"is"'
        va.tick_labels.number_format_is_linked = False
        x0, wl, xa, wa, xb, wb = 0.5, 1.5, 2.05, 5.4, 7.5, 5.33
        text(box(s, xa, 2.72, wa, 0.34, fill=BAD, line=None), "What is (today)", size=11, bold=True, color=WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, xb, 2.72, wb, 0.34, fill=GOOD, line=None), "What could be (with the product)", size=11, bold=True,
             color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        rows = [("Beginning", "a1", "b1", "in 2026 a missed slot costs a family an evening", "a dinner on time with one tap in the app"),
                ("Middle 1", "a2", "b2", "couriers come in a 2-hour window and families wait at home", "a fixed slot and a reminder 15 minutes before"),
                ("Middle 2", "a3", "b3", "the shop is out of stock for the items on the list", "the family orders the same basket in one tap"),
                ("Middle 3", "a4", "b4", "the slot is gone when they check at 19:00", "the courier calls at the wrong time"),
                ("Middle 4", "a5", "b5", "the slot is booked on the first tap", "the courier calls 15 minutes before")]
        y, rh, gap = 3.08, 0.46, 0.04
        for i, (name, ka, kb, ha, hb) in enumerate(rows):
            yy = y + i * (rh + gap)
            label(s, x0, yy, wl, rh, name, size=11, bold=True, anchor=MSO_ANCHOR.MIDDLE)
            text(box(s, xa, yy, wa, rh, fill=BAD_BG), "{{%s: what is today}}" % ka, size=10, anchor=MSO_ANCHOR.MIDDLE)
            text(box(s, xb, yy, wb, rh, fill=GOOD_BG), "{{%s: what could be with the product}}" % kb, size=10, anchor=MSO_ANCHOR.MIDDLE)
        yy = y + 5 * (rh + gap)
        label(s, x0, yy, wl, rh, "End:\ncall to action", size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, xa, yy, wa + wb + 0.05, rh), "{{ask: call to action}}",
             size=10, anchor=MSO_ANCHOR.MIDDLE)
        yy += rh + gap
        label(s, x0, yy, wl, rh, "New\nbliss", size=11, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, xa, yy, wa + wb + 0.05, rh), "{{bliss: closing vision}}",
             size=10, anchor=MSO_ANCHOR.MIDDLE)
        yy += rh + 0.08
        text(box(s, 0.5, yy, 1.9, 0.5, fill=INK, line=None), "Decision", size=12, bold=True, color=WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 2.4, yy, 10.43, 0.5, fill=GOOD_BG),
             "{{decision: decision and open gaps}}",
             size=10, anchor=MSO_ANCHOR.MIDDLE)


class UserFlow(PptxSpec):
    @property
    def rel(self):
        return "product-planning/user-flow/user-flow.pptx"

    example = {"text": {
        "title": "FreshDrop app, buyer books a delivery slot",
        "goal": "I want to pick a delivery slot for today, so that the order arrives after I get home",
        "scope": "Entry: slot picker from the cart. End: slot confirmed in the order. Payment and address editing are separate flows",
        "start": "Cart: tap «Choose a slot»",
        "s1": "Slot picker: choose the day",
        "s2": "Slot picker: choose a 2-hour window",
        "s3": "Confirmation: check address and time",
        "s4": "Order summary: slot shown, tap «Pay»",
        "end": "Slot confirmed: the order shows the delivery window",
        "cond": "is the chosen slot still free?",
        "alt": "Slot picker: «slot taken» banner, pick another window",
        "other": "«Express in 30 min» and rescheduling from the order page are separate flows",
        "issues": "Test of 8 buyers: 3 went back to the cart to check the address and lost the slot; 2 did not see the «no free slots» state",
        "decision": "Merged day and time pickers into one screen; address check moved before the slot is held",
        "check": "5 moderated tests after the change: all 5 picked a slot without going back; slot-to-order conversion +9 pp in a week",
    }}

    def draw(self, prs, slide):
        header(slide, "USER FLOW",
               "{{title: product, user goal and flow}}")
        sh = slide.shapes

        def block(x, y, w, h, tag, key, hint, fill=ACCENT_BG, color=ACCENT, size=10):
            box(sh, x, y, w, h, fill=fill, line=None)
            label(sh, x + 0.06, y + 0.02, w - 0.12, 0.36, tag, size=12, bold=True, color=color)
            tb = text(box(sh, x + 0.06, y + 0.38, w - 0.12, h - 0.42, line=None), "{{%s: %s}}" % (key, hint), size=size)
            tb.text_frame.paragraphs[0].space_after = Pt(3)

        block(0.5, 1.25, 6.05, 1.1, "User goal", "goal",
              "{{goal: what the user wants to get}}")
        block(6.78, 1.25, 6.05, 1.1, "Flow boundaries", "scope",
              "entry, end and flows left out")

        # main row of nodes
        y, h = 2.55, 1.45
        cy = y + h / 2
        kinds = [  # x, w, kind, key, hint
            (0.4, 1.4, "term", "start", "entry point"),
            (2.25, 1.9, "step", "s1", "screen and user action"),
            (4.5, 1.9, "step", "s2", "screen and user action"),
            (6.75, 1.9, "step", "s3", "screen and user action"),
            (9.0, 1.9, "step", "s4", "screen and user action"),
            (11.25, 1.65, "term", "end", "end state and result"),
        ]
        for x, w, kind, key, hint in kinds:
            if kind == "term":
                s = box(sh, x, y, w, h, fill=GOOD_BG, line=GOOD, kind=MSO_SHAPE.FLOWCHART_TERMINATOR)
                col = GOOD
            else:
                s = box(sh, x, y, w, h, fill=WHITE, line=ACCENT)
                col = INK
            text(s, "{{%s: %s}}" % (key, hint), size=9, color=col, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        for (x1, w1, *_), (x2, *_r) in zip(kinds, kinds[1:]):
            user_flow_arrow(sh, x1 + w1, cy, x2, cy)

        # optional condition after step s3 (removed when cond and alt are empty)
        grp = sh.add_group_shape()
        grp.name = "optional_condition"
        g = grp.shapes
        dy, dh = 4.2, 1.15
        mid = dy + dh / 2
        user_flow_arrow(g, 7.7, y + h, 7.7, dy)
        d = box(g, 6.75, dy, 1.9, dh, fill=WHITE, line=ACCENT, kind=MSO_SHAPE.FLOWCHART_DECISION)
        text(d, "{{cond: yes-or-no condition}}", size=9, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # yes: forward to s4
        user_flow_arrow(g, 8.65, mid, 9.95, mid, head=False)
        user_flow_arrow(g, 9.95, mid, 9.95, y + h)
        label(g, 8.7, mid - 0.34, 0.5, 0.3, "yes", size=9, bold=True, color=GOOD)
        # no: to the alternative step, then back to the flow (s2)
        user_flow_arrow(g, 6.75, mid, 6.1, mid)
        label(g, 6.2, mid - 0.34, 0.5, 0.3, "no", size=9, bold=True, color=BAD)
        alt = box(g, 4.2, mid - 0.43, 1.9, 0.86, fill=BAD_BG, line=BAD)
        text(alt, "{{alt: screen on the no branch}}", size=9, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        user_flow_arrow(g, 5.15, mid - 0.43, 5.15, y + h)

        block(0.5, 4.4, 3.6, 0.95, "Other flows and entries", "other",
              "neighboring flows and other entries", fill=WHITE, color=MUTED)

        block(0.5, 5.5, 4.0, 1.25, "Problems of the old interface", "issues",
              "where people got lost, and the evidence")
        block(4.65, 5.5, 4.2, 1.25, "Decision (new interface)", "decision",
              "merged, removed or moved, and why", fill=GOOD_BG, color=GOOD)
        block(9.0, 5.5, 3.83, 1.25, "Check and result", "check",
              "how it was verified and the result")

        label(sh, 0.5, 6.85, 12.33, 0.4,
              "Legend: oval is entry and end, rectangle is a step (a screen or a screen state), diamond is a condition (if any), arrow is a transition.",
              size=10, color=MUTED)


class MoscowPrioritization(PptxSpec):
    @property
    def rel(self):
        return "product-planning/moscow-prioritization/moscow-prioritization.pptx"

    example = {"text": {
        "title": "MoreThan TALK (University of Southampton student project), site requirements, 2018",
        "timeframe": "Whole project: first version of the site; priorities per requirement",
        "effort": "N/A: the page gives no effort estimates. By count: 25 Must of 48 rows (52%)",
        "must": ["Login with username and password", "Profile page for every user", "Choose which data is public",
                 "Search for users by language, country, interest", "Third-party ad blocks", "Account suspension by admins"],
        "should": ["Login via Google or Facebook", "Automatic translation of profiles", "Map with approximate location",
                   "Photo albums", "Users create own groups"],
        "could": ["Link to city or country information", "Email alert on a new message", "Recorded messages for matches"],
        "wont": ["Account lock after three failed logins", "User-created page layout", "Monthly password change prompt"],
        "decision": "N/A: the page records no scope decision or cut line; 3 of 48 rows have no rating",
    }}

    def draw(self, prs, slide):
        header(slide, "MoSCoW PRIORITISATION", "{{title: product, scope and date}}")
        sh = slide.shapes
        left, full, g = 0.5, 12.33, 0.1
        tb = text(box(sh, left, 1.25, full, 0.5, fill=ACCENT_BG, line=None),
                  "{{timeframe: timeframe the priorities apply to}}", size=11, anchor=MSO_ANCHOR.MIDDLE)
        tb.text_frame.margin_left = Inches(1.6)
        label(sh, left + 0.1, 1.25, 1.5, 0.5, "Timeframe", size=12, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        tb = text(box(sh, left, 1.8, full, 0.5, fill=ACCENT_BG, line=None),
                  "{{effort: share of effort in Must and Could, or N/A}}", size=11, anchor=MSO_ANCHOR.MIDDLE)
        tb.text_frame.margin_left = Inches(1.6)
        label(sh, left + 0.1, 1.8, 1.5, 0.5, "Effort split", size=12, bold=True, anchor=MSO_ANCHOR.MIDDLE)

        cw = (full - 3 * g) / 4
        y, h = 2.45, 3.55
        cols = [("Must Have", "must", "{{must: requirements without which the release is cancelled}}", GOOD, GOOD_BG),
                ("Should Have", "should", "{{should: important, with a workaround}}", ACCENT, ACCENT_BG),
                ("Could Have", "could", "{{could: desirable, first to drop}}", MUTED, WHITE),
                ("Won't Have this time", "wont", "{{wont: agreed out of scope for this timeframe}}", BAD, BAD_BG)]
        for i, (tag, key, token, colr, bg) in enumerate(cols):
            x = left + i * (cw + g)
            text(box(sh, x, y, cw, 0.4, fill=colr, line=None), tag, size=12, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, y + 0.4, cw, h - 0.4, fill=bg, line=LINE), token, size=10)

        y3 = y + h + g
        label(sh, left, y3, 3, 0.35, "Decision", size=12, bold=True)
        text(box(sh, left, y3 + 0.35, full, 7.3 - y3 - 0.35), "{{decision: what is committed, what is dropped first, and who agreed}}", size=11)


class NowNextLaterRoadmap(PptxSpec):
    @property
    def rel(self):
        return "product-planning/now-next-later-roadmap/now-next-later-roadmap.pptx"

    example = {"text": {
        "title": "WooCommerce public roadmap, announced 30 May 2023",
        "objectives": "Give the developer community visibility into current work, future plans and the overall direction of WooCommerce. Items by objective: N/A (the announcement lists no items)",
        "now": ["Projects the team is currently working on", "Item names: N/A (not in the announcement)"],
        "next": ["Projects the team is committed to executing but has not started", "Item names: N/A (not in the announcement)"],
        "later": ["Projects being scoped and likely to happen, not yet scheduled", "Item names: N/A (not in the announcement)"],
        "decision": ["Roadmap published as a living document, kept updated", "Fourth stage Ideation: planned, no work begun", "Office hours and community events to discuss items"],
    }}

    def draw(self, prs, slide):
        header(slide, "NOW-NEXT-LATER ROADMAP · PRODUCT DIRECTION WITHOUT DATES",
               "{{title: product or team, planning period or publication date}}")
        sh = slide.shapes
        left, full, g = 0.5, 12.33, 0.12
        text(box(sh, left, 1.25, full, 0.85, fill=ACCENT_BG, line=None),
             "{{objectives: business objectives the items serve, one line each}}", size=10).text_frame.margin_top = Inches(0.3)
        label(sh, left + 0.08, 1.25, 3, 0.3, "Business objectives", size=10, bold=True, color=ACCENT)
        cw = (full - 2 * g) / 3
        y, h = 2.25, 3.35
        for i, (tag, key, hint, fill) in enumerate([
            ("NOW", "now", "{{now: problems being solved now, each with its idea or experiment and objective}}", ACCENT),
            ("NEXT", "next", "{{next: problems expected after Now, less detailed}}", RGBColor(0x5B, 0x8F, 0xE6)),
            ("LATER", "later", "{{later: big problems on the radar, no solutions yet}}", RGBColor(0x8F, 0xB2, 0xEE)),
        ]):
            x = left + i * (cw + g)
            hd = label(sh, x, y, cw, 0.42, tag, size=14, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            hd.fill.solid()
            hd.fill.fore_color.rgb = fill
            text(box(sh, x, y + 0.42, cw, h - 0.42, fill=WHITE), hint, size=11)
        text(box(sh, left, y + h + g, full, 1.2, fill=WHITE, line=LINE),
             "{{decision: decision made from this roadmap and who is told}}", size=10).text_frame.margin_top = Inches(0.36)
        label(sh, left + 0.08, y + h + g + 0.03, 4, 0.3, "Decision", size=10, bold=True)


class OpportunitySolutionTree(PptxSpec):
    @property
    def rel(self):
        return "product-planning/opportunity-solution-tree/opportunity-solution-tree.pptx"

    example = {"text": {
        "title": "Grailed Discovery team: a feed for users who browse without a specific item",
        "outcome": "N/A: the article does not state the outcome; reported result is about 20% higher LTV for feed users",
        "opp1": "Show me things I interact with",
        "target": "Show me stuff that's popular",
        "opp3": "There should always be new stuff when I come",
        "sol1": "Add popular items to the feed for users who want them",
        "sol2": "Interleave content and recommendations with different parameters",
        "sol3": "Track previously seen items to keep the feed fresh",
        "test1": "Quick low-lift test; the result of this test is N/A",
        "test2": "N/A: no individual experiment results in the source",
        "test3": "N/A: no individual experiment results in the source",
        "decision": "Feed developed over about 6 months; feed users: ~30% more app opens, ~40% more discoveries, ~20% higher LTV",
    }}

    def draw(self, prs, slide):
        header(slide, "OPPORTUNITY SOLUTION TREE", "{{title: product, team and the outcome the tree serves}}")
        sh = slide.shapes
        lx, lw = 0.5, 1.6
        cx0, cw, gap = 2.15, 3.35, 0.4
        xs = [cx0 + i * (cw + gap) for i in range(3)]
        mid = xs[1] + cw / 2

        def row_label(y, h, title, sub):
            lab = box(sh, lx, y, lw, h, line=None)
            text(lab, title, size=11, bold=True, color=ACCENT, anchor=MSO_ANCHOR.MIDDLE)
            p = lab.text_frame.add_paragraph()
            r = p.add_run()
            r.text = sub
            r.font.size, r.font.name, r.font.color.rgb = Pt(9), FONT, MUTED

        # outcome
        ow = 6.0
        ox = mid - ow / 2
        row_label(1.3, 0.8, "Outcome", "one per tree")
        text(box(sh, ox, 1.3, ow, 0.8, fill=ACCENT_BG, line=ACCENT), "{{outcome: the one outcome the team is asked to move}}",
             size=12, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # opportunities
        oy, oh = 2.55, 1.0
        row_label(oy, oh, "Opportunities", "customer needs, pain points, desires")
        for i, (x, tok, tgt) in enumerate(zip(xs, [
                "{{opp1: an unmet customer need in the customer's words}}",
                "{{target: the target opportunity, in the customer's words}}",
                "{{opp3: another unmet customer need in the customer's words}}"], [False, True, False])):
            connector(sh, (mid, 2.1), (x + cw / 2, oy), color=MUTED, width=1.5)
            text(box(sh, x, oy, cw, oh, fill=ACCENT_BG if tgt else None, line=ACCENT if tgt else LINE),
                 tok, size=11, bold=tgt, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        label(sh, xs[1], oy + oh, cw, 0.3, "target opportunity", size=9, color=ACCENT, align=PP_ALIGN.CENTER)
        # solutions
        sy, shh = 4.0, 1.0
        row_label(sy, shh, "Solutions", "for the target only")
        for i, x in enumerate(xs):
            connector(sh, (mid, oy + oh + 0.3), (x + cw / 2, sy), color=MUTED, width=1.5)
            text(box(sh, x, sy, cw, shh), "{{sol%d: a solution for the target opportunity}}" % (i + 1),
                 size=11, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        # assumption tests
        ty, th = 5.3, 1.15
        row_label(ty, th, "Assumption tests", "riskiest assumption of each solution")
        for i, x in enumerate(xs):
            connector(sh, (x + cw / 2, sy + shh), (x + cw / 2, ty), color=MUTED, width=1.5)
            text(box(sh, x, ty, cw, th, line=LINE), "{{test%d: the riskiest assumption, the test and its result}}" % (i + 1),
                 size=10, anchor=MSO_ANCHOR.MIDDLE)
        # decision
        row_label(6.6, 0.6, "Decision", "")
        text(box(sh, cx0, 6.6, 3 * cw + 2 * gap, 0.6, fill=GOOD_BG, line=GOOD),
             "{{decision: what the team keeps, drops or targets next}}", size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)


class WorkingBackwardsPrFaq(PptxSpec):
    @property
    def rel(self):
        return "product-planning/working-backwards-pr-faq/working-backwards-pr-faq.pptx"

    example = {"text": {
        "title": "Fulfillment by Amazon (FBA): two PR/FAQs, seller view and buyer view",
        "heading": "N/A: the PR/FAQ text is not published",
        "subheading": "N/A",
        "summary": "N/A",
        "problem": "N/A",
        "solution": "N/A",
        "quote_company": "N/A",
        "quote_customer": "N/A",
        "start": "N/A",
        "faq_ext": ["N/A: not published for FBA"],
        "faq_int": ["N/A: not published for FBA"],
        "decision": ["Developed using two PR/FAQs: one from the seller perspective, one from the buyer perspective", "Outcome of the review, date and changes: N/A"],
    }}

    def draw(self, prs, slide):
        header(slide, "WORKING BACKWARDS PR/FAQ · PRESS RELEASE AND QUESTIONS",
               "{{title: product or initiative, customer, working date}}")
        sh = slide.shapes
        left, g = 0.5, 0.1
        lw, rx = 6.6, 0.5 + 6.6 + 0.1
        rw = 12.83 - rx

        def block(x, y, w, h, tag, hint, fill=WHITE, line=LINE, size=10, bold=False):
            tb = text(box(sh, x, y, w, h, fill=fill, line=line), hint, size=size, bold=bold)
            tb.text_frame.margin_top = Inches(0.3)
            label(sh, x + 0.08, y + 0.03, w - 0.16, 0.28, tag, size=9, bold=True, color=MUTED)

        label(sh, left, 1.2, lw, 0.3, "PRESS RELEASE (less than one page)", size=11, bold=True, color=ACCENT)
        y = 1.55
        block(left, y, lw, 0.75, "Heading", "{{heading: product name the customer understands}}", size=12, bold=True)
        y += 0.75 + g
        block(left, y, lw, 0.75, "Subheading", "{{subheading: who the customer is and the benefit}}")
        y += 0.75 + g
        block(left, y, lw, 0.9, "Summary", "{{summary: city, date, what is launched and its benefit}}")
        y += 0.9 + g
        block(left, y, lw / 2 - g / 2, 1.2, "Problem", "{{problem: the problem in the customer's words}}")
        block(left + lw / 2 + g / 2, y, lw / 2 - g / 2, 1.2, "Solution", "{{solution: how it solves it, how it differs from today}}")
        y += 1.2 + g
        cw = (lw - 2 * g) / 3
        block(left, y, cw, 0.95, "Company quote", "{{quote_company: one quote from the company}}", size=9)
        block(left + cw + g, y, cw, 0.95, "Customer quote", "{{quote_customer: one quote from a customer}}", size=9)
        block(left + 2 * (cw + g), y, cw, 0.95, "Getting started", "{{start: how the customer starts}}", size=9)

        label(sh, rx, 1.2, rw, 0.3, "FAQ (five pages or less)", size=11, bold=True, color=ACCENT)
        block(rx, 1.55, rw, 2.15, "External FAQ: customers and press", "{{faq_ext: questions customers and press ask: price, how it works, support, where to buy}}")
        block(rx, 3.8, rw, 2.0, "Internal FAQ: every department", "{{faq_int: hard questions: market size, unit economics, investment, risks}}")
        block(rx, 5.9, rw, 1.1, "Decision of the review", "{{decision: go, no go or more work; reasons and next step}}",
              fill=ACCENT_BG, line=None)


class PughMatrix(XlsxSpec):
    @property
    def rel(self):
        return "product-planning/pugh-matrix/pugh-matrix.xlsx"

    _alts = ["Magnetic Swivel", "Pincer", "4 Bar", "Sand Bag", "Sensor Gate", "2 Long Poles", "Swedish Wheels",
             "Self-nesting T"]
    _rows = [  # criterion, one mark per alternative in the order of _alts
        ("Protects Ceramics", "SSSSSSSS"),
        ("Scaleable for Ceramics", "++S+S++S"),
        ("Limit Human Interaction", "++++++++"),
        ("Works with Given Space", "+S+SS-++"),
        ("Works with Conveyor Conditions", "+S++S+++"),
        ("Material Choice", "---S-S--"),
        ("Improves Current Method", "+++SSSS+"),
    ]
    example = {
        "text": {
            "title": "Corning conveyor: stabilizing short ceramic parts, concept selection, first Pugh chart",
            "datum": "Current T system (plexiglass T supports)",
            "decision": "Sensor Gate and Swedish Wheels dropped; Magnetic Swivel became the datum of the next chart; "
                        "the final three (Magnetic Swivel, Pincer, Self-nesting T) went to an AHP step, which chose Self-nesting T",
            **dict(zip([f"alt{i}" for i in range(1, 9)], _alts)),
        },
        "rows": [[crit, None, "S", *list(marks)] for crit, marks in _rows],
    }

    def draw(self, wb):
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Pugh"
        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        grey = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        datum_fill = PatternFill("solid", fgColor="F3F4F6")
        thin = Side(style="thin", color="C9CED6")
        center = Alignment(horizontal="center", vertical="center")

        ws["A1"] = "Pugh Matrix: {{title: the decision and the product, in one line}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws["A2"] = ("Mark every alternative against the datum, criterion by criterion: + better, S same, - worse. "
                    "The counts below are the result; Pugh says the marks must not be summed as absolute scores. "
                    "Importance (High, Medium, Low) is optional.")
        ws["A2"].font = grey
        ws.merge_cells("A1:L1")
        ws.merge_cells("A2:L2")

        n_alt, first, last = 8, 5, 34
        cols = list(range(4, 4 + n_alt))  # D..K
        wcol = 4 + n_alt                  # L: weight used
        L = lambda c: ws.cell(4, c).column_letter

        headers = [
            ("Criterion", "Criterion: one clear requirement per row, defined so that two people mark it the same way", 34),
            ("Importance\n(optional)", "Importance: Pugh grades criteria in three categories (important, moderately "
                                        "important, desirable), not numerically. Enter High, Medium or Low. A number is "
                                        "accepted for the later-practice weighted net only. Agree before marking.", 12),
            ("Datum: {{datum: baseline alternative: the current solution or the strongest known one}}",
             "Datum: the reference every alternative is compared with. Its column is always S.", 18),
        ]
        for i in range(1, n_alt + 1):
            headers.append(("{{alt%d: alternative %d, described at the same level of detail}}" % (i, i),
                            "Alternative %d: mark each criterion + (better than the datum), S (same) or - (worse)" % i, 16))
        headers.append(("Weight\nused", "Calculated automatically, for the later-practice weighted net only: High 3, Medium 2, "
                                         "Low 1, a typed number as is, 1 if blank; 0 on empty rows.", 10))
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(4, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="left" if i == 1 else "center")
            c.border = Border(bottom=thin)
            c.comment = Comment(hint, "pdm-skills", width=260, height=110)
            ws.column_dimensions[c.column_letter].width = width
        ws.row_dimensions[4].height = 62

        for r in range(first, last + 1):
            ws.cell(r, wcol, f'=IF(A{r}="",0,IF(B{r}="High",3,IF(B{r}="Medium",2,IF(B{r}="Low",1,IF(ISNUMBER(B{r}),B{r},1)))))').number_format = "0.##;-0.##;;@"
            ws.cell(r, wcol).font = grey
            for c in range(1, wcol + 1):
                cell = ws.cell(r, c)
                if c != wcol:
                    cell.font = regular
                if 2 <= c < wcol:
                    cell.alignment = center
                if 3 <= c < wcol:
                    cell.number_format = "@"
            ws.cell(r, 3).fill = datum_fill

        top, bottom = first, last
        rows = [
            ("Better (+)", lambda c: f'=IF({c}$4="","",SUMPRODUCT(({c}${top}:{c}${bottom}="+")*1))'),
            ("Same (S)", lambda c: f'=IF({c}$4="","",SUMPRODUCT(({c}${top}:{c}${bottom}="S")*1))'),
            ("Worse (-)", lambda c: f'=IF({c}$4="","",SUMPRODUCT(({c}${top}:{c}${bottom}="-")*1))'),
            ("Criteria not marked", lambda c: f'=IF({c}$4="","",SUMPRODUCT(($A${top}:$A${bottom}<>"")*({c}${top}:{c}${bottom}="")))'),
            ("Later practice, not Pugh's (the marks must not be summed):", None),
            ("Net (better minus worse)", lambda c: f'=IF({c}$4="","",{c}36-{c}38)'),
            ("Weighted net", lambda c: (f'=IF({c}$4="","",SUMPRODUCT($L${top}:$L${bottom}*({c}${top}:{c}${bottom}="+"))'
                                        f'-SUMPRODUCT($L${top}:$L${bottom}*({c}${top}:{c}${bottom}="-")))')),
            ("Rank by net", lambda c: f'=IF({c}$4="","",RANK({c}41,$D$41:$K$41))'),
            ("Rank by weighted net", lambda c: f'=IF({c}$4="","",RANK({c}42,$D$42:$K$42))'),
        ]
        for k, (name, make) in enumerate(rows):
            r = 36 + k
            a = ws.cell(r, 1, name)
            a.font = bold
            for c in range(1, wcol + 1):
                ws.cell(r, c).border = Border(top=thin) if k == 0 else Border()
            if make is None:
                a.font = Font(name=FONT, italic=True, size=10, color="6B7280")
                continue
            for c in cols:
                cell = ws.cell(r, c, make(L(c)))
                cell.font, cell.alignment = (bold if name.startswith("Net") else regular), center
        ws.cell(36, 3, "S only").font = grey
        ws.cell(36, 3).alignment = center
        ws["A46"] = "Decision: {{decision: which alternatives are dropped, combined or taken forward, and why}}"
        ws["A46"].font = bold
        ws.merge_cells("A46:L46")
        ws["A47"] = ("Read the pattern, not only the totals: an alternative with many + can still lose on the criterion "
                     "that matters most. The matrix does not make the decision; control stays with the participants.")
        ws["A47"].font = grey
        ws.merge_cells("A47:L47")
        ws.freeze_panes = "C5"
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text="Pugh!$A$5")

        dv_mark = DataValidation(type="list", formula1='"+,S,-"', allow_blank=True, errorStyle="stop",
                                 showErrorMessage=True, errorTitle="Mark", error="Use + (better), S (same) or - (worse)")
        dv_datum = DataValidation(type="list", formula1='"S"', allow_blank=True, errorStyle="stop",
                                  showErrorMessage=True, errorTitle="Datum", error="The datum is always S")
        dv_w = DataValidation(type="list", formula1='"High,Medium,Low"', allow_blank=True, errorStyle="warning",
                              showErrorMessage=True, errorTitle="Importance",
                              error="Pugh grades criteria High, Medium or Low; a number is accepted for the weighted net")
        dv_mark.add(f"D{first}:K{last}")
        dv_datum.add(f"C{first}:C{last}")
        dv_w.add(f"B{first}:B{last}")
        for dv in (dv_mark, dv_datum, dv_w):
            ws.add_data_validation(dv)
