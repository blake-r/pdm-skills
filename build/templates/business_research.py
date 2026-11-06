from .base import *


class GartnersHypeCycle(PptxSpec):
    @property
    def rel(self):
        return "business-research/gartners-hype-cycle/gartners-hype-cycle.pptx"

    example = {"text": {
        "title": "Grocery delivery technologies, October 2026",
        "phase1": "Robot couriers: over 10 years",
        "phase2": "15-minute delivery: 2–5 years",
        "phase3": "Drone drops: 5–10 years",
        "phase4": "Cold-chain sensors: 2–5 years",
        "phase5": "Online grocery ordering",
    }}

    def draw(self, prs, slide):
        import math
        from pptx.enum.dml import MSO_LINE_DASH_STYLE
        from pptx.enum.shapes import MSO_CONNECTOR
        header(slide, "GARTNER HYPE CYCLE", "{{title: area, assessment date}}")
        sh = slide.shapes
        cx, cy, cw, chh = 0.9, 1.35, 11.9, 3.05  # chart area

        def line(x1, y1, x2, y2, color=LINE, width=1.0, dash=None):
            return connector(sh, (x1, y1), (x2, y2), color=color, width=width, dash=dash)

        def curve(t):  # expectations 0..1 over time 0..1: peak, trough, slope, plateau
            return 0.93 * math.exp(-((t - 0.24) / 0.075) ** 2) + 0.5 / (1 + math.exp(-(t - 0.6) / 0.07)) + 0.03

        pts = [(cx + t * cw, cy + chh - curve(t) * chh) for t in (i / 200 for i in range(201))]
        ff = sh.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
        ff.add_line_segments([(Inches(x), Inches(y)) for x, y in pts[1:]], close=False)
        c = ff.convert_to_shape()
        c.fill.background()
        c.line.color.rgb, c.line.width = ACCENT, Pt(3)
        c.shadow.inherit = False
        line(cx, cy + chh, cx + cw, cy + chh, color=INK, width=1.25)
        line(cx, cy - 0.05, cx, cy + chh, color=INK, width=1.25)
        ax = label(sh, 0.05, cy + chh / 2 - 0.15, 1.2, 0.3, "Expectations →", size=9, color=MUTED, align=PP_ALIGN.CENTER)
        ax.rotation = -90
        label(sh, cx + cw - 1.0, cy + chh + 0.02, 1.0, 0.28, "Time →", size=9, color=MUTED, align=PP_ALIGN.RIGHT)
        bounds = [0, 0.16, 0.34, 0.49, 0.75, 1]
        for b in bounds[1:-1]:
            line(cx + b * cw, cy, cx + b * cw, cy + chh, dash=MSO_LINE_DASH_STYLE.DASH)
        phases = [
            ("1 · Innovation trigger", "phase1"),
            ("2 · Peak of inflated expectations", "phase2"),
            ("3 · Trough of disillusionment", "phase3"),
            ("4 · Slope of enlightenment", "phase4"),
            ("5 · Plateau of productivity", "phase5"),
        ]
        ly = cy + chh + 0.25
        for (a, b), (tag, key) in zip(zip(bounds, bounds[1:]), phases):
            x, w = cx + a * cw, (b - a) * cw
            label(sh, x, ly, w, 0.46, tag, size=10, bold=True, color=ACCENT, anchor=MSO_ANCHOR.BOTTOM)
            tb = text(box(sh, x + 0.03, ly + 0.5, w - 0.06, 1.8, fill=ACCENT_BG, line=None),
                      f"{{{{{key}: technology (years to plateau)}}}}", size=9)
            tb.text_frame.paragraphs[0].space_after = Pt(2)
        label(sh, cx, 7.08, cw, 0.3,
              "Years to plateau: under 2 · 2–5 · 5–10 · over 10 · obsolete before plateau",
              size=9, color=MUTED)


