# /// script
# requires-python = ">=3.10"
# dependencies = ["openpyxl>=3.1"]
# ///
"""Build the ICE scoring workbook and fill it with data, in one step.

Self-contained: the template is constructed in code, no files are read
except DATA.json.

Usage:
    uv run ice_scoring.py DATA.json OUTPUT.xlsx [--force]
    uv run ice_scoring.py --list

DATA.json:
    {
      "text": {"title": "Onboarding ideas", "method": "average"},
      "rows": [["Idea A", 7, 6, 5]]   # idea, impact, confidence, ease
    }

`method` must be exactly "average" or "product" (lower case); the workbook
switches its ICE formula on this word. Do not pass the ICE score or the rank:
the workbook computes them with live formulas. Up to 30 rows are prepared.

`--list` prints the header row with its hints and exits.
"""

import argparse
import json
import re
import sys
from copy import copy
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formula.translate import Translator
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils.cell import column_index_from_string, coordinate_from_string
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation

TOKEN = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*(?::([^}]*))?\}\}")
FONT = "Arial"
DATA_START = ("ICE", 1, 4)  # sheet, column, row


def build_workbook():
    """The ICE template, drawn in code (mirrors build/templates IceScoring spec)."""
    wb = Workbook()
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
        ("Impact", "Impact: 1–10, how far the idea moves the goal metric", 14),
        ("Confidence", "Confidence: 1–10, how well the evidence backs the estimate", 16),
        ("Ease", "Ease: 1–10, 10 = easiest to build", 14),
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
                          error='Method: "average" or "product"', showErrorMessage=True)
    dv_m.add("B2")
    dv_s = DataValidation(type="decimal", operator="between", formula1="1", formula2="10", allow_blank=True,
                          errorStyle="warning", showErrorMessage=True, error="ICE scores are from 1 to 10")
    dv_s.add(f"B{first}:D{last}")
    for dv in (dv_m, dv_s):
        ws.add_data_validation(dv)
    return wb


def fill(wb, data):
    """Replace {{key}} tokens and write rows from data_start (mirrors fill_xlsx.py)."""
    values = data.get("text", {})
    missing = set()

    for sheet in wb.worksheets:
        for row in sheet.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and TOKEN.search(cell.value):
                    def sub(m):
                        if m.group(1) not in values:
                            missing.add(m.group(1))
                        v = values.get(m.group(1), "")
                        return "\n".join(map(str, v)) if isinstance(v, list) else str(v)
                    cell.value = TOKEN.sub(sub, cell.value)
                    if "\n" in cell.value:
                        wrapped = copy(cell.alignment)
                        wrapped.wrap_text = True
                        cell.alignment = wrapped

    ws, col0, row0 = wb[DATA_START[0]], DATA_START[1], DATA_START[2]
    formulas = {
        c.column: c.value
        for c in ws[row0]
        if isinstance(c.value, str) and c.value.startswith("=")
    }
    for i, values_row in enumerate(data.get("rows", [])):
        r = row0 + i
        for j, value in enumerate(values_row):
            col = col0 + j
            if col in formulas:
                sys.exit(f"row {i + 1}: column {ws.cell(r, col).column_letter} holds a formula; drop that value")
            ws.cell(r, col, value)
        for col, formula in formulas.items():
            target = ws.cell(r, col)
            if target.value is None:
                origin = ws.cell(row0, col).coordinate
                target.value = Translator(formula, origin=origin).translate_formula(target.coordinate)
                target.number_format = ws.cell(row0, col).number_format
    return missing


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("data", nargs="?")
    ap.add_argument("output", nargs="?")
    ap.add_argument("--force", action="store_true", help="overwrite OUTPUT")
    ap.add_argument("--list", action="store_true", help="print header hints and exit")
    args = ap.parse_args()

    wb = build_workbook()

    if args.list:
        ws = wb[DATA_START[0]]
        for cell in ws[DATA_START[2] - 1]:
            if cell.value is not None:
                hint = cell.comment.text.strip() if cell.comment else ""
                print(f"{cell.column_letter}\t{cell.value}\t{hint}")
        return
    if not args.data or not args.output:
        ap.error("DATA and OUTPUT are required unless --list is given")
    out = Path(args.output)
    if out.exists() and not args.force:
        sys.exit(f"{out} exists; pass --force to overwrite")

    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    missing = fill(wb, data)

    wb.calculation.fullCalcOnLoad = True
    wb.save(out)
    if missing:
        print(f"warning: no value for {', '.join(sorted(missing))}; left empty", file=sys.stderr)
    print(out)


if __name__ == "__main__":
    main()
