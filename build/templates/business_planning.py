from .base import *


class BusinessModelCanvas(PptxSpec):
    @property
    def rel(self):
        return "business-planning/business-model-canvas/business-model-canvas.pptx"

    example = {"text": {
        "title": "FreshDrop business model, September 2026",
        "partners": "local farms and a courier fleet partner; produce at cost",
        "activities": "picking and packing, route planning, quality checks",
        "resources": "dark stores in 6 districts, courier app, stock data",
        "value": "a full weekly grocery list in 2 hours, with live stock",
        "relationships": "weekly reminder, personal substitutes chat, loyalty points",
        "channels": "app search and referral codes; order in app; delivery to the door",
        "segments": "busy families in new districts, aged 30–40",
        "costs": "courier pay 38%, dark-store rent 22%, marketing 12% of revenue",
        "revenues": "basket fee per order, delivery fee below 1 500 ₽, card payment",
    }}

    def draw(self, prs, slide):
        header(slide, "BUSINESS MODEL CANVAS", "{{title: company or product, date}}")
        sh = slide.shapes
        # Osterwalder's layout: five columns on top, costs and revenues below
        x0, y0, w, h = 0.5, 1.25, 12.33, 5.95
        cw, th = w / 5, 4.15
        bh = h - th

        def block(x, y, bw, bh, tag, key, hint, fill=WHITE):
            tb = text(box(sh, x, y, bw, bh, fill=fill), f"{{{{{key}: {hint}}}}}", size=9)
            tb.text_frame.margin_top = Inches(0.34)
            tb.text_frame.paragraphs[0].space_after = Pt(2)
            label(sh, x + 0.06, y + 0.04, bw - 0.12, 0.28, tag, size=10, bold=True, color=INK)

        block(x0, y0, cw, th, "Key partners", "partners", "partners and what we get from them")
        block(x0 + cw, y0, cw, th / 2, "Key activities", "activities", "what we do to make the model work")
        block(x0 + cw, y0 + th / 2, cw, th / 2, "Key resources", "resources", "key resources the model depends on")
        block(x0 + 2 * cw, y0, cw, th, "Value proposition", "value",
              "customer problem solved and offer", fill=ACCENT_BG)
        block(x0 + 3 * cw, y0, cw, th / 2, "Customer relationships", "relationships", "how we attract and retain customers")
        block(x0 + 3 * cw, y0 + th / 2, cw, th / 2, "Channels", "channels", "how customers find, buy and receive")
        block(x0 + 4 * cw, y0, cw, th, "Customer segments", "segments", "customer groups we create value for")
        block(x0, y0 + th, w / 2, bh, "Cost structure", "costs", "the main cost items")
        block(x0 + w / 2, y0 + th, w / 2, bh, "Revenue streams", "revenues", "what and how customers pay")


class LeanCanvas(PptxSpec):
    @property
    def rel(self):
        return "business-planning/lean-canvas/lean-canvas.pptx"

    example = {"text": {
        "title": "FreshDrop, 10 September 2026, v3",
        "problem": "no time to shop; missing items; late couriers",
        "alternatives": "supermarket visits, or supermarket delivery slots booked a day ahead",
        "solution": "weekly list in the app; live stock picking; 2-hour slots",
        "metrics": "weekly orders per buyer; on-time rate; repeat rate in week 4",
        "uvp": "groceries in 2 hours, every item in stock",
        "concept": "a supermarket in your pocket",
        "advantage": "own dark-store network and two years of stock data",
        "channels": "referral codes, metro posters, Telegram ads",
        "segments": "busy families in new districts",
        "early_adopters": "parents with 2+ children and no car",
        "costs": "dark stores 40 M, couriers 25 M, marketing 15 M a year",
        "revenues": "12% margin on goods, delivery fee below 1 500 ₽",
    }}

    def draw(self, prs, slide):
        header(slide, "LEAN CANVAS", "{{title: product, date, version}}")
        sh = slide.shapes
        # Ash Maurya's layout: five columns on top, costs and revenues below
        x0, y0, w, h = 0.5, 1.25, 12.33, 5.95
        cw, th = w / 5, 4.15
        bh = h - th

        def block(x, y, bw, bh, tag, key, hint, fill=WHITE, sub=None):
            tb = text(box(sh, x, y, bw, bh, fill=fill), f"{{{{{key}: {hint}}}}}", size=9)
            tb.text_frame.margin_top = Inches(0.34)
            tb.text_frame.paragraphs[0].space_after = Pt(2)
            label(sh, x + 0.06, y + 0.04, bw - 0.12, 0.28, tag, size=10, bold=True, color=INK)
            if sub:  # secondary field in the lower part of the block, as on the original canvas
                skey, stag, shint = sub
                sy = y + bh * 0.62
                label(sh, x + 0.06, sy, bw - 0.12, 0.26, stag, size=9, bold=True, color=MUTED)
                st = text(box(sh, x + 0.02, sy + 0.26, bw - 0.04, bh * 0.38 - 0.3, line=None),
                          f"{{{{{skey}: {shint}}}}}", size=9)
                st.text_frame.paragraphs[0].space_after = Pt(2)

        block(x0, y0, cw, th, "Problem", "problem", "the three main problems",
              sub=("alternatives", "Existing alternatives", "how the problem is solved today"))
        block(x0 + cw, y0, cw, th / 2, "Solution", "solution", "one solution per problem")
        block(x0 + cw, y0 + th / 2, cw, th / 2, "Key metrics", "metrics", "key numbers that show the model works")
        block(x0 + 2 * cw, y0, cw, th, "Unique value proposition", "uvp",
              "one phrase: how we differ and why to buy", fill=ACCENT_BG,
              sub=("concept", "High-level concept", "high-level concept in one phrase"))
        block(x0 + 3 * cw, y0, cw, th / 2, "Unfair advantage", "advantage", "what cannot be quickly copied or bought")
        block(x0 + 3 * cw, y0 + th / 2, cw, th / 2, "Channels", "channels", "the path to customers")
        block(x0 + 4 * cw, y0, cw, th, "Customer segments", "segments", "target customer groups",
              sub=("early_adopters", "Early adopters", "who feels the problem most acutely"))
        block(x0, y0 + th, w / 2, bh, "Cost structure", "costs", "costs of launch and operation")
        block(x0 + w / 2, y0 + th, w / 2, bh, "Revenue streams", "revenues", "revenue model, price, margin")


