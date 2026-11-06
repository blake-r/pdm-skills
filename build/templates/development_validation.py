from .base import *


class TestCase(XlsxSpec):
    @property
    def rel(self):
        return "development-validation/test-case/test-case.xlsx"

    example = {"text": {
        "title": "express slot reminder, FreshDrop 3.4, 12 August 2026",
        "item": "US-214: reminder 15 minutes before the slot, linked to the spec",
        "risk": "buyer misses the courier; order is cancelled and refunded",
        "env": "staging build 3.4.1-rc2, test accounts with express slots, push enabled",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Test cases"

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

        ws["A1"] = "Test Case: {{title: what is tested, product, version and date}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:J1")
        top = [
            (2, "Under test:", "{{item: requirement or task, with link}}", bold, 32),
            (3, "Risk:", "{{risk: what happens to the user or business}}", regular, 32),
            (4, "Environment:", "{{env: test environment, build, data and access}}", regular, 32),
        ]
        for r, name, token, font, height in top:
            ws.cell(r, 1, name).font = muted
            c = ws.cell(r, 3, token)
            c.font = font
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.merge_cells(f"C{r}:J{r}")
            ws.row_dimensions[r].height = height

        headers = [
            ("ID", "A unique case code. It does not change while the case lives: it links the case to a requirement and a defect.", 10),
            ("Title", "The goal of the case in one line: what we check and under what condition. Not \"verify correctness\": "
                         "be specific, e.g. \"method, scenario\".", 36),
            ("Type", "main, negative, validation or boundary. Helps to see which checks are missing.", 12),
            ("Priority", "The importance of running the case, if needed: high, medium or low. Rely on the risk from row 3.", 11),
            ("Preconditions", "The state of the environment and data before the first step: what must exist and in what form. "
                            "May refer to another case that prepares it.", 34),
            ("Steps: action → expected result", "One row is one action and, right after it, the expected result: "
                                                     "\"action → result\". Specific data and values go in the step itself.", 52),
            ("Expected outcome", "What the output should be overall: values, status, state. Fixed in advance and by the requirement, "
                               "not by what the system showed.", 32),
            ("Basis", "Where the expected result comes from: a requirement item, documentation, an agreement. "
                          "Not the code of the system under test.", 28),
            ("Result", "Filled in during the run: passed, failed or skipped.", 11),
            ("Actual result", "Filled in during the run: what was actually obtained. For a failed case — "
                                      "what differs from the expected.", 28),
        ]
        hr = 6
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(hr, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            note(c, hint, 110)
            ws.column_dimensions[c.column_letter].width = width
        ws.column_dimensions["A"].width = 16
        ws.row_dimensions[hr].height = 34

        first, last = hr + 1, hr + 50
        for r in range(first, last + 1):
            for c in range(1, 11):
                ws.cell(r, c).font = regular
                ws.cell(r, c).alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = ws.cell(first, 3)
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'Test cases'!$A${first}")

        dv_list(ws, "main,negative,validation,boundary", f"C{first}:C{last}")
        dv_list(ws, "high,medium,low", f"D{first}:D{last}")
        dv_list(ws, "passed,failed,skipped", f"I{first}:I{last}")

        rng = lambda col: f"${col}${first}:${col}${last}"
        ws["L6"] = "Summary"
        ws["L6"].font, ws["L6"].fill = bold, head_fill
        ws["M6"].fill = head_fill
        ws.column_dimensions["K"].width = 3
        ws.column_dimensions["L"].width = 34
        ws.column_dimensions["M"].width = 12
        stats = [
            ("Cases", f'=COUNTA({rng("B")})', "0", "How many cases are in the table."),
            ("Main", f'=COUNTIF({rng("C")},"main")', "0",
             "Main scenarios alone are a blind spot: failures and boundaries are unchecked."),
            ("Negative", f'=COUNTIF({rng("C")},"negative")', "0", "Checks for wrong actions and failures."),
            ("Validation", f'=COUNTIF({rng("C")},"validation")', "0", "Checks of input data."),
            ("Boundary", f'=COUNTIF({rng("C")},"boundary")', "0", "Checks at the limits of valid values."),
            ("No expected outcome", f'=SUMPRODUCT(({rng("B")}<>"")*({rng("G")}=""))', "0",
             "Cases with an empty \"Expected outcome\" column. Must be 0: without an expected result it is not a check."),
            ("Run", f'=COUNTIF({rng("I")},"passed")+COUNTIF({rng("I")},"failed")', "0",
             "Cases with the value \"passed\" or \"failed\". Skipped ones are not counted."),
            ("Failed", f'=COUNTIF({rng("I")},"failed")', "0", "Every failed case is a reason to file a defect or fix the case itself."),
            ("Pass rate", '=IF(M13=0,"",COUNTIF($I$7:$I$56,"passed")/M13)', "0%",
             "Passed divided by run. Not a measure of product quality: it only shows that these cases were checked."),
        ]
        for i, (name, formula, fmt, hint) in enumerate(stats, start=7):
            a = ws.cell(i, 12, name)
            a.font = regular
            note(a, hint, 90)
            b = ws.cell(i, 13, formula)
            b.font, b.fill = bold, calc_fill
            b.number_format = fmt
