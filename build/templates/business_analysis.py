from .base import *


class SegmentScoring(XlsxSpec):
    @property
    def rel(self):
        return "business-analysis/segment-scoring/segment-scoring.xlsx"

    example = {"text": {
        "title": "FreshDrop, 5 customer segments for the autumn campaign",
        "method": "weighted sum",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Segments"

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        thin = Side(style="thin", color="C9CED6")

        ws["A1"] = "Segment Scoring: {{title: product, what is being chosen, date}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:H1")
        ws["A2"] = "Calculation method:"
        ws["A2"].font = muted
        ws["B2"] = "{{method: \"product\" or \"weighted sum\"}}"
        ws["B2"].font = bold
        ws.merge_cells("B2:F2")
        ws["A3"] = "Criterion weight (for the weighted sum):"
        ws["A3"].font = muted
        for c in range(2, 6):
            ws.cell(3, c, 1).font = bold

        headers = [
            ("Segment", "customer group and its situation", 34),
            ("Volume", "customers or money in the segment; score 1–3", 13),
            ("Ability to pay", "willingness and ability to pay; score 1–3", 15),
            ("Pain", "how acute the problem is; score 1–3", 13),
            ("Accessibility", "ease of reaching the segment; score 1–3", 13),
            ("Rationale", "facts and sources behind the scores", 44),
            ("Score", "product or weighted sum of the criteria", 10),
            ("Rank", "rank by score, 1 is the top segment", 10),
        ]
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(4, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            c.comment = Comment(hint, "pdm-skills", width=260, height=110)
            ws.column_dimensions[c.column_letter].width = width
        ws.row_dimensions[4].height = 34
        ws.column_dimensions["A"].width = 36

        first, last = 5, 34
        for r in range(first, last + 1):
            ws.cell(r, 7, f'=IF(COUNT(B{r}:E{r})=0,"",'
                          f'IF($B$2="weighted sum",SUMPRODUCT(B{r}:E{r},$B$3:$E$3),PRODUCT(B{r}:E{r})))'
                          ).number_format = "0.##"
            ws.cell(r, 8, f'=IF(G{r}="","",RANK(G{r},$G${first}:$G${last}))')
            for c in range(1, 9):
                ws.cell(r, c).font = regular
            for c in (1, 6):
                ws.cell(r, c).alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = "B5"
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text="'Segments'!$A$5")

        dv_m = DataValidation(type="list", formula1='"product,weighted sum"', allow_blank=True,
                              errorStyle="warning", showErrorMessage=True,
                              error="Method: \"product\" or \"weighted sum\"")
        dv_m.add("B2")
        dv_s = DataValidation(type="whole", operator="between", formula1="1", formula2="3", allow_blank=True,
                              errorStyle="warning", showErrorMessage=True, error="Scores are from 1 to 3")
        dv_s.add(f"B{first}:E{last}")
        for dv in (dv_m, dv_s):
            ws.add_data_validation(dv)


class SwotAnalysis(PptxSpec):
    @property
    def rel(self):
        return "business-analysis/swot-analysis/swot-analysis.pptx"

    example = {"text": {
        "title": "FreshDrop, grocery delivery in Moscow, Q3 2026",
        "corner": "FreshDrop · Q3 2026",
        "opportunities": "office districts go remote: more home deliveries; 2 new metro lines",
        "threats": "Kuper cuts prices 15%; courier wages rising in Moscow",
        "strengths": "2-hour delivery in 80% of districts; 98% on time in June",
        "weaknesses": "narrow range: 4 000 items vs 12 000 at rivals",
        "so": "use the on-time record to win remote-office families with a weekly plan",
        "st": "match Kuper prices on 200 staple items using our stock data",
        "wo": "use the new metro lines to add 10 dark-store pickup points",
        "wt": "cut low-margin categories; stop non-food delivery in 2 districts",
    }}

    def draw(self, prs, slide):
        header(slide, "SWOT · EXTENDED MATRIX", "{{title: company, product or decision, date}}")
        sh = slide.shapes
        # Internal factors head the rows, external ones the columns; strategies sit at the crossings (TOWS)
        x0, y0, w, h = 0.5, 1.25, 12.33, 5.95
        c0, r0 = 3.2, 1.75
        cw, rh = (w - c0) / 2, (h - r0) / 2

        def cell(x, y, bw, bh, tag, key, hint, fill=WHITE, tag_color=INK):
            tb = text(box(sh, x, y, bw, bh, fill=fill), f"{{{{{key}: {hint}}}}}", size=9)
            tb.text_frame.margin_top = Inches(0.34)
            tb.text_frame.paragraphs[0].space_after = Pt(2)
            label(sh, x + 0.06, y + 0.04, bw - 0.12, 0.28, tag, size=10, bold=True, color=tag_color)

        corner = box(sh, x0, y0, c0, r0, fill=ACCENT_BG)
        text(corner, "{{corner: product and period}}",
             size=9, color=MUTED, anchor=MSO_ANCHOR.MIDDLE)
        cell(x0 + c0, y0, cw, r0, "O · Opportunities", "opportunities", "external trends and events that help", fill=ACCENT_BG)
        cell(x0 + c0 + cw, y0, cw, r0, "T · Threats", "threats", "external trends and events that hinder", fill=ACCENT_BG)
        cell(x0, y0 + r0, c0, rh, "S · Strengths", "strengths", "what we do better than competitors", fill=ACCENT_BG)
        cell(x0, y0 + r0 + rh, c0, rh, "W · Weaknesses", "weaknesses", "what we do worse than competitors", fill=ACCENT_BG)
        cell(x0 + c0, y0 + r0, cw, rh, "SO · Strengths → opportunities", "so", "strategy from strengths and opportunities")
        cell(x0 + c0 + cw, y0 + r0, cw, rh, "ST · Strengths against threats", "st", "strategy from strengths and threats")
        cell(x0 + c0, y0 + r0 + rh, cw, rh, "WO · Opportunities cover weaknesses", "wo", "strategy from weaknesses and opportunities")
        cell(x0 + c0 + cw, y0 + r0 + rh, cw, rh, "WT · Reduce weaknesses, avoid threats", "wt", "strategy from weaknesses and threats")


class YcGuideToBusinessModels(XlsxSpec):
    @property
    def rel(self):
        return "business-analysis/yc-guide-to-business-models/yc-guide-to-business-models.xlsx"

    example = {"text": {
        "title": "FreshDrop, September 2026",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        models = [
            ("SaaS", "Cloud software by subscription", "MRR or ARR; growth rate by week or month; Net Revenue Retention; CAC",
             "Recurring revenue; one-off payments are not included in MRR/ARR; usually sold to businesses, ideally on annual contracts", "Adobe, Zoom, Slack"),
            ("Transactional", "Processes transactions and takes a cut", "GTV — payment volume; net revenue — fees; user retention; CAC",
             "Usually fintech and payments; one-off transactions, not a subscription; large volume at a low fee, 1–3%; the best have stable revenue from repeat transactions", "Stripe, Coinbase, Wise"),
            ("Marketplaces", "Connects buyers and sellers", "GMV — sales volume; net revenue — commission (take rate); growth rate; user retention",
             "Hard to launch: the chicken-and-egg problem; demand and supply grow together; network effects; successful ones often take the whole market", "Airbnb, DoorDash, Etsy"),
            ("Subscription", "Regular payment, usually from consumers", "MRR or ARR; growth rate; user retention; CAC",
             "Recurring revenue is the most valuable; usually monthly payment, low price, many customers; growth through self-service channels", "Amazon Prime, ClassPass, Netflix"),
            ("Enterprise", "Large contracts with big companies", "Bookings — signed contracts; revenue as delivered; ACV — annual contract value; pipeline — deals in progress",
             "Few customers, deals from $100K a year; direct sales, long cycle; the buyer is not always the user; growth in jumps, the monthly rate means little", "Workday, Salesforce, SAP"),
            ("Usage Based", "Pay for consumption", "Monthly revenue is not recurring; growth rate; revenue retention; gross margin",
             "Do not confuse usage revenue with recurring revenue; pay per request, record, data volume; you grow together with customers", "AWS, Twilio, Algolia"),
            ("E-commerce", "Sells goods online", "Monthly revenue; growth rate; gross margin and unit economics; CAC",
             "D2C brands and Shopify stores; not a marketplace — the whole sale amount is yours, but cost of goods is higher and margin lower; acquisition and operations decide", "Amazon, Warby Parker, Home Depot"),
            ("Advertising", "Sells ads, users are free", "DAU; MAU; retention on days 1, 7, 30; CPM or CPC",
             "The customer is the advertiser, not the user; billions of impressions a month are needed; the number of registrations is a vanity metric", "Facebook, Twitter, Reddit"),
            ("Hardtech/Bio/Moonshots", "Big technical risk, long horizon", "Milestones toward the goal; signed contracts; LOI — letters of intent",
             "Years often pass before a product because of technical and regulatory risks; technical milestones and experiment data reduce the risk; LOIs show demand", "Boom, Pfizer, Cruise"),
        ]

        ws = wb.active
        ws.title = "Metrics"
        ref = wb.create_sheet("Reference")

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        thin = Side(style="thin", color="C9CED6")
        top = Alignment(wrap_text=True, vertical="top")

        ref["A1"] = "Nine business models and their main metrics (Y Combinator, Aaron Epstein)"
        ref["A1"].font = Font(name=FONT, bold=True, size=14)
        ref.merge_cells("A1:E1")
        for i, (title, width) in enumerate([("Model", 22), ("What it is", 30), ("Main metrics", 48),
                                            ("What to know", 60), ("Examples", 26)], start=1):
            c = ref.cell(2, i, title)
            c.font, c.fill, c.border = bold, head_fill, Border(bottom=thin)
            ref.column_dimensions[c.column_letter].width = width
        for r, row in enumerate(models, start=3):
            for i, v in enumerate(row, start=1):
                c = ref.cell(r, i, v)
                c.font, c.alignment = (bold if i == 1 else regular), top
        ref.freeze_panes = "B3"

        ws["A1"] = "YC Guide to Business Models: {{title: company or product, date}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:I1")
        ws["A2"].font = muted
        ws.merge_cells("A2:I2")

        headers = [
            ("Line", "product or line of business", 22),
            ("Model", "one of the nine models, or your own", 18),
            ("Metric", "metric tracked for this line", 24),
            ("How it is counted", "exact definition: what is included and not", 36),
            ("Value", "latest value with its unit", 14),
            ("Period", "period the value covers: month, quarter, year", 12),
            ("Change", "growth against the previous period", 14),
            ("Conclusion", "what the metric says and what follows", 40),
            ("Guide metrics", "main metrics of the model", 40),
        ]
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(3, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            c.comment = Comment(hint, "pdm-skills", width=260, height=110)
            ws.column_dimensions[c.column_letter].width = width
        ws.row_dimensions[3].height = 22

        first, last = 4, 53
        for r in range(first, last + 1):
            f = ws.cell(r, 9, f'=IF(B{r}="","",IFERROR(VLOOKUP(B{r},\'Reference\'!$A$3:$C$11,3,FALSE),"not in the guide"))')
            f.fill = calc_fill
            for c in range(1, 10):
                ws.cell(r, c).font = regular
                ws.cell(r, c).alignment = top
        ws.freeze_panes = "A4"
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text="'Metrics'!$A$4")

        dv = DataValidation(type="list", formula1="'Reference'!$A$3:$A$11", allow_blank=True,
                            errorStyle="information", showErrorMessage=True,
                            error="The model is not in the guide: explain it in the \"Conclusion\" column")
        dv.add(f"B{first}:B{last}")
        ws.add_data_validation(dv)


class BcgMatrix(PptxSpec):
    @property
    def rel(self):
        return "business-analysis/bcg-matrix/bcg-matrix.pptx"

    example = {"text": {
        "title": "FreshDrop portfolio, 2026: 6 product lines",
        "scales": "Market data from Nielsen, 2025. Growth boundary 10%. Circle size = revenue of the line",
        "decision": "Fund: ready meals. Hold: groceries. Withdraw cash: fresh flowers. Sell: none",
        "cash": "Groceries fund ready meals; flowers return 4 M a year, to be closed in Q4",
    }}

    def draw(self, prs, slide):
        from lxml import etree
        header(slide, "BCG MATRIX · GROWTH-SHARE MATRIX", "{{title: company, portfolio, year}}")
        # x is stored as 1/relative share: high share on the left in every viewer
        # (fill_pptx.py flips data for charts whose alt text says "invert_x")
        quadrants = [("Stars", 1 / 3.2, 28.5), ("Question marks", 1 / 0.32, 28.5),
                     ("Cash cows", 1 / 3.2, -8.5), ("Dogs", 1 / 0.32, -8.5)]
        units = [("Unit A", 1 / 2.5, 18), ("Unit B", 1 / 0.4, 22), ("Unit C", 1 / 1.8, 3),
                 ("Unit D", 1 / 0.3, 1)]
        data = XyChartData()
        series = [("Share boundary", [(1, -10), (1, 30)]), ("Growth boundary", [(0.1, 10), (10, 10)])]
        series += [(name, [(x, y)]) for name, x, y in quadrants]
        series += [(name, [(x, y)]) for name, x, y in units]
        for name, pts in series:
            ser = data.add_series(name)
            for x, y in pts:
                ser.add_data_point(x, y)
        frame = slide.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER, Inches(0.4), Inches(1.3),
                                       Inches(8.6), Inches(5.9), data)
        frame.name = "matrix"
        frame._element.nvGraphicFramePr.cNvPr.set("descr", "invert_x")
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


        for ser in all_series[2:6]:
            ser.marker.style = XL_MARKER_STYLE.NONE
            ser.format.line.fill.background()
            name_label(ser, XL_LABEL_POSITION.CENTER, 12, True, MUTED)
        for ser in all_series[6:]:
            ser.format.line.fill.background()
            ser.marker.style = XL_MARKER_STYLE.CIRCLE
            ser.marker.size = 24
            ser.marker.format.fill.solid()
            ser.marker.format.fill.fore_color.rgb = ACCENT
            ser.marker.format.line.color.rgb = WHITE
            name_label(ser, XL_LABEL_POSITION.RIGHT, 11, False, INK)
        axes = ((chart.category_axis, None, 0.1, 10, 10, "0.0#"),
                (chart.value_axis, "Market growth, % per year →", -10, 30, 10, '0"%"'))
        for axis, title, lo, hi, unit, fmt in axes:
            axis.minimum_scale, axis.maximum_scale, axis.major_unit = lo, hi, unit
            axis.has_major_gridlines = False
            axis.format.line.color.rgb = LINE
            axis.tick_labels.font.size = Pt(10)
            axis.tick_labels.font.color.rgb = MUTED
            axis.tick_labels.number_format, axis.tick_labels.number_format_is_linked = fmt, False
            if title is None:
                continue
            axis.has_title = True
            axis.axis_title.text_frame.text = title
            r = axis.axis_title.text_frame.paragraphs[0].runs[0]
            r.font.size, r.font.bold, r.font.name = Pt(11), False, FONT
            r.font.color.rgb = MUTED
        # share axis: logarithmic, own tick labels (the plotted values are 1/share)
        ns = "http://schemas.openxmlformats.org/drawingml/2006/chart"
        scaling = chart.category_axis._element.find(f"{{{ns}}}scaling")
        scaling.insert(0, etree.SubElement(scaling, f"{{{ns}}}logBase", val="10"))
        chart.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.NONE
        for el in chart.value_axis._element.findall(f"{{{ns}}}crosses"):
            el.getparent().remove(el)
        chart.value_axis._element.find(f"{{{ns}}}crossAx").addnext(etree.Element(f"{{{ns}}}crossesAt", val="0.1"))
        for el in chart.category_axis._element.findall(f"{{{ns}}}crosses"):
            el.getparent().remove(el)
        chart.category_axis._element.find(f"{{{ns}}}crossAx").addnext(etree.Element(f"{{{ns}}}crossesAt", val="-10"))
        # fixed plot area, so the tick labels below can be placed exactly
        lx, ly, lw, lh = 0.1, 0.03, 0.87, 0.84
        plot = chart._chartSpace.find(f"{{{ns}}}chart/{{{ns}}}plotArea")
        for el in plot.findall(f"{{{ns}}}layout"):
            plot.remove(el)
        layout = etree.Element(f"{{{ns}}}layout")
        manual = etree.SubElement(layout, f"{{{ns}}}manualLayout")
        for tag, val in (("layoutTarget", "inner"), ("xMode", "edge"), ("yMode", "edge"),
                         ("x", lx), ("y", ly), ("w", lw), ("h", lh)):
            etree.SubElement(manual, f"{{{ns}}}{tag}", val=str(val))
        plot.insert(0, layout)
        left, width = 0.4 + lx * 8.6, lw * 8.6
        bottom = 1.3 + (ly + lh) * 5.9
        for frac, tick in ((0, "10×"), (0.5, "1×"), (1, "0,1×")):
            label(slide.shapes, left + frac * width - 0.4, bottom + 0.04, 0.8, 0.28, tick, size=10, color=MUTED,
                  align=PP_ALIGN.CENTER)
        label(slide.shapes, left, bottom + 0.32, width, 0.3,
              "← Relative market share, times the largest competitor (log scale)", size=11, color=MUTED,
              align=PP_ALIGN.CENTER)

        x, w = 9.25, 3.6
        panels = [
            ("Markets and data", "{{scales: market data, growth boundary, circle size}}", 1.3, 1.75),
            ("Decisions", "{{decision: what we fund, hold, withdraw from or sell}}", 3.15, 2.2),
            ("Cash flow", "{{cash: where the cash comes from and goes}}", 5.45, 1.75),
        ]
        for tag, token, py, ph in panels:
            label(slide.shapes, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            text(box(slide.shapes, x, py + 0.35, w, ph - 0.35), token, size=11)


class SalesFunnel(PptxSpec):
    @property
    def rel(self):
        return "business-analysis/sales-funnel/sales-funnel.pptx"

    example = {"text": {
        "title": "FreshDrop checkout funnel, new app users, June 2026",
        "stage_1": "Open the app", "count_1": "4,200", "days_1": "—",
        "stage_2": "Add to cart", "count_2": "1,260", "conv_2": "30% from stage 1", "days_2": "3 min",
        "stage_3": "Choose a slot", "count_3": "530", "conv_3": "42% from stage 2", "days_3": "4 min",
        "stage_4": "Pay", "count_4": "480", "conv_4": "91% from stage 3", "days_4": "1 min",
        "stage_5": "Second order in 14 days", "count_5": "150", "conv_5": "31% from stage 4", "days_5": "7 days",
        "stage_6": "Weekly buyer", "count_6": "58", "conv_6": "39% from stage 5", "days_6": "14 days",
        "scope": "App analytics, unique users; time = median minutes between stages",
        "bottleneck": "Cart to slot choice loses 58%: the delivery slot step asks too much",
        "decision": "Shorten the slot picker to 2 taps. Expect cart-to-slot at 60% in 4 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "SALES FUNNEL", "{{title: product, whose customers, for what period}}")
        sh = slide.shapes
        # Stage widths are fixed, not proportional: the numbers carry the data, the shape only shows the order
        cx, top, rh, gap = 3.2, 1.75, 0.68, 0.18
        widths = [5.0, 4.4, 3.8, 3.2, 2.6, 2.0]
        for x, w, tag in ((0.7, 5.0, "Stage and how many customers are on it"), (5.9, 1.35, "Conversion from previous"),
                          (7.3, 1.2, "Time at stage")):
            label(sh, x, 1.25, w, 0.45, tag, size=10, bold=True, color=MUTED, anchor=MSO_ANCHOR.BOTTOM)
        for i, w in enumerate(widths, start=1):
            shapes = sh
            if i > 2:
                group = sh.add_group_shape()
                group.name = f"optional_stage_{i}"
                shapes = group.shapes
            y = top + (i - 1) * (rh + gap)
            text(box(shapes, cx - w / 2, y, w, rh, fill=ACCENT if i == 1 else ACCENT_BG, line=None),
                 f"{{{{stage_{i}: stage name}}}}: {{{{count_{i}: number of customers}}}}", size=12, bold=True,
                 color=WHITE if i == 1 else INK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            conv = "entry" if i == 1 else f"{{{{conv_{i}: % from previous stage}}}}"
            label(shapes, 5.9, y, 1.35, rh, conv, size=12, bold=i > 1, color=MUTED if i == 1 else INK,
                  anchor=MSO_ANCHOR.MIDDLE)
            label(shapes, 7.3, y, 1.2, rh, f"{{{{days_{i}: days or minutes}}}}", size=12, anchor=MSO_ANCHOR.MIDDLE)
            if i > 1:
                box(shapes, 5.65, y - gap - 0.05, 0.2, gap + 0.1, fill=LINE, line=None, kind=MSO_SHAPE.DOWN_ARROW)

        x, w = 8.75, 4.08
        panels = [
            ("Data", "{{scope: data source and how time is measured}}", INK, 1.3, 1.45),
            ("Bottleneck", "{{bottleneck: where we lose most customers and why}}", ACCENT, 2.9, 1.9),
            ("Decision", "{{decision: what we change and the expected result}}", INK, 4.95, 2.1),
        ]
        for tag, token, color, py, ph in panels:
            label(sh, x, py, w, 0.35, tag, size=12, bold=True, color=color)
            body = box(sh, x, py + 0.35, w, ph - 0.35, fill=ACCENT_BG if color == ACCENT else None,
                       line=ACCENT if color == ACCENT else LINE)
            text(body, token, size=11)


class ProductLifecycle(PptxSpec):
    @property
    def rel(self):
        return "business-analysis/product-lifecycle/product-lifecycle.pptx"

    example = {"text": {
        "title": "FreshDrop click-and-collect, Moscow, 2022–2026",
        "stages": "Introduction 2022, growth 2023–2024, maturity from 2025: growth under 3% a quarter",
        "now": "Maturity: orders +2% a quarter, margin 9%, new customers 11% of orders",
        "decision": "Extend: add a family bundle for the new market. Do not exit: margin is above 0",
        "result": "Bundle tested in 2 districts from 1 July; check new-customer share in 8 weeks",
    }}

    def draw(self, prs, slide):
        from pptx.enum.chart import XL_LEGEND_POSITION

        header(slide, "PRODUCT LIFECYCLE", "{{title: product, market, years}}")
        # The sample shows the textbook shape: slow start, growth, plateau, decline; the data replaces it
        data = CategoryChartData()
        data.categories = [f"Year {i}" for i in range(1, 11)]
        data.add_series("Revenue", [1, 2, 5, 11, 18, 23, 25, 24, 20, 15])
        data.add_series("Profit", [-3, -3, -1, 2, 5, 7, 7, 6, 3, 0])
        frame = slide.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.4), Inches(1.3),
                                       Inches(8.6), Inches(4.9), data)
        frame.name = "curve"
        chart = frame.chart
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(11)
        chart.font.name, chart.font.size = FONT, Pt(11)
        chart.font.color.rgb = INK
        for ser, color in zip(chart.plots[0].series, (ACCENT, GOOD)):
            ser.smooth = False
            ser.format.line.color.rgb = color
            ser.format.line.width = Pt(2.5)
            ser.marker.style = XL_MARKER_STYLE.CIRCLE
            ser.marker.size = 7
            ser.marker.format.fill.solid()
            ser.marker.format.fill.fore_color.rgb = color
            ser.marker.format.line.color.rgb = WHITE
        va = chart.value_axis
        va.has_major_gridlines = True
        va.major_gridlines.format.line.color.rgb = RGBColor(0xEC, 0xEE, 0xF1)
        va.tick_labels.number_format, va.tick_labels.number_format_is_linked = "#,##0", False
        for axis in (chart.category_axis, va):
            axis.format.line.color.rgb = LINE
            axis.tick_labels.font.size = Pt(10)
            axis.tick_labels.font.color.rgb = MUTED

        label(slide.shapes, 0.5, 6.3, 1.3, 0.35, "Stages", size=12, bold=True)
        text(box(slide.shapes, 1.8, 6.25, 7.1, 0.95),
             "{{stages: years of each stage and signs}}", size=11)

        x, w = 9.25, 3.6
        panels = [
            ("Current stage", "{{now: current stage and the numbers showing it}}", ACCENT, 1.3, 1.9),
            ("Decision", "{{decision: extend or exit, and the reason}}", INK, 3.25, 2.0),
            ("Result", "{{result: what changed after the decision, with dates}}", INK, 5.3, 1.9),
        ]
        for tag, token, color, py, ph in panels:
            label(slide.shapes, x, py, w, 0.35, tag, size=12, bold=True, color=color)
            body = box(slide.shapes, x, py + 0.35, w, ph - 0.35, fill=ACCENT_BG if color == ACCENT else None,
                       line=ACCENT if color == ACCENT else LINE)
            text(body, token, size=11)


class TechnologyAdoptionLifecycle(PptxSpec):
    @property
    def rel(self):
        return "business-analysis/technology-adoption-lifecycle/technology-adoption-lifecycle.pptx"

    example = {"text": {
        "title": "FreshDrop in Moscow: which buyers adopt the app first, August 2026",
        "innovators": "Foodies who try a new app within a week; 2–3% of Moscow buyers",
        "early_adopters": "Busy professionals who already order groceries online; accept a slot delay",
        "early_majority": "Families who want one fixed slot and a full list; need proof of reliability",
        "late_majority": "Older buyers and price-driven shoppers; need phone support and a price match",
        "laggards": "Store-only shoppers; not a target before 2028",
        "now": "4% of Moscow households, July 2026; busy families buy first",
        "beachhead": "Families with two kids in new districts: they lack time and parking",
        "whole_product": "Pickup at home metro, 24/7 support, free returns, price matched to the store",
    }}

    def draw(self, prs, slide):
        import math
        from pptx.enum.dml import MSO_LINE_DASH_STYLE
        from pptx.enum.shapes import MSO_CONNECTOR
        header(slide, "TECHNOLOGY ADOPTION LIFECYCLE · THE CHASM",
               "{{title: product or technology, market, date}}")
        sh = slide.shapes
        cx, cy, cw, chh = 0.6, 1.3, 12.1, 2.45  # chart area; x runs from -3 to +3 standard deviations

        def line(x1, y1, x2, y2, color=LINE, width=1.0, dash=None):
            return connector(sh, (x1, y1), (x2, y2), color=color, width=width, dash=dash)

        pts = [(cx + t * cw, cy + chh - math.exp(-((t * 6 - 3) ** 2) / 2) * chh * 0.95)
               for t in (i / 240 for i in range(241))]
        ff = sh.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
        ff.add_line_segments([(Inches(x), Inches(y)) for x, y in pts[1:]], close=False)
        c = ff.convert_to_shape()
        c.fill.background()
        c.line.color.rgb, c.line.width = ACCENT, Pt(3)
        c.shadow.inherit = False
        line(cx, cy + chh, cx + cw, cy + chh, color=INK, width=1.25)
        bounds = [0, 1 / 6, 2 / 6, 3 / 6, 4 / 6, 1]
        for b in bounds[1:-1]:
            line(cx + b * cw, cy + 0.2, cx + b * cw, cy + chh, dash=MSO_LINE_DASH_STYLE.DASH)
        # The chasm: a visible break in the curve between early adopters and the early majority
        gx = cx + 2 / 6 * cw
        box(sh, gx - 0.12, cy, 0.24, chh - 0.03, fill=WHITE, line=None)
        label(sh, gx - 0.8, cy - 0.05, 1.6, 0.3, "CHASM", size=10, bold=True, color=BAD, align=PP_ALIGN.CENTER)

        segments = [
            ("Innovators, 2.5%", "innovators"),
            ("Early adopters, 13.5%", "early_adopters"),
            ("Early majority, 34%", "early_majority"),
            ("Late majority, 34%", "late_majority"),
            ("Laggards, 16%", "laggards"),
        ]
        ly = cy + chh + 0.08
        for (a, b), (tag, key) in zip(zip(bounds, bounds[1:]), segments):
            x, w = cx + a * cw, (b - a) * cw
            label(sh, x, ly, w, 0.45, tag, size=10, bold=True, color=ACCENT, anchor=MSO_ANCHOR.MIDDLE)
            who = f"{{{{{key}: who they are and what they need}}}}"
            tb = text(box(sh, x + 0.03, ly + 0.47, w - 0.06, 1.05, fill=ACCENT_BG, line=None), who, size=9)
            tb.text_frame.paragraphs[0].space_after = Pt(2)

        py, ph = 5.85, 1.4
        panels = [
            ("Where we are now", "{{now: share of adopters and who buys now}}", ACCENT),
            ("Beachhead", "{{beachhead: the niche we take first, and why}}", INK),
            ("Whole product", "{{whole_product: what to add for this niche}}", INK),
        ]
        pw = (cw - 0.3) / 3
        for i, (tag, token, color) in enumerate(panels):
            x = cx + i * (pw + 0.15)
            label(sh, x, py - 0.36, pw, 0.34, tag, size=12, bold=True, color=color)
            body = box(sh, x, py, pw, ph, fill=ACCENT_BG if color == ACCENT else None,
                       line=ACCENT if color == ACCENT else LINE)
            text(body, token, size=10)


class AbcAnalysis(XlsxSpec):
    @property
    def rel(self):
        return "business-analysis/abc-analysis/abc-analysis.xlsx"

    example = {"text": {
        "title": "FreshDrop SKUs, sales in revenue, January–August 2026",
    }}

    def draw(self, wb):
        from openpyxl.chart import Reference, ScatterChart, Series
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "ABC"
        cv = wb.create_sheet("Curve")

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        thin = Side(style="thin", color="C9CED6")

        first, last = 8, 507
        rng = lambda col: f"${col}${first}:${col}${last}"
        ws["A1"] = "ABC Analysis: {{title: what is ranked, by which value, for which period}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:G1")
        ws["A2"], ws["B2"] = "A boundary: cumulative share of value up to", 0.8
        ws["A3"], ws["B3"] = "B boundary: cumulative share of value up to", 0.95
        for r in (2, 3):
            ws.cell(r, 1).font = muted
            ws.cell(r, 2).font, ws.cell(r, 2).number_format = bold, "0%"
        ws["B2"].comment = Comment("An object falls into A while the cumulative share before it is below this boundary. "
                                   "The canon is 80%; change it before the calculation, not after.", "pdm-skills", width=260, height=90)
        ws["B3"].comment = Comment("An object falls into B while the cumulative share before it is below this boundary, "
                                   "but not below the A boundary; the rest are C. The canon is 95%.", "pdm-skills", width=260, height=90)

        ws["D2"] = "Class"
        ws["E2"] = "Objects"
        ws["F2"] = "Share of objects"
        ws["G2"] = "Share of value"
        for c in "DEFG":
            ws[f"{c}2"].font, ws[f"{c}2"].fill = bold, head_fill
        for i, k in enumerate("ABC", start=3):
            ws[f"D{i}"] = k
            ws[f"D{i}"].font = bold
            ws[f"E{i}"] = f'=COUNTIF({rng("F")},"{k}")'
            ws[f"F{i}"] = f'=IF(COUNT({rng("B")})=0,"",E{i}/COUNT({rng("B")}))'
            ws[f"G{i}"] = f'=IF(SUM({rng("B")})=0,"",SUMIF({rng("F")},"{k}",{rng("B")})/SUM({rng("B")}))'
            for c in "EFG":
                ws[f"{c}{i}"].fill = calc_fill
            ws[f"F{i}"].number_format = ws[f"G{i}"].number_format = "0%"

        headers = [
            ("Object", "A product, customer, seller, feature — one row per object. Row order is arbitrary: rank and classes are calculated automatically.", 34),
            ("Value", "The number to rank by: revenue, margin, orders, frequency — one measure and one period for all rows.", 14),
            ("Comment", "Features of the object: new, seasonal, strategic — what the formula does not see.", 36),
            ("Rank", "Calculated automatically: position by value, 1 — the most valuable.", 9),
            ("Share", "Calculated automatically: the object's share of total value.", 10),
            ("Class", "Calculated automatically: A, B or C by the cumulative share of value up to the object and the boundaries in B2 and B3.", 9),
            ("Cumulative", "Calculated automatically: the cumulative share of value of objects ranked at or above this one, including it.", 12),
        ]
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(first - 1, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            c.comment = Comment(hint, "pdm-skills", width=260, height=100)
            ws.column_dimensions[c.column_letter].width = width
        ws.column_dimensions["A"].width = 40
        for r in range(first, last + 1):
            ws.cell(r, 4, f'=IF(B{r}="","",RANK(B{r},{rng("B")})+COUNTIF(B${first}:B{r},B{r})-1)')
            ws.cell(r, 5, f'=IF(B{r}="","",B{r}/SUM({rng("B")}))').number_format = "0.0%"
            ws.cell(r, 7, f'=IF(B{r}="","",SUMIF({rng("D")},"<="&D{r},{rng("B")})/SUM({rng("B")}))').number_format = "0.0%"
            ws.cell(r, 6, f'=IF(B{r}="","",IF(G{r}-E{r}<$B$2,"A",IF(G{r}-E{r}<$B$3,"B","C")))')
            for c in range(1, 8):
                ws.cell(r, c).font = regular
                if c >= 4:
                    ws.cell(r, c).fill = calc_fill
            ws.cell(r, 3).alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = f"B{first}"
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'ABC'!$A${first}")
        dv = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=False,
                            errorStyle="warning", showErrorMessage=True, error="The boundary is a share from 0 to 1, e.g. 0.8")
        dv.add("B2:B3")
        ws.add_data_validation(dv)

        # Pareto curve: objects sorted by rank, cumulative shares
        cv["A1"] = "Pareto curve"
        cv["A1"].font = bold
        for i, title in enumerate(["Rank", "Share of objects", "Share of value"], start=1):
            cv.cell(2, i, title).font = bold
        n = last - first + 1
        cv.cell(3, 1, 0)
        cv.cell(3, 2, 0)
        cv.cell(3, 3, 0)
        for k in range(1, n + 1):
            r = k + 3
            cv.cell(r, 1, k)
            # past the last object the curve stays at its end point (1; 1)
            cnt = f"COUNT(ABC!{rng('B')})"
            cv.cell(r, 2, f"=IF({cnt}=0,0,MIN(A{r},{cnt})/{cnt})").number_format = "0%"
            cv.cell(r, 3, f"=IF({cnt}=0,0,SUMIF(ABC!{rng('D')},\"<=\"&MIN(A{r},{cnt}),ABC!{rng('B')})"
                           f"/SUM(ABC!{rng('B')}))").number_format = "0%"
        chart = ScatterChart()
        chart.title = "Pareto curve"
        chart.style = 13
        chart.scatterStyle = "line"
        chart.x_axis.title = "Share of objects"
        chart.y_axis.title = "Share of value"
        chart.x_axis.number_format = chart.y_axis.number_format = "0%"
        chart.x_axis.scaling.min = chart.y_axis.scaling.min = 0
        chart.x_axis.scaling.max = chart.y_axis.scaling.max = 1
        chart.x_axis.delete = chart.y_axis.delete = False
        chart.legend = None
        s = Series(Reference(cv, min_col=3, min_row=3, max_row=n + 3), Reference(cv, min_col=2, min_row=3, max_row=n + 3))
        s.marker.symbol = "none"
        s.smooth = False
        chart.series.append(s)
        chart.width, chart.height = 18, 10
        ws.add_chart(chart, "I2")


class AdlMatrix(PptxSpec):
    @property
    def rel(self):
        return "business-analysis/adl-matrix/adl-matrix.pptx"

    example = {"text": {
        "title": "Grocery retailer FreshDrop, food delivery, assessment 1 September 2026",
        "c11": "Lock in early buyers: free first delivery, lead the Moscow market",
        "c12": "Expand to new districts; invest in courier capacity",
        "c13": "Defend share: loyalty bonuses and fixed slots",
        "c14": "Harvest cash: cut paid promos, keep the core",
        "c21": "Build the base: referral bonus and fast onboarding",
        "c22": "Invest to grow: new districts and weekly boxes",
        "c23": "Protect margin: raise basket size, not promos",
        "c24": "Hold position: automate support, cut costs",
        "c31": "Test a niche: family boxes in 2 districts",
        "c32": "Focus on 2 districts where we lead",
        "c33": "Differentiate: fast delivery and fresh goods",
        "c34": "Consider a partnership or exit weak districts",
        "c41": "Partner with a store chain before scaling",
        "c42": "Keep pace with cost; no new markets yet",
        "c43": "Cut costs; run only profitable districts",
        "c44": "Sell or close the service in this district",
        "c51": "Do not enter alone; wait for a partner",
        "c52": "Exit or merge with a rival",
        "c53": "Exit unless the niche is profitable",
        "c54": "Exit now and close the service",
        "cell": "Moscow grocery delivery, Growth · Strong: share 14% in our districts",
        "stage_basis": "Orders grow 35% a year; 6 rivals in Moscow; shares stable for 2 quarters; high entry costs",
        "position_basis": "14% share in our districts, second after a national chain; advantage: 30-minute slots",
        "decision": "Invest in courier capacity and 3 new districts; review in Q1 2027 with the district P&L",
        "risk": "A rival cuts prices; orders stop growing (change of stage); the share comes from a survey",
    }}

    def draw(self, prs, slide):
        header(slide, "ADL MATRIX · ARTHUR D. LITTLE MATRIX",
               "{{title: business unit, industry and assessment date}}")
        sh = slide.shapes
        stages = ["Embryonic", "Growth", "Mature", "Aging"]
        positions = ["Dominant", "Strong", "Favorable", "Acceptable (tenable)", "Weak"]
        x0, y0, rw, cw, hh, rh = 0.5, 1.3, 1.45, 1.7, 0.45, 0.93

        label(sh, x0, y0, rw, hh, "Position ↓ / stage →", size=9, bold=True, color=MUTED, anchor=MSO_ANCHOR.MIDDLE)
        for j, s in enumerate(stages):
            text(box(sh, x0 + rw + j * cw, y0, cw, hh, fill=INK, line=WHITE), s,
                 size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        for i, p in enumerate(positions):
            y = y0 + hh + i * rh
            text(box(sh, x0, y, rw, rh, fill=ACCENT_BG, line=WHITE), p,
                 size=11, bold=True, color=ACCENT, anchor=MSO_ANCHOR.MIDDLE)
            for j in range(4):
                tb = text(box(sh, x0 + rw + j * cw, y, cw, rh), "{{c%d%d: strategy for the cell}}" % (i + 1, j + 1),
                          size=9, anchor=MSO_ANCHOR.MIDDLE)

        x, w = 9.6, 3.23
        panels = [
            ("Business cell", "cell", "{{cell: industry stage and business position}}", 1.3, 0.95, True),
            ("Stage basis", "stage_basis", "{{stage_basis: factors that define the stage}}", 2.35, 1.15, False),
            ("Position basis", "position_basis", "{{position_basis: fact that proves the position}}", 3.6, 1.15, False),
            ("Decision", "decision", "{{decision: family of actions, specific step, review date}}", 4.75, 1.4, True),
            ("Risks and limitations", "risk", "{{risk: what could invalidate the conclusion}}", 6.2, 0.95, False),
        ]
        for tag, key, hint, py, ph, accent in panels:
            box(sh, x, py, w, ph, fill=ACCENT_BG if accent else None, line=ACCENT if accent else LINE)
            label(sh, x + 0.06, py + 0.02, w - 0.12, 0.3, tag, size=11, bold=True, color=ACCENT)
            tb = text(box(sh, x + 0.06, py + 0.3, w - 0.12, ph - 0.34, line=None), hint, size=10)


class GeMckinseyMatrix(PptxSpec):
    @property
    def rel(self):
        return "business-analysis/ge-mckinsey-matrix/ge-mckinsey-matrix.pptx"

    example = {"text": {
        "title": "eBay, three reportable segments, end of 2019 (our scoring)",
        "hh": None, "hm": None, "hl": None,
        "mh": "Marketplace: 3.15 / 3.80",
        "mm": "Classifieds: 3.40 / 3.55",
        "ml": None,
        "lh": None,
        "lm": "StubHub: 2.25 / 2.65",
        "ll": None,
        "attr": ["Size 20%, growth 25%, few rivals 25%, entry barriers 15%, low external risk 15%",
                 "Scores: Marketplace 3.15, Classifieds 3.40, StubHub 2.25"],
        "strength": ["Share 30%, brand 15%, margin 20%, momentum 20%, fit with the rest 15%",
                     "Scores: Marketplace 3.80, Classifieds 3.55, StubHub 2.65"],
        "scale": "Ratings 1 to 5, high = better for the unit. Cut-offs fixed before scoring: 2.33 and 3.67",
        "decision": ["Marketplace: invest, it is the core", "StubHub: sold to viagogo, $4.05 bn, Feb 2020",
                     "Classifieds: sold to Adevinta, about $9.2 bn, June 2021"],
        "risk": ["Ratings are ours; eBay did not use the matrix", "The grid ignores price and the buyer's synergies"],
    }}

    def draw(self, prs, slide):
        header(slide, "GE–McKINSEY MATRIX · NINE-BOX MATRIX",
               "{{title: company or portfolio, date, who scored}}")
        sh = slide.shapes
        GREEN, YELLOW, RED = RGBColor(0xE1, 0xF0, 0xE5), RGBColor(0xFA, 0xF0, 0xCC), RGBColor(0xF7, 0xDD, 0xDA)
        zones = {"g": (GREEN, "Invest, grow"), "y": (YELLOW, "Selective, earnings"), "r": (RED, "Harvest, divest")}
        # rows: attractiveness high, medium, low; columns: strength low, medium, high
        grid = [["y", "g", "g"], ["r", "y", "g"], ["r", "r", "y"]]
        keys = [["hl", "hm", "hh"], ["ml", "mm", "mh"], ["ll", "lm", "lh"]]
        rows = ["High", "Medium", "Low"]
        cols = ["Low", "Medium", "High"]
        x0, y0, rw, cw, rh, ch = 0.5, 1.3, 0.9, 1.9, 1.55, 0.4
        for i, name in enumerate(rows):
            label(sh, x0, y0 + i * rh, rw, rh, name, size=11, bold=True, color=MUTED, align=PP_ALIGN.RIGHT,
                  anchor=MSO_ANCHOR.MIDDLE)
        for j, name in enumerate(cols):
            label(sh, x0 + rw + j * cw, y0 + 3 * rh, cw, ch, name, size=11, bold=True, color=MUTED,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        for i in range(3):
            for j in range(3):
                fill, zone = zones[grid[i][j]]
                cx, cy = x0 + rw + j * cw, y0 + i * rh
                box(sh, cx, cy, cw - 0.06, rh - 0.06, fill=fill, line=None)
                label(sh, cx, cy, cw - 0.06, 0.3, zone, size=9, bold=True, color=MUTED, align=PP_ALIGN.CENTER)
                text(box(sh, cx, cy + 0.3, cw - 0.06, rh - 0.4, line=None),
                     "{{%s: units in this cell, attractiveness / strength}}" % keys[i][j], size=10,
                     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        label(sh, x0 + rw, y0 + 3 * rh + ch, 3 * cw, 0.3, "Strength of the unit →", size=11, color=MUTED,
              align=PP_ALIGN.CENTER)
        label(sh, 0.5, 1.0, 3.2, 0.32, "↑ Attractiveness of the industry", size=10, color=MUTED)

        x, w = 7.35, 5.48
        panels = [
            ("Attractiveness: factors, weights, scores", "attr", "{{attr: factors with weights; unit scores}}", 1.3, 1.1, False),
            ("Strength: factors, weights, scores", "strength", "{{strength: factors with weights; unit scores}}", 2.5, 1.1, False),
            ("Scale and cut-offs", "scale", "{{scale: rating scale, direction, cut-offs fixed before scoring}}", 3.7, 0.8, False),
            ("Decision", "decision", "{{decision: posture and money per unit, review date}}", 4.6, 1.3, True),
            ("Risks and limitations", "risk", "{{risk: what could invalidate the placement}}", 6.0, 1.1, False),
        ]
        for tag, key, hint, py, ph, accent in panels:
            box(sh, x, py, w, ph, fill=ACCENT_BG if accent else None, line=ACCENT if accent else LINE)
            label(sh, x + 0.06, py + 0.02, w - 0.12, 0.3, tag, size=11, bold=True, color=ACCENT)
            text(box(sh, x + 0.06, py + 0.3, w - 0.12, ph - 0.34, line=None), hint, size=10)


class UnitEconomics(XlsxSpec):
    @property
    def rel(self):
        return "business-analysis/unit-economics/unit-economics.xlsx"

    example = {"text": {
        "title": "FreshDrop, one order in Moscow, September 2026",
        "unit": "order",
        "period": "one order; the data comes from the finance report for August 2026",
        "decision": "scale the express slots in the two busiest districts; cut the courier bonus; check the margin per order in October",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Unit Economics"

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        thin = Side(style="thin", color="C9CED6")

        def note(cell, hint, height=100):
            return comment(cell, hint, height=height, width=280)

        ws["A1"] = "Unit Economics: {{title: business, what is being calculated, date}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:O1")
        top = [
            (2, "Unit:", "{{unit: unit of analysis: customer, order or item}}", bold, 32),
            (3, "Period:", "{{period: period length and data source}}", regular, 32),
            (4, "Decision:", "{{decision: decision taken and how we check it}}", regular, 46),
        ]
        for r, name, token, font, height in top:
            ws.cell(r, 1, name).font = muted
            c = ws.cell(r, 3, token)
            c.font = font
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.merge_cells(f"C{r}:O{r}")
            ws.row_dimensions[r].height = height

        headers = [
            ("Scenario", "What is being compared: a channel, a customer cohort, a period, a price or terms variant. One row is one scenario. "
                         "Do not average channels: an average CAC hides the unprofitable ones.", 30, False),
            ("Acquisition spend per period", "All spending to acquire customers in this scenario: advertising, salaries and "
                                                 "tools of marketing and sales. The ad budget alone understates CAC. In roubles or "
                                                 "another currency, the same for the whole table.", 18, False),
            ("New customers", "How many customers were acquired in the same period. Count those who made a first purchase, not visitors.", 12, False),
            ("Revenue per customer per period", "Average revenue per customer per period (ARPA, average revenue per account). "
                                             "If there is no lifetime period, use revenue for the observation window. Without VAT and after refunds.", 16, False),
            ("Contribution margin, %", "The share of revenue left after the unit's variable costs: cost of goods, delivery, "
                                "payment fees, support, refunds. Enter a share of one or a percentage: 0.2 or 20%.", 12, False),
            ("Churn per period, %", "The share of customers lost in the period. Empty if there is no churn data: then lifetime is taken from "
                                   "the \"Horizon\" column. The churn period must match the revenue period (month with month).", 12, False),
            ("Horizon, periods", "How many periods a customer is counted for if churn is unknown. Enter 1 if the revenue already covers the whole "
                                   "observation window. The horizon is your assumption, not a measurement: write where it comes from.", 12, False),
            ("Basis", "Where the numbers come from: a report, an export, a source page with a date. Mark here what is an estimate rather than a fact.", 30, False),
            ("CAC", "Customer acquisition cost: acquisition spend ÷ new customers. A formula, not entered by hand.", 11, True),
            ("Contribution per period", "Revenue per customer × contribution margin. How much one customer leaves after variable costs in a period.", 12, True),
            ("Lifetime, periods", "1 ÷ churn if it is above 0; otherwise the value from \"Horizon\". This is how David Skok calculates lifetime; "
                                     "constant churn is an assumption.", 12, True),
            ("LTV", "Contribution per period × lifetime. Margin version: revenue × margin ÷ churn. This is customer value by contribution, not by revenue.", 15, True),
            ("LTV/CAC", "LTV ÷ CAC. Skok's benchmark for SaaS is above 3 (in his version, without margin and at a margin of 80% or more). "
                        "Set the threshold yourself, it is in the cell on the right.", 11, True),
            ("CAC payback, periods", "CAC ÷ contribution per period: how many periods it takes a customer to repay the acquisition cost. "
                                          "Skok's benchmark for SaaS is 12 months or less, up to 20 for healthy models.", 13, True),
            ("Verdict", "A label based on the thresholds on the right; without thresholds, only \"does not pay back\" or \"pays back\". A signal to look closer, not a decision: the decision goes in the \"Decision\" row.", 24, True),
        ]
        hr = 6
        for i, (title, hint, width, calc) in enumerate(headers, start=1):
            c = ws.cell(hr, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            note(c, hint, 120)
            ws.column_dimensions[c.column_letter].width = width
        ws.row_dimensions[hr].height = 48

        first, last = hr + 1, hr + 30
        rng = lambda col: f"${col}${first}:${col}${last}"
        for r in range(first, last + 1):
            for c in range(1, 16):
                ws.cell(r, c).font = regular
                ws.cell(r, c).alignment = Alignment(wrap_text=True, vertical="top")
            f = {
                "I": f'=IF(AND(ISNUMBER(B{r}),ISNUMBER(C{r})),IF(C{r}>0,B{r}/C{r},""),"")',
                "J": f'=IF(AND(ISNUMBER(D{r}),ISNUMBER(E{r})),D{r}*E{r},"")',
                "K": f'=IF(AND(ISNUMBER(F{r}),F{r}>0),1/F{r},IF(ISNUMBER(G{r}),G{r},""))',
                "L": f'=IF(AND(ISNUMBER(J{r}),ISNUMBER(K{r})),J{r}*K{r},"")',
                "M": f'=IF(AND(ISNUMBER(L{r}),ISNUMBER(I{r})),IF(I{r}>0,L{r}/I{r},""),"")',
                "N": f'=IF(AND(ISNUMBER(I{r}),ISNUMBER(J{r})),IF(J{r}>0,I{r}/J{r},""),"")',
                "O": (f'=IF(A{r}="","",IF(NOT(ISNUMBER(M{r})),"no data",IF(M{r}<1,"does not pay back",'
                      f'IF(ISNUMBER($R$7),IF(M{r}>=$R$7,"LTV/CAC above threshold","LTV/CAC below threshold"),"pays back, LTV/CAC threshold not set")'
                      f'&IF(AND(ISNUMBER($R$8),ISNUMBER(N{r})),IF(N{r}<=$R$8,"; payback within threshold","; payback longer than threshold"),""))))'),
            }
            fmt = {"I": "#,##0.00", "J": "#,##0.00", "K": "0.0", "L": "#,##0.00", "M": "0.00", "N": "0.00"}
            for col, formula in f.items():
                cell = ws[f"{col}{r}"]
                cell.value = formula
                cell.fill = calc_fill
                if col in fmt:
                    cell.number_format = fmt[col]
            for col in "BD":
                ws[f"{col}{r}"].number_format = "#,##0.00"
            ws[f"C{r}"].number_format = "#,##0"
            for col in "EF":
                ws[f"{col}{r}"].number_format = "0.0%"
        ws.freeze_panes = ws.cell(first, 2)
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'Unit Economics'!$A${first}")

        pct = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True,
                             errorStyle="warning", showErrorMessage=True,
                             error="A share from 0 to 1: enter 0.2 or 20%.")
        pct.add(f"E{first}:F{last}")
        ws.add_data_validation(pct)
        pos = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                             errorStyle="warning", showErrorMessage=True, error="A number not less than zero is required.")
        pos.add(f"B{first}:D{last}")
        pos.add(f"G{first}:G{last}")
        ws.add_data_validation(pos)

        ws.column_dimensions["P"].width = 3
        ws.column_dimensions["Q"].width = 38
        ws.column_dimensions["R"].width = 14
        ws["Q6"] = "Thresholds and totals"
        ws["Q6"].font, ws["Q6"].fill = bold, head_fill
        ws["R6"].fill = head_fill
        items = [
            ("LTV/CAC threshold", None, "0.0", True,
             "Empty until you set a threshold. Set it before looking at the results: it depends on the industry, margin and risks. Skok's benchmark for SaaS is above 3."),
            ("Payback threshold, periods", None, "0", True,
             "Empty until you set a threshold. The period is the same as in the table. Skok's benchmark for SaaS is up to 12 months, up to 20 for healthy models."),
            ("Scenarios with a result", f"=SUMPRODUCT(--ISNUMBER({rng('M')}))", "0", False,
             "How many rows produced an LTV/CAC number."),
            ("Rows without a result", f'=SUMPRODUCT(({rng("A")}<>"")*(1-ISNUMBER({rng("M")})))', "0", False,
             "Scenarios with missing data. Should be 0, otherwise no conclusion can be drawn about them."),
            ("Above LTV/CAC threshold", f'=IF(ISNUMBER($R$7),SUMPRODUCT(ISNUMBER({rng("M")})*({rng("M")}>=$R$7)),"")', "0", False,
             "How many scenarios reached the LTV/CAC threshold."),
            ("Pay back within the threshold", f'=IF(ISNUMBER($R$8),SUMPRODUCT(ISNUMBER({rng("N")})*({rng("N")}<=$R$8)),"")', "0", False,
             "How many scenarios repaid the acquisition cost within the payback threshold or faster."),
            ("Best by LTV/CAC", f'=IF(R9=0,"",INDEX({rng("A")},MATCH(MAX({rng("M")}),{rng("M")},0)))', "General", False,
             "The scenario with the highest LTV/CAC. The best by ratio is not always the best by amount: look at total contribution too."),
        ]
        for i, (name, value, fmt, inp, hint) in enumerate(items, start=7):
            a = ws.cell(i, 17, name)
            a.font = regular
            note(a, hint, 90)
            b = ws.cell(i, 18, value)
            b.font = bold
            b.number_format = fmt
            b.fill = PatternFill("solid", fgColor="FFF7E0") if inp else calc_fill
            b.alignment = Alignment(wrap_text=True, vertical="top")


class ValueChainAndNets(PptxSpec):
    @property
    def rel(self):
        return "business-analysis/value-chain-and-nets/value-chain-and-nets.pptx"

    example = {"text": {
        "title": "FreshDrop, company level, value chain, September 2026",
        "sup_infra": "Dark-store leases: 6 sites",
        "sup_hr": "Pickers and couriers: 520 staff",
        "sup_tech": "App, routing and slot engine",
        "sup_proc": "Supplier contracts: 400 vendors",
        "n1": "Supplier buys",
        "n2": "Dark-store storage",
        "n3": "Picking",
        "n4": "Courier dispatch",
        "n5": "Delivery",
        "n6": "Returns and support",
        "r1": "Buys from 400 suppliers, 3 distributors",
        "r2": "Stores 1,800 SKUs in 6 dark stores",
        "r3": "Picks and checks an order in 6 min",
        "r4": "Routes couriers by slot and district",
        "r5": "Delivers in 30–120 min, one drop at a time",
        "r6": "Handles refunds and complaints in chat",
        "c1": "Purchases: 72% of revenue; 2 days lead",
        "c2": "Rent and staff: 4% of revenue",
        "c3": "Labour: 3% of revenue; 6 min per order",
        "c4": "Routing software: 0.5%; 4 min per order",
        "c5": "Courier pay: 11% of revenue; 28 min per drop",
        "c6": "Support: 1.2% of revenue; 1 min per chat",
        "s1": "Fresh, on-time stock in the app",
        "s2": "Items in stock: 92% fill rate",
        "s3": "Correct items, substitutions shown",
        "s4": "Slot shown and kept",
        "s5": "Courier on the map, delivered in the slot",
        "s6": "Refund within 24 hours",
        "margin": "order revenue 1,200 rub minus the costs of all links, 180 rub",
        "value": "Fresh groceries at store prices, delivered within 2 hours; app rating 4.7",
        "waste": "Picking mistakes and returns: 3% of orders; double handling in dark stores",
        "decision": "Add a barcode scan step to picking; move slow SKUs out of 2 dark stores",
        "check": "Error rate below 1.5% and margin 180 RUB per order by 1 December",
        "sources": "finance report August 2026, courier logs, supplier price lists",
    }}

    def draw(self, prs, slide):
        header(slide, "VALUE CHAIN & NETS · VALUE CHAIN AND VALUE NETS",
               "{{title: level, object and analysis date}}")
        S = slide.shapes

        # support activities (optional group)
        sup = S.add_group_shape()
        sup.name = "optional_support"
        sw, sg = 2.95, 0.177
        for i, (tag, key) in enumerate([("Firm infrastructure", "sup_infra"), ("Human resources", "sup_hr"),
                                        ("Technology", "sup_tech"), ("Procurement", "sup_proc")]):
            x = 0.5 + i * (sw + sg)
            box(sup.shapes, x, 1.2, sw, 0.64, fill=GOOD_BG, line=None)
            label(sup.shapes, x + 0.02, 1.2, sw - 0.04, 0.3, "Support: " + tag, size=8, color=GOOD)
            text(box(sup.shapes, x, 1.44, sw, 0.4, line=None), "{{%s: what it does}}" % key, size=9)

        # links
        opt = S.add_group_shape()
        opt.name = "optional_node_6"
        n, w, gap, x0 = 6, 1.9, 0.186, 0.5
        for i in range(n):
            x = x0 + i * (w + gap)
            k = i + 1
            sh = opt.shapes if i == 5 else S
            text(box(sh, x, 1.92, w, 0.55, fill=ACCENT_BG, line=ACCENT),
                 "{{n%d: link name}}" % k,
                 size=11, bold=True, color=ACCENT, anchor=MSO_ANCHOR.MIDDLE)
            if i < n - 1:
                box(opt.shapes if i == 4 else S, x + w + 0.02, 2.07, gap - 0.04, 0.24,
                    fill=ACCENT, line=None, kind=MSO_SHAPE.RIGHT_ARROW)
            for tag, key, hint, y in [("What it does", f"r{k}", "what the link does", 2.52),
                                      ("Cost and time", f"c{k}", "cost and time of the link", 3.27),
                                      ("What the customer sees", f"s{k}", "what the customer sees", 4.02)]:
                box(sh, x, y, w, 0.7)
                label(sh, x + 0.02, y, w - 0.04, 0.3, tag, size=8, color=MUTED)
                text(box(sh, x, y + 0.24, w, 0.46, line=None), "{{%s: %s}}" % (key, hint), size=10)

        # margin (optional)
        mg = S.add_group_shape()
        mg.name = "optional_margin"
        text(box(mg.shapes, 0.5, 4.78, 12.33, 0.32, fill=ACCENT_BG, line=None, kind=MSO_SHAPE.PENTAGON),
             "Margin: {{margin: output value minus link costs}}", size=10, bold=True,
             color=ACCENT, anchor=MSO_ANCHOR.MIDDLE)

        for x, pw, tag, key, hint, fill, color in [
            (0.5, 3.3, "Customer value", "value", "customer value and proof", ACCENT_BG, ACCENT),
            (3.95, 2.85, "Where value is not created", "waste", "where value is lost", BAD_BG, BAD),
            (6.95, 3.2, "Decision", "decision", "decision and next step", GOOD_BG, GOOD),
            (10.3, 2.53, "Check", "check", "check metric and target date", ACCENT_BG, ACCENT),
        ]:
            box(S, x, 5.2, pw, 1.3, fill=fill, line=None)
            label(S, x + 0.06, 5.2, pw - 0.12, 0.34, tag, size=12, bold=True, color=color)
            text(box(S, x + 0.06, 5.52, pw - 0.12, 0.96, line=None), "{{%s: %s}}" % (key, hint), size=9)

        label(S, 0.5, 6.55, 12.33, 0.3, "{{sources: where the data on the links comes from}}", size=9, color=INK)


class AnsoffMatrix(PptxSpec):
    @property
    def rel(self):
        return "business-analysis/ansoff-matrix/ansoff-matrix.pptx"

    example = {"text": {
        "title": "Amazon, grocery: Whole Foods Market deal, June 2017",
        "pen": "N/A: the press release gives no figures on Amazon's existing grocery sales",
        "dev_p": "N/A: not described in the press release",
        "dev_m": "N/A: not described in the press release",
        "div": "Buy Whole Foods Market, a natural and organic grocery chain: about $16 billion sales in fiscal 2016, 460+ stores in the US, Canada and the UK. $42 per share in cash, about $13.7 billion with net debt",
        "choice": "Diversification: the release does not name the matrix, the quadrant is our reading",
        "decision": "16 June 2017: agreement to acquire. Whole Foods keeps its brand, John Mackey stays CEO, headquarters stay in Austin. Closing expected in the second half of 2017 after shareholder and regulatory approval",
    }}

    def draw(self, prs, slide):
        header(slide, "ANSOFF MATRIX · PRODUCT-MARKET GROWTH GRID",
               "{{title: company, business, planning horizon}}")
        sh = slide.shapes
        left, top = 0.5, 1.3
        lw, cw, hh, rh, g = 1.3, 3.65, 0.45, 2.4, 0.08
        for j, name in enumerate(["Existing products", "New products"]):
            text(box(sh, left + lw + g + j * (cw + g), top, cw, hh, fill=INK, line=None),
                 name, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        for i, name in enumerate(["Existing markets", "New markets"]):
            text(box(sh, left, top + hh + g + i * (rh + g), lw, rh, fill=INK, line=None),
                 name, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        cells = [
            ("Market penetration", "pen", "{{pen: how to sell more of existing products to existing customers}}", ACCENT_BG),
            ("Product development", "dev_p", "{{dev_p: new products for existing customers}}", WHITE),
            ("Market development", "dev_m", "{{dev_m: existing products for new segments, regions or channels}}", WHITE),
            ("Diversification", "div", "{{div: new products for new markets}}", WHITE),
        ]
        for k, (tag, key, hint, fill) in enumerate(cells):
            i, j = divmod(k, 2)
            x = left + lw + g + j * (cw + g)
            y = top + hh + g + i * (rh + g)
            tb = text(box(sh, x, y, cw, rh, fill=fill), hint, size=11)
            tb.text_frame.margin_top = Inches(0.4)
            label(sh, x + 0.08, y + 0.04, cw - 0.16, 0.32, tag, size=12, bold=True, color=ACCENT)
        label(sh, left + lw + g, top + hh + 2 * rh + 2 * g + 0.05, 2 * cw + g, 0.3,
              "Risk grows from the top left to the bottom right", size=10, color=MUTED)
        x, w = 9.55, 3.28
        for tag, hint, y, h, fill, line in [
            ("Chosen direction", "{{choice: quadrant chosen and why}}", 1.3, 2.3, ACCENT_BG, ACCENT),
            ("Decision", "{{decision: what was decided, owner, date, check}}", 3.7, 3.4, WHITE, LINE),
        ]:
            tb = text(box(sh, x, y, w, h, fill=fill, line=line), hint, size=11)
            tb.text_frame.margin_top = Inches(0.4)
            label(sh, x + 0.08, y + 0.04, w - 0.16, 0.32, tag, size=12, bold=True, color=INK)