class ObjectivesAndKeyResults(XlsxSpec):
    @property
    def rel(self):
        return "business-planning/objectives-and-key-results/objectives-and-key-results.xlsx"

    example = {"text": {
        "title": "Delivery team, Q3 2026",
        "why": "reduce churn of families who order weekly; the strategy is to make the weekly order easy",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "OKR"
        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        thin = Side(style="thin", color="C9CED6")

        ws["A1"] = "OKR: {{title: team or company, period}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:K1")
        ws["A2"] = "Why:"
        ws["A2"].font = muted
        ws["B2"] = "{{why: strategy or problem the objectives address}}"
        ws["B2"].font = bold
        ws.merge_cells("B2:K2")

        headers = [
            ("Level", "company, department, team or employee", 14),
            ("Objective", "qualitative statement of what we want to achieve", 30),
            ("Type", "\"committed\" or \"aspirational\"", 14),
            ("Key result", "measurable outcome, not a task", 40),
            ("Unit", "unit of measure: %, pieces, money, days", 11),
            ("Baseline", "value at the start of the period", 10),
            ("KR target", "value to reach by the end of the period", 10),
            ("Current", "current value at the check-in", 10),
            ("Owner", "person responsible for the key result", 16),
            ("Actions", "tasks that move the key result", 36),
            ("Progress", "progress from baseline to target", 11),
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
            ws.cell(r, 11, f'=IF(OR(F{r}="",G{r}="",H{r}="",F{r}=G{r}),"",MAX(0,MIN(1,(H{r}-F{r})/(G{r}-F{r}))))'
                    ).number_format = "0.0"
            for c in range(1, 12):
                ws.cell(r, c).font = regular
            for c in (2, 4, 10):
                ws.cell(r, c).alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = "A4"
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text="OKR!$A$4")
        dv = DataValidation(type="list", formula1='"committed,aspirational"', allow_blank=True, errorStyle="warning",
                            error="Type: \"committed\" or \"aspirational\"", showErrorMessage=True)
        dv.add(f"C{first}:C{last}")
        ws.add_data_validation(dv)


class BusinessModelPatterns(PptxSpec):
    @property
    def rel(self):
        return "business-planning/business-model-patterns/business-model-patterns.pptx"

    example = {"text": {
        "title": "FreshDrop, grocery delivery, September 2026",
        "pattern": "No. 17 of 55: subscription, pay per period instead of per order",
        "logic": "Buyers pay a monthly fee for free delivery; FreshDrop earns on the basket and the fee; buyers order more often",
        "examples": "Amazon Prime (2005), Costco membership, Netflix (2007)",
        "now_who": "Moscow families, one-off orders; 1 in 4 never comes back",
        "new_who": "Same families on a monthly plan; 40% of buyers subscribe",
        "now_what": "groceries delivered per order; 199 RUB delivery fee each time",
        "new_what": "unlimited delivery for 499 RUB a month; same baskets",
        "now_how": "dark stores pick each order; couriers paid per drop",
        "new_how": "dark stores batch plan orders; couriers get a weekly bonus",
        "now_value": "2,450 RUB revenue per order; margin 9%",
        "new_value": "499 RUB fee plus margin on the basket; target margin 12%",
        "decision": "Test the monthly plan with 2,000 families in 3 districts from 1 November",
        "check": "Churn after month 1 (target below 15%); cannibalised free deliveries; the effect on basket size is not proven",
    }}

    def draw(self, prs, slide):
        header(slide, "BUSINESS MODEL PATTERNS",
               "{{title: company, product and date}}")
        S = slide.shapes
        # pattern card
        y = 1.25
        for x, w, tag, key, hint in [
            (0.5, 3.0, "Pattern (card)", "pattern", "{{pattern: pattern number and name}}"),
            (3.6, 6.0, "Pattern logic", "logic", "{{logic: essence: what changes and who benefits}}"),
            (9.7, 3.13, "Examples from the card", "examples", "{{examples: companies with years, from the pattern card}}"),
        ]:
            text(box(S, x, y, w, 0.3, fill=INK, line=None), tag, size=10, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            text(box(S, x, y + 0.3, w, 0.85, fill=ACCENT_BG, line=None), hint, size=10)
        # mapping across four dimensions
        y0 = 2.55
        lw, cw, gap = 1.5, 5.4, 0.015
        text(box(S, 0.5, y0, lw, 0.32, fill=INK, line=None), "Dimension", size=10, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(S, 0.5 + lw, y0, cw, 0.32, fill=INK, line=None), "Now (before the pattern)", size=10, bold=True, color=WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
        text(box(S, 0.5 + lw + cw, y0, cw - 0.0, 0.32, fill=ACCENT, line=None), "With the pattern (what changes)", size=10,
             bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        rows = [
            ("Who", "the customer", "{{now_who: who the customer is and who pays}}", "{{new_who: who the customer is and who pays}}"),
            ("What", "what we offer", "{{now_what: what the customer gets, on what terms}}", "{{new_what: what the customer gets, on what terms}}"),
            ("How", "how we create it", "{{now_how: processes and resources}}", "{{new_how: processes and resources}}"),
            ("Value", "how we earn", "{{now_value: how we earn: price, revenue, costs, metric}}", "{{new_value: how we earn: price, revenue, costs, metric}}"),
        ]
        rh = 0.8
        for i, (name, sub, now_text, new_text) in enumerate(rows):
            yy = y0 + 0.34 + i * (rh + 0.03)
            t = box(S, 0.5, yy, lw, rh, fill=ACCENT_BG, line=None)
            text(t, f"{name}: {sub}", size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
            text(box(S, 0.5 + lw, yy, cw, rh), now_text, size=10)
            text(box(S, 0.5 + lw + cw, yy, cw, rh), new_text, size=10)
        y2 = y0 + 0.34 + 4 * (rh + 0.03) + 0.1
        h = 7.5 - 0.25 - y2
        for x, bw, tag, key, hint, fill, col in [
            (0.5, 6.3, "Decision", "decision", "{{decision: what we decided and by when}}", GOOD_BG, GOOD),
            (6.9, 5.93, "Check and risks", "check", "{{check: figures to verify, what cannot be confirmed}}", BAD_BG, BAD),
        ]:
            text(box(S, x, y2, bw, 0.3, fill=col, line=None), tag, size=10, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            text(box(S, x, y2 + 0.3, bw, h - 0.3, fill=fill, line=None), hint, size=10)


class ProductEcosystemMap(PptxSpec):
    @property
    def rel(self):
        return "business-planning/product-ecosystem-map/product-ecosystem-map.pptx"

    example = {"text": {
        "title": "FreshDrop, customer ecosystem, Moscow, September 2026",
        "touch": "app, website, bank card app, messenger bot; reach: 60% of orders",
        "lead": "Slot reminder and weekly list: bring in and activate new buyers",
        "lead_m": "activation 38% in 3 days (app analytics)",
        "value": "FreshDrop app: the core product, orders in 30 minutes",
        "value_m": "1.8 orders per buyer a week (app analytics)",
        "profit": "Delivery fee and subscription: earns on each order",
        "profit_m": "ARPPU 2,450 RUB a month (finance report)",
        "engage": "Recipes and gift cards: other needs, more visits",
        "engage_m": "2.4 visits a week per user (app analytics)",
        "upsale": "Fresh flowers and pet food: extra-profit add-ons",
        "upsale_m": "average check +6% from add-ons (CRM)",
        "retain": "Loyalty points and saved baskets bring the next order",
        "retain_m": "D30 retention 41% (cohort report)",
        "transfer": "from the bank app to FreshDrop: card payment and loyalty points; level: transactions",
        "platform": "One profile across app, bank app and messenger; one login",
        "ops": "Auto-routing and stock sync; courier cost per order 149 RUB",
        "decision": "Keep loyalty points in the bank app, close the gift card pilot; check courier cost per order monthly",
    }}

    def draw(self, prs, slide):
        header(slide, "PRODUCT ECOSYSTEM MAP",
               "{{title: company, customer and map date}}")
        S = slide.shapes
        text(box(S, 0.5, 1.25, 12.33, 0.34, fill=INK, line=None), "Touchpoints: entry points with no value of their own",
             size=11, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(S, 0.5, 1.59, 12.33, 0.5), "{{touch: entry apps and sites, and their reach}}",
             size=10, anchor=MSO_ANCHOR.MIDDLE)
        cols = [
            ("Lead", "activation conversion", "lead", "products that bring in customers"),
            ("Value", "North Star Metric", "value", "products the customer comes for"),
            ("Profit", "average revenue per paying user", "profit", "products the company earns on"),
            ("Engagement", "average conversions per user per period", "engage", "products that raise engagement"),
            ("Upsale", "average check", "upsale", "extra-profit products"),
            ("Retention", "short-term and long-term retention rate", "retain", "retention products and next steps"),
        ]
        n, gap = 6, 0.1
        w = (12.33 - gap * (n - 1)) / n
        y0 = 2.2
        for i, (role, metric, key, hint) in enumerate(cols):
            x = 0.5 + i * (w + gap)
            text(box(S, x, y0, w, 0.4, fill=ACCENT, line=None, kind=MSO_SHAPE.PENTAGON), role,
                 size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            label(S, x, y0 + 0.4, w, 0.6, "Metric: " + metric, size=9, color=MUTED, anchor=MSO_ANCHOR.MIDDLE)
            text(box(S, x, y0 + 1.02, w, 1.15), "{{%s: %s}}" % (key, hint), size=10)
            text(box(S, x, y0 + 2.2, w, 0.7, fill=ACCENT_BG, line=None), "{{%s_m: metric value and source}}" % key,
                 size=9, anchor=MSO_ANCHOR.MIDDLE)
        y1 = y0 + 3.05
        text(box(S, 0.5, y1, 12.33, 0.34, fill=GOOD, line=None), "Transfer value: data passed between products",
             size=11, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(S, 0.5, y1 + 0.34, 12.33, 0.5, fill=GOOD_BG, line=None),
             "{{transfer: from and to which product, data and level}}",
             size=10, anchor=MSO_ANCHOR.MIDDLE)
        y2 = y1 + 0.95
        h = 7.5 - 0.3 - y2
        for x, bw, tag, key, hint, fill in [
            (0.5, 3.9, "Platform", "platform", "platform and unified user profile", ACCENT_BG),
            (4.5, 3.5, "Operational Efficiency", "ops", "internal automation products and metric", ACCENT_BG),
            (8.1, 4.73, "Decision", "decision", "launch, close or move, and metric", GOOD_BG),
        ]:
            text(box(S, x, y2, bw, 0.3, fill=GOOD if key == "decision" else INK, line=None), tag, size=10, bold=True,
                 color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            text(box(S, x, y2 + 0.3, bw, h - 0.3, fill=fill if key == "decision" else None), "{{%s: %s}}" % (key, hint), size=10)


class SmartGoals(PptxSpec):
    @property
    def rel(self):
        return "business-planning/smart-goals/smart-goals.pptx"

    example = {"text": {
        "title": "Ops lead's goal: fewer late deliveries, Q3 2026",
        "goal": "Cut late-delivery complaints from 6% to 3% of orders by 30 September 2026. Owner: Ops lead Ivan",
        "s": "Late-delivery complaints",
        "m": "Complaints from 6% to 3% of orders; source: weekly support report",
        "a": "Ops lead Ivan Petrov",
        "r": "2 analysts, 150 000 ₽ budget, 4 hours a week from couriers",
        "t": "30 September 2026; checks on 15 August and 15 September",
        "actions": "1. ETA alert 15 minutes before arrival: Ivan, 1 August. 2. Re-plan routes after 19:00: Olga, 15 August",
        "decision": "Accepted. Rework: the resources line does not name a budget owner",
    }}

    def draw(self, prs, slide):
        header(slide, "SMART GOALS · GOAL WORDING CHECK",
               "{{title: whose goal, period}}")
        text(box(slide.shapes, 0.5, 1.25, 12.33, 0.34, fill=ACCENT, line=None), "The goal in one sentence",
             size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(slide.shapes, 0.5, 1.59, 12.33, 0.55, fill=ACCENT_BG, line=None),
             "{{goal: what changes, by how much, by when}}", size=12, anchor=MSO_ANCHOR.MIDDLE)
        rows = [
            ("S", "Specific", "specific", "s", "one area of improvement"),
            ("M", "Measurable", "measurable", "m", "indicator, values and data source"),
            ("A", "Assignable", "has an owner", "a", "name or role of the owner"),
            ("R", "Realistic", "with the available resources", "r", "resources and the resource ceiling"),
            ("T", "Time-related", "by what date", "t", "target date and interim checks"),
        ]
        y0, rh, gap = 2.3, 0.9, 0.08
        for i, (ch, en, ru, key, hint) in enumerate(rows):
            y = y0 + i * (rh + gap)
            text(box(slide.shapes, 0.5, y, 0.7, rh, fill=ACCENT, line=None), ch, size=26, bold=True, color=WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            label(slide.shapes, 1.25, y, 1.9, rh, f"{en}\n{ru}", size=11, bold=True, anchor=MSO_ANCHOR.MIDDLE)
            text(box(slide.shapes, 3.2, y, 4.9, rh), "{{%s: %s}}" % (key, hint), size=11, anchor=MSO_ANCHOR.MIDDLE)
        x, w = 8.3, 4.53
        h1 = 2.5
        text(box(slide.shapes, x, y0, w, 0.32, fill=INK, line=None), "Action plan", size=12, bold=True,
             color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(slide.shapes, x, y0 + 0.32, w, h1 - 0.32),
             "{{actions: steps to the goal, who and when}}", size=11)
        y2 = y0 + h1 + 0.1
        h2 = y0 + 5 * (rh + gap) - gap - y2
        text(box(slide.shapes, x, y2, w, 0.32, fill=GOOD, line=None), "Decision", size=12, bold=True,
             color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(slide.shapes, x, y2 + 0.32, w, h2 - 0.32, fill=GOOD_BG),
             "{{decision: decision and what to rework}}", size=11)


class Usp4u(PptxSpec):
    @property
    def rel(self):
        return "business-planning/usp-4u/usp-4u.pptx"

    example = {"text": {
        "title": "Families in Moscow who order groceries for the week",
        "useful": "Empty fridge on a workday: no time to shop",
        "unique": "Pickers scan a live stock map, so no surprise substitutes",
        "specific": "Delivery in 2 hours; 98% on time in June; free above 1 500 ₽",
        "urgent": "Free delivery for the first 3 orders until 30 September",
        "phrase": "Groceries in 2 hours, or the delivery is on us",
        "risk": "The 98% figure covers June only; the 2-hour promise may fail in heavy rain",
        "check": "Share of orders on time and refund requests per 100 orders, reviewed every 2 weeks",
        "decision": "Publish on the home page from 1 October. Confirm the on-time figure with July data",
    }}

    def draw(self, prs, slide):
        s = slide.shapes
        header(slide, "USP FORMULA 4U · USEFUL + UNIQUE + ULTRA-SPECIFIC + URGENT",
               "{{title: audience and where the phrase appears}}")
        blocks = [("Useful", "useful", "how it is useful"),
                  ("Unique", "unique", "what makes it unique"),
                  ("Ultra-specific", "specific", "concrete figures and terms"),
                  ("Urgent", "urgent", "reason to act now")]
        x, w, gap, y = 0.5, 2.9, 0.243, 1.25
        for i, (name, key, hint) in enumerate(blocks):
            xx = x + i * (w + gap)
            text(box(s, xx, y, w, 0.5, fill=ACCENT, line=None), name, size=13, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            text(box(s, xx, y + 0.5, w, 1.6, fill=ACCENT_BG), "{{%s: %s}}" % (key, hint), size=11)
        label(s, 0.5, 3.5, 12.33, 0.35, "The full phrase", size=12, bold=True)
        text(box(s, 0.5, 3.85, 12.33, 0.9, fill=GOOD_BG), "{{phrase: the USP in one phrase}}", size=14, bold=True,
             anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 0.5, 4.95, 6.07, 0.4, fill=BAD, line=None), "What is missing or unconfirmed", size=12, bold=True,
             color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 0.5, 5.35, 6.07, 1.0, fill=BAD_BG), "{{risk: unconfirmed claims and limits}}", size=11)
        text(box(s, 6.76, 4.95, 6.07, 0.4, fill=INK, line=None), "How we will check after publishing", size=12, bold=True, color=WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 6.76, 5.35, 6.07, 1.0, fill=ACCENT_BG), "{{check: what we measure and when}}", size=11)
        text(box(s, 0.5, 6.5, 1.9, 0.6, fill=INK, line=None), "Decision", size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 2.4, 6.5, 10.43, 0.6, fill=GOOD_BG), "{{decision: decision and missing data}}", size=10,
             anchor=MSO_ANCHOR.MIDDLE)


class UspAida(PptxSpec):
    @property
    def rel(self):
        return "business-planning/usp-aida/usp-aida.pptx"

    example = {"text": {
        "title": "Families in new Moscow districts, banner on the app home page",
        "attention": "Tired of queuing for groceries after work?",
        "interest": "Pickers scan stock live, so the list you order is the list you get",
        "desire": "Groceries at your door in 2 hours; 98% on time in June",
        "action": "Order before 20:00 for same-evening delivery; first delivery free",
        "satisfaction": "Order on time, or the delivery is refunded; we check it weekly",
        "offer": "Tired of queues? Order before 20:00 and get groceries in 2 hours, free the first time",
        "risk": "The 98% figure covers June only; evening slots may sell out",
        "check": "Banner click-through and share of first orders on time, every 2 weeks",
        "decision": "Run the banner in 2 districts from 1 October; decide after 4 weeks",
    }}

    def draw(self, prs, slide):
        s = slide.shapes
        header(slide, "USP FORMULA AIDA(s) · ATTENTION → INTEREST → DESIRE → ACTION → SATISFACTION",
               "{{title: audience and where the text appears}}")
        blocks = [("Attention", "attention", "what catches attention"),
                  ("Interest", "interest", "what raises interest"),
                  ("Desire", "desire", "what makes them want it"),
                  ("Action", "action", "what the customer does next"),
                  ("Satisfaction", "satisfaction", "what the customer gets after")]
        x, w, gap, y = 0.5, 2.3, 0.2075, 1.25
        for i, (name, key, hint) in enumerate(blocks):
            xx = x + i * (w + gap)
            text(box(s, xx, y, w, 0.5, fill=ACCENT, line=None), name, size=11, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            text(box(s, xx, y + 0.5, w, 1.6, fill=ACCENT_BG), "{{%s: %s}}" % (key, hint), size=11)
        label(s, 0.5, 3.5, 12.33, 0.35, "The full offer text", size=12, bold=True)
        text(box(s, 0.5, 3.85, 12.33, 0.9, fill=GOOD_BG), "{{offer: offer text, in block order}}", size=14, bold=True,
             anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 0.5, 4.95, 6.07, 0.4, fill=BAD, line=None), "What is missing or unconfirmed", size=12, bold=True,
             color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 0.5, 5.35, 6.07, 1.0, fill=BAD_BG), "{{risk: unconfirmed claims and limits}}", size=11)
        text(box(s, 6.76, 4.95, 6.07, 0.4, fill=INK, line=None), "How we will check after publishing", size=12, bold=True, color=WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 6.76, 5.35, 6.07, 1.0, fill=ACCENT_BG), "{{check: what we measure and when}}", size=11)
        text(box(s, 0.5, 6.5, 1.9, 0.6, fill=INK, line=None), "Decision", size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 2.4, 6.5, 10.43, 0.6, fill=GOOD_BG), "{{decision: decision and missing data}}", size=10,
             anchor=MSO_ANCHOR.MIDDLE)


class UspHabitualWithoutHabitual(PptxSpec):
    @property
    def rel(self):
        return "business-planning/usp-habitual-without-habitual/usp-habitual-without-habitual.pptx"

    example = {"text": {
        "title": "Grocery delivery in Moscow for busy families",
        "habit": "Supermarket delivery",
        "removed": "A shop floor the customer walks through",
        "replacement": "A photo stock list with live availability",
        "reason": "18 interviews: people lose time choosing items on the floor",
        "phrase": "Supermarket without the aisles",
        "risk": "Impulse buys drop; the app suggests add-ons to replace them",
        "check": "Average basket size and add-on rate, reviewed monthly",
        "decision": "Launch the banner from 1 October; check basket size after 4 weeks",
    }}

    def draw(self, prs, slide):
        s = slide.shapes
        header(slide, "USP \"THE FAMILIAR WITHOUT THE FAMILIAR\"", "{{title: audience and where the phrase appears}}")
        x, y = 0.5, 1.25
        text(box(s, x, y, 5.6, 0.5, fill=ACCENT, line=None), "The familiar (category)", size=13, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, x, y + 0.5, 5.6, 1.1, fill=ACCENT_BG), "{{habit: the category, as the customer calls it}}", size=11)
        label(s, x + 5.6, y + 0.7, 1.13, 0.6, "without", size=14, bold=True, color=ACCENT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, x + 6.73, y, 5.6, 0.5, fill=BAD, line=None), "Without the familiar (what is removed)", size=13, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, x + 6.73, y + 0.5, 5.6, 1.1, fill=BAD_BG), "{{removed: mandatory element that was removed}}", size=11)
        text(box(s, 0.5, 3.0, 6.07, 0.4, fill=INK, line=None), "What replaces it", size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 0.5, 3.4, 6.07, 1.0, fill=ACCENT_BG), "{{replacement: what replaces the removed element}}", size=11)
        text(box(s, 6.76, 3.0, 6.07, 0.4, fill=INK, line=None), "Basis: why it bothered the customer", size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 6.76, 3.4, 6.07, 1.0, fill=ACCENT_BG), "{{reason: how we know, and the source}}", size=11)
        label(s, 0.5, 4.45, 12.33, 0.35, "The full phrase", size=12, bold=True)
        text(box(s, 0.5, 4.8, 12.33, 0.7, fill=GOOD_BG), "{{phrase: category without element, one phrase}}", size=14, bold=True,
             anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 0.5, 5.6, 6.07, 0.35, fill=BAD, line=None), "What jobs the removed element did", size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 0.5, 5.95, 6.07, 0.85, fill=BAD_BG), "{{risk: what the removed element did, and its cover}}", size=11)
        text(box(s, 6.76, 5.6, 6.07, 0.35, fill=INK, line=None), "How we will check after launch", size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 6.76, 5.95, 6.07, 0.85, fill=ACCENT_BG), "{{check: what we measure and when}}", size=11)
        text(box(s, 0.5, 6.85, 1.9, 0.5, fill=INK, line=None), "Decision", size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 2.4, 6.85, 10.43, 0.5, fill=GOOD_BG), "{{decision: decision and missing data}}", size=10,
             anchor=MSO_ANCHOR.MIDDLE)