class TamSamSomModel(PptxSpec):
    @property
    def rel(self):
        return "business-research/tam-sam-som-model/tam-sam-som-model.pptx"

    example = {"text": {
        "title": "FreshDrop, grocery delivery in 15 Russian cities, 2026",
        "tam": "14 M households",
        "sam": "4.2 M households",
        "som": "180 000 households",
        "tam_how": "all households that buy groceries weekly: Rosstat 2025 survey, 14 M",
        "sam_how": "households in 15 cities with an app-based delivery option: 4.2 M",
        "som_how": "4% of the SAM in 2 years, given 6 dark stores and 3 rivals",
        "sources": "Rosstat 2025; Data Insight e-commerce report 2026. Assumption: 4% share of SAM in 2 years",
    }}

    def draw(self, prs, slide):
        header(slide, "TAM / SAM / SOM · MARKET SIZE", "{{title: product, market, year}}")
        sh = slide.shapes
        # nested circles share the bottom point, as in the classic diagram
        cxm, bottom = 3.45, 7.05
        levels = [
            ("TAM", "tam", 5.6, ACCENT_BG, INK, "Total market"),
            ("SAM", "sam", 3.75, RGBColor(0xB9, 0xCF, 0xF5), INK, "Available market"),
            ("SOM", "som", 1.95, ACCENT, WHITE, "Obtainable share"),
        ]
        for tag, key, d, fill, color, name in levels:
            box(sh, cxm - d / 2, bottom - d, d, d, fill=fill, line=WHITE, kind=MSO_SHAPE.OVAL)
        for i, (tag, key, d, fill, color, name) in enumerate(levels):
            y = bottom - d + (0.3 if i < 2 else 0.45)
            w = min(2.8, d - 0.3)
            label(sh, cxm - w / 2, y, w, 0.4, tag, size=16 if i < 2 else 14, bold=True, color=color, align=PP_ALIGN.CENTER)
            label(sh, cxm - w / 2, y + 0.4, w, 0.55, f"{{{{{key}: size and unit}}}}", size=12 if i < 2 else 11, bold=True,
                  color=color, align=PP_ALIGN.CENTER)
        rx, rw = 6.75, 6.08
        rows = [
            ("TAM · Total Addressable Market", "tam_how", "market definition and counting basis"),
            ("SAM · Serviceable Available Market", "sam_how", "geography, segments and channels served"),
            ("SOM · Serviceable Obtainable Market", "som_how", "realistic share and its basis"),
        ]
        y, rh = 1.35, 1.3
        for (tag, key, hint), (_, _, _, fill, _, _) in zip(rows, levels):
            box(sh, rx, y, 0.12, rh, fill=fill if fill != ACCENT_BG else RGBColor(0xD6, 0xE3, 0xFA), line=None)
            label(sh, rx + 0.2, y, rw - 0.2, 0.32, tag, size=11, bold=True, color=ACCENT)
            tb = text(box(sh, rx + 0.2, y + 0.34, rw - 0.2, rh - 0.34, line=None), f"{{{{{key}: {hint}}}}}", size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(2)
            y += rh + 0.1
        label(sh, rx, y, rw, 0.36, "Sources and assumptions", size=11, bold=True, color=INK)
        tb = text(box(sh, rx, y + 0.38, rw, 7.05 - y - 0.38, fill=ACCENT_BG, line=None),
                  "{{sources: data sources and main assumptions}}", size=9)
        tb.text_frame.paragraphs[0].space_after = Pt(2)


class StrategyCanvas(PptxSpec):
    @property
    def rel(self):
        return "business-research/strategy-canvas/strategy-canvas.pptx"

    example = {
        "text": {
            "title": "Grocery delivery in Moscow: FreshDrop vs supermarkets and Kuper",
            "factors": "Delivery speed: hours to the door. Price: total basket cost. Stock: items on offer",
            "moves": "Eliminate: slot picker. Reduce: delivery fee. Raise: live stock accuracy. Create: 1-hour express slots",
        },
        "charts": {"canvas": {
            "categories": ["Delivery speed", "Price", "Stock range", "Slot choice", "Support", "App ease"],
            "series": [
                {"name": "Our offering", "values": [4, 1, 5, 2, 4, 1]},
                {"name": "Supermarket delivery", "values": [2, 4, 2, 4, 2, 4]},
                {"name": "Kuper", "values": [3, 3, 3, 3, 3, 3]},
            ],
        }},
    }

    def draw(self, prs, slide):
        from pptx.enum.chart import XL_LEGEND_POSITION
        header(slide, "STRATEGY CANVAS", "{{title: the market and the offerings compared}}")
        sh = slide.shapes
        data = CategoryChartData()
        data.categories = ["Factor 1", "Factor 2", "Factor 3", "Factor 4", "Factor 5", "Factor 6"]
        data.add_series("Our offering", (4, 1, 5, 2, 4, 1))
        data.add_series("Competitor X", (2, 4, 2, 4, 2, 4))
        data.add_series("Competitor Y", (3, 3, 3, 3, 3, 3))
        gf = sh.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.5), Inches(1.3), Inches(8.6), Inches(5.8), data)
        gf.name = "canvas"
        ch = gf.chart
        ch.has_legend = True
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
        ch.legend.font.size, ch.legend.font.name = Pt(10), FONT
        va = ch.value_axis
        va.minimum_scale, va.maximum_scale, va.major_unit = 0, 5, 1
        va.has_major_gridlines = True
        va.major_gridlines.format.line.color.rgb = LINE
        va.tick_labels.font.size, va.tick_labels.font.name = Pt(9), FONT
        va.has_title = True
        va.axis_title.text_frame.text = "Offering level: 0 — none, 5 — high"
        va.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(9)
        ca = ch.category_axis
        ca.tick_labels.font.size, ca.tick_labels.font.name = Pt(9), FONT
        from pptx.oxml.ns import qn

        # show every factor name: let long names wrap instead of being skipped
        skip = ca._element.makeelement(qn("c:tickLblSkip"), {"val": "1"})
        nml = ca._element.find(qn("c:noMultiLvlLbl"))
        nml.addprevious(skip) if nml is not None else ca._element.append(skip)
        for ser, color, width in zip(ch.plots[0].series, [ACCENT, MUTED, RGBColor(0xE0, 0x8A, 0x2E)], [3, 2, 2]):
            ser.smooth = False
            ser.format.line.color.rgb = color
            ser.format.line.width = Pt(width)
            ser.marker.style = XL_MARKER_STYLE.CIRCLE
            ser.marker.size = 8
            ser.marker.format.fill.solid()
            ser.marker.format.fill.fore_color.rgb = color
            ser.marker.format.line.color.rgb = color
        rx, rw = 9.35, 3.48
        label(sh, rx, 1.35, rw, 0.32, "Competitive factors", size=11, bold=True, color=ACCENT)
        tb = text(box(sh, rx, 1.7, rw, 2.35, fill=ACCENT_BG, line=None),
                  "{{factors: factor and what it means}}", size=9)
        tb.text_frame.paragraphs[0].space_after = Pt(2)
        label(sh, rx, 4.2, rw, 0.32, "Where the curves diverge", size=11, bold=True, color=ACCENT)
        tb = text(box(sh, rx, 4.55, rw, 2.55, fill=WHITE), "{{moves: eliminate, reduce, raise, create}}", size=9)
        tb.text_frame.paragraphs[0].space_after = Pt(2)


