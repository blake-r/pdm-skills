from .base import *


class FinancialModeling(XlsxSpec):
    @property
    def rel(self):
        return "business-validation/financial-modeling/financial-modeling.xlsx"

    example = {"text": {
        "hypothesis": "if 8% of buyers take a slot at 149 rub, the margin per order is positive",
        "task": "forward: target margin computed from the initial metrics",
        "unit_period": "order; a month; the data comes from the finance report",
        "decision": "test the slot in 2 districts for 6 weeks; change the price if the margin is below 80 rub; check on 15 November 2026",
        "title": "FreshDrop, express slots, Moscow, September 2026",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Financial model"

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        in_fill = PatternFill("solid", fgColor="FFF7E0")
        thin = Side(style="thin", color="C9CED6")

        def note(cell, hint, height=100):
            return comment(cell, hint, height=height, width=300)

        ws["A1"] = "Financial Modeling: {{title: business, product or channel, date of calculation}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:G1")
        top = [
            (2, "Hypothesis:", "{{hypothesis: business-model hypothesis and its conditions}}", 46),
            (3, "Task:", "{{task: forward or inverse; boundary conditions}}", 32),
            (4, "Unit and period:", "{{unit_period: unit, period, and data source}}", 32),
            (5, "Decision:", "{{decision: result of the calculation, and its check}}", 46),
        ]
        for r, name, token, height in top:
            ws.cell(r, 1, name).font = muted
            ws.cell(r, 1).alignment = Alignment(vertical="top")
            c = ws.cell(r, 3, token)
            c.font = regular
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.merge_cells(f"C{r}:G{r}")
            ws.row_dimensions[r].height = height

        heads = [
            ("Metric group", "Metric group by PAF (Product Architecture Framework): product creation, acquisition, sales, logistics, retention, upsell, support. A hint on which cost lines not to forget.", 42),
            ("Metric", "Model metric. You fill rows 8–14; the Calculation block and sensitivity are computed automatically.", 56),
            ("Unit", "What the metric is measured in.", 14),
            ("Pessimistic", "Scenario with assumptions worse than expected. One scenario is one set of assumptions for all rows.", 27),
            ("Base", "Expected scenario. The sensitivity below is computed from it.", 27),
            ("Optimistic", "Scenario with assumptions better than expected.", 27),
            ("Basis", "Where the number comes from: fact (source, date), estimate, company goal or hypothesis. A model without experimental data remains an a priori hypothesis; this must be visible in the basis.", 62),
        ]
        hr = 7
        for i, (t, h, w) in enumerate(heads, start=1):
            c = ws.cell(hr, i, t)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            note(c, h, 90)
            ws.column_dimensions[c.column_letter].width = w
        ws.row_dimensions[hr].height = 32

        inputs = [
            ("Sales and acquisition", "Volume: units per period", "pcs", "#,##0",
             "How many growth units per period: customers, orders, stores. From a budget: budget ÷ cost of a lead × conversion to a customer."),
            ("Sales", "Revenue per unit per period", "currency units", "#,##0.00",
             "Average check × number of orders per unit per period, excluding VAT and after returns."),
            ("Creation, logistics, support", "Variable costs, share of revenue", "share 0–1", "0.0%",
             "Share of revenue spent per unit: cost of goods, delivery, payment fees, returns, support. Enter 0.65 or 65%."),
            ("Acquisition", "One-off launch cost per unit", "currency units", "#,##0.00",
             "Cost of acquiring a customer or investment in opening one unit. Advertising plus salaries and acquisition tools, not only the ad budget."),
            ("Product creation", "Fixed costs of the period", "currency units", "#,##0.00",
             "Costs independent of volume: development, servers, staff, office."),
            ("Criterion", "Target net profit over the payback term", "currency units", "#,##0.00",
             "Net profit over the allowed payback term (row below) at which the hypothesis counts as confirmed. Set it before looking at results. Empty if there is no profit criterion. Requires the allowed term."),
            ("Criterion", "Allowed payback term, periods", "periods", "0.00",
             "In how many periods a unit must repay its launch cost; it is also the horizon of net profit. The period is the same as in the table. Convert months to periods: 20 months ÷ 12 ≈ 1.67 years. Empty if there is no criterion."),
        ]
        first = hr + 1
        for k, (g, m, u, fmt, hint) in enumerate(inputs):
            r = first + k
            for c, v in enumerate((g, m, u), start=1):
                ws.cell(r, c, v).font = regular
                ws.cell(r, c).alignment = Alignment(wrap_text=True, vertical="top")
            note(ws.cell(r, 2), hint, 110)
            for c in range(4, 7):
                ws.cell(r, c).alignment = Alignment(vertical="top")
                ws.cell(r, c).number_format = fmt
                ws.cell(r, c).fill = in_fill
                ws.cell(r, c).font = regular
            ws.cell(r, 7).font = regular
            ws.cell(r, 7).alignment = Alignment(wrap_text=True, vertical="top")
        last = first + len(inputs) - 1  # 14
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'Financial model'!$D${first}")

        dv_share = DataValidation(type="decimal", operator="between", formula1="0", formula2="1", allow_blank=True,
                                  errorStyle="warning", showErrorMessage=True, error="Share from 0 to 1: enter 0.65 or 65%.")
        dv_share.add("D10:F10")
        dv_pos = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                                errorStyle="warning", showErrorMessage=True, error="A number not less than zero is required.")
        for rng in ("D8:F9", "D11:F14"):
            dv_pos.add(rng)
        ws.add_data_validation(dv_share)
        ws.add_data_validation(dv_pos)

        # calculation
        ws.cell(16, 1, "Calculation (formulas)").font = bold
        for c in range(1, 8):
            ws.cell(16, c).fill = head_fill
        for c, t in zip((4, 5, 6), ("Pessimistic", "Base", "Optimistic")):
            ws.cell(16, c, t).font = bold
        calc = []

        def N(c): return f"{c}8"
        def R(c): return f"{c}9"
        def V(c): return f"{c}10"
        def C(c): return f"{c}11"
        def F(c): return f"{c}12"
        def T(c): return f"{c}13"
        def P(c): return f"{c}14"

        rows = [
            ("Revenue", "currency units", "#,##0.00", lambda c: f'=IF(AND(ISNUMBER({N(c)}),ISNUMBER({R(c)})),{N(c)}*{R(c)},"")',
             "Volume × revenue per unit."),
            ("Contribution of a unit per period", "currency units", "#,##0.00", lambda c: f'=IF(AND(ISNUMBER({R(c)}),ISNUMBER({V(c)})),ROUND({R(c)}*(1-{V(c)}),6),"")',
             "Revenue per unit minus variable costs: how much a unit leaves per period."),
            ("Payback of a unit, periods", "periods", "0.00", lambda c: f'=IF(AND(ISNUMBER({C(c)}),ISNUMBER({c}18)),IF({c}18>0,{C(c)}/{c}18,"does not pay back"),"")',
             "One-off launch cost ÷ contribution of a unit per period."),
            ("Profit of a period after launch has paid back", "currency units", "#,##0.00", lambda c: f'=IF(AND(ISNUMBER({N(c)}),ISNUMBER({c}18),ISNUMBER({F(c)})),{N(c)}*{c}18-{F(c)},"")',
             "Volume × contribution of a unit − fixed costs. Launch cost is not included here: it is accounted for in the payback term and in net profit over the term."),
            ("Net profit over the payback term", "currency units", "#,##0.00", lambda c: f'=IF(AND(ISNUMBER({c}20),ISNUMBER({P(c)}),ISNUMBER({N(c)}),ISNUMBER({C(c)})),{P(c)}*{c}20-{N(c)}*{C(c)},"")',
             "Allowed term × profit of a period − volume × launch cost. The horizon is the same for payback and for profit, so the criteria are consistent."),
            ("Break-even, units", "pcs", "#,##0", lambda c: f'=IF(AND(ISNUMBER({F(c)}),ISNUMBER({c}18)),IF({c}18>0,{F(c)}/{c}18,"not reached"),"")',
             "Fixed costs ÷ contribution of a unit: how many units cover the fixed costs of the period once launch has paid back."),
            ("Limit of launch cost by payback", "currency units", "#,##0.00", lambda c: f'=IF(AND(ISNUMBER({P(c)}),ISNUMBER({c}18)),{P(c)}*{c}18,"")',
             "Inverse problem: allowed term × contribution of a unit. Above this amount a unit will not pay back in time."),
            ("Limit of launch cost by target profit", "currency units", "#,##0.00", lambda c: f'=IF(AND(ISNUMBER({N(c)}),ISNUMBER({F(c)}),ISNUMBER({T(c)}),ISNUMBER({P(c)}),ISNUMBER({c}18)),IF({N(c)}>0,{P(c)}*{c}18-({P(c)}*{F(c)}+{T(c)})/{N(c)},""),"")',
             "Inverse problem: allowed term × contribution of a unit − (allowed term × fixed costs + target profit) ÷ volume. Above this amount the target profit over the term is not reached."),
            ("Limit of launch cost per unit", "currency units", "#,##0.00", lambda c: f'=IF(COUNT({c}23:{c}24)=0,"",MIN({c}23:{c}24))',
             "The smaller of the two limits: the launch cost assumption must fit within both. There are many solutions; you choose the boundary conditions."),
            ("Margin to the launch cost limit", "currency units", "#,##0.00", lambda c: f'=IF(AND(ISNUMBER({c}25),ISNUMBER({C(c)})),{c}25-{C(c)},"")',
             "Limit of launch cost minus the assumption. A negative margin means the assumption does not fit the criteria."),
            ("Payback within the criterion", "yes / no", "General", lambda c: f'=IF(AND(ISNUMBER({P(c)}),ISNUMBER({c}19)),IF({c}19<={P(c)},"yes","no"),IF(AND(ISNUMBER({P(c)}),{c}19="does not pay back"),"no",""))',
             "Comparison of the payback term with the criterion."),
            ("Net profit over the term not below target", "yes / no", "General", lambda c: f'=IF(AND(ISNUMBER({T(c)}),ISNUMBER({c}21)),IF({c}21>={T(c)},"yes","no"),"")',
             "Comparison of net profit over the payback term with the target."),
            ("Verdict", "", "General", lambda c: f'=IF(AND({c}27="",{c}28=""),"no data for the criteria",IF(OR({c}27="no",{c}28="no"),"does not add up","adds up on paper")&IF(OR({c}27="",{c}28="")," (one criterion)",""))',
             "A signal, not a decision: \"does not add up\" means change the assumptions or the criterion, \"adds up on paper\" means facts are needed. A model without experimental data is an a priori hypothesis: \"adds up\" means \"worth testing in the real world\". If only one criterion is set, the verdict is marked."),
        ]
        for k, (name, unit, fmt, fn, hint) in enumerate(rows):
            r = 17 + k
            ws.cell(r, 2, name).font = regular
            ws.cell(r, 3, unit).font = muted
            note(ws.cell(r, 2), hint, 100)
            for col in "DEF":
                cell = ws[f"{col}{r}"]
                cell.value = fn(col)
                cell.fill = calc_fill
                cell.number_format = fmt
                cell.font = bold if name == "Verdict" else regular
                cell.alignment = Alignment(wrap_text=True, vertical="top")
            ws.cell(r, 2).alignment = Alignment(wrap_text=True, vertical="top")
            ws.cell(r, 3).alignment = Alignment(wrap_text=True, vertical="top")
            if len(name) > 40:
                ws.row_dimensions[r].height = 32
        ws.row_dimensions[29].height = 62

        # sensitivity
        ws.cell(31, 1, "Sensitivity of the base scenario").font = bold
        for c in range(1, 8):
            ws.cell(31, c).fill = head_fill
        ws.cell(32, 2, "Assumption shift, ± share").font = regular
        s = ws["E32"]
        s.value = 0.1
        s.number_format = "0%"
        s.fill = in_fill
        s.font = regular
        note(ws.cell(32, 2), "By how many percent each assumption is shifted up and down. 10% is the starting value; focus on the assumptions you know least.", 80)
        for c, t in zip((4, 5, 6, 7), ("Profit at −shift", "Profit at +shift", "Swing", "Impact rank")):
            h = ws.cell(33, c, t)
            h.font, h.fill = bold, head_fill
            h.alignment = Alignment(wrap_text=True, vertical="center")
        note(ws.cell(33, 6), "Absolute difference in net profit over the payback term between \"+shift\" and \"−shift\". The larger it is, the more the assumption affects the outcome.", 70)
        note(ws.cell(33, 7), "Rank 1 is the most influential assumption. With equal swing the rank may be shared.", 60)
        ws.row_dimensions[33].height = 48
        ws.cell(33, 2, "Assumption").font = bold
        ws.cell(33, 2).alignment = Alignment(vertical="center")
        ws.cell(33, 2).fill = head_fill
        n, r_, v, c_, f, p = "$E$8", "$E$9", "$E$10", "$E$11", "$E$12", "$E$14"
        sh = "$E$32"
        def prof(nn=n, rr=r_, vv=v, cc=c_, ff=f):
            return f"{p}*({nn}*{rr}*(1-{vv})-{ff})-{nn}*{cc}"
        drivers = [
            ("Volume", lambda sg: prof(nn=f"{n}*(1{sg}{sh})")),
            ("Revenue per unit", lambda sg: prof(rr=f"{r_}*(1{sg}{sh})")),
            ("Variable costs, share", lambda sg: prof(vv=f"{v}*(1{sg}{sh})")),
            ("Launch cost per unit", lambda sg: prof(cc=f"{c_}*(1{sg}{sh})")),
            ("Fixed costs", lambda sg: prof(ff=f"{f}*(1{sg}{sh})")),
        ]
        guard = f"AND(COUNT($E$8:$E$12)=5,ISNUMBER({p}),ISNUMBER({sh}))"
        for k, (name, fn) in enumerate(drivers):
            r = 34 + k
            ws.cell(r, 2, name).font = regular
            ws[f"D{r}"] = f'=IF({guard},{fn("-")},"")'
            ws[f"E{r}"] = f'=IF({guard},{fn("+")},"")'
            ws[f"F{r}"] = f'=IF(AND(ISNUMBER(D{r}),ISNUMBER(E{r})),ABS(E{r}-D{r}),"")'
            ws[f"G{r}"] = f'=IF(ISNUMBER(F{r}),RANK(F{r},$F$34:$F$38),"")'
            for col in "DEF":
                ws[f"{col}{r}"].number_format = "#,##0.00"
            ws[f"G{r}"].number_format = "0"
            for col in "DEFG":
                ws[f"{col}{r}"].fill = calc_fill
                ws[f"{col}{r}"].font = regular
                ws[f"{col}{r}"].alignment = Alignment(vertical="top")
        ws["B40"].font = muted

        ws.freeze_panes = "A8"