class UspMaxwellFormula(PptxSpec):
    @property
    def rel(self):
        return "business-planning/usp-maxwell-formula/usp-maxwell-formula.pptx"

    example = {"text": {
        "title": "Moscow families who want the week's groceries in one order",
        "result": "A full fridge for the week, without a shop trip",
        "time": "Delivered in 2 hours; 9 in 10 orders on time",
        "objection": "Worried about wrong items? Any missing item is refunded within 24 hours",
        "phrase": "A full fridge in 2 hours, or we refund the missing items",
        "risk": "The 2-hour promise may fail at peak hours; the guarantee covers items only",
        "check": "Failures and refund claims per 100 orders, reviewed weekly",
        "decision": "Publish from 1 October; if refund claims pass 5 per 100 orders, change the promise",
    }}

    def draw(self, prs, slide):
        s = slide.shapes
        header(slide, "MAXWELL USP FORMULA · RESULT + TIMEFRAME + ANSWER TO THE OBJECTION", "{{title: audience and where the phrase appears}}")
        blocks = [("The end result", "result", "the end result for the customer"),
                  ("Time to get it", "time", "time to get it, and on-time share"),
                  ("Answer to the objection", "objection", "objection and how we answer it")]
        x, w, gap, y = 0.5, 3.9, 0.315, 1.25
        for i, (name, key, hint) in enumerate(blocks):
            xx = x + i * (w + gap)
            text(box(s, xx, y, w, 0.5, fill=ACCENT, line=None), name, size=13, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            text(box(s, xx, y + 0.5, w, 1.6, fill=ACCENT_BG), "{{%s: %s}}" % (key, hint), size=11)
            if i < 2:
                label(s, xx + w, y + 0.9, gap, 0.6, "+", size=20, bold=True, color=ACCENT, align=PP_ALIGN.CENTER,
                      anchor=MSO_ANCHOR.MIDDLE)
        label(s, 0.5, 3.5, 12.33, 0.35, "The full phrase", size=12, bold=True)
        text(box(s, 0.5, 3.85, 12.33, 0.9, fill=GOOD_BG), "{{phrase: the USP in one phrase}}", size=14, bold=True,
             anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 0.5, 4.95, 6.07, 0.4, fill=BAD, line=None), "What could break the promise", size=12, bold=True, color=WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 0.5, 5.35, 6.07, 1.0, fill=BAD_BG), "{{risk: conditions under which the promise fails}}", size=11)
        text(box(s, 6.76, 4.95, 6.07, 0.4, fill=INK, line=None), "How we will check after launch", size=12, bold=True, color=WHITE,
             anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 6.76, 5.35, 6.07, 1.0, fill=ACCENT_BG), "{{check: what we measure and when}}", size=11)
        text(box(s, 0.5, 6.5, 1.9, 0.6, fill=INK, line=None), "Decision", size=12, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        text(box(s, 2.4, 6.5, 10.43, 0.6, fill=GOOD_BG), "{{decision: decision and trigger to revisit}}", size=10,
             anchor=MSO_ANCHOR.MIDDLE)


class RapidDecisionRights(PptxSpec):
    @property
    def rel(self):
        return "business-planning/rapid-decision-rights/rapid-decision-rights.pptx"

    example = {"text": {
        "title": "Wyeth: expanding Enbrel production capacity (Ireland plant), 2006 article",
        "decision": "How to expand Enbrel production capacity quickly, including a new plant in Ireland",
        "r_who": "People closest to the knowledge; some responsibilities pushed down to the business units",
        "r_note": "Make a proposal or offer alternatives; individual names are not given",
        "a_who": "Wyeth top executives",
        "a_note": "Kept veto power over many important proposals; a veto comes with an alternative or goes to the Decide role",
        "p_who": "The business unit",
        "p_note": "Carries out the plan; responsibility for execution rested firmly with it",
        "i_who": "Other managers",
        "i_note": "Gave input to the Enbrel team before the decisions; the recommender weighs it but need not follow it",
        "d_who": "Cavan Redmond, executive vice president and general manager of the biotech division",
        "d_note": "Took many Enbrel decisions after he and his team gathered input from other managers",
        "conflict": "Veto holder offers an alternative or escalates to the person with the D",
        "outcome": "Roles assigned for Enbrel decisions; the article gives no date, result or confirmation that the Irish plant was approved",
    }}

    def draw(self, prs, slide):
        header(slide, "RAPID DECISION RIGHTS · WHO DOES WHAT IN ONE DECISION",
               "{{title: decision area, company or team, date}}")
        sh = slide.shapes
        left, full, g = 0.5, 12.33, 0.1
        label(sh, left, 1.2, 1.55, 0.7, "Decision", size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(box(sh, left + 1.65, 1.2, full - 1.65, 0.7, fill=ACCENT_BG, line=None),
             "{{decision: the decision in one sentence, with a deadline if there is one}}",
             size=12, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        roles = [("r", "Recommend (R)"), ("a", "Agree (A)"), ("p", "Perform (P)"),
                 ("i", "Input (I)"), ("d", "Decide (D)")]
        lw = 1.55
        gx = left + lw + g
        cw = (left + full - gx) / 5
        y = 2.05
        label(sh, left, y, lw, 0.45, "Role", size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        label(sh, left, y + 0.51, lw, 1.1, "Who", size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        label(sh, left, y + 1.67, lw, 1.45, "Scope and limits", size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        for i, (k, name) in enumerate(roles):
            x = gx + i * cw + 0.03
            w = cw - 0.06
            fill = ACCENT if k != "d" else INK
            text(box(sh, x, y, w, 0.45, fill=fill, line=None), name, size=12, bold=True,
                 color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, y + 0.51, w, 1.1, fill=ACCENT_BG, line=None),
                 "{{%s_who: name or role holder; one person for R and D}}" % k, size=10, bold=True)
            text(box(sh, x, y + 1.67, w, 1.45, fill=WHITE, line=LINE),
                 "{{%s_note: what this role covers in this decision and its limits}}" % k, size=10)
        y2 = y + 3.3
        for j, (tag, key, hint, fill, line) in enumerate([
            ("If Recommend and Agree disagree", "conflict", "{{conflict: who settles it and how}}", WHITE, LINE),
            ("Outcome", "outcome", "{{outcome: decision made, by whom, when, and what is not known}}", ACCENT_BG, None),
        ]):
            bw = (full - g) / 2
            bx = left + j * (bw + g)
            tb = text(box(sh, bx, y2, bw, 1.55, fill=fill, line=line), hint, size=10)
            tb.text_frame.margin_top = Inches(0.36)
            label(sh, bx + 0.08, y2 + 0.03, bw - 0.16, 0.32, tag, size=10, bold=True, color=INK)


class BalancedScorecard(PptxSpec):
    @property
    def rel(self):
        return "business-planning/balanced-scorecard/balanced-scorecard.pptx"

    example = {"text": {
        "title": "Analog Devices IC operations: QIP goals to 1992",
        "strategy": "Business objectives: market leadership, revenue growth, profitability. Driver: be rated number 1 by customers in total value delivered",
        "g1": "Market leadership, revenue growth, profitability",
        "m1": "N/A: no financial measure on the slides read",
        "t1": "N/A: no financial target on the slides read",
        "g2": "Be rated number 1 by customers in total value delivered",
        "m2": "On-time delivery; outgoing defect level; lead time; share of customer requested dates (CRDs) matched; excess lead time",
        "t2": "1987 / 1990 / 1992 goal: delivery 85% / 96% / >99.8%; defects 500 / 230 / <10 PPM; lead time 10 / 5.4 / <3 weeks; CRDs matched 31% / 50% / n/a",
        "g3": "Eliminate all forms of waste at all entities, functions and levels",
        "m3": "Manufacturing cycle time; process defect level; yield",
        "t3": "1987 / 1990 / 1992 goal: cycle time 15 / 8 / 4-5 weeks; process defects 5000 / 1100 / <10 PPM; yield 20% / 38% / >50%",
        "g4": "Shorter time to market; reduced turnover",
        "m4": "Time to market; labor turnover as a proxy for employee satisfaction; from FY1990 bookings of products introduced after 1985",
        "t4": "Time to market 1987 / 1990 / 1992 goal: 36 months / not read / 6 months; turnover target not read",
        "decision": "FY1990: delivery is measured against the customer's requested date; the old new-product measures, poor predictors, are replaced by a product tracking system and two innovation measures. FY1991-92: scorecard unchanged",
    }}

    def draw(self, prs, slide):
        header(slide, "BALANCED SCORECARD · FOUR PERSPECTIVES",
               "{{title: company or unit and the period}}")
        sh = slide.shapes
        left, full, g = 0.5, 12.33, 0.06
        lw = 2.5
        cw = (full - lw - 3 * g) / 3
        text(box(sh, left, 1.25, full, 0.5, fill=ACCENT_BG, line=None),
             "{{strategy: the strategy or vision the scorecard serves}}", size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        y = 1.85
        for i, tag in enumerate(["Goals", "Measures", "Targets"]):
            label(sh, left + lw + g + i * (cw + g), y, cw, 0.3, tag, size=11, bold=True, color=ACCENT)
        y += 0.32
        rows = [
            ("Financial", "How do we look to shareholders?"),
            ("Customer", "How do customers see us?"),
            ("Internal business process", "What must we excel at?"),
            ("Innovation and learning", "Can we continue to improve and create value?"),
        ]
        rh = 0.98
        for r, (name, question) in enumerate(rows, start=1):
            tb = text(box(sh, left, y, lw, rh, fill=ACCENT, line=None), name, size=11, bold=True, color=WHITE)
            p = tb.text_frame.add_paragraph()
            run = p.add_run()
            run.text = question
            run.font.size, run.font.name, run.font.color.rgb = Pt(9), FONT, WHITE
            for i, key in enumerate("gmt"):
                hint = {"g": "what we want to achieve", "m": "how we measure it", "t": "target value and date"}[key]
                text(box(sh, left + lw + g + i * (cw + g), y, cw, rh),
                     "{{%s%d: %s in this perspective}}" % (key, r, hint), size=9)
            y += rh + g
        label(sh, left, y + 0.02, 1.9, 0.3, "Decision", size=11, bold=True)
        text(box(sh, left, y + 0.3, full, 0.82, fill=ACCENT_BG, line=None),
             "{{decision: what the scorecard changed in the plan or the measures}}", size=10, anchor=MSO_ANCHOR.MIDDLE)


class RiskRegister(XlsxSpec):
    @property
    def rel(self):
        return "business-planning/risk-register/risk-register.xlsx"

    _risks = [
        ("Risk 01/26", "Partnership may be unable to fully deliver the HOIP strategic priorities",
         "Limited or uncertain resources, weak cross-partner coordination, competing organisational pressures, weak performance monitoring",
         "Reduced impact for communities, missed statutory or strategic commitments, lower confidence in the partnership",
         "People, Place, Prosperity", "CPP Board", 4, 3,
         "Strengthen delivery oversight and escalation routes; agree priority areas for focused action; confirm agency leads"),
        ("Risk 02/26", "Partnership may be unable to sustain long-term financial viability or align funding streams",
         "Reducing or unpredictable budgets, competing demands, short-term or ring-fenced funding, little flexibility to redirect money",
         "Constrained delivery, hindered strategic planning, less ability to invest in preventative or joint approaches",
         "People, Place, Prosperity", "CPP Senior Officers Group", 4, 5,
         "Agree budget arrangements beyond May 2027 and partner contributions; align funding streams; explore joint investment, bids and pooled resources"),
        ("Risk 03/26", "Insufficient capacity and critical skills limit delivery of services and priorities",
         "Recruitment and retention problems, ageing workforce, limited specialist expertise, difficulty attracting talent to remote areas",
         "Lower service resilience, hindered innovation, weaker ability to meet current and future needs",
         "People, Place, Prosperity", "CPP Senior Officers Group", 3, 2,
         "Develop and implement a new Induction Module; review induction materials regularly"),
        ("Risk 04/26", "Barriers to accessing services continue, particularly in remote and rural communities",
         "Poor digital connectivity, limited access to technology, geographic isolation, workforce shortages, financial pressures",
         "Reduced engagement with services, widening inequalities, slower progress toward HOIP priorities",
         "People, Place", "CPP Board", 3, 3,
         "Target communities with poor internet or mobile signal; support community broadband projects; expand awareness campaigns"),
        ("Risk 05/26", "Cost-of-living crisis and persistent poverty increase demand for support services",
         "Ongoing cost-of-living crisis; persistent levels of poverty",
         "Worse health and wellbeing, wider inequalities, strain on limited resources, less capacity for preventative support",
         "People, Prosperity", "Poverty Reduction Delivery Group", 4, 5,
         "Strengthen coordination of hardship and crisis support; locality-based interventions; Poverty Reduction Action Plan; better signposting"),
        ("Risk 06/26", "Ineffective engagement may reduce public confidence in partnership decision-making",
         "Ineffective engagement, limited participation, few chances for communities to influence decisions",
         "Lower involvement in local initiatives, less support for service changes, diminished impact of HOIP priorities",
         "People, Place, Prosperity", "CPP Board", 3, 4,
         "Strengthen lived experience forums; publish regular 'You Said / We Did' updates; produce an accessible annual report"),
        ("Risk 07/26", "CPP may not fully implement or align with Scottish Government policies and statutory duties",
         "Limited capacity, competing priorities, insufficient coordination, unclear national guidance",
         "Non-compliance, reputational harm, missed statutory or strategic commitments",
         "People, Place, Prosperity", "CPP Senior Officers Group", 4, 4,
         "Build a Policy Implementation Tracker; assign leads per policy area; annual compliance reviews; forward planning"),
        ("Risk 08/26", "CPP may be unable to maintain fit-for-purpose data-sharing agreements and data collection",
         "Poor data quality, inconsistent sharing practices, gaps in analytical capacity",
         "Weaker understanding of local need, planning, decisions and evaluation of impact",
         "People, Place, Prosperity", "CPP Senior Officers Group", 3, 4,
         "Develop data-sharing agreements; improve consistency of shared data; strengthen analytical capacity; implement the indicator framework"),
    ]
    example = {
        "text": {
            "title": "Highland Community Planning Partnership, Strategic Risk Register as at January 2026",
            "scope": "Delivery of the Highland Outcome Improvement Plan (HOIP) 2024-2027, reported to the Board on 10 March 2026",
            "decision": "Board noted the update and agreed the revised approach, including the Risk Appetite Statement applied to all "
                        "strategic risks; funding (02/26), policy implementation (07/26) and data sharing (08/26) seen above appetite",
        },
        "rows": [[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], None, r[8], None, None, None, None] for r in _risks],
    }

    def draw(self, wb):
        from openpyxl.formatting.rule import CellIsRule, FormulaRule
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Risk register"
        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        input_fill = PatternFill("solid", fgColor="FFF8E1")
        thin = Side(style="thin", color="C9CED6")
        top_wrap = Alignment(wrap_text=True, vertical="top")

        ws["A1"] = "Risk Register: {{title: what the register covers, organization or product, and the date}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:R1")
        ws["A2"] = "Scope:"
        ws["A2"].font = muted
        ws["C2"] = "{{scope: the objective or project whose risks are listed, and who reviews the register}}"
        ws["A3"] = "Decision:"
        ws["A3"].font = muted
        ws["C3"] = "{{decision: what the review decided about the top risks: response, escalation or acceptance}}"
        for r in (2, 3):
            ws.cell(r, 3).font = bold
            ws.cell(r, 3).alignment = top_wrap
            ws.merge_cells(f"C{r}:N{r}")
            ws.row_dimensions[r].height = 32

        hr, first, last = 5, 6, 55
        headers = [
            ("ID", "Risk identifier: a short code that does not change, for example R-01. Used to refer to the risk in meetings and reports.", 11),
            ("Risk statement", "The risk as one event that could happen, in common phrasing so rows compare: what could happen to which asset or objective. "
                               "Not \"supplier issues\" but \"main payment provider is unavailable for more than a day\".", 40),
            ("Cause", "What makes the event possible: the threat, weakness or condition behind it.", 34),
            ("Effect", "What happens to the objective if the event occurs: money, customers, schedule, compliance, reputation.", 34),
            ("Category", "Theme for grouping rows and comparing registers, for example operational, financial, legal, technology, market.", 18),
            ("Owner", "One named person accountable for keeping this risk within agreed limits. A group or \"team\" is not an owner.", 20),
            ("Likelihood\n(1-5)", "How likely the event is now, with existing controls: 1 rare, 2 unlikely, 3 possible, 4 likely, 5 almost certain. "
                                 "Write the meaning of each level down before scoring.", 12),
            ("Impact\n(1-5)", "How severe the effect is now, with existing controls: 1 minor to 5 severe. Define each level in money, customers or delay "
                              "before scoring.", 12),
            ("Response type", "Accept (monitor only, within tolerance), transfer (share the consequences, for example insurance), mitigate (reduce likelihood or "
                              "impact), avoid (do not take the action). For opportunities: realize, share, enhance, accept.", 14),
            ("Response", "What will be done, by whom and by when. For accept, write what is monitored and the trigger to revisit.", 44),
            ("Status", "Open, In progress (response under way) or Closed (risk ended or the response is complete and the risk is back within limits).", 13),
            ("Date raised", "Date the risk was first entered in the register.", 12),
            ("Last reviewed", "Date of the last reassessment of likelihood and impact.", 12),
            ("Next review", "Date by which the risk must be reviewed again. Rows past this date are flagged.", 12),
            ("Score", "Calculated: likelihood x impact. An ordinal number for ranking, not a probability or a loss.", 9),
            ("Rating", "Calculated: High at or above the High-from score, Medium at or above the Medium-from score, otherwise Low. Bands are set in the summary.", 10),
            ("Priority\nrank", "Calculated: 1 is the highest score among open risks; equal scores share a rank. Closed risks are not ranked.", 11),
            ("Review flag", "Calculated: Overdue when the next review date is before today and the risk is not closed.", 11),
        ]
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(hr, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center" if 7 <= i <= 8 or i >= 15 else "left")
            c.border = Border(bottom=thin)
            c.comment = Comment(hint, "pdm-skills", width=260, height=130)
            ws.column_dimensions[c.column_letter].width = width
        ws.row_dimensions[hr].height = 48

        rng = lambda col: f"${col}${first}:${col}${last}"
        for r in range(first, last + 1):
            for c in range(1, 19):
                cell = ws.cell(r, c)
                cell.font = regular
                cell.alignment = top_wrap if c not in (7, 8, 15, 16, 17, 18) else Alignment(horizontal="center", vertical="top")
            for c in (12, 13, 14):
                ws.cell(r, c).number_format = "yyyy-mm-dd"
            ws.cell(r, 15, f'=IF(OR(G{r}="",H{r}=""),"",G{r}*H{r})')
            ws.cell(r, 16, f'=IF(O{r}="","",IF(O{r}>=$U$6,"High",IF(O{r}>=$U$7,"Medium","Low")))')
            ws.cell(r, 17, f'=IF(OR(O{r}="",K{r}="Closed"),"",1+COUNTIFS({rng("O")},">"&O{r},{rng("K")},"<>Closed"))')
            ws.cell(r, 18, f'=IF(OR(N{r}="",K{r}="Closed"),"",IF(N{r}<TODAY(),"Overdue",""))')
            for c in range(15, 19):
                ws.cell(r, c).fill = calc_fill
            ws.cell(r, 15).font = bold
        ws.freeze_panes = ws.cell(first, 3)
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'Risk register'!$A${first}")

        def dv(kind, ref, **kw):
            d = DataValidation(type=kind, allow_blank=True, showErrorMessage=True, errorStyle="stop", **kw)
            d.add(ref)
            ws.add_data_validation(d)

        dv("whole", f"G{first}:H{last}", operator="between", formula1="1", formula2="5",
           errorTitle="Scale", error="Use a whole number from 1 to 5")
        dv("list", f"I{first}:I{last}", formula1='"Accept,Transfer,Mitigate,Avoid,Realize,Share,Enhance"',
           errorTitle="Response type", error="Accept, Transfer, Mitigate, Avoid (opportunities: Realize, Share, Enhance)")
        dv("list", f"K{first}:K{last}", formula1='"Open,In progress,Closed"', errorTitle="Status", error="Open, In progress or Closed")
        dv("date", f"L{first}:N{last}", operator="greaterThan", formula1="36526",
           errorTitle="Date", error="Enter a date")

        ws.conditional_formatting.add(f"P{first}:P{last}", CellIsRule(operator="equal", formula=['"High"'],
                                      fill=PatternFill("solid", bgColor="FBEAEA"), font=Font(color="C63D3D", bold=True)))
        ws.conditional_formatting.add(f"P{first}:P{last}", CellIsRule(operator="equal", formula=['"Medium"'],
                                      fill=PatternFill("solid", bgColor="FFF4D6"), font=Font(color="8A6100", bold=True)))
        ws.conditional_formatting.add(f"P{first}:P{last}", CellIsRule(operator="equal", formula=['"Low"'],
                                      fill=PatternFill("solid", bgColor="E8F5EC"), font=Font(color="2E8B57", bold=True)))
        ws.conditional_formatting.add(f"R{first}:R{last}", CellIsRule(operator="equal", formula=['"Overdue"'],
                                      font=Font(color="C63D3D", bold=True)))

        ws.column_dimensions["S"].width = 3
        ws.column_dimensions["T"].width = 30
        ws.column_dimensions["U"].width = 12
        ws["T5"], ws["U5"] = "Summary", None
        for ref in ("T5", "U5"):
            ws[ref].font, ws[ref].fill = bold, head_fill
        stats = [
            ("High from (score)", 15, "Score at or above this value is rated High. Set it with your scale and risk appetite; 15 suits a 5 x 5 grid.", True),
            ("Medium from (score)", 6, "Score at or above this value, and below High, is rated Medium; lower is Low.", True),
            ("Risks listed", f'=COUNTA({rng("B")})', "Rows with a risk statement.", False),
            ("High, not closed", f'=COUNTIFS({rng("P")},"High",{rng("K")},"<>Closed")', "Risks rated High that are not closed.", False),
            ("Medium, not closed", f'=COUNTIFS({rng("P")},"Medium",{rng("K")},"<>Closed")', "Risks rated Medium that are not closed.", False),
            ("Low, not closed", f'=COUNTIFS({rng("P")},"Low",{rng("K")},"<>Closed")', "Risks rated Low that are not closed.", False),
            ("Closed", f'=COUNTIF({rng("K")},"Closed")', "Risks with status Closed.", False),
            ("Review overdue", f'=COUNTIF({rng("R")},"Overdue")', "Open risks whose next review date has passed.", False),
            ("Without owner", f'=SUMPRODUCT(({rng("B")}<>"")*({rng("F")}=""))', "Must be 0: a risk without an owner is nobody's.", False),
            ("Without response", f'=SUMPRODUCT(({rng("B")}<>"")*({rng("J")}=""))', "Risks with an empty Response column.", False),
            ("Highest score", f'=IF(COUNT({rng("O")})=0,"",MAX({rng("O")}))', "The largest score in the register.", False),
        ]
        for i, (name, value, hint, is_input) in enumerate(stats, start=6):
            a = ws.cell(i, 20, name)
            a.font = regular
            a.comment = Comment(hint, "pdm-skills", width=260, height=90)
            b = ws.cell(i, 21, value)
            b.font = bold
            b.fill = input_fill if is_input else calc_fill
            b.alignment = Alignment(horizontal="center")
        dv("whole", "U6:U7", operator="between", formula1="1", formula2="25",
           errorTitle="Band", error="Use a whole number from 1 to 25")