class CompetitionMap(PptxSpec):
    @property
    def rel(self):
        return "business-research/competition-map/competition-map.pptx"

    example = {"text": {
        "title": "FreshDrop: weekly grocery order in Moscow",
        "direct": "Overlap: 62% of buyers use both",
        "direct_note": "Overlap: 62% of buyers use both",
        "indirect": "Supermarket online: weekly slots",
        "indirect_note": "Supermarket online: weekly slots",
        "displace": "Meal kits take 40% of the food budget",
        "displace_note": "Meal kits take 40% of the food budget",
        "channel": "Telegram, Instagram: 30% of installs",
        "channel_note": "Telegram, Instagram: 30% of installs",
        "steps": "Order, pay, delivery in 2 hours",
        "insight": "Search: Kuper wins. Delivery: we win on time. Next: fix the slot picker",
    }}

    def draw(self, prs, slide):
        from pptx.enum.shapes import MSO_CONNECTOR
        header(slide, "COMPETITION MAP", "{{title: product and the key scenario}}")
        sh = slide.shapes
        cx, cy, R, r = 6.67, 4.2, 2.9, 1.2
        box(sh, cx - R, cy - R, 2 * R, 2 * R, fill=ACCENT_BG, line=LINE, kind=MSO_SHAPE.OVAL)
        for x1, y1, x2, y2 in ((cx - R, cy, cx + R, cy), (cx, cy - R, cx, cy + R)):
            c = sh.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
            c.line.color.rgb, c.line.width = WHITE, Pt(3)
        # quadrants: top-left, top-right, bottom-right, bottom-left
        quads = [
            ("Direct", "direct", "competitors, same solution", -1, -1),
            ("Indirect", "indirect", "other ways to solve it", 1, -1),
            ("Displacers", "displace", "products for wallet and time", 1, 1),
            ("Channel", "channel", "channels to reach customers", -1, 1),
        ]
        dx, dy, w, h = 1.6, 1.5, 1.9, 1.1
        for name, key, hint, sx, sy in quads:
            tb = text(box(sh, cx + sx * dx - w / 2, cy + sy * dy - h / 2, w, h, line=None), f"{{{{{key}: {hint}}}}}",
                      size=9, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            tb.text_frame.paragraphs[0].space_after = Pt(1)
            align = PP_ALIGN.RIGHT if sx < 0 else PP_ALIGN.LEFT
            lx = cx - R - 3.0 if sx < 0 else cx + R + 0.15
            ly = cy - 2.2 if sy < 0 else cy + 0.35
            label(sh, lx, ly, 2.85, 0.4, name, size=12, bold=True, color=ACCENT, align=align)
            label(sh, lx, ly + 0.38, 2.85, 0.32, f"{{{{{key}_note: short note}}}}", size=9, color=MUTED, align=align)
        text(box(sh, cx - r, cy - r, 2 * r, 2 * r, fill=ACCENT, line=WHITE, kind=MSO_SHAPE.OVAL),
             "{{steps: steps of the key scenario}}", size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
        label(sh, cx + R + 0.15, cy + 1.2, 2.85, 0.32, "Takeaway", size=11, bold=True, color=INK)
        text(box(sh, cx + R + 0.15, cy + 1.55, 3.0, 7.1 - cy - 1.55, fill=WHITE),
             "{{insight: main competitor at each step and our move}}", size=9)


class CompetitorAnalysis(XlsxSpec):
    @property
    def rel(self):
        return "business-research/competitor-analysis-template/competitor-analysis-template.xlsx"

    example = {"text": {
        "title": "QuickBasket, grocery delivery, Moscow, 1 September 2026",
        "decision": "compete on slot reliability in the same districts; do not match their price on the premium range",
        "kind": "direct: same buyers, same delivery time, same districts",
        "conclusion": "strong on range and price; weak on slot reliability and app ratings (3.9); their support does not answer at night; our place is reliability",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Competitor Analysis"
        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        sec_fill = PatternFill("solid", fgColor="F3F4F6")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        thin = Side(style="thin", color="C9CED6")

        def note(cell, hint, height=90):
            return comment(cell, hint, height=height, width=260)

        ws["A1"] = "Competitor Analysis: Competitor: {{title: competitor, market and analysis date}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:E1")
        top = [
            (2, "Decision:", "{{decision: decision this analysis prepares}}"),
            (3, "Competitor type:", "{{kind: competitor type and why}}"),
            (4, "Conclusion:", "{{conclusion: strengths and weaknesses, where our place is}}"),
        ]
        for r, name, token in top:
            ws.cell(r, 1, name).font = muted
            c = ws.cell(r, 3, token)
            c.font = regular
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.merge_cells(f"C{r}:E{r}")
            ws.row_dimensions[r].height = 48

        headers = [
            ("Block", "Section of the competitor analysis template from the PAF description. Blocks can be removed or added to fit the market.", 22),
            ("Parameter", "What to find out about the competitor. A hint for each parameter is in the cell note.", 32),
            ("Data", "What is established about the competitor. Do not invent what is unavailable: leave it empty and mark it \"no data\".", 52),
            ("Source and date", "Where the data comes from: link, document, interview, and when obtained. Without a source the value cannot be checked.", 36),
            ("Confidence", "fact: confirmed by a source; estimate: your own calculation or inference, write the reasoning in the data; no data: nothing found.", 14),
        ]
        hr = 6
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(hr, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            note(c, hint, 100)
            ws.column_dimensions[c.column_letter].width = width
        ws.row_dimensions[hr].height = 30

        r = hr + 1
        first = r
        for section, params in SECTIONS:
            for k, (name, hint) in enumerate(params):
                a = ws.cell(r, 1, section if k == 0 else None)
                a.font = bold
                b = ws.cell(r, 2, name)
                b.font = regular
                note(b, hint, 70)
                for col in range(1, 6):
                    ws.cell(r, col).alignment = Alignment(wrap_text=True, vertical="top")
                    if k == 0:
                        ws.cell(r, col).fill = sec_fill
                    if col > 2:
                        ws.cell(r, col).font = regular
                r += 1
        last = r - 1
        ws.freeze_panes = ws.cell(first, 3)
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'Competitor Analysis'!$C${first}")

        dv = DataValidation(type="list", formula1='"fact,estimate,no data"', allow_blank=True, errorStyle="warning",
                            showErrorMessage=True, error="Values: fact, estimate, no data")
        dv.add(f"E{first}:E{last}")
        ws.add_data_validation(dv)

        rng = lambda col: f"${col}${first}:${col}${last}"
        ws["G6"] = "Totals"
        ws["G6"].font, ws["G6"].fill = bold, head_fill
        ws["H6"].fill = head_fill
        ws.column_dimensions["F"].width = 3
        ws.column_dimensions["G"].width = 34
        ws.column_dimensions["H"].width = 12
        stats = [
            ("Parameters", f'=COUNTA({rng("B")})', "0", "How many parameters are in the table."),
            ("Filled", f'=COUNTIF({rng("E")},"fact")+COUNTIF({rng("E")},"estimate")', "0",
             "Parameters marked \"fact\" or \"estimate\". A row marked \"no data\" does not count as filled."),
            ("Filled without a source", f'=SUMPRODUCT((({rng("E")}="fact")+({rng("E")}="estimate"))*({rng("D")}=""))', "0",
             "Parameters marked \"fact\" or \"estimate\" without a source and date. Must be 0: the value cannot be checked."),
            ("Estimates", f'=COUNTIF({rng("E")},"estimate")', "0", "Values you estimated rather than found."),
            ("No data", f'=COUNTIF({rng("E")},"no data")', "0", "Honest gaps: only facts found are better than these."),
            ("Without a confidence mark", f'=SUMPRODUCT(({rng("C")}<>"")*({rng("E")}=""))', "0",
             "Rows with text in \"Data\" but without a fact/estimate/no data mark. Must be 0."),
            ("Share filled", '=IF(H7=0,"",H8/H7)', "0%",
             "Filled divided by parameters. Not a measure of analysis quality: empty blocks can be removed to fit the context."),
        ]
        for i, (name, formula, fmt, hint) in enumerate(stats, start=7):
            a = ws.cell(i, 7, name)
            a.font = regular
            note(a, hint, 80)
            b = ws.cell(i, 8, formula)
            b.font, b.fill = bold, calc_fill
            b.number_format = fmt


        for sec, ps in SECTIONS:
            pass


class PestelAnalysis(PptxSpec):
    @property
    def rel(self):
        return "business-research/pestel-analysis/pestel-analysis.pptx"

    example = {"text": {
        "title": "Grocery delivery, Russia, 2026–2028",
        "p": "courier rules: from 1 March 2026 couriers need a registered contract; source: ministry notice, 14 January 2026",
        "e": "real incomes up 3% in 2026; key rate 14% to 13% by September 2026 (central bank data)",
        "s": "58% of Moscow households order food online at least once a month (survey, May 2026)",
        "t": "courier route app updated in Q2 2026; personal data rules for orders tightened in 2026",
        "env": "packaging fee for plastic bags from 2027; not yet in our plans",
        "l": "consumer protection on refunds; licence for alcohol delivery needed",
        "threats": "courier costs rise with the new contract rules; the alcohol licence delays the launch",
        "opportunities": "more households order online; the rate cut lowers the loan cost for the courier fleet",
        "decision": "start the courier contract change in Q4; apply for the alcohol licence in Q1 2027; revisit when the key rate passes 12%",
    }}

    def draw(self, prs, slide):
        header(slide, "PESTEL ANALYSIS · EXTERNAL ENVIRONMENT ANALYSIS",
               "{{title: subject, country, horizon}}")
        blocks = [
            ("P · Political", "{{p: government and political facts}}"),
            ("E · Economic", "{{e: growth, rates, incomes and prices}}"),
            ("S · Sociocultural", "{{s: demographics, habits and trust}}"),
            ("T · Technological", "{{t: technologies, standards and threats}}"),
            ("E · Environmental", "{{env: climate and ESG requirements}}"),
            ("L · Legal", "{{l: laws, licences and data protection}}"),
        ]
        w, h, gx, gy = 4.0, 1.85, 0.15, 0.12
        for i, (tag, token) in enumerate(blocks):
            x = 0.5 + (i % 3) * (w + gx)
            y = 1.3 + (i // 3) * (h + gy)
            text(box(slide.shapes, x, y, w, 0.34, fill=ACCENT_BG, line=None), tag, size=12, bold=True,
                 color=ACCENT, anchor=MSO_ANCHOR.MIDDLE)
            text(box(slide.shapes, x, y + 0.34, w, h - 0.34), token, size=11)
        y0 = 1.3 + 2 * (h + gy) + 0.08
        h2 = 7.3 - y0
        panels = [
            ("Threats", "{{threats: facts that harm, and how}}", BAD, BAD_BG),
            ("Opportunities", "{{opportunities: facts that open something, and how}}", GOOD, GOOD_BG),
            ("Decision", "{{decision: decision, owner, date and trigger to revisit}}", INK, None),
        ]
        for i, (tag, token, color, bg) in enumerate(panels):
            x = 0.5 + i * (w + gx)
            text(box(slide.shapes, x, y0, w, 0.32, fill=color, line=None), tag, size=12, bold=True,
                 color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            text(box(slide.shapes, x, y0 + 0.32, w, h2 - 0.32, fill=bg), token, size=11)


class PortersFiveForces(PptxSpec):
    @property
    def rel(self):
        return "business-research/porters-five-forces/porters-five-forces.pptx"

    example = {"text": {
        "title": "Grocery delivery, Moscow, analysis date 1 September 2026",
        "entrants_level": "Medium: 2 new chains in 2025",
        "entrants": "Entry needs 15–20 dark stores (about 60 M RUB) and a courier base; capital is the main barrier",
        "suppliers_level": "Medium: 3 distributors hold 60% of fresh goods",
        "suppliers": "About 400 suppliers; switching cost is low for dry goods and high for fresh; supply is 70% of costs",
        "rivalry_level": "Strong: 7 apps compete on 30-minute delivery",
        "rivalry": "Price wars in promos; the market grows 25% a year; fixed dark-store costs make exit expensive",
        "buyers_level": "Strong: buyers switch apps for a 200 RUB promo",
        "buyers": "Buyers aged 25–45; switching cost is low; 1 in 3 uses two apps",
        "substitutes_level": "Medium: store chains with their own delivery",
        "substitutes": "Supermarket delivery and restaurants for quick meals; switching cost is low, price gap about 10%",
        "verdict": "Attractive for a niche: rivalry limits profit the most",
        "dynamics": "More chains enter the same districts; courier pay rules may tighten in 2027",
        "sources": "Market reports 2026, app store data, 6 interviews with couriers and store managers",
        "decision": "Enter only 3 districts with weekly boxes; defend against rivalry with fixed slots",
    }}

    def draw(self, prs, slide):
        header(slide, "PORTER'S FIVE FORCES",
               "{{title: industry, boundaries and analysis date}}")
        sh = slide.shapes

        def force(x, y, w, h, tag, lvl_key, facts_key, lvl_hint, facts_hint, color=ACCENT, fill=None):
            box(sh, x, y, w, h, fill=fill, line=color)
            label(sh, x + 0.06, y + 0.02, w - 0.12, 0.36, tag, size=12, bold=True, color=color)
            label(sh, x + 0.06, y + 0.36, w - 0.12, 0.28, "{{%s: %s}}" % (lvl_key, lvl_hint),
                  size=9, bold=True, color=INK)
            tb = text(box(sh, x + 0.06, y + 0.64, w - 0.12, h - 0.7, line=None),
                      "{{%s: %s}}" % (facts_key, facts_hint), size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(3)

        force(4.55, 1.3, 4.25, 1.4, "Threat of new entrants", "entrants_level", "entrants",
              "level and key figure",
              "facts behind the level")
        force(0.5, 2.85, 3.9, 1.95, "Bargaining power of suppliers", "suppliers_level", "suppliers",
              "level and key figure",
              "facts behind the level")
        force(4.55, 2.85, 4.25, 1.95, "Rivalry among players", "rivalry_level", "rivalry",
              "level and key figure",
              "facts behind the level",
              color=BAD, fill=BAD_BG)
        force(8.9, 2.85, 3.93, 1.95, "Bargaining power of buyers", "buyers_level", "buyers",
              "level and key figure",
              "facts behind the level")
        force(4.55, 4.95, 4.25, 1.4, "Threat of substitutes", "substitutes_level", "substitutes",
              "level and key figure",
              "facts behind the level")

        for x, y, w, h, tag, key, hint in (
            (0.5, 1.3, 3.9, 3.0 - 0.0 - 1.6, "Industry verdict", "verdict",
             "overall verdict on the industry"),
            (8.9, 1.3, 3.93, 1.4, "Dynamics", "dynamics",
             "trends that change the forces"),
            (0.5, 4.95, 3.9, 1.4, "Sources of facts", "sources",
             "where the facts come from"),
            (8.9, 4.95, 3.93, 1.4, "Decision", "decision",
             "entry decision and the defence"),
        ):
            box(sh, x, y, w, h, fill=ACCENT_BG, line=None)
            label(sh, x + 0.06, y + 0.04, w - 0.12, 0.32, tag, size=12, bold=True, color=ACCENT)
            tb = text(box(sh, x + 0.06, y + 0.38, w - 0.12, h - 0.42, line=None), "{{%s: %s}}" % (key, hint), size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(3)
