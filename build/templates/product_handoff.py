from .base import *


class UserStory(PptxSpec):
    @property
    def rel(self):
        return "product-handoff/user-story/user-story.pptx"

    example = {"text": {
        "title": "Express slot reminder",
        "role": "a Moscow parent who orders groceries every week",
        "goal": "get a reminder 15 minutes before my delivery slot",
        "benefit": "I do not miss the slot and the courier does not wait: 0 missed slots a month",
        "size": "5 SP",
        "notes": "reminder time fixed at 15 minutes; no SMS in this version; slot change is out of scope",
        "given1": "the slot is tomorrow at 18:00",
        "when1": "the clock reaches 17:45",
        "then1": "push: «Your courier comes at 18:00»",
        "given2": "the buyer turned reminders off",
        "when2": "the slot time comes",
        "then2": "no push is sent",
        "given3": "the slot was cancelled",
        "when3": "the reminder time arrives",
        "then3": "no push; the slot shows as cancelled",
        "given4": "the app is closed",
        "when4": "the reminder time arrives",
        "then4": "push appears on the lock screen within 60 seconds",
        "i": "✓", "n": "✓", "v": "✓", "e": "✓", "s": "✓", "t": "✓",
    }}

    def draw(self, prs, slide):
        header(slide, "USER STORY · CARD FRONT", "{{title: short story title}}")
        sh = slide.shapes
        x, w, y = 0.5, 12.33, 1.35
        for tag, key, hint in [
            ("As a", "role", "{{role: a specific role or segment}}"),
            ("I want to", "goal", "{{goal: what the person wants to do}}"),
            ("So that", "benefit", "{{benefit: benefit and how it is noticed}}"),
        ]:
            box(sh, x, y, w, 1.5, fill=ACCENT_BG, line=None)
            label(sh, x + 0.1, y + 0.08, w - 0.2, 0.35, tag, size=13, bold=True, color=ACCENT)
            text(box(sh, x + 0.05, y + 0.45, w - 0.1, 1.0, line=None), hint, size=18)
            y += 1.62
        box(sh, x, y, w, 7.2 - y)
        label(sh, x + 0.1, y + 0.05, 2.2, 0.8, "Size", size=12, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        text(box(sh, x + 2.4, y + 0.05, w - 2.5, 0.8, line=None), "{{size: team estimate and unit}}", size=14,
             anchor=MSO_ANCHOR.MIDDLE)

        slide = prs.slides.add_slide(prs.slide_layouts[6])
        header(slide, "USER STORY · CARD BACK · CONVERSATION & CONFIRMATION", "{{title: short story title}}")
        sh = slide.shapes
        lx, lw = 0.5, 4.2
        box(sh, lx, 1.3, lw, 7.2 - 1.3)
        label(sh, lx + 0.05, 1.33, lw - 0.1, 0.3, "Notes from the discussion · conversation", size=10, bold=True)
        text(box(sh, lx, 1.65, lw, 7.2 - 1.65, line=None),
             "{{notes: what was clarified with the team}}", size=10)

        rx, rw = 4.9, 7.93
        label(sh, rx, 1.3, rw, 0.3, "Acceptance criteria", size=11, bold=True)
        tbl = sh.add_table(5, 4, Inches(rx), Inches(1.65), Inches(rw), Inches(3.7)).table
        for c, wd in enumerate([0.4, 2.51, 2.51, 2.51]):
            tbl.columns[c].width = Inches(wd)
        rows = [["#", "Given", "When", "Then"]]
        rows += [
            ["1", "{{given1: initial state}}", "{{when1: action}}", "{{then1: observable result}}"],
            ["2", "{{given2: initial state}}", "{{when2: action}}", "{{then2: observable result}}"],
            ["3", "{{given3: initial state}}", "{{when3: action}}", "{{then3: observable result}}"],
            ["4", "{{given4: initial state}}", "{{when4: action}}", "{{then4: observable result}}"],
        ]
        for r, row in enumerate(rows):
            for c, value in enumerate(row):
                cell = tbl.cell(r, c)
                cell.text = ""
                tf = cell.text_frame
                tf.word_wrap = True
                run = tf.paragraphs[0].add_run()
                run.text = value
                run.font.size, run.font.name = Pt(10), FONT
                run.font.bold = r == 0
                run.font.color.rgb = WHITE if r == 0 else INK
                cell.fill.solid()
                cell.fill.fore_color.rgb = INK if r == 0 else WHITE
                cell.vertical_anchor = MSO_ANCHOR.TOP if r else MSO_ANCHOR.MIDDLE
        y = 5.75
        label(sh, rx, y, rw, 0.3, "INVEST check · ✓ where the property holds", size=11, bold=True)
        g = 0.08
        cw = (rw - 5 * g) / 6
        for k, (tag, key) in enumerate([
            ("Independent", "i"), ("Negotiable", "n"), ("Valuable", "v"),
            ("Estimable", "e"), ("Small", "s"), ("Testable", "t"),
        ]):
            xx = rx + k * (cw + g)
            box(sh, xx, y + 0.4, cw, 1.05, line=ACCENT)
            label(sh, xx + 0.04, y + 0.45, cw - 0.08, 0.35, tag, size=10, bold=True, color=ACCENT,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, xx + 0.04, y + 0.82, cw - 0.08, 0.55, line=None), "{{%s: ✓ if yes}}" % key, size=12,
                 bold=True, color=ACCENT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


class StoryMapping(PptxSpec):
    @property
    def rel(self):
        return "product-handoff/story-mapping/story-mapping.pptx"

    example = {"text": {
        "title": "FreshDrop, the buyer's weekly order, September 2026",
        "act1": "Find the product",
        "act2": "Build the basket",
        "act3": "Choose a slot",
        "act4": "Pay",
        "act5": "Track and rate",
        "task1": "search and filters; scan a category",
        "task2": "add items, edit quantities, see the total",
        "task3": "pick a 2-hour window, see the fee",
        "task4": "card or SBP; apply a promo code",
        "task5": "live courier map; rate the order",
        "r1_goal": "Buyers order once, end to end, in Moscow",
        "r2_goal": "Buyers book the same slot each week",
        "r3_goal": "Buyers get reminders and reorder in one tap",
        "s1_1": "Search «milk» with typo fix",
        "s1_2": "Add and edit items in cart",
        "s1_3": "Pick a 2-hour slot",
        "s1_4": "Pay by card",
        "s1_5": "See courier on map",
        "s2_1": "Category filters, sort by price",
        "s2_2": "Saved basket",
        "s2_3": "Fixed weekly slot",
        "s2_4": "Save card for auto-pay",
        "s2_5": "Rate courier, leave a note",
        "s3_1": "Promo banners by history",
        "s3_2": "Reorder last basket",
        "s3_3": "Slot reminder 15 minutes before",
        "s3_4": "Split payment with a partner",
        "s3_5": "Order history with repeat",
    }}

    def draw(self, prs, slide):
        header(slide, "STORY MAPPING", "{{title: product, whose journey, date}}")
        sh = slide.shapes
        x0, lw, g = 0.5, 2.0, 0.08
        n = 5
        cw = (12.33 - lw - g * n) / n
        xs = [x0 + lw + g + i * (cw + g) for i in range(n)]
        label(sh, x0, 1.3, lw, 0.6, "Activities", size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        label(sh, x0, 2.0, lw, 1.1, "Tasks\nin journey order →", size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
        for i, x in enumerate(xs, start=1):
            text(box(sh, x, 1.3, cw, 0.6, fill=INK, line=None),
                 "{{act%d: what the person does, at a high level}}" % i,
                 size=10, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, 2.0, cw, 1.1, fill=ACCENT_BG, line=None),
                 "{{task%d: steps of this activity}}" % i,
                 size=9)
        y, rh = 3.25, 1.24
        for r in range(1, 4):
            line = sh.add_connector(1, Inches(x0), Inches(y - 0.04), Inches(12.83), Inches(y - 0.04))
            line.line.color.rgb = ACCENT if r == 1 else MUTED
            line.line.width = Pt(1.5)
            line.line.dash_style = 4
            box(sh, x0, y, lw, rh, fill=ACCENT_BG if r == 1 else None, line=None)
            label(sh, x0 + 0.02, y + 0.02, lw - 0.04, 0.3, f"Release {r}", size=10, bold=True,
                  color=ACCENT if r == 1 else INK)
            text(box(sh, x0, y + 0.3, lw, rh - 0.3, line=None), "{{r%d_goal: what outcome this slice delivers}}" % r, size=9)
            for i, x in enumerate(xs, start=1):
                text(box(sh, x, y, cw, rh), "{{s%d_%d: story for this activity and release}}" % (r, i), size=9)
            y += rh + 0.08


class UseCase(PptxSpec):
    @property
    def rel(self):
        return "product-handoff/use-case/use-case.pptx"

    example = {"text": {
        "title": "FreshDrop app: the buyer books an express slot",
        "actor": "Moscow buyer (primary actor)",
        "actor2": "Courier dispatch system",
        "system": "FreshDrop app and dispatch",
        "uc1": "Book an express slot",
        "uc2": "Pay for the order",
        "uc3": "Track the courier",
        "uc4": "Apply a promo code (extends booking)",
        "uc5": "Check card or SBP token (always included)",
        "name": "Book an express slot",
        "goal": "Buyer gets a delivery slot within 2 hours for tonight",
        "primary": "Moscow buyer, logged in",
        "pre": "Buyer has items in the cart and a saved address",
        "trigger": "Buyer taps «Choose a slot» in the cart",
        "success": "Slot is held for 15 minutes and shown on the order",
        "minimal": "No slot is charged; the cart is kept",
        "scope": "FreshDrop app and dispatch",
        "level": "User goal",
        "main": "1. Buyer opens the cart. 2. Buyer taps «Choose a slot». 3. App shows free 2-hour windows. 4. Buyer picks 19:00–21:00. 5. App holds the slot and shows the total. 6. Buyer confirms the order.",
        "ext": "3a. No free slots: app offers the next day. 4a. Slot taken while choosing: app shows the free ones again. 6a. Card declined: buyer pays with SBP or changes the card.",
    }}

    def draw(self, prs, slide):
        from pptx.oxml.ns import qn
        header(slide, "USE CASE · USE CASE DIAGRAM", "{{title: system and user goal}}")
        sh = slide.shapes

        def line(a, b, dashed=False, arrow=False, color=INK):
            return connector(sh, a, b, color=color, dash=4 if dashed else None, arrow=arrow)

        def actor(cx, top, key, hint):
            box(sh, cx - 0.22, top, 0.44, 0.44, fill=WHITE, line=INK, kind=MSO_SHAPE.OVAL)
            line((cx, top + 0.44), (cx, top + 1.2))
            line((cx - 0.4, top + 0.7), (cx + 0.4, top + 0.7))
            line((cx, top + 1.2), (cx - 0.3, top + 1.65))
            line((cx, top + 1.2), (cx + 0.3, top + 1.65))
            text(box(sh, cx - 1.0, top + 1.72, 2.0, 0.8, line=None), hint, size=10, bold=True,
                 align=PP_ALIGN.CENTER)

        actor(1.4, 2.6, "actor", "{{actor: primary actor: a role}}")
        actor(11.9, 2.6, "actor2", "{{actor2: external system or second actor}}")
        bx, by, bw, bh = 3.0, 1.35, 7.4, 5.35
        box(sh, bx, by, bw, bh, line=INK)
        text(box(sh, bx + 0.1, by + 0.05, bw - 0.2, 0.35, line=None), "{{system: system boundary: what we build}}",
             size=11, bold=True, color=ACCENT)
        ow, oh = 3.0, 0.95
        pos = {1: (3.35, 1.8), 2: (3.35, 3.4), 3: (3.35, 5.0), 4: (7.05, 1.8), 5: (7.05, 3.4)}
        hints = {1: "{{uc1: main use case: verb and object}}", 2: "{{uc2: use case}}", 3: "{{uc3: use case}}",
                 4: "{{uc4: extension: runs under a condition}}", 5: "{{uc5: shared step that is always included}}"}
        for k, (x, y) in pos.items():
            o = box(sh, x, y, ow, oh, fill=ACCENT_BG if k in (1, 2, 3) else WHITE, line=ACCENT, kind=MSO_SHAPE.OVAL)
            text(o, hints[k], size=10, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        for k in (1, 2, 3):
            x, y = pos[k]
            line((1.85, 3.3), (x, y + oh / 2))
        line((11.45, 3.3), (7.05 + ow, 3.4 + oh / 2))
        line((7.05, 1.8 + oh / 2), (3.35 + ow, 1.8 + oh / 2), dashed=True, arrow=True, color=MUTED)
        label(sh, 6.15, 1.9, 1.1, 0.3, "«extend»", size=9, color=MUTED, align=PP_ALIGN.CENTER)
        line((3.35 + ow, 3.4 + oh / 2), (7.05, 3.4 + oh / 2), dashed=True, arrow=True, color=MUTED)
        label(sh, 6.15, 3.5, 1.1, 0.3, "«include»", size=9, color=MUTED, align=PP_ALIGN.CENTER)
        text(box(sh, 7.05, 5.0, 3.2, 1.5, line=None),
             "\"include\" — the step always runs inside the use case; the arrow points to the included one.\n"
             "\"extend\" — behaviour added under a condition; the arrow points to the extended one.", size=9, color=MUTED)

        slide = prs.slides.add_slide(prs.slide_layouts[6])
        header(slide, "USE CASE · SCENARIO DESCRIPTION", "{{title: system and user goal}}")
        sh = slide.shapes
        lx, lw = 0.5, 4.3

        def field(x, y, w, h, tag, key, hint, size=10, fill=None):
            box(sh, x, y, w, h, fill=fill, line=LINE)
            label(sh, x + 0.05, y + 0.03, w - 0.1, 0.3, tag, size=10, bold=True, color=ACCENT)
            text(box(sh, x, y + 0.3, w, h - 0.3, line=None), hint, size=size)

        y = 1.3
        rows = [
            ("Use case", "name", "{{name: verb + object: what the actor does}}", 0.7),
            ("Goal", "goal", "{{goal: what the primary actor wants to achieve}}", 0.75),
            None,
            ("Primary actor", "primary", "{{primary: role that starts the scenario}}", 0.6),
            ("Preconditions", "pre", "{{pre: what is already true before the start}}", 0.75),
            ("Trigger", "trigger", "{{trigger: event that starts the scenario}}", 0.65),
            ("Success guarantee", "success", "{{success: what is true after successful completion}}", 0.8),
            ("Minimal guarantee", "minimal", "{{minimal: what is true in any outcome}}", 0.65),
        ]
        for row in rows:
            if row is None:
                hw = (lw - 0.08) / 2
                field(lx, y, hw, 0.7, "Scope", "scope", "{{scope: which system is described}}", size=9)
                field(lx + hw + 0.08, y, hw, 0.7, "Level", "level", "{{level: user, subfunction, strategic}}", size=9)
                y += 0.74
                continue
            tag, key, hint, h = row
            field(lx, y, lw, h, tag, key, hint)
            y += h + 0.04
        rx, rw = 5.0, 7.83
        field(rx, 1.3, rw, 3.15, "Main success scenario", "main",
              "{{main: steps in order: who does what, the actor or the system}}", fill=ACCENT_BG)
        field(rx, 4.55, rw, 2.64, "Extensions", "ext",
              "{{ext: step and letter: condition and result}}")


class EntitiesAnalysis(PptxSpec):
    @property
    def rel(self):
        return "product-handoff/entities-analysis/entities-analysis.pptx"

    example = {"text": {
        "title": "FreshDrop order domain: orders, slots, payments and couriers",
        "e1": "Order",
        "e2": "Buyer",
        "e3": "Delivery slot",
        "e4": "Payment",
        "e5": "Promo code",
        "e6": "Courier",
        "e7": "Product",
        "a1": "order id, created at, slot, total in RUB, status",
        "a2": "phone, name, district, address, card token",
        "a3": "date, 2-hour window, capacity, fee in RUB",
        "a4": "amount, method (card, SBP), status, paid at",
        "a5": "code, discount %, valid until, minimum basket",
        "a6": "name, vehicle, district, rating",
        "a7": "SKU, name, unit price, stock, category",
        "m1a": "1", "m1b": "0..*", "r1": "places",
        "m3a": "1", "m3b": "0..*", "r3": "paid by",
        "m2a": "0..*", "m2b": "1", "r2": "booked for",
        "m5a": "1", "m5b": "1..*", "r5": "contains",
        "m6a": "0..*", "m6b": "0..1", "r6": "discounts",
        "m4a": "0..*", "m4b": "1", "r4": "delivered by",
        "rules": "A buyer makes many orders; an order has one slot, one courier, one payment and one promo code. Payments are kept apart to allow retries.",
    }}

    def draw(self, prs, slide):
        from pptx.oxml.ns import qn
        header(slide, "ENTITIES ANALYSIS · ENTITY MODEL", "{{title: subject area and why we build the model}}")
        sh = slide.shapes
        W = {"L": (0.4, 3.0), "C": (4.95, 3.4), "R": (9.9, 3.0)}
        Y = [1.35, 3.55, 5.75]
        H = 1.45
        slots = {1: ("C", 1), 2: ("C", 0), 3: ("L", 1), 4: ("C", 2), 5: ("L", 2), 6: ("R", 0), 7: ("R", 1)}
        names = {1: "{{e1: main noun}}", 2: "{{e2: noun}}", 3: "{{e3: noun}}", 4: "{{e4: noun}}", 5: "{{e5: noun}}", 6: "{{e6: noun}}", 7: "{{e7: noun}}"}
        attrs = {
            1: "{{a1: attributes}}",
            2: "{{a2: attributes}}",
            3: "{{a3: attributes}}",
            4: "{{a4: attributes}}",
            5: "{{a5: attributes}}",
            6: "{{a6: attributes}}",
            7: "{{a7: attributes}}",
        }
        geo = {}
        for k, (col, row) in slots.items():
            x, w = W[col]
            y = Y[row]
            geo[k] = (x, y, w)
            box(sh, x, y, w, H, fill=WHITE, line=INK)
            text(box(sh, x, y, w, 0.42, fill=ACCENT_BG if k == 1 else RGBColor(0xF3, 0xF4, 0xF6), line=INK),
                 names[k], size=11, bold=True,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, y + 0.42, w, H - 0.42, line=None), attrs[k], size=10)

        def line(a, b):
            return connector(sh, a, b, color=INK)

        def small(x, y, w, value, size=9, color=MUTED, align=PP_ALIGN.LEFT):
            s = label(sh, x, y, w, 0.28, value, size=size, color=color, align=align)
            s.text_frame.margin_left = s.text_frame.margin_right = Inches(0.02)
            return s

        # r1: e2 (top) — e1, vertical
        x1, y1, w1 = geo[1]
        cx = x1 + w1 / 2
        line((cx, Y[0] + H), (cx, Y[1]))
        small(cx + 0.05, Y[0] + H + 0.01, 1.0, "{{m1a}}")
        small(cx + 0.05, Y[1] - 0.29, 1.0, "{{m1b}}")
        small(x1, Y[0] + H + 0.22, w1 / 2 - 0.08, "{{r1}}", size=8, align=PP_ALIGN.RIGHT)
        # r3: e1 — e4 (bottom), vertical
        line((cx, Y[1] + H), (cx, Y[2]))
        small(cx + 0.05, Y[1] + H + 0.01, 1.0, "{{m3a}}")
        small(cx + 0.05, Y[2] - 0.29, 1.0, "{{m3b}}")
        small(x1, Y[1] + H + 0.22, w1 / 2 - 0.08, "{{r3}}", size=8, align=PP_ALIGN.RIGHT)

        def horiz(xa, xb, y, ma, mb, rel):
            line((xa, y), (xb, y))
            small(xa + 0.03, y - 0.3, 0.85, ma, size=8)
            small(xb - 0.88, y - 0.3, 0.85, mb, size=8, align=PP_ALIGN.RIGHT)
            small(xa - 0.05, y + 0.03, xb - xa + 0.1, rel, size=8, align=PP_ALIGN.CENTER)

        mid = Y[1] + H / 2
        horiz(W["L"][0] + W["L"][1], W["C"][0], mid, "{{m2a}}", "{{m2b}}", "{{r2}}")
        horiz(W["C"][0] + W["C"][1], W["R"][0], mid, "{{m5a}}", "{{m5b}}", "{{r5}}")
        horiz(W["L"][0] + W["L"][1], W["C"][0], Y[2] + H / 2, "{{m6a}}", "{{m6b}}", "{{r6}}")
        # r4: e6 (top right) — e1, diagonal
        xa, ya = W["R"][0] + 0.4, Y[0] + H
        xb, yb = W["C"][0] + W["C"][1] - 0.3, Y[1]
        line((xa, ya), (xb, yb))
        small(xa + 0.05, ya + 0.02, 0.85, "{{m4a}}", size=8)
        small(xb - 0.9, yb - 0.3, 0.85, "{{m4b}}", size=8, align=PP_ALIGN.RIGHT)
        s4 = small(8.45, 2.3, 1.4, "{{r4}}", size=8)
        s4.height = Inches(0.45)
        s4.text_frame.vertical_anchor = MSO_ANCHOR.BOTTOM

        # legend
        lx, ly = W["L"][0], Y[0]
        box(sh, lx, ly, W["L"][1], H, line=LINE)
        label(sh, lx + 0.08, ly + 0.03, 2.8, 0.28, "UML notation", size=9, bold=True, color=ACCENT)
        rows = [("Association: objects are linked", None), ("Generalisation: \"is a kind of\"", "tri"),
                ("Composition: part of a whole", "dia_full"), ("Aggregation: clarify the meaning", "dia_empty")]
        for i, (name, mark) in enumerate(rows):
            yy = ly + 0.3 + i * 0.21
            line((lx + 0.12, yy + 0.12), (lx + 0.75, yy + 0.12))
            if mark == "tri":
                t_ = box(sh, lx + 0.7, yy + 0.03, 0.18, 0.18, fill=WHITE, line=INK, kind=MSO_SHAPE.ISOSCELES_TRIANGLE)
                t_.rotation = 90
            elif mark:
                box(sh, lx + 0.66, yy + 0.04, 0.24, 0.16, fill=INK if mark == "dia_full" else WHITE, line=INK,
                    kind=MSO_SHAPE.DIAMOND)
            small(lx + 0.92, yy, 2.06, name, size=8, color=INK)
        small(lx + 0.08, ly + H - 0.32, 2.85, "Multiplicity: 1 · 0..1 · 0..* · 1..*", size=8)
        # rules
        rx, rw = W["R"]
        box(sh, rx, Y[2], rw, H, fill=ACCENT_BG, line=LINE)
        label(sh, rx + 0.08, Y[2] + 0.03, rw - 0.16, 0.28, "Rules and decisions", size=9, bold=True, color=ACCENT)
        text(box(sh, rx, Y[2] + 0.3, rw, H - 0.3, line=None),
             "{{rules: business rules and decisions behind the model}}", size=8)


class ProductBacklog(XlsxSpec):
    @property
    def rel(self):
        return "product-handoff/product-backlog/product-backlog.xlsx"

    example = {"text": {
        "title": "FreshDrop delivery team, snapshot 1 September 2026",
        "goal": "buyers plan the week in the app and get the order in a fixed slot",
        "unit": "story points",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Backlog"

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        thin = Side(style="thin", color="C9CED6")

        ws["A1"] = "Product Backlog: {{title: product, team and snapshot date}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:J1")
        ws["A2"] = "Product goal:"
        ws["A2"].font = muted
        ws["C2"] = "{{goal: product goal for the next months}}"
        ws["C2"].font = bold
        ws["C2"].alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells("C2:J2")
        ws.row_dimensions[2].height = 32
        ws["A3"] = "Capacity per sprint:"
        ws["A3"].font = muted
        ws["C3"].font = bold
        ws["C3"].fill = calc_fill
        ws["C3"].comment = Comment("How many size units the team completes on average per sprint — in the same units "
                                   "as the \"Size\" column. Empty — the stock of ready items in sprints is not counted.",
                                   "pdm-skills", width=260, height=100)
        ws["D3"] = "{{unit: size unit}}"
        ws["D3"].font = muted
        ws.merge_cells("D3:F3")

        headers = [
            ("Rank", "Calculated automatically: the row order. Higher means earlier to work on. The product owner sets the order; "
                      "two items cannot share a position.", 8),
            ("Item", "What needs to be done for the product, one row per item. The top of the list holds small, clear items, "
                      "the bottom large and rough ones.", 44),
            ("Type", "Feature, bug, technical work, research or requirement.", 16),
            ("Contribution to the goal", "How the item brings the product goal from row 2 closer. Empty — the item is a candidate for removal.", 30),
            ("Why in this position", "Value, risk, deadline, dependencies — what put the item above or below its neighbours.", 34),
            ("Size", "An estimate by those who will do the work, in the units from row 3. Required for the top items.", 10),
            ("Ready\nfor sprint", "\"yes\" — the team is sure it can finish the item in one sprint: it is understood, estimated and not blocked.", 11),
            ("Requested\nby", "The customer or source of the item: users, support, the regulator, the team.", 16),
            ("Added", "The date the item entered the list. Old items with no movement are candidates for removal.", 12),
            ("Decision", "The outcome of the last review: keep, postpone or delete.", 12),
        ]
        hr = 5
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(hr, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            c.comment = Comment(hint, "pdm-skills", width=260, height=110)
            ws.column_dimensions[c.column_letter].width = width
        ws.row_dimensions[hr].height = 46

        first, last = hr + 1, hr + 100
        for r in range(first, last + 1):
            ws.cell(r, 1, f'=IF(B{r}="","",COUNTA($B${first}:B{r}))').fill = calc_fill
            for c in range(1, 11):
                ws.cell(r, c).font = regular
                ws.cell(r, c).alignment = Alignment(wrap_text=True, vertical="top")
            ws.cell(r, 9).number_format = "DD.MM.YYYY"
        ws.freeze_panes = ws.cell(first, 3)
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'Backlog'!$B${first}")

        rng = lambda col: f"${col}${first}:${col}${last}"
        ws["L5"] = "State of the list"
        ws["L5"].font, ws["L5"].fill = bold, head_fill
        ws["M5"].fill = head_fill
        ws.column_dimensions["L"].width = 34
        ws.column_dimensions["M"].width = 12
        stats = [
            ("Total items", f'=COUNTA({rng("B")})', "Hundreds or thousands of items are a sign of a dumping ground: the top of the list gets lost."),
            ("No contribution to the goal", f'=SUMPRODUCT(({rng("B")}<>"")*({rng("D")}=""))',
             "Items that do not lead to the product goal. Each one raises a question: delete it or change the goal."),
            ("No size estimate", f'=SUMPRODUCT(({rng("B")}<>"")*({rng("F")}=""))',
             "The top of the list needs an estimate, for the bottom a rough one is enough."),
            ("Ready for sprint", f'=COUNTIF({rng("G")},"yes")', "Items that can be taken into the next planning."),
            ("Size of ready items", f'=SUMIF({rng("G")},"yes",{rng("F")})', "The sum of the sizes of ready items."),
            ("Ready stock, sprints", '=IF(OR($C$3="",$C$3=0),"",M10/$C$3)',
             "The size of ready items divided by capacity. Under one sprint — refine the top of the list before planning."),
            ("Older than 6 months", f'=SUMPRODUCT(({rng("I")}<>"")*({rng("I")}<TODAY()-182))',
             "Items added more than half a year ago. Candidates for review."),
            ("Marked \"delete\"", f'=COUNTIF({rng("J")},"delete")', "Remove them from the list after the review."),
        ]
        for i, (name, formula, hint) in enumerate(stats, start=6):
            a = ws.cell(i, 12, name)
            a.font = regular
            a.comment = Comment(hint, "pdm-skills", width=260, height=90)
            b = ws.cell(i, 13, formula)
            b.font, b.fill = bold, calc_fill
            b.number_format = "0.0" if i == 11 else "0"

        def dv_list(values, ref):
            dv = DataValidation(type="list", formula1=f'"{values}"', allow_blank=True, errorStyle="warning",
                                showErrorMessage=True, error=f"Values: {values}")
            dv.add(ref)
            ws.add_data_validation(dv)

        dv_list("feature,bug,technical work,research,requirement", f"C{first}:C{last}")
        dv_list("yes,no", f"G{first}:G{last}")
        dv_list("keep,postpone,delete", f"J{first}:J{last}")
        dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                            errorStyle="warning", showErrorMessage=True, error="Size must be a non-negative number")
        dv.add(f"F{first}:F{last}")
        dv.add("C3")
        ws.add_data_validation(dv)


class ServiceBlueprint(PptxSpec):
    @property
    def rel(self):
        return "product-handoff/service-blueprint/service-blueprint.pptx"

    example = {"text": {
        "title": "FreshDrop: weekly shop by a Moscow parent, now",
        "s1": "Open the app",
        "s2": "Search and add",
        "s3": "Choose a slot",
        "s4": "Pay",
        "s5": "Courier delivers",
        "s6": "Rate and reorder",
        "e1": "App home, search results",
        "e2": "Cart with total and fee",
        "e3": "Slot picker with 2-hour windows",
        "e4": "Card form, SMS code",
        "e5": "SMS and courier map",
        "e6": "Receipt email, rating prompt",
        "c1": "Opens the app, types «milk»",
        "c2": "Adds 15–20 items",
        "c3": "Picks an evening slot",
        "c4": "Enters card, pays",
        "c5": "Waits at the door, checks map",
        "c6": "Rates the courier, reorders",
        "f1": "Search returns in 1 second",
        "f2": "Cart total and substitutions shown",
        "f3": "Slot list updates live",
        "f4": "Payment page, 3-D Secure check",
        "f5": "Courier status pushed",
        "f6": "Rating form, reorder button",
        "b1": "Picker assembles order in dark store",
        "b2": "Picker checks stock and substitutes",
        "b3": "Dispatch books courier by district",
        "b4": "Payment service captures funds",
        "b5": "Courier scans and delivers",
        "b6": "Support reviews low ratings",
        "p1": "Catalog and search index",
        "p2": "Stock and price feed from stores",
        "p3": "Routing software, courier app",
        "p4": "Bank acquirer, SBP",
        "p5": "GPS feed from courier app",
        "p6": "CRM and loyalty points",
        "x1": "Typos miss: 3 of 10 leave search",
        "x2": "Stock gaps: 8% of items",
        "x3": "Slot full: 22% drop at 19:00",
        "x4": "Payment fails: 4.2% of attempts",
        "x5": "Courier 15+ minutes late: 12%",
        "x6": "Low rating: 6% of orders",
    }}

    def draw(self, prs, slide):
        from pptx.enum.dml import MSO_LINE_DASH_STYLE
        from pptx.enum.shapes import MSO_CONNECTOR
        header(slide, "SERVICE BLUEPRINT", "{{title: service, scenario and customer; current or future state}}")
        sh = slide.shapes
        lx, lw, gx, n = 0.5, 1.75, 2.3, 6
        cw = (12.83 - gx) / n
        top, hh = 1.25, 0.42
        label(sh, lx, top, lw, hh, "Steps", size=10, bold=True, color=ACCENT, anchor=MSO_ANCHOR.MIDDLE)
        for i in range(n):
            text(box(sh, gx + i * cw + 0.03, top, cw - 0.06, hh, fill=ACCENT, line=None),
                 "{{s%d: step name}}" % (i + 1), size=9, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
        rows = [
            ("Evidence", "e", "", WHITE),
            ("Customer actions", "c", "", ACCENT_BG),
            ("Frontstage", "f", "", WHITE),
            ("Backstage", "b", "", WHITE),
            ("Support processes", "p", "", WHITE),
            ("Failures and time", "x", "", BAD_BG),
        ]
        y, rh, gap, wide = top + hh + 0.08, 0.78, 0.08, 0.26
        ys = []
        for r, (tag, key, hint, fill) in enumerate(rows):
            label(sh, lx, y, lw, rh, tag, size=10, bold=True, color=BAD if key == "x" else INK,
                  anchor=MSO_ANCHOR.MIDDLE)
            for i in range(n):
                blueprint = {
                    "e": ["{{e1: what the customer sees and holds}}", "{{e2: what the customer sees and holds}}", "{{e3: what the customer sees and holds}}", "{{e4: what the customer sees and holds}}", "{{e5: what the customer sees and holds}}", "{{e6: what the customer sees and holds}}"],
                    "c": ["{{c1: what the customer does}}", "{{c2: what the customer does}}", "{{c3: what the customer does}}", "{{c4: what the customer does}}", "{{c5: what the customer does}}", "{{c6: what the customer does}}"],
                    "f": ["{{f1: what visible staff and systems do}}", "{{f2: what visible staff and systems do}}", "{{f3: what visible staff and systems do}}", "{{f4: what visible staff and systems do}}", "{{f5: what visible staff and systems do}}", "{{f6: what visible staff and systems do}}"],
                    "b": ["{{b1: what hidden staff do, and who owns it}}", "{{b2: what hidden staff do, and who owns it}}", "{{b3: what hidden staff do, and who owns it}}", "{{b4: what hidden staff do, and who owns it}}", "{{b5: what hidden staff do, and who owns it}}", "{{b6: what hidden staff do, and who owns it}}"],
                    "p": ["{{p1: systems, data, other departments, partners}}", "{{p2: systems, data, other departments, partners}}", "{{p3: systems, data, other departments, partners}}", "{{p4: systems, data, other departments, partners}}", "{{p5: systems, data, other departments, partners}}", "{{p6: systems, data, other departments, partners}}"],
                    "x": ["{{x1: where it breaks, how long, metric}}", "{{x2: where it breaks, how long, metric}}", "{{x3: where it breaks, how long, metric}}", "{{x4: where it breaks, how long, metric}}", "{{x5: where it breaks, how long, metric}}", "{{x6: where it breaks, how long, metric}}"],
                }[key]
                text(box(sh, gx + i * cw + 0.03, y, cw - 0.06, rh, fill=fill,
                         line=None if fill != WHITE else LINE),
                     blueprint[i], size=8)
            ys.append(y)
            y += rh + (wide if r in (1, 2, 3) else gap)

        def divider(after, name):
            yy = ys[after] + rh + wide / 2
            c = sh.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(lx), Inches(yy), Inches(12.83), Inches(yy))
            c.line.color.rgb = ACCENT
            c.line.width = Pt(1.25)
            c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
            lbl = label(sh, lx, yy + 0.01, 3.0, 0.14, name, size=8, color=ACCENT)
            lbl.text_frame.margin_top = lbl.text_frame.margin_bottom = Inches(0)

        divider(1, "line of interaction")
        divider(2, "line of visibility")
        divider(3, "line of internal interaction")


class ProductRequirementsDocument(PptxSpec):
    @property
    def rel(self):
        return "product-handoff/product-requirements-document/product-requirements-document.pptx"

    example = {"text": {
        "title": "FreshDrop reminder feature, PRD v1.2, 1 September 2026",
        "background": "1 in 3 buyers misses an evening slot (survey, 420 answers); support gets 60 calls a week",
        "goals": "Cut missed slots by 30% by Q4 2026; not in scope: SMS and web reminders",
        "segment": "Moscow families who order weekly; they plan the week on Sunday",
        "market": "About 180,000 weekly buyers in Moscow; a push costs 0.3 RUB",
        "proposal": "A push 15 minutes before the slot with a one-tap change",
        "risks": "Buyers turn push off: test with 50 buyers; opt-out must stay below 10%",
        "solution": "Push at slot minus 15 minutes; change or cancel in one tap; mockups in Figma v3",
        "plan": "3 sprints, 2 mobile engineers, 1 tester; launch after the QA gate on 20 September",
        "launch": "500 weekly buyers in Khimki first; in-app banner and push; support briefed",
        "postlaunch": "Success: missed slots below 6%. Failure: opt-out above 20% means rollback",
        "decision": "Engineers can build it and the tester can check each requirement; hand off to development on 1 October",
    }}

    def draw(self, prs, slide):
        header(slide, "PRODUCT REQUIREMENTS DOCUMENT",
               "{{title: product or feature, document version and date}}")
        sh = slide.shapes
        rows = [
            ("1. Purpose", "Why we build it", [
                ("Background", "background", "what prompted the work, links"),
                ("Business & Product Goals", "goals", "goals with metrics, and non-goals"),
            ]),
            ("2. Customer & Value", "Who it is for and what value", [
                ("Customer Segment", "segment", "segment, needs and current solution"),
                ("Market & Business Analysis", "market", "segment size and economics"),
                ("Proposal & Value Propositions", "proposal", "customer benefit and value delta"),
                ("Risk Assumptions", "risks", "riskiest hypotheses and their tests"),
            ]),
            ("3. Solution", "What we build", [
                ("Solution", "solution", "product properties, scope, mockups"),
                ("Project Plan", "plan", "steps, resources and launch criteria"),
            ]),
            ("4. Execution", "How we launch", [
                ("Launch Strategy", "launch", "early adopters, channels, operations"),
                ("Post-Launch Plan", "postlaunch", "actions on success and on failure"),
            ]),
        ]
        x0, lw, gap = 0.5, 1.75, 0.1
        bx = x0 + lw + gap
        bw_total = 12.83 - bx
        y, rh, rg = 1.25, 1.2, 0.08
        for name, sub, blocks in rows:
            box(sh, x0, y, lw, rh, fill=INK, line=None)
            label(sh, x0 + 0.04, y + 0.1, lw - 0.08, 0.5, name, size=11, bold=True, color=WHITE)
            label(sh, x0 + 0.04, y + 0.62, lw - 0.08, 0.5, sub, size=9, color=WHITE)
            n = len(blocks)
            w = (bw_total - gap * (n - 1)) / n
            for i, (tag, key, hint) in enumerate(blocks):
                x = bx + i * (w + gap)
                box(sh, x, y, w, rh)
                label(sh, x + 0.04, y + 0.02, w - 0.08, 0.28, tag, size=9 if n > 3 else 10, bold=True, color=ACCENT)
                text(box(sh, x + 0.04, y + 0.3, w - 0.08, rh - 0.34, line=None),
                     "{{%s: %s}}" % (key, hint), size=9)
            y += rh + rg
        box(sh, x0, y, 12.33, 0.85, fill=ACCENT_BG, line=ACCENT)
        label(sh, x0 + 0.06, y + 0.02, 12.2, 0.28, "Handoff readiness and decision", size=10, bold=True, color=ACCENT)
        text(box(sh, x0 + 0.06, y + 0.3, 12.2, 0.52, line=None),
             "{{decision: hand off to development or send back}}",
             size=9)


class ScreenMap(PptxSpec):
    @property
    def rel(self):
        return "product-handoff/screen-map/screen-map.pptx"

    example = {"text": {
        "title": "FreshDrop app, slot reminder release, 14 screens",
        "s1": "Home: «Book a slot» button, slot list, new",
        "s2": "Slot picker: day and time grid, existing",
        "s3": "Address check: map pin, existing",
        "s4": "Reminder settings: 15 min before, new",
        "s5": "Order summary: slot, total, pay, existing",
        "scenario": "The buyer sets a reminder for a booked slot, from the slot picker to the confirmation toast",
        "change": "Added: reminder settings screen. Changed: home gets a «Book a slot» button. Nothing removed",
        "transitions": "Home → Slot picker (user taps «Book a slot»); Slot picker → Reminder settings (user toggles the reminder); Reminder settings → Order summary (system saves and returns)",
        "states": "Slot picker: skeleton while loading, «no slots» empty state; Address check: full-screen error when the address is out of the zone",
        "affected": "Push service (notifications team) sends the reminder; the courier app is out of scope",
        "decision": "Reminder kept as a separate screen, not a modal: it is reused from the order page; day and time pickers merged into one",
        "check": "Click-test on 6 buyers: all 6 set the reminder without help; time-to-set not measured, only success",
    }}

    def draw(self, prs, slide):
        header(slide, "SCREEN MAP",
               "{{title: product, change and number of screens}}")
        sh = slide.shapes

        def block(x, y, w, h, tag, key, hint, fill=ACCENT_BG, color=ACCENT, size=10):
            box(sh, x, y, w, h, fill=fill, line=None)
            label(sh, x + 0.06, y + 0.02, w - 0.12, 0.36, tag, size=12, bold=True, color=color)
            tb = text(box(sh, x + 0.06, y + 0.38, w - 0.12, h - 0.42, line=None), "{{%s: %s}}" % (key, hint), size=size)
            tb.text_frame.paragraphs[0].space_after = Pt(3)

        block(0.5, 1.25, 6.05, 1.1, "User scenario", "scenario",
              "what the person does, start and end")
        block(6.78, 1.25, 6.05, 1.1, "What changes on the map", "change",
              "screens added, removed, merged or moved")

        def screen(x, y, w, h, key, hint):
            s = box(sh, x, y, w, h, fill=WHITE, line=ACCENT)
            text(s, "{{%s: %s}}" % (key, hint), size=9, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        screen(0.5, 3.0, 2.6, 1.5, "s1", "entry screen: name, contents, note")
        screen(3.8, 2.55, 2.6, 1.2, "s2", "second-level screen: name, contents, note")
        screen(3.8, 4.15, 2.6, 1.2, "s3", "second-level screen: name, contents, note")
        screen(7.1, 2.55, 2.4, 1.2, "s4", "third-level screen: name, contents, note")
        screen(7.1, 4.15, 2.4, 1.2, "s5", "third-level screen: name, contents, note")
        screen_map_arrow(sh, 3.1, 3.5, 3.8, 3.15)
        screen_map_arrow(sh, 3.1, 4.0, 3.8, 4.75)
        screen_map_arrow(sh, 6.4, 3.15, 7.1, 3.15)
        screen_map_arrow(sh, 6.4, 4.75, 7.1, 4.75)

        block(9.7, 2.55, 3.13, 1.5, "Transitions", "transitions",
              "from, to and trigger", fill=WHITE, color=MUTED)
        block(9.7, 4.15, 3.13, 1.2, "Screen states", "states",
              "loading, data, empty and error states", fill=WHITE, color=MUTED)

        block(0.5, 5.5, 4.0, 1.25, "Affected and not shown", "affected",
              "affected screens of other teams")
        block(4.65, 5.5, 4.2, 1.25, "Decision on the map", "decision",
              "kept, merged, removed or added, and why", fill=GOOD_BG, color=GOOD)
        block(9.0, 5.5, 3.83, 1.25, "Check and result", "check",
              "how it was checked and the result")

        label(sh, 0.5, 6.85, 12.33, 0.4,
              "Legend: rectangle = screen, arrow = transition.",
              size=10, color=MUTED)


class SequenceDiagrams(PptxSpec):
    @property
    def rel(self):
        return "product-handoff/sequence-diagrams/sequence-diagrams.pptx"

    example = {"text": {
        "title": "FreshDrop, buyer pays for an express slot",
        "participant_1": "Buyer",
        "participant_2": "FreshDrop app",
        "participant_3": "Slot service",
        "participant_4": "Bank payment API",
        "m1": "1. initiator's message",
        "m2": "2. call to an internal participant",
        "m3": "3. request to the external system",
        "m4": "4. response from the external system",
        "m5": "5a. service result to the screen on success",
        "m6": "5b. reason to the screen on failure or silence",
        "m7": "6. screen result to the initiator",
        "g1": "[payment succeeded]",
        "g2": "else: payment failed or timeout",
        "scope": "One scenario: a buyer pays for a 2-hour express slot; starts at «Pay», ends at order confirmation",
        "decision": "Add a 3-second timeout with one retry on the payment call; confirm the result asynchronously from the bank",
        "gaps": "The 3-D Secure branch, the 5-minute slot hold and the courier notice are collapsed",
    }}

    def draw(self, prs, slide):
        header(slide, "SEQUENCE DIAGRAMS",
               "{{title: scenario and product, one line}}")
        sh = slide.shapes

        # participants and lifelines
        for i, x in enumerate(CX):
            s = box(sh, x - 0.9, 1.3, 1.8, 0.6, fill=ACCENT_BG, line=ACCENT)
            text(s, "{{participant_%d: participant name}}" % (i + 1), size=10, bold=True, color=INK,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            line(sh, x, TOP, x, BOTTOM, color=LINE, width=1, dash=MSO_LINE.DASH)

        def msg(key, hint, a, b, y, reply=False, color=MUTED):
            x1, x2 = CX[a], CX[b]
            line(sh, x1, y, x2, y, color=color, width=1.5,
                 dash=MSO_LINE.DASH if reply else None, head="arrow" if reply else "triangle")
            lx = min(x1, x2) + 0.04
            label(sh, lx, y - 0.47, abs(x2 - x1) - 0.08, 0.46, "{{%s: %s}}" % (key, hint), size=9,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM)

        msg("m1", "message 1 text", 0, 1, 2.4)
        msg("m2", "message 2 text", 1, 2, 2.85)
        msg("m3", "message 3 text", 2, 3, 3.3)
        msg("m4", "message 4 text", 3, 2, 3.75, reply=True)

        # alt block: normal outcome and failure
        fy, fh = 3.95, 2.0
        frame = box(sh, 0.55, fy, 9.0, fh, fill=None, line=MUTED)
        tab = box(sh, 0.55, fy, 0.55, 0.28, fill=MUTED, line=None)
        text(tab, "alt", size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        label(sh, 1.15, fy, 8.3, 0.3, "{{g1: main branch condition}}", size=10, bold=True, color=GOOD)
        msg("m5", "message 5a text", 2, 1, 4.75, color=GOOD)
        line(sh, 0.55, 5.0, 9.55, 5.0, color=MUTED, width=1, dash=MSO_LINE.DASH)
        label(sh, 1.15, 5.0, 8.3, 0.3, "{{g2: else condition}}", size=10, bold=True, color=BAD)
        msg("m6", "message 5b text", 2, 1, 5.7, color=BAD)

        msg("m7", "message 6 text", 1, 0, 6.45)

        # right column
        def block(y, h, tag, key, hint, fill=ACCENT_BG, color=ACCENT):
            x, w = 10.0, 2.83
            box(sh, x, y, w, h, fill=fill, line=None)
            label(sh, x + 0.06, y + 0.02, w - 0.12, 0.32, tag, size=12, bold=True, color=color)
            tb = text(box(sh, x + 0.06, y + 0.36, w - 0.12, h - 0.4, line=None), "{{%s: %s}}" % (key, hint), size=10)
            tb.text_frame.paragraphs[0].space_after = Pt(3)

        block(1.3, 1.65, "Scenario and boundaries", "scope", "scenario and its boundaries")
        block(3.1, 1.95, "Decision on the diagram", "decision", "decision on the diagram",
              fill=GOOD_BG, color=GOOD)
        block(5.2, 1.5, "What the diagram lacks", "gaps", "what the diagram lacks", fill=WHITE, color=MUTED)

        label(sh, 0.5, 6.85, 12.33, 0.45,
              "Legend: rectangle on top = participant, dashed line down = lifeline, filled arrow = call, dashed arrow = response, alt frame = choice of one branch.",
              size=10, color=MUTED)


class StateModelling(PptxSpec):
    @property
    def rel(self):
        return "product-handoff/state-modelling/state-modelling.pptx"

    example = {"text": {
        "title": "FreshDrop order, from placed to delivered",
        "entity": "A grocery order. The lifecycle starts when the buyer pays and ends at delivery or refund",
        "scope": "Events from the app, the warehouse system and the courier app. Payment internals are outside the model",
        "s1": "paid: money captured, the order waits for assembly",
        "s2": "assembling: a picker collects items in the dark store",
        "s3": "assembled: all items packed and weighed",
        "s4": "handed to courier: the order left the store",
        "s5": "on the way: the courier is driving to the address",
        "s6": "at the door: the courier arrived and waits for the buyer",
        "s7": "pending check: the buyer checks the items",
        "e1": "completed: the buyer accepted the order",
        "e2": "refunded: cancelled or returned, money back",
        "start": "order paid",
        "t8": "item complaint [within 24 h] → back to assembling for the missing item",
        "tc": "cancel: buyer [before assembly], support [no courier 2 h]",
        "t1": "assembly started [store confirmed capacity]",
        "t2": "assembly done [all items found or replaced]",
        "t3": "courier assigned [courier within 1 km]",
        "t4": "courier picked up [bag scan matches]",
        "t5": "courier arrived [GPS within 100 m]",
        "t6": "handover done [buyer confirmed]",
        "t7": "check passed [no claims within 15 min]",
        "t9": "claim accepted [photo] → refund",
        "forbidden": "paid → on the way; pending check → assembling; refunded → any state",
        "gaps": "No state for «buyer unreachable»: support handles it by phone, outside the model",
        "decision": "7 states and the refund branch agreed with dev and support, recorded in the PRD; «buyer unreachable» state scheduled for the next release",
    }}

    def draw(self, prs, slide):
        header(slide, "STATE MODELLING",
               "{{title: entity and system}}")
        sh = slide.shapes

        def block(x, y, w, h, tag, key, hint, fill=ACCENT_BG, color=ACCENT, size=10):
            box(sh, x, y, w, h, fill=fill, line=None)
            label(sh, x + 0.06, y + 0.02, w - 0.12, 0.34, tag, size=12, bold=True, color=color)
            tb = text(box(sh, x + 0.06, y + 0.36, w - 0.12, h - 0.4, line=None), "{{%s: %s}}" % (key, hint), size=size)
            tb.text_frame.paragraphs[0].space_after = Pt(3)

        block(0.5, 1.2, 6.05, 0.8, "Entity", "entity",
              "object and its lifecycle", size=9)
        block(6.78, 1.2, 6.05, 0.8, "What the model describes", "scope",
              "events changing states, and exclusions", size=9)

        W, H = 1.4, 0.8

        def state(x, y, key, final=False, hint="state name and meaning"):
            s = box(sh, x, y, W, H, fill=WHITE, line=INK if final else ACCENT, kind=MSO_SHAPE.ROUNDED_RECTANGLE)
            s.line.width = Pt(3 if final else 1.5)
            text(s, "{{%s: %s}}" % (key, hint), size=8, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

        def tlabel(x, y, w, h, key, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM, hint="event and condition"):
            text(box(sh, x, y, w, h, line=None), "{{%s: %s}}" % (key, hint), size=8, color=MUTED, align=align, anchor=anchor)

        TOP, BOT = 2.55, 4.2
        XS = [1.0 + i * 1.7 for i in range(7)]
        mid = TOP + H / 2
        dot = box(sh, 0.35, mid - 0.15, 0.3, 0.3, fill=INK, line=None, kind=MSO_SHAPE.OVAL)
        dot.name = "initial"
        for i, key in enumerate(["s1", "s2", "s3", "s4", "s5", "s6"]):
            state(XS[i], TOP, key)
        state(XS[6], TOP, "e1", final=True, hint="final success state")
        state(XS[1], BOT, "s7")
        state(XS[4], BOT, "e2", final=True, hint="final failure state")

        state_modelling_arrow(sh, 0.65, mid, XS[0], mid)
        for i in range(6):
            state_modelling_arrow(sh, XS[i] + W, mid, XS[i + 1], mid)
        state_modelling_arrow(sh, XS[1] + 0.3, TOP + H, XS[1] + 0.3, BOT)
        state_modelling_arrow(sh, XS[1] + 1.1, BOT, XS[1] + 1.1, TOP + H)
        state_modelling_arrow(sh, XS[1] + W, BOT + H / 2, XS[4], BOT + H / 2)
        state_modelling_arrow(sh, XS[1] + W, TOP + H, XS[4], BOT + 0.15)
        state_modelling_arrow(sh, XS[2] + 0.7, TOP + H, XS[4] + 0.5, BOT)
        state_modelling_arrow(sh, XS[5] + 0.3, TOP + H, XS[4] + W - 0.2, BOT)

        tlabel(0.2, 1.97, 1.0, 0.5, "start", hint="initial event")
        for i in range(6):
            c = XS[i] + W + 0.15
            tlabel(c - 0.6, 1.97, 1.2, 0.5, f"t{i + 1}")
        tlabel(1.0, 3.5, XS[1] + 0.25 - 1.0, 0.6, "t7", align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
        tlabel(XS[1] - 0.5, 5.0, 3.0, 0.42, "t8", anchor=MSO_ANCHOR.TOP, hint="return transition event and condition")
        tlabel(XS[1] + W + 0.3, BOT + 0.05, 2.4, 0.3, "t9")
        # label above the diagonal cancel arrows (to e2), listing the source states
        tlabel(XS[3] + 0.7, TOP + H + 0.02, 2.75, 0.4, "tc", align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
               hint="cancel event and source states")

        block(0.5, 5.45, 4.7, 1.35, "Forbidden transitions", "forbidden",
              "{{forbidden: forbidden transition lines}}",
              fill=BAD_BG, color=BAD)
        block(5.35, 5.45, 3.75, 1.35, "Assumptions and what is not shown", "gaps",
              "{{gaps: missing states and transitions}}", fill=WHITE, color=MUTED)
        block(9.25, 5.45, 3.58, 1.35, "Decision on the model", "decision",
              "{{decision: agreed states, rules and reasons}}",
              fill=GOOD_BG, color=GOOD)

        label(sh, 0.5, 6.85, 12.33, 0.4,
              "Legend: black circle = start; rounded frame = state; thick frame = final; arrow (→) = transition, label \"event [condition] / action\".",
              size=10, color=MUTED)
