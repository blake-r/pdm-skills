# /// script
# requires-python = ">=3.10"
# dependencies = ["python-pptx>=1.0", "openpyxl>=3.1"]
# ///
"""Dev-only builder for the pilot templates. Not shipped."""

import datetime as dt
import inspect
import json
import os
import posixpath
import re
from abc import ABC, abstractmethod
from pathlib import Path

from pptx import Presentation
from pptx.opc.packuri import PackURI
from pptx.chart.data import CategoryChartData, XyChartData
from pptx.chart.datalabel import DataLabels
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_MARKER_STYLE, XL_TICK_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE, PP_PLACEHOLDER
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
from lxml import etree
from openpyxl import Workbook
from openpyxl.comments import Comment
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.oxml.ns import qn

ROOT = Path(os.environ.get("BUILD_OUT", Path(__file__).resolve().parents[1] / "skills"))
FONT = "Arial"
INK = RGBColor(0x26, 0x2B, 0x33)
MUTED = RGBColor(0x6B, 0x72, 0x80)
LINE = RGBColor(0xC9, 0xCE, 0xD6)
ACCENT = RGBColor(0x2F, 0x6F, 0xDE)
ACCENT_BG = RGBColor(0xE8, 0xF0, 0xFC)
GOOD, GOOD_BG = RGBColor(0x2E, 0x8B, 0x57), RGBColor(0xE8, 0xF5, 0xEC)
BAD, BAD_BG = RGBColor(0xC6, 0x3D, 0x3D), RGBColor(0xFB, 0xEA, 0xEA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


class ToolSpec(ABC):
    """What one tool contributes to a template: its path, and its drawing in draw()."""

    @property
    @abstractmethod
    def rel(self):
        """Output path relative to ROOT, e.g. "business-analysis/bcg-matrix/bcg-matrix.pptx"."""

    example = None
    """Example data in the format of scripts/fill_pptx.py or fill_xlsx.py, written as example.json
    next to the template. Only the example fills the placeholders; the template itself stays empty."""


class PptxSpec(ToolSpec):
    @abstractmethod
    def draw(self, prs, slide):
        """Draw on the first slide of a new deck; prs is the deck, for adding slides or charts."""


class XlsxSpec(ToolSpec):
    @abstractmethod
    def draw(self, wb):
        """Fill a new workbook, whose first sheet is wb.active."""


class Builder:
    """Assembles one template. The steps shared by all tools live here; a spec supplies the tool's part."""

    def __init__(self, spec):
        self.spec = spec

    def build(self, out):
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(self.spec, PptxSpec):
            prs, slide = new_deck()
            self.spec.draw(prs, slide)
            save_pptx(prs, out)
        else:
            wb = Workbook()
            self.spec.draw(wb)
            wb.save(out)
        if self.spec.example is not None:
            (out.parent / "example.json").write_text(
                json.dumps(self.spec.example, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def concrete_specs():
    """Every spec that can be built, in definition order."""
    found, todo = [], list(ToolSpec.__subclasses__())
    while todo:
        cls = todo.pop(0)
        todo.extend(cls.__subclasses__())
        if not inspect.isabstract(cls):
            found.append(cls)
    return found


def save_pptx(prs, out):
    """Save a deck with its charts, embedded workbooks and images named after the tool.

    Parts are renamed to <tool>_<name> (tool = the output folder), so decks built
    from different templates can be merged at the XML level without name clashes.
    """
    prefix = Path(out).parent.name.replace("-", "_")
    for part in prs.part.package.iter_parts():
        name = str(part.partname)
        if re.match(r"/ppt/(charts|embeddings|media)/[^/]+$", name) and not name.split("/")[-1].startswith(prefix + "_"):
            part.partname = PackURI(f"{posixpath.dirname(name)}/{prefix}_{posixpath.basename(name)}")
    prs.save(out)


def new_deck():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    for holder in [prs.slide_master, *prs.slide_layouts]:
        for ph in list(holder.placeholders):
            if ph.placeholder_format.type in (PP_PLACEHOLDER.DATE, PP_PLACEHOLDER.FOOTER, PP_PLACEHOLDER.SLIDE_NUMBER):
                ph._element.getparent().remove(ph._element)
    return prs, prs.slides.add_slide(prs.slide_layouts[6])


def text(shape, value, size=12, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for side in ("left", "right"):
        setattr(tf, f"margin_{side}", Inches(0.1))
    tf.margin_top = tf.margin_bottom = Inches(0.06)
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = value
    r.font.size, r.font.bold, r.font.name = Pt(size), bold, FONT
    r.font.color.rgb = color
    return shape


def box(shapes, x, y, w, h, fill=None, line=LINE, kind=MSO_SHAPE.RECTANGLE, name=None):
    s = shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(1)
    s.shadow.inherit = False
    if name:
        s.name = name
    return s


def label(shapes, x, y, w, h, value, **kw):
    return text(box(shapes, x, y, w, h, line=None), value, **kw)


def connector(shapes, a, b, color=LINE, width=1.25, dash=None, arrow=False):
    """Straight line from point a to point b, inches; arrow adds a head at b."""
    c = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(a[0]), Inches(a[1]), Inches(b[0]), Inches(b[1]))
    c.line.color.rgb, c.line.width = color, Pt(width)
    if dash:
        c.line.dash_style = dash
    if arrow:
        ln = c.line._get_or_add_ln()
        ln.append(ln.makeelement(qn("a:tailEnd"), {"type": "arrow", "w": "med", "len": "med"}))
    return c


def comment(cell, hint, height=100, width=260):
    cell.comment = Comment(hint, "pdm-skills", width=width, height=height)


def name_label(ser, position, size, bold, color):
    """Data labels that show only the series name, at the given position."""
    dls = DataLabels(ser._element.get_or_add_dLbls())
    dls.show_series_name, dls.show_value, dls.show_category_name = True, False, False
    dls.position = position
    dls.font.size, dls.font.bold, dls.font.name = Pt(size), bold, FONT
    dls.font.color.rgb = color


def header(slide, kicker, title_token):
    label(slide.shapes, 0.5, 0.3, 12.3, 0.35, kicker, size=12, bold=True, color=ACCENT)
    label(slide.shapes, 0.5, 0.6, 12.3, 0.55, title_token, size=22, bold=True)


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

# ---------------------------------------------------------------- retrospective
class RetrospectiveMeeting(PptxSpec):
    @property
    def rel(self):
        return "development-execution/retrospective-meeting/retrospective-meeting.pptx"

    example = {"text": {
        "title": "Delivery team, 1–14 March 2026",
        "good": "Daily stand-ups kept blockers visible (+5); couriers app shipped on time (+3)",
        "bad": "Test environment was down for 3 days (+4); requirements changed twice after sprint start (+2)",
        "improve": "Book the test environment in advance (+4); write acceptance criteria before the sprint (+2)",
        "actions": "1. Agree a test-environment booking with QA: Ivan, by 20 March. 2. Add a Definition of Ready check to planning: Anna, by 27 March. Check: no environment downtime in the next sprint",
    }}

    def draw(self, prs, slide):
        header(slide, "RETROSPECTIVE", "{{title: team and period}}")
        cols = [
            ("What went well", "What's good?", GOOD, GOOD_BG,
             "{{good: what went well, one item per line}}"),
            ("What went badly", "What's bad?", BAD, BAD_BG,
             "{{bad: what got in the way, facts only}}"),
            ("How to improve", "How to improve?", ACCENT, ACCENT_BG,
             "{{improve: improvement ideas, one per line}}"),
        ]
        x, w, gap = 0.5, 3.95, 0.225
        for title, original, color, bg, token in cols:
            head = box(slide.shapes, x, 1.3, w, 0.6, fill=color, line=None)
            text(head, title, size=14, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            p = head.text_frame.add_paragraph()
            r = p.add_run()
            r.text = original
            r.font.size, r.font.name, r.font.color.rgb = Pt(10), FONT, WHITE
            text(box(slide.shapes, x, 1.9, w, 3.35, fill=bg, line=None), token, size=12)
            x += w + gap
        label(slide.shapes, 0.5, 5.4, 12.3, 0.35, "Actions before the next retrospective", size=12, bold=True, color=INK)
        text(box(slide.shapes, 0.5, 5.75, 12.3, 1.45),
             "{{actions: 1–3 actions with owner, date and check}}",
             size=12)

# ---------------------------------------------------------------- gantt
def excel_serial(d):
    return (d - dt.date(1899, 12, 30)).days


class GanttChart(PptxSpec):
    @property
    def rel(self):
        return "development-planning/gantt-chart/gantt-chart.pptx"

    example = {
        "text": {
            "title": "Coupon feature for FreshDrop, 5 Jan – 16 Feb 2026",
            "start_date": "5 January 2026",
            "milestones": "26 Jan: design approved. 9 Feb: QA complete. 16 Feb: launch to all users",
            "dependencies": "Screens wait for the design; QA waits for the API and screens. The QA chain (days 21–35) sets the launch date",
            "risks": "Payment provider certification may take 5 days; a 3-day buffer sits inside the QA task",
        },
        "charts": {"gantt": {
            "categories": ["1. Design coupon flow · Anna", "2. Build API · Ivan", "3. Build app screens · Olga (after 1)",
                           "4. QA and fixes · Ivan (after 2, 3)", "5. Staged rollout · Lena (after 4)", "◆ Milestone: launch"],
            "series": [{"name": "Start, day from kickoff", "values": [0, 7, 10, 21, 35, 42]},
                       {"name": "Duration, days", "values": [10, 14, 10, 14, 7, 0]},
                       {"name": "Milestone", "values": [0, 0, 0, 0, 0, 0.5]}],
        }},
    }

    def draw(self, prs, slide):
        header(slide, "GANTT CHART", "{{title: project and planning horizon}}")
        tasks = [("{{task: task name, owner and dependencies}}", 0, 0, 0)]
        data = CategoryChartData()
        data.categories = [t[0] for t in tasks]
        data.add_series("Start, day from kickoff", [t[1] for t in tasks])
        data.add_series("Duration, days", [t[2] for t in tasks])
        data.add_series("Milestone", [t[3] for t in tasks])
        frame = slide.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED, Inches(0.4), Inches(1.3),
                                       Inches(8.6), Inches(5.5), data)
        label(slide.shapes, 0.5, 6.85, 8.5, 0.4,
              "Scale — days from kickoff. Start: {{start_date: project start date}}", size=11, color=MUTED)
        frame.name = "gantt"
        chart = frame.chart
        ids = {}
        for el in chart._chartSpace.xpath(".//c:axId | .//c:crossAx"):
            el.set("val", str(ids.setdefault(el.get("val"), 500000 + len(ids))))
        chart.has_legend = False
        chart.font.name, chart.font.size = FONT, Pt(11)
        chart.font.color.rgb = INK
        offset, duration, milestone = chart.plots[0].series
        milestone.format.fill.solid()
        milestone.format.fill.fore_color.rgb = INK
        offset.format.fill.background()
        offset.format.line.fill.background()
        duration.format.fill.solid()
        duration.format.fill.fore_color.rgb = ACCENT
        chart.plots[0].gap_width = 60
        cat = chart.category_axis
        cat.reverse_order = True
        cat.format.line.color.rgb = LINE
        cat.has_major_gridlines = False
        val = chart.value_axis
        val.minimum_scale = 0
        val.major_unit = 7
        val.has_major_gridlines = True
        val.major_gridlines.format.line.color.rgb = LINE
        val.tick_labels.number_format = "0"
        val.tick_labels.number_format_is_linked = False
        val.format.line.fill.background()

        x, w = 9.25, 3.6
        panels = [
            ("Milestones", "{{milestones: key dates, one per line}}", 1.3, 1.75),
            ("Dependencies", "{{dependencies: tasks that wait for others, critical chain}}", 3.15, 2.0),
            ("Schedule risks", "{{risks: what could shift the plan, and the buffer}}", 5.25, 1.95),
        ]
        for tag, token, py, ph in panels:
            label(slide.shapes, x, py, w, 0.35, tag, size=12, bold=True, color=INK)
            text(box(slide.shapes, x, py + 0.35, w, ph - 0.35), token, size=11)

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

class StakeholdersMatrix(PptxSpec):
    @property
    def rel(self):
        return "product-research/stakeholders-matrix/stakeholders-matrix.pptx"

    example = {"text": {
        "title": "Express pilot in Moscow: stakeholders, July 2026",
        "keep_satisfied": "head of finance: approves the budget, sees little of daily work",
        "manage_closely": "ops director: runs couriers; reviews the pilot every week",
        "monitor": "local media: low impact; coverage checked monthly",
        "keep_informed": "couriers: routes change; told by push and at the weekly meeting",
        "decision": "ops director decides; finance signs off the budget",
        "result": "pilot routes approved 1 July; courier churn checked after 6 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "STAKEHOLDERS MATRIX", "{{title: product, project or decision, date}}")
        sh = slide.shapes
        # Influence of the stakeholder on the product runs up, the product's impact on the stakeholder runs right
        mx, my, mw, mh = 0.95, 1.35, 7.9, 5.5
        cw, ch = mw / 2, mh / 2

        def cell(col, row, tag, key, hint, fill=WHITE, tag_color=INK):
            x, y = mx + col * cw, my + row * ch
            tb = text(box(sh, x, y, cw, ch, fill=fill), f"{{{{{key}: {hint}}}}}", size=10)
            tb.text_frame.margin_top = Inches(0.4)
            label(sh, x + 0.06, y + 0.05, cw - 0.12, 0.3, tag, size=11, bold=True, color=tag_color)

        cell(0, 0, "Keep satisfied", "keep_satisfied",
             "role and influence on the product")
        cell(1, 0, "Manage closely", "manage_closely",
             "role and involvement in the pilot",
             fill=ACCENT_BG, tag_color=ACCENT)
        cell(0, 1, "Monitor", "monitor", "role, influence and impact")
        cell(1, 1, "Keep informed", "keep_informed",
             "role and what changes for them")
        ax = label(sh, 0.2, my, 0.35, mh, "Stakeholder's influence on the product →", size=10, color=MUTED,
                   align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        ax.text_frame._txBody.bodyPr.set("vert", "vert270")
        ax.text_frame.margin_left = ax.text_frame.margin_right = 0
        label(sh, mx - 0.6, my, 0.55, 0.3, "high", size=9, color=MUTED, align=PP_ALIGN.RIGHT)
        label(sh, mx - 0.6, my + mh - 0.3, 0.55, 0.3, "low", size=9, color=MUTED, align=PP_ALIGN.RIGHT)
        label(sh, mx, my + mh + 0.03, mw, 0.3, "Product's impact on the stakeholder →", size=10, color=MUTED, align=PP_ALIGN.CENTER)
        label(sh, mx, my + mh + 0.03, 0.8, 0.3, "low", size=9, color=MUTED)
        label(sh, mx + mw - 0.8, my + mh + 0.03, 0.8, 0.3, "high", size=9, color=MUTED, align=PP_ALIGN.RIGHT)

        px, pw = 9.2, 3.63
        for y, h, name, key, hint in [
            (my, 2.55, "Decision", "decision", "who decides and who signs off"),
            (my + 2.95, 2.55, "Result", "result", "result with dates and checks"),
        ]:
            label(sh, px, y - 0.07, pw, 0.37, name, size=12, bold=True)
            text(box(sh, px, y + 0.3, pw, h - 0.3), f"{{{{{key}: {hint}}}}}", size=10)

class KanoModel(XlsxSpec):
    @property
    def rel(self):
        return "product-research/kano-model/kano-model.xlsx"

    example = {"text": {
        "title": "FreshDrop app, 240 buyers surveyed, 24 August 2026, online form",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.formatting.rule import FormulaRule
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Kano"
        ev = wb.create_sheet("Evaluation table")

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        thin = Side(style="thin", color="C9CED6")

        ws["A1"] = "Kano Model: {{title: product, who was surveyed, how many people, when}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws["A2"].font = Font(name=FONT, size=11, color="6B7280")
        ws.merge_cells("A1:M1")
        ws.merge_cells("A2:M2")

        headers = [
            ("Feature", "product property as the user sees it", 36),
            ("A\nattractive", "Attractive: delights if present, does not upset if absent.", 11),
            ("O\none-dimensional", "One-dimensional: the better it is done, the happier people are; if absent, they are unhappy.", 11),
            ("M\nmust-be", "Must-be: not noticed if present, strongly dissatisfying if absent.", 13),
            ("I\nindifferent", "Indifferent: people do not care whether it is there or not.", 12),
            ("R\nreverse", "Reverse: unhappy if present, happy if absent.", 10),
            ("Q\nquestionable", "Questionable: the answers contradict each other, the question was misunderstood.", 12),
            ("Decision", "decision on the feature and why", 40),
            ("Answers", "sum of answers B to G", 10),
            ("Category", "category with the most answers", 22),
            ("Category\nby most answers", "A+O+M vs I+R+Q category rule", 16),
            ("Better", "share of A and O answers", 10),
            ("Worse", "negative share of O and M answers", 10),
        ]
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(3, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            c.comment = Comment(hint, "pdm-skills", width=260, height=110)
            ws.column_dimensions[c.column_letter].width = width
        ws.row_dimensions[3].height = 46

        names = ["A · attractive", "O · one-dimensional", "M · must-be", "I · indifferent", "R · reverse", "Q · questionable"]
        first, last = 4, 53
        for r in range(first, last + 1):
            rng = f"B{r}:G{r}"
            ws.cell(r, 9, f'=IF(COUNT({rng})=0,"",SUM({rng}))')
            pick = " ".join(f'IF(MAX({rng})={chr(66 + k)}{r},"{names[k]}",' for k in range(6)) + '""' + ")" * 6
            ws.cell(r, 10, f'=IF(I{r}="","",IF(COUNTIF({rng},MAX({rng}))>1,"tie",{pick}))'.replace(", IF", ",IF"))
            pick3 = lambda cols: " ".join(f'IF(MAX({",".join(c + str(r) for c in cols)})={c}{r},"{names[ord(c) - 66]}",' for c in cols) + '""' + ")" * len(cols)
            ws.cell(r, 11, f'=IF(I{r}="","",IF(B{r}+C{r}+D{r}>E{r}+F{r}+G{r},{pick3("CBD")},{pick3("EFG")}))'.replace(", IF", ",IF"))
            base = f"(B{r}+C{r}+D{r}+E{r})"
            ws.cell(r, 12, f'=IF(OR(I{r}="",{base}=0),"",(B{r}+C{r})/{base})').number_format = "0.00"
            ws.cell(r, 13, f'=IF(OR(I{r}="",{base}=0),"",-(C{r}+D{r})/{base})').number_format = "0.00"
            for c in range(1, 14):
                ws.cell(r, c).font = regular
            ws.cell(r, 8).alignment = Alignment(wrap_text=True, vertical="top")
        ws.conditional_formatting.add(f"J{first}:J{last}", FormulaRule(
            formula=[f'J{first}="tie"'], font=Font(color="C63D3D", bold=True)))
        ws.freeze_panes = "B4"
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text="Kano!$A$4")
        dv = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                            error="The number of respondents must be a whole number, at least 0", showErrorMessage=True)
        dv.add(f"B{first}:G{last}")
        ws.add_data_validation(dv)

        ev["A1"] = "Kano evaluation table: answer to the functional question × answer to the dysfunctional question"
        ev["A1"].font = Font(name=FONT, bold=True, size=12)
        ev["A2"] = ("Functional: \"If the product has X, how would you feel about it?\" "
                    "Dysfunctional: \"If the product does not have X, how would you feel about it?\"")
        ev["A2"].font = Font(name=FONT, size=10, color="6B7280")
        answers = ["I like it", "I expect it", "I am neutral", "I can tolerate it", "I dislike it"]
        grid = ["QAAAO", "RIIIM", "RIIIM", "RIIIM", "RRRRQ"]
        ev.cell(4, 1, "X present ↓ / X absent →").font = bold
        for j, a in enumerate(answers):
            c = ev.cell(4, 2 + j, a)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, horizontal="center")
            ev.column_dimensions[c.column_letter].width = 16
            rc = ev.cell(5 + j, 1, a)
            rc.font, rc.fill = bold, head_fill
            for k, v in enumerate(grid[j]):
                cc = ev.cell(5 + j, 2 + k, v)
                cc.font, cc.alignment = regular, Alignment(horizontal="center")
                cc.border = Border(left=thin, right=thin, top=thin, bottom=thin)
        ev.column_dimensions["A"].width = 22
        ev.row_dimensions[4].height = 32
        for i, n in enumerate(names):
            ev.cell(11 + i, 1, n).font = regular

class PerceptualMap(PptxSpec):
    @property
    def rel(self):
        return "product-research/perceptual-map/perceptual-map.pptx"

    example = {"text": {
        "title": "Grocery delivery apps in Moscow: 300 buyers, August 2026",
        "x_axis": "Price: from cheap (left) to premium (right), 1–10",
        "y_axis": "Speed: slow (bottom) to fast (top)",
        "scope": "ratings of 300 buyers, August 2026; circle size = market share",
        "gap": "fast and premium: no strong brand; buyers say they would pay for it",
        "decision": "move FreshDrop to fast, mid-price; message «delivery in 2 hours»",
        "result": "message tested in 2 districts from 1 September; share checked after 6 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "PERCEPTUAL MAP", "{{title: market, who was asked, when}}")
        data = XyChartData()
        series = [("Midpoint X", [(5.5, 1), (5.5, 10)]), ("Midpoint Y", [(1, 5.5), (10, 5.5)]),
                  ("Brand A", [(7.5, 8)]), ("Brand B", [(3, 7)]), ("Brand C", [(4, 3)]), ("Our product", [(6.5, 4)])]
        for name, pts in series:
            ser = data.add_series(name)
            for x, y in pts:
                ser.add_data_point(x, y)
        cx, cy, cw, chh = 0.9, 1.3, 7.9, 5.45
        frame = slide.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER, Inches(cx), Inches(cy), Inches(cw), Inches(chh), data)
        frame.name = "map"
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
            ser.format.line.color.rgb = LINE
            ser.format.line.width = Pt(1.25)
            ser.smooth = False
        for ser in all_series[2:]:
            ser.format.line.fill.background()
            ser.marker.style = XL_MARKER_STYLE.CIRCLE
            ser.marker.size = 22
            ser.marker.format.fill.solid()
            ser.marker.format.fill.fore_color.rgb = ACCENT
            ser.marker.format.line.color.rgb = WHITE
            dls = DataLabels(ser._element.get_or_add_dLbls())
            dls.show_series_name, dls.show_value, dls.show_category_name = True, False, False
            dls.position = XL_LABEL_POSITION.RIGHT
            dls.font.size, dls.font.name = Pt(11), FONT
            dls.font.color.rgb = INK
        for axis in (chart.category_axis, chart.value_axis):
            axis.minimum_scale, axis.maximum_scale, axis.major_unit = 1, 10, 1
            axis.has_major_gridlines = False
            axis.format.line.color.rgb = LINE
            axis.tick_labels.font.size = Pt(10)
            axis.tick_labels.font.color.rgb = MUTED
        text(box(slide.shapes, cx, cy + chh + 0.02, cw, 0.4, line=None),
             "{{x_axis: horizontal axis: from what to what}}", size=11, color=MUTED, align=PP_ALIGN.CENTER)
        ax = text(box(slide.shapes, 0.3, cy, 0.5, chh, line=None),
                  "{{y_axis: vertical axis: from what to what}}", size=11, color=MUTED,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        ax.text_frame._txBody.bodyPr.set("vert", "vert270")

        x, w = 9.25, 3.6
        panels = [
            ("Data", "{{scope: data source, sample and circle size}}", 1.3, 1.3),
            ("Open position", "{{gap: empty position and whether buyers need it}}", 2.75, 1.35),
            ("Decision", "{{decision: where we move the product and how}}", 4.25, 1.35),
            ("Result", "{{result: result with dates and checks}}", 5.75, 1.35),
        ]
        for tag, token, py, ph in panels:
            label(slide.shapes, x, py - 0.05, w, 0.37, tag, size=12, bold=True, color=INK)
            text(box(slide.shapes, x, py + 0.32, w, ph - 0.32), token, size=10)

class EmpathyMap(PptxSpec):
    @property
    def rel(self):
        return "product-research/empathy-map/empathy-map.pptx"

    example = {"text": {
        "title": "Parents who order groceries online: 12 interviews, May 2026",
        "who": "Olga, 34, marketing manager, two kids, evening commute",
        "need_to_do": "plan the family week, choose a slot, know the order will be on time",
        "see": "rival apps with cheap offers; friends posting about fresh deliveries",
        "say": "«I never know if the slot will be on time»",
        "do": "checks the app 5 times a day; calls support when late",
        "hear": "friends recommend cheaper rivals; news about courier shortages",
        "pains": "late deliveries, missed items, wasted evenings",
        "gains": "time for family, fresh food, peace of mind",
        "think_feel": "wants a weekly plan she does not have to check",
        "decision": "add a delivery-time guarantee to the slot picker; product lead decides",
        "result": "guarantee shown in the slot picker from 1 July; complaints checked after 4 weeks",
    }}

    def draw(self, prs, slide):
        # Layout follows Dave Gray's Empathy Map Canvas (2017): goal on top, a big head in the middle
        # holding thoughts and feelings, observable sectors around it, numbered in the intended order
        header(slide, "EMPATHY MAP", "{{title: who was studied, how and when}}")
        sh = slide.shapes
        x0, y0, x1, y1 = 0.5, 1.3, 9.0, 7.2
        cx, cy, r = 4.75, 4.45, 1.9
        d = r * 0.7071
        ul, ur, ll, lr = (cx - d, cy - d), (cx + d, cy - d), (cx - d, cy + d), (cx + d, cy + d)

        box(sh, x0, y0, x1 - x0, y1 - y0)
        emu = lambda pt: (int(Inches(pt[0])), int(Inches(pt[1])))
        ff = sh.build_freeform(*emu((x0, y0)))
        ff.add_line_segments([emu((x1, y0)), emu(ur), emu(ul)], close=True)
        goal = ff.convert_to_shape()
        goal.fill.solid()
        goal.fill.fore_color.rgb = ACCENT_BG
        goal.line.color.rgb = LINE
        goal.shadow.inherit = False

        def line(a, b):
            return connector(sh, a, b, width=1)

        line((cx, y0), (cx, cy - r))
        line((x0, y1), ll)
        line((x1, y1), lr)
        line((cx + r, cy), (x1, cy))
        box(sh, cx - r, cy - r, 2 * r, 2 * r, fill=WHITE, kind=MSO_SHAPE.OVAL, line=INK)

        def cell(x, y, w, h, tag, key, hint, tag_color=INK):
            label(sh, x, y, w, 0.3, tag, size=11, bold=True, color=tag_color)
            text(box(sh, x, y + 0.28, w, h - 0.28, line=None), f"{{{{{key}: {hint}}}}}", size=10)

        cell(2.05, 1.36, 2.6, 1.05, "1 Who", "who", "name, age, role and situation",
             tag_color=ACCENT)
        cell(4.85, 1.36, 2.9, 1.05, "2 What they need to do", "need_to_do",
             "the job they are trying to do", tag_color=ACCENT)
        cell(6.75, 3.0, 2.2, 1.4, "3 See", "see", "what they see in the market")
        cell(6.75, 4.55, 2.2, 1.3, "4 Say", "say", "what they say out loud")
        cell(3.1, 6.4, 3.3, 0.78, "5 Do", "do", "observable actions and habits")
        cell(0.6, 3.2, 2.2, 2.4, "6 Hear", "hear", "what they hear from others")
        label(sh, cx - 1.8, cy - r + 0.3, 3.6, 0.3, "7 Think and feel", size=11, bold=True,
              align=PP_ALIGN.CENTER)
        line((cx, cy - r + 0.68), (cx, cy + 0.85))
        cell(cx - 1.5, cy - r + 0.68, 1.45, 2.1, "Pains", "pains", "frustrations and obstacles")
        cell(cx + 0.05, cy - r + 0.68, 1.45, 2.1, "Gains", "gains", "wants and measures of success")
        text(box(sh, cx - 1.3, cy + 0.9, 2.6, 0.75, line=None),
             "{{think_feel: thoughts and feelings that drive behaviour}}", size=10, align=PP_ALIGN.CENTER)

        px, pw = 9.25, 3.6
        for y, h, name, key, hint in [
            (1.3, 2.75, "Decision", "decision", "what we change and who decides"),
            (4.45, 2.75, "Result", "result", "result with dates and checks"),
        ]:
            label(sh, px, y - 0.07, pw, 0.37, name, size=12, bold=True)
            text(box(sh, px, y + 0.3, pw, h - 0.3), f"{{{{{key}: {hint}}}}}", size=10)

class JobsToBeDone(PptxSpec):
    @property
    def rel(self):
        return "product-research/jobs-to-be-done/jobs-to-be-done.pptx"

    example = {"text": {
        "title": "FreshDrop, families who plan the week: 18 interviews, May 2026",
        "job1": "Get groceries for the week",
        "job2": "Find a slot that fits",
        "job3": "Reorder the usual basket",
        "job1_when": "Sunday evening, fridge nearly empty",
        "job1_want": "order the full weekly list in one go",
        "job1_so_that": "the family eats well all week",
        "job1_solution": "weekly list from last order; 2-hour slots",
        "job2_when": "Tuesday, after the school run",
        "job2_want": "pick a window within 2 hours",
        "job2_so_that": "I am home for the courier",
        "job2_solution": "slot picker shows free windows first",
        "job3_when": "milk runs out in the morning",
        "job3_want": "repeat last week's basket in 2 taps",
        "job3_so_that": "I save 15 minutes",
        "job3_solution": "one-tap reorder on the home screen",
        "who": "families with children in Moscow; 18 interviews, May 2026",
        "result": "slot picker on the first screen from 1 July; reorder rate checked after 4 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "JOBS-TO-BE-DONE", "{{title: whose product, who was studied, how and when}}")
        sh = slide.shapes
        x0, y0, w, gap = 0.5, 1.3, 2.75, 0.08
        rows = [
            ("When", "when", "situation in which the job arises", 1.2, WHITE, INK),
            ("I want to", "want", "what the person wants to do", 1.2, WHITE, INK),
            ("So that", "so_that", "which outcome they need", 1.2, WHITE, INK),
            ("What we did", "solution", "what we changed for this job", 1.45, ACCENT_BG, ACCENT),
        ]
        for i in range(3):
            n = i + 1
            x = x0 + i * (w + gap)
            text(box(sh, x, y0, w, 0.45, fill=INK, line=None), f"{{{{job{n}: job name}}}}",
                 size=11, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            y = y0 + 0.5
            for tag, key, hint, h, fill, tag_color in rows:
                box(sh, x, y, w, h, fill=fill)
                label(sh, x + 0.04, y + 0.03, w - 0.08, 0.3, tag, size=10, bold=True, color=tag_color)
                text(box(sh, x, y + 0.3, w, h - 0.3, line=None), f"{{{{job{n}_{key}: {hint}}}}}", size=10)
                y += h + 0.05

        px, pw = 9.25, 3.6
        for y, h, name, key, hint in [
            (1.3, 2.75, "Who and where the data is from", "who", "who was studied, where and when"),
            (4.45, 2.75, "Result", "result", "result with dates and checks"),
        ]:
            label(sh, px, y - 0.07, pw, 0.37, name, size=12, bold=True)
            text(box(sh, px, y + 0.3, pw, h - 0.3), f"{{{{{key}: {hint}}}}}", size=10)

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

class TeamCanvas(PptxSpec):
    @property
    def rel(self):
        return "development-execution/team-canvas/team-canvas.pptx"

    example = {"text": {
        "title": "Delivery team, 6 people, 10 September 2026: reset after the release",
        "people": "Olga, product lead: slot picker; Dmitry, mobile lead: app; Anna, QA; Ilya, analyst",
        "common_goals": "Slot-to-order conversion 70% by 1 November; weekly-order retention 40% by Q1 2027",
        "personal_goals": "Olga: own the slot picker roadmap; Dmitry: cut app start time to 2 seconds",
        "values": "Buyers first: a late courier is our bug; ship small and check the data",
        "needs": "Olga needs weekly slot data; Anna needs test devices and 2 days before each release",
        "rules": "Stand-up at 10:00; decisions in the Thursday review; Friday release only after QA sign-off",
        "strengths": "Dark-store ops know-how, 2 years of slot data, a fast mobile release pipeline",
        "weaknesses": "Olga: too many tests in parallel; Dmitry: decisions not written down",
        "purpose": "Every Moscow buyer gets their slot on time",
    }}

    def draw(self, prs, slide):
        header(slide, "TEAM CANVAS", "{{title: team, date and occasion of the session}}")
        sh = slide.shapes
        # coordinates follow the original canvas (theteamcanvas.com), px of a 2000-px-wide image
        x0, y0, sx, sy = 0.5, 1.25, 12.33 / 1885, 5.5 / 1102
        X = lambda px: x0 + (px - 60) * sx
        Y = lambda py: y0 + (py - 228) * sy

        def block(l, t, r, b, tag, key, hint, agreed, tr=None, tl=None):
            fill = ACCENT_BG if agreed else WHITE
            box(sh, X(l), Y(t), X(r) - X(l), Y(b) - Y(t), fill=fill)
            left, right = X(tl or l), X(tr or r)
            label(sh, left + 0.06, Y(t) + 0.03, right - left - 0.12, 0.28, tag, size=10, bold=True, color=INK)
            tb = label(sh, left + 0.02, Y(t) + 0.3, right - left - 0.04, Y(b) - Y(t) - 0.34,
                       hint, size=9)
            return tb

        block(60, 228, 472, 1010, "1 · People and roles", "people", "{{people: name, role; who is responsible for what}}", True)
        block(472, 228, 1003, 602, "2 · Common goals", "common_goals",
              "{{common_goals: what we want to achieve together}}", True, tr=840)
        block(472, 602, 1003, 1010, "3 · Personal goals", "personal_goals",
              "{{personal_goals: goal, [name]: what each person wants for themselves}}", False, tr=850)
        block(1003, 228, 1533, 602, "5 · Values", "values", "{{values: principles the team stands for}}",
              True, tl=1160)
        block(1003, 602, 1533, 1010, "8 · Needs and expectations", "needs",
              "{{needs: needs of each person and team support}}", False, tl=1160)
        block(1533, 228, 1945, 1010, "9 · Rules & Activities", "rules",
              "{{rules: working rules: communication, decisions, rituals}}", True)
        block(60, 1010, 1003, 1330, "6 · Strengths and assets", "strengths",
              "{{strengths: skills and resources for the goals}}", False)
        block(1003, 1010, 1945, 1330, "7 · Weaknesses & Development Areas", "weaknesses",
              "{{weaknesses: own weaknesses and what holds the team back}}", False)
        hx, hy, hw, hh = 850, 430, 300, 290
        heart = box(sh, X(hx), Y(hy), hw * sx, hh * sy, fill=ACCENT, line=None, kind=MSO_SHAPE.HEART, name="Purpose")
        tb = text(heart, "{{purpose: why we do this, beyond the common goal}}", size=9, color=WHITE,
                  align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        tb.text_frame.margin_left = tb.text_frame.margin_right = Inches(0.25)
        tb.text_frame.margin_top = Inches(0.15)
        label(sh, X(hx), Y(hy) - 0.32, hw * sx, 0.32, "4 · Purpose", size=10, bold=True, color=ACCENT,
              align=PP_ALIGN.CENTER)
        ly = Y(1330) + 0.12
        box(sh, 0.5, ly + 0.07, 0.22, 0.16, fill=ACCENT_BG)
        label(sh, 0.75, ly, 4.2, 0.3, "agreed by the whole team", size=9, color=MUTED)
        box(sh, 3.3, ly + 0.07, 0.22, 0.16, fill=WHITE)
        label(sh, 3.55, ly, 4.0, 0.3, "each person can fill in for themselves", size=9, color=MUTED)
        label(sh, 6.9, ly, 5.93, 0.42, "After the Team Canvas by A. Ivanov and D. Voloshchuk, CC BY-SA 4.0",
              size=9, color=MUTED, align=PP_ALIGN.RIGHT)

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

class Sprint(XlsxSpec):
    @property
    def rel(self):
        return "development-execution/sprint/sprint.xlsx"

    example = {"text": {
        "title": "FreshDrop team, sprint 14, 3–14 August 2026",
        "goal": "ship the express slot reminder to 50% of buyers",
        "product_goal": "cut missed express slots from 22% to 10%",
        "unit": "story points",
        "review": "reminder demo to 6 buyers; decided to add an SMS fallback in sprint 15",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Sprint"

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

        def dv_number(sheet, *refs):
            dv = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                                errorStyle="warning", showErrorMessage=True, error="A non-negative number")
            for ref in refs:
                dv.add(ref)
            sheet.add_data_validation(dv)

        ws["A1"] = "Sprint: {{title: team, sprint number, start and end dates}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:I1")
        top = [
            (2, "Sprint goal:", "{{goal: sprint goal and why it matters now}}", bold, 32),
            (3, "Product goal:", "{{product_goal: what the sprint leads towards}}", regular, 18),
        ]
        for r, name, token, font, height in top:
            ws.cell(r, 1, name).font = muted
            c = ws.cell(r, 3, token)
            c.font = font
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.merge_cells(f"C{r}:I{r}")
            ws.row_dimensions[r].height = height
        ws["A4"] = "Sprint limit:"
        ws["A4"].font = muted
        ws["C4"].font, ws["C4"].fill = bold, calc_fill
        note(ws["C4"], "How much the team is ready to take, in the units of the \"Estimate\" column: capacity accounting for time off "
                       "and the results of past sprints. A guide, not a hard limit.")
        ws["D4"] = "{{unit: estimate unit}}"
        ws["D4"].font = muted
        ws.merge_cells("D4:E4")
        ws["F4"] = "Goal achieved:"
        ws["F4"].font = muted
        ws["G4"].font, ws["G4"].fill = bold, calc_fill
        note(ws["G4"], "Filled in at the sprint review: yes, partly or no.")
        dv_list(ws, "yes,partly,no", "G4")
        ws["A5"] = "Review outcome:"
        ws["A5"].font = muted
        ws["C5"] = "{{review: what was shown and decided next}}"
        ws["C5"].alignment = Alignment(wrap_text=True, vertical="top")
        ws["C5"].font = regular
        ws.merge_cells("C5:I5")
        ws.row_dimensions[5].height = 32

        headers = [
            ("#", "Calculated automatically.", 5),
            ("Item", "An item from the product's shared work list, taken into the sprint. The most important at the top.", 40),
            ("For the goal", "\"yes\" — the item is needed for the sprint goal. The other items are done if there is capacity.", 9),
            ("How we will do it", "The plan: subtasks or steps to a finished result.", 34),
            ("Who", "Who takes the item. The team distributes the work itself.", 14),
            ("Estimate", "An estimate by those who will do the work, in the units from row 4.", 9),
            ("Source", "\"planned\" — taken at planning; \"added\" — came in during the sprint.", 11),
            ("Done", "\"yes\" — the item meets the team's definition of done. Filled in at the end of the sprint.", 9),
            ("What next", "For unfinished items: return to the shared list, carry over to the next sprint, cancel — and why.", 28),
        ]
        hr = 7
        for i, (title, hint, width) in enumerate(headers, start=1):
            c = ws.cell(hr, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            note(c, hint)
            ws.column_dimensions[c.column_letter].width = width
        ws.column_dimensions["A"].width = 16
        ws.row_dimensions[hr].height = 30

        first, last = hr + 1, hr + 50
        for r in range(first, last + 1):
            ws.cell(r, 1, f'=IF(B{r}="","",COUNTA($B${first}:B{r}))').fill = calc_fill
            for c in range(1, 10):
                ws.cell(r, c).font = regular
                ws.cell(r, c).alignment = Alignment(wrap_text=True, vertical="top")
        ws.freeze_panes = ws.cell(first, 3)
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'Sprint'!$B${first}")

        rng = lambda col: f"${col}${first}:${col}${last}"
        ws["K7"] = "Sprint results"
        ws["K7"].font, ws["K7"].fill = bold, head_fill
        ws["L7"].fill = head_fill
        ws.column_dimensions["K"].width = 34
        ws.column_dimensions["L"].width = 12
        stats = [
            ("Items", f'=COUNTA({rng("B")})', "0", "How many items are in the sprint."),
            ("Of them for the goal", f'=COUNTIF({rng("C")},"yes")', "0",
             "Zero — there is no goal, the sprint became a task list. All — the goal most likely just restates the items."),
            ("Taken at planning", f'=SUMIF({rng("G")},"planned",{rng("F")})', "0.0", "The sum of estimates of \"planned\" items."),
            ("Load vs limit", '=IF(OR($C$4="",$C$4=0),"",L10/$C$4)', "0%",
             "What was taken at planning divided by the limit. Above 100% — the team promises more than it has delivered before."),
            ("Added during the sprint", f'=SUMIF({rng("G")},"added",{rng("F")})', "0.0",
             "Work that arrived after planning. Its volume hints at how much reserve to leave."),
            ("Not done", f'=SUMPRODUCT(({rng("B")}<>"")*({rng("H")}<>"yes"),{rng("F")})', "0.0",
             "The sum of estimates of items without \"yes\" in the \"Done\" column."),
            ("Share unfinished", '=IF(L10+L12=0,"",L13/(L10+L12))', "0%",
             "Not done divided by everything taken and added."),
            ("Goal items not done", f'=SUMPRODUCT(({rng("C")}="yes")*({rng("H")}<>"yes"))', "0",
             "More than zero at the end of the sprint — the goal is at risk, even if the rest is done."),
        ]
        for i, (name, formula, fmt, hint) in enumerate(stats, start=8):
            a = ws.cell(i, 11, name)
            a.font = regular
            note(a, hint, 90)
            b = ws.cell(i, 12, formula)
            b.font, b.fill = bold, calc_fill
            b.number_format = fmt

        dv_list(ws, "yes,no", f"C{first}:C{last}")
        dv_list(ws, "planned,added", f"G{first}:G{last}")
        dv_list(ws, "yes,no", f"H{first}:H{last}")
        dv_number(ws, f"F{first}:F{last}", "C4")

        hs = wb.create_sheet("History")
        hs["A1"] = "Sprint history"
        hs["A1"].font = Font(name=FONT, bold=True, size=14)
        hs["A2"].font = muted
        hhead = [
            ("Sprint", "Number or dates.", 14),
            ("Sprint goal", "The goal statement.", 40),
            ("Goal achieved", "yes, partly or no.", 12),
            ("Limit", "The limit the team agreed on at planning.", 9),
            ("Taken", "Taken at planning, in estimate units.", 9),
            ("Added", "Added during the sprint, including growth of estimates.", 11),
            ("Not done", "Removed from the sprint or not brought to done by its end.", 11),
            ("Done", "Calculated automatically: taken + added − not done.", 10),
            ("Share unfinished", "Calculated automatically: not done / (taken + added).", 14),
            ("All done", "Calculated automatically: \"yes\" if not done is 0.", 11),
        ]
        for i, (title, hint, width) in enumerate(hhead, start=1):
            c = hs.cell(4, i, title)
            c.font, c.fill = bold, head_fill
            c.alignment = Alignment(wrap_text=True, vertical="center")
            c.border = Border(bottom=thin)
            note(c, hint, 70)
            hs.column_dimensions[c.column_letter].width = width
        hs.row_dimensions[4].height = 30
        h1, h2 = 5, 30
        for r in range(h1, h2 + 1):
            for c in range(1, 11):
                hs.cell(r, c).font = regular
                hs.cell(r, c).alignment = Alignment(wrap_text=True, vertical="top")
            done = hs.cell(r, 8, f'=IF(OR(E{r}="",G{r}=""),"",E{r}+N(F{r})-G{r})')
            done.fill, done.number_format = calc_fill, "0.0"
            g = hs.cell(r, 9, f'=IF(OR(E{r}="",G{r}=""),"",IF(E{r}+N(F{r})=0,"",G{r}/(E{r}+N(F{r}))))')
            g.fill, g.number_format = calc_fill, "0%"
            hs.cell(r, 10, f'=IF(OR(E{r}="",G{r}=""),"",IF(G{r}=0,"yes","no"))').fill = calc_fill
        dv_list(hs, "yes,partly,no", f"C{h1}:C{h2}")
        dv_number(hs, f"D{h1}:G{h2}")
        hs["L4"] = "Over the last 10 sprints"
        hs["L4"].font, hs["L4"].fill = bold, head_fill
        hs["M4"].fill = head_fill
        hs.column_dimensions["L"].width = 34
        hs.column_dimensions["M"].width = 10
        hist = [
            ("Sprints in history", f"=COUNTA(A{h1}:A{h2})", "0", "How many sprints are recorded."),
            ("Goal achieved", f'=COUNTIF(C{h1}:C{h2},"yes")', "0", "In how many sprints the goal was fully achieved."),
            ("Everything taken was done", f'=COUNTIF(J{h1}:J{h2},"yes")', "0",
             "The benchmark of M. Cohn as retold by Rosbank: in 8 of the last 10 sprints the team did everything it promised."),
        ]
        for i, (name, formula, fmt, hint) in enumerate(hist, start=5):
            a = hs.cell(i, 12, name)
            a.font = regular
            note(a, hint, 90)
            b = hs.cell(i, 13, formula)
            b.font, b.fill = bold, calc_fill
            b.number_format = fmt
        hs["L9"].font = muted
        hs.freeze_panes = "B5"

class StandUpMeeting(PptxSpec):
    @property
    def rel(self):
        return "development-execution/stand-up-meeting/stand-up-meeting.pptx"

    example = {"text": {
        "title": "Delivery team, 6 people, agreed 1 September 2026",
        "purpose": "slot reminders live for 50% of buyers; progress checked every day",
        "when": "10:00 every day, video call link pinned in the team chat",
        "length": "Limit 15 minutes; actual average 11 minutes",
        "people": "6 people: 4 developers, QA and the product lead",
        "facilitator": "Scrum master Ilya; the role rotates each sprint",
        "agenda": "By board: blocked cards first, then cards in review, then the rest by priority",
        "prep": "Each person moves their cards on the board by 09:50 and marks blockers",
        "offline": "Topics over 2 minutes go offline; the people involved stay after the call",
        "outcome": "Plan for the day and help requests, recorded in the team chat",
        "check": "Length measured weekly; usefulness asked in the retro, reviewed each sprint",
        "decision": "From 1 October: a 15-minute cap, blockers first, and no status round",
    }}

    def draw(self, prs, slide):
        header(slide, "STAND-UP MEETING · STAND-UP AGREEMENT",
               "{{title: team, size and date of the agreement}}")
        sh = slide.shapes
        left, full, g = 0.5, 12.33, 0.1

        def block(x, y, w, h, tag, key, hint, fill=WHITE, line=LINE, size=10):
            tb = text(box(sh, x, y, w, h, fill=fill, line=line), hint, size=size)
            tb.text_frame.margin_top = Inches(0.36)
            label(sh, x + 0.08, y + 0.03, w - 0.16, 0.32, tag, size=10, bold=True, color=INK)

        tb = text(box(sh, left, 1.25, full, 0.6, fill=ACCENT_BG, line=None),
                  "Sprint goal: {{purpose: goal the progress is checked against}}",
                  size=11, anchor=MSO_ANCHOR.MIDDLE)
        tb.text_frame.margin_left = Inches(1.6)
        label(sh, left + 0.1, 1.25, 1.4, 0.6, "Why", size=12, bold=True, anchor=MSO_ANCHOR.MIDDLE)

        y1, h1 = 1.95, 1.3
        qw = (full - 3 * g) / 4
        for i, (tag, key, hint) in enumerate([
            ("When and where", "when", "{{when: time, place or link}}"),
            ("Length", "length", "{{length: limit in minutes and actual average}}"),
            ("Who", "people", "{{people: who takes part and how many}}"),
            ("Facilitator", "facilitator", "{{facilitator: who leads and how the role rotates}}"),
        ]):
            block(left + i * (qw + g), y1, qw, h1, tag, key, hint)

        y2, h2 = y1 + h1 + g, 2.0
        lw = 5.6
        block(left, y2, lw, h2, "Order of discussion", "agenda",
              "{{agenda: order of topics: by board or by person}}",
              fill=ACCENT_BG, line=None)
        rw = (full - lw - 2 * g) / 2
        block(left + lw + g, y2, rw, h2, "Preparation", "prep", "{{prep: what each person does before the meeting}}")
        block(left + lw + g + rw + g, y2, rw, h2, "What we take offline", "offline",
              "{{offline: how long discussions are moved, and who stays}}")

        y3, h3 = y2 + h2 + g, 1.55
        tw = (full - 2 * g) / 3
        block(left, y3, tw, h3, "Meeting outcome", "outcome", "{{outcome: day plan and help requests: where recorded}}")
        block(left + tw + g, y3, tw, h3, "How we check the format", "check",
              "{{check: how the format is checked, and when}}")
        block(left + 2 * (tw + g), y3, tw, h3, "Decision", "decision", "{{decision: format change, date and reason}}",
              fill=ACCENT_BG, line=None)

class KanbanBoard(PptxSpec):
    @property
    def rel(self):
        return "development-execution/kanban-board/kanban-board.pptx"

    example = {"text": {
        "title": "FreshDrop mobile team: delivery board for the buyer app, September 2026",
        "c1": "Backlog",
        "c2": "Ready",
        "c3": "In progress",
        "c4": "Code review",
        "c5": "QA",
        "c6": "Done",
        "w1": "—",
        "w2": "8",
        "w3": "4",
        "w4": "3",
        "w5": "3",
        "w6": "—",
        "x1": "Story has criteria and design",
        "x2": "Developer has capacity, WIP below limit",
        "x3": "PR opened, tests pass",
        "x4": "2 approvals, CI green",
        "x5": "Checked on staging, no open bugs",
        "x6": "Released to all Moscow users",
        "bounds": "Started when a card leaves Ready; finished in Done; lead time counted from creation",
        "lanes": "Expedite lane for production bugs, one card at a time; features and QA bugs in standard lanes",
        "blocked": "Red flag with reason and owner; the team lead removes it by the next stand-up",
        "replenish": "Every Monday product adds up to 10 cards to Backlog; the team pulls 8 into Ready",
        "metrics": "WIP 14 on average; throughput 9 cards a week; median cycle time 3.1 days; oldest card 6 days (checked daily)",
        "sle": "85% of cards done in 5 days or faster; July: 78%",
        "decision": "Code review is the bottleneck: cards wait 1.8 days. From 1 October: pair review for cards over 3 files; check the wait time in 2 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "KANBAN BOARD · BOARD AND FLOW RULES",
               "{{title: team, what work goes through the board, date}}")
        sh = slide.shapes
        left, full, g = 0.5, 12.33, 0.1
        lw, n = 1.55, 6
        gx = left + lw + g
        cw = (left + full - gx) / n
        rows = [
            ("Column", "c", ["{{c1: stage name}}", "{{c2: stage name}}", "{{c3: stage name}}", "{{c4: stage name}}", "{{c5: stage name}}", "{{c6: stage name}}"], 0.42),
            ("WIP limit", "w", ["{{w1: cards at once}}", "{{w2: cards at once}}", "{{w3: cards at once}}", "{{w4: cards at once}}", "{{w5: cards at once}}", "{{w6: cards at once}}"], 0.42),
            ("Can pull on when", "x", ["{{x1: exit rule for the stage}}", "{{x2: exit rule for the stage}}", "{{x3: exit rule for the stage}}", "{{x4: exit rule for the stage}}", "{{x5: exit rule for the stage}}", "{{x6: exit rule for the stage}}"], 1.1),
        ]
        y = 1.25
        for tag, key, hint, h in rows:
            label(sh, left, y, lw, h, tag, size=10, bold=True, anchor=MSO_ANCHOR.MIDDLE)
            for i in range(n):
                fill, line, color, bold = WHITE, LINE, INK, False
                if key == "c":
                    fill, line, color, bold = ACCENT, None, WHITE, True
                elif key == "w":
                    fill, line = ACCENT_BG, None
                text(box(sh, gx + i * cw + 0.03, y, cw - 0.06, h, fill=fill, line=line),
                     hint[i], size=9, bold=bold, color=color,
                     anchor=MSO_ANCHOR.TOP if key == "x" else MSO_ANCHOR.MIDDLE)
            y += h + 0.06

        def block(x, y, w, h, tag, key, hint, fill=WHITE, line=LINE, size=10):
            tb = text(box(sh, x, y, w, h, fill=fill, line=line), hint, size=size)
            tb.text_frame.margin_top = Inches(0.36)
            label(sh, x + 0.08, y + 0.03, w - 0.16, 0.32, tag, size=10, bold=True, color=INK)

        y1, h1 = y + 0.1, 1.5
        qw = (full - 3 * g) / 4
        for i, (tag, key, hint) in enumerate([
            ("Start and finish", "bounds", "{{bounds: column where work starts, column where it ends}}"),
            ("Lanes and urgent", "lanes", "{{lanes: lanes and classes of work, expedite rules}}"),
            ("Blockers", "blocked", "{{blocked: how blocked work is marked and unblocked}}"),
            ("Replenishment", "replenish", "{{replenish: work entering the first column: when, how much}}"),
        ]):
            block(left + i * (qw + g), y1, qw, h1, tag, key, hint)

        y2, h2 = y1 + h1 + g, 1.75
        mw = 4.3
        block(left, y2, mw, h2, "Flow metrics", "metrics",
              "{{metrics: flow metrics: values, period, where we look}}")
        sw = 2.9
        block(left + mw + g, y2, sw, h2, "Expected lead time", "sle", "{{sle: service level: share of cards and days}}")
        block(left + mw + sw + 2 * g, y2, full - mw - sw - 2 * g, h2, "Bottleneck and decision", "decision",
              "{{decision: bottleneck and decision, and how it is checked}}",
              fill=ACCENT_BG, line=None)

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

class DefinitionOfDone(PptxSpec):
    @property
    def rel(self):
        return "development-handoff/definition-of-done/definition-of-done.pptx"

    example = {"text": {
        "title": "Delivery team, FreshDrop app, agreed 1 September 2026",
        "scope": "all user stories in the app; done = live for buyers and the support team knows it",
        "k1": "Code merged to main, build green",
        "k2": "Unit tests cover new logic at 80%+",
        "k3": "Reviewed and approved by 2 developers",
        "k4": "Passes QA on staging, no open bugs",
        "k5": "Works on iOS and Android, last 2 versions",
        "k6": "Accessibility check passed",
        "k7": "Analytics events tracked",
        "k8": "Support has a reply template",
        "h1": "CI pipeline; the author checks before merge",
        "h2": "coverage report in CI; reviewer checks the diff",
        "h3": "GitHub approvals; reviewer lists risks in the PR",
        "h4": "QA lead signs the ticket; 0 open bugs of any severity",
        "h5": "device farm run; QA lead checks the release notes",
        "h6": "designer runs the checklist; screen reader test on the main flow",
        "h7": "analyst checks the events in the dashboard within 24 hours",
        "h8": "support lead checks the help center article before release",
        "auto": "Build, unit tests, lint and the release checklist in Jira block the merge by themselves",
        "fail": "Back to In progress; a part can ship behind a feature flag if the rest is green",
        "review": "Every 2 sprints in the retro; the team lead makes the edits, the team votes",
        "agreed": "Mobile team lead, QA lead and product owner; based on the company engineering standard",
        "decision": "From 1 October for all stories; we add the accessibility check and drop the manual smoke test",
    }}

    def draw(self, prs, slide):
        header(slide, "DEFINITION OF DONE · DEFINITION OF DONE AGREEMENT",
               "{{title: team, product and date of the agreement}}")
        sh = slide.shapes
        left, full, g = 0.5, 12.33, 0.1

        def block(x, y, w, h, tag, key, hint, fill=WHITE, line=LINE, size=10):
            tb = text(box(sh, x, y, w, h, fill=fill, line=line), hint, size=size)
            tb.text_frame.margin_top = Inches(0.36)
            label(sh, x + 0.08, y + 0.03, w - 0.16, 0.32, tag, size=10, bold=True, color=INK)

        tb = text(box(sh, left, 1.25, full, 0.55, fill=ACCENT_BG, line=None),
                  "{{scope: work covered and what done means}}",
                  size=11, anchor=MSO_ANCHOR.MIDDLE)
        tb.text_frame.margin_left = Inches(1.6)
        label(sh, left + 0.1, 1.25, 1.4, 0.55, "Applies to", size=12, bold=True, anchor=MSO_ANCHOR.MIDDLE)

        cw1, cw2 = 3.3, 4.5
        x2 = left + cw1 + g
        y = 1.9
        for x, w, tag in [(left, cw1, "Done criterion"), (x2, cw2, "How we check and who")]:
            text(box(sh, x, y, w, 0.3, fill=ACCENT, line=None), tag, size=10, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
        y += 0.35
        rh = 0.42
        for i in range(8):
            text(box(sh, left, y, cw1, rh, fill=WHITE, line=LINE), "{{k%d: criterion, checkable yes or no}}" % (i + 1),
                 size=9, bold=True, anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x2, y, cw2, rh, fill=WHITE, line=LINE),
                 "{{h%d: how it is checked and by whom}}" % (i + 1), size=9, anchor=MSO_ANCHOR.MIDDLE)
            y += rh + 0.05
        ybot = y

        rx = left + cw1 + cw2 + 2 * g
        rw = left + full - rx
        rbh = (ybot - 1.9 - 2 * g) / 3
        for i, (tag, key, hint) in enumerate([
            ("Automatic checks", "auto", "{{auto: what blocks release by itself}}"),
            ("Criteria not met", "fail", "{{fail: where work goes back, and what may ship}}"),
            ("How we review", "review", "{{review: review frequency, triggers and editors}}"),
        ]):
            block(rx, 1.9 + i * (rbh + g), rw, rbh, tag, key, hint)

        y3 = ybot + g - 0.05
        h3 = 7.3 - y3
        hw = (full - g) / 2
        block(left, y3, hw, h3, "Who agreed", "agreed", "{{agreed: roles that accepted, and standard}}")
        block(left + hw + g, y3, hw, h3, "Decision", "decision", "{{decision: from which date, what changes, and why}}",
              fill=ACCENT_BG, line=None)

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

SECTIONS = [
    ("Business model", [
        ("Mission", "Why the company exists, as it states it itself."),
        ("Customer segments", "Who it sells to: the customer segments it targets."),
        ("Key value propositions", "What it promises customers first of all."),
        ("Who it differentiates from and how", "Who it compares itself with and how it differs."),
        ("Customer channels", "How it finds customers and delivers the product."),
        ("Customer relationship types", "Self-service, personal manager, community, etc."),
        ("Key partners", "Without whom the business does not work: suppliers, banks, platforms."),
        ("Monetization model", "How it earns: commission, subscription, interest, advertising."),
        ("Awards and achievements", "Prizes, ratings, wins it uses to support its position."),
    ]),
    ("Market size estimate", [
        ("Monthly audience", "Number of active users or visitors per month; state the estimation method."),
        ("Geographic market", "Which countries and regions it operates in."),
        ("Customer base growth rate", "Customer growth over a period; if there is no data, say so."),
        ("Revenue growth rate", "Revenue growth over a period; for private companies usually \"no data\"."),
        ("Market share", "Share of the chosen market with a note on how it was calculated."),
        ("Funding rounds", "Dates, amounts, investors."),
        ("Company size", "Number of employees."),
        ("Year founded", "Year of foundation."),
    ]),
    ("Contacts", [
        ("Website", "Link to the website."),
        ("Social networks", "Links to official accounts."),
        ("Newsletter or blog", "Link to the subscription: it shows news and promotions."),
        ("Knowledge base and cases", "Links to the help center and customer cases."),
    ]),
    ("Product", [
        ("Product category", "Product class in your market classification."),
        ("Ranking position", "Link to the ranking and the place in it."),
        ("Key integrations", "What the product connects to: services, platforms, banks."),
        ("Signals and development vectors", "Where it is heading: new features, hiring, announcements."),
        ("Localization", "Languages, currencies, local specifics."),
    ]),
    ("Competition", [
        ("Main competitor", "Who the competitor itself fights first of all."),
        ("Other competitors", "Other direct competitors."),
        ("Indirect competitors", "Same problems, a different way of solving them."),
    ]),
    ("Pricing and sales", [
        ("Pricing", "Pricing scheme, price, terms of connecting and disconnecting, trial period, tariff grid and its segmentation."),
        ("Sales process", "How the customer comes to buy: on their own, through a manager, by request."),
        ("Acquisition specifics", "How it attracts customers (Acquisition)."),
        ("Activation and onboarding specifics", "How it leads to first value (Activation)."),
        ("Revenue specifics", "How it increases revenue per customer (Revenue)."),
        ("Retention specifics", "How it brings back and retains customers (Retention)."),
        ("Referral specifics", "How it encourages referrals (Referral)."),
    ]),
    ("Users", [
        ("User characteristics", "Significant audience parameters the marketing is tuned to: age, gender, income, etc."),
    ]),
    ("Offer", [
        ("What changes in the customer's life", "The main result for the customer in the competitor's words."),
        ("How it packages the USP", "How it presents the unique selling proposition: slogans, proof."),
        ("Functionality", "Important features, how it describes them, what benefit it guarantees."),
        ("Key screens", "Links to screenshots: sign-up, onboarding, payment, main feature."),
    ]),
    ("Customer reviews", [
        ("What is praised", "Recurring praise from aggregators, social networks, forums."),
        ("What is criticized", "Recurring complaints."),
        ("What customers lack", "Requests and wished-for features."),
    ]),
]

def screen_map_arrow(shapes, x1, y1, x2, y2):
    c = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = MUTED
    c.line.width = Pt(1.5)
    tail = etree.SubElement(c.line._get_or_add_ln(), qn("a:tailEnd"))
    tail.set("type", "triangle")
    return c

def state_modelling_arrow(shapes, x1, y1, x2, y2):
    c = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = MUTED
    c.line.width = Pt(1.5)
    tail = etree.SubElement(c.line._get_or_add_ln(), qn("a:tailEnd"))
    tail.set("type", "triangle")
    return c

def user_flow_arrow(shapes, x1, y1, x2, y2, head=True):
    c = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = MUTED
    c.line.width = Pt(1.5)
    if head:
        ln = c.line._get_or_add_ln()
        tail = etree.SubElement(ln, qn("a:tailEnd"))
        tail.set("type", "triangle")
    return c

CX = [1.4, 3.9, 6.4, 8.9]

TOP, BOTTOM = 1.9, 6.7

def line(shapes, x1, y1, x2, y2, color=MUTED, width=1.5, dash=None, head=None):
    c = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    if dash:
        c.line.dash_style = dash
    if head:
        ln = c.line._get_or_add_ln()
        tail = etree.SubElement(ln, qn("a:tailEnd"))
        tail.set("type", head)
    return c


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

class CustomerSurvey(PptxSpec):
    @property
    def rel(self):
        return "product-research/customer-survey/customer-survey.pptx"

    example = {"text": {
        "title": "FreshDrop team, buyers in Moscow, 3–10 August 2026",
        "hypothesis": "buyers who miss a slot would pay for a reminder; the reminder feature depends on the answer",
        "audience": "buyers with 2+ orders in the last 3 months; 1,800 invited, screening: 1 order a week or more",
        "channel": "email and push; 412 answered (23%); trial run with 20 people",
        "q1": "Do you order groceries online? («Yes» / «No»)",
        "q2": "How often do you miss a delivery slot?",
        "q3": "How much would you pay for a fixed slot, rub?",
        "q4": "Which reminder time do you prefer?",
        "a1": "Yes: 91% (n=412)",
        "a2": "Once a month or more: 38%",
        "a3": "median 150 rub",
        "a4": "15 minutes before: 61%",
        "c1": "most buyers order online",
        "c2": "missed slots are common",
        "c3": "a fixed slot is worth paying for",
        "c4": "a reminder 15 minutes before wins",
        "gaps": "no answers from non-app buyers; no data on the 18–25 group",
        "decision": "build the reminder first; add a slot guarantee to the next release",
        "check": "reminder opened by 40% of users in 2 weeks; missed slots down by a fifth",
    }}

    def draw(self, prs, slide):
        header(slide, "CUSTOMER SURVEY · SURVEY PLAN AND RESULTS",
               "{{title: who ran the survey, whom, when}}")
        sh = slide.shapes
        top = [
            ("Hypothesis and decision", "{{hypothesis: what we test, and the decision it drives}}"),
            ("Whom we survey (screening)", "{{audience: screening condition and people invited}}"),
            ("Channel and collection", "{{channel: how it was sent, answers, trial run}}"),
        ]
        w, gap = 4.0, 0.165
        for i, (tag, token) in enumerate(top):
            x = 0.5 + i * (w + gap)
            text(box(sh, x, 1.25, w, 0.32, fill=ACCENT, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, 1.57, w, 0.85), token, size=10)
        cols = [("Question (closed or open)", "q", 4.2, INK, ["{{q1: exact wording}}", "{{q2: exact wording}}", "{{q3: exact wording}}", "{{q4: exact wording}}"]),
                ("Answers (shares, number of respondents)", "a", 4.0, INK, ["{{a1: shares or 'not in the source'}}", "{{a2: shares or 'not in the source'}}", "{{a3: shares or 'not in the source'}}", "{{a4: shares or 'not in the source'}}"]),
                ("Conclusion", "c", 3.8, BAD, ["{{c1: what follows from the answers}}", "{{c2: what follows from the answers}}", "{{c3: what follows from the answers}}", "{{c4: what follows from the answers}}"])]
        x = 0.5
        for tag, key, cw, color, hint in cols:
            text(box(sh, x, 2.55, cw, 0.32, fill=color, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            for r in range(4):
                text(box(sh, x, 2.87 + r * 0.58, cw, 0.58), hint[r], size=10)
            x += cw + 0.15
        panels = [
            ("What the data does not show", "{{gaps: what is unknown: respondents, groups, caveats}}", BAD, BAD_BG),
            ("Decision", "{{decision: what we change as a result}}", GOOD, GOOD_BG),
            ("Decision check", "{{check: how we check it by behavior, and when}}", INK, None),
        ]
        for i, (tag, token, color, fill) in enumerate(panels):
            px = 0.5 + i * (w + gap)
            text(box(sh, px, 5.2, w, 0.32, fill=color, line=None), tag, size=12, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, px, 5.52, w, 1.6, fill=fill), token, size=11)

class DiaryStudy(PptxSpec):
    @property
    def rel(self):
        return "product-research/diary-study/diary-study.pptx"

    example = {"text": {
        "title": "FreshDrop team, weekly shopping of families, Moscow, August 2026",
        "question": "how families plan and change the weekly order, and what makes them cancel",
        "sample": "14 families, 2 children each on average; 7 days; 2 dropouts",
        "entry": "event-based: an entry after each order; messenger photos of the fridge",
        "a1": "Tue 19:10: opened the app, searched «milk», gave up",
        "a2": "Thu 18:40: ordered by phone, asked for the 19:00 slot",
        "a3": "Sat 10:20: planned the week in the messenger",
        "t1": "«I always lose the slot, it is annoying»",
        "t2": "«The phone is easier, I trust the operator»",
        "t3": "«Relief when the courier calls»",
        "c1": "the family plans on Sunday; the slot is the trigger",
        "c2": "phone ordering is the fallback for missed slots",
        "c3": "weekend planning is the habit to support",
        "interview": "what we clarified: the weekly plan is made on Sunday; cancellation is the fear of a missed slot",
        "gaps": "dropout after day 3 for 2 families; some entries are late",
        "decision": "build the reminder and the weekly plan; test with 50 families",
    }}

    def draw(self, prs, slide):
        header(slide, "DIARY STUDY · DIARY STUDY LOG",
               "{{title: who ran the study, whom, where, year}}")
        sh = slide.shapes
        top = [
            ("Research question", "{{question: what we want to learn about behavior}}"),
            ("Participants and duration", "{{sample: people, group, days, dropout}}"),
            ("Entry: type and medium", "{{entry: entry type and medium}}"),
        ]
        w, gap = 4.0, 0.165
        for i, (tag, token) in enumerate(top):
            x = 0.5 + i * (w + gap)
            text(box(sh, x, 1.25, w, 0.32, fill=ACCENT, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, 1.57, w, 0.8), token, size=10)
        cols = [("Entry: what they did (day, time)", "a", 4.2, INK,
                 ["{{a1: action, place, method; verbatim or 'not in the source'}}", "{{a2: action, place, method; verbatim or 'not in the source'}}", "{{a3: action, place, method; verbatim or 'not in the source'}}"]),
                ("Entry: what they thought and felt", "t", 3.6, INK,
                 ["{{t1: participant's words or 'not in the source'}}", "{{t2: participant's words or 'not in the source'}}", "{{t3: participant's words or 'not in the source'}}"]),
                ("Researcher's conclusion", "c", 4.2, BAD,
                 ["{{c1: what this means, in the researcher's view}}", "{{c2: what this means, in the researcher's view}}", "{{c3: what this means, in the researcher's view}}"])]
        x = 0.5
        for tag, key, cw, color, hint in cols:
            text(box(sh, x, 2.5, cw, 0.32, fill=color, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            for r in range(3):
                text(box(sh, x, 2.82 + r * 0.72, cw, 0.72), hint[r], size=10)
            x += cw + 0.15
        panels = [
            ("Closing interview", "{{interview: what was clarified in the interview}}", INK, None),
            ("Data gaps and risks", "{{gaps: dropout, missing entries, distortions}}", BAD, BAD_BG),
            ("Decision and check", "{{decision: what we change and how we check it}}", GOOD, GOOD_BG),
        ]
        for i, (tag, token, color, fill) in enumerate(panels):
            px = 0.5 + i * (w + gap)
            text(box(sh, px, 5.1, w, 0.32, fill=color, line=None), tag, size=12, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, px, 5.42, w, 1.8, fill=fill), token, size=11)

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

class ExpertInterview(PptxSpec):
    @property
    def rel(self):
        return "product-research/expert-interview/expert-interview.pptx"

    example = {"text": {
        "title": "FreshDrop team, 6 experts from logistics and retail, 20 August 2026",
        "hypothesis": "courier delays are caused by the slot model, not by the route; the slot decision depends on it",
        "experts": "2 former courier managers, 2 category managers, 2 logistics analysts; 6 people",
        "format": "interview, 60 minutes each; led by the product lead, notes by the analyst",
        "q1": "How long does a courier wait at a slot in a dense district?",
        "q2": "Where does a late delivery start: in the slot or in the route?",
        "q3": "What would you fix first in a delivery service?",
        "q4": "What do buyers complain about most?",
        "a1": "«12–15 min» (former courier manager)",
        "a2": "«The slot, the route is fine» (logistics analyst)",
        "a3": "«Slots first» (category manager)",
        "a4": "«Late courier, then no call» (category manager)",
        "c1": "waiting is the main cost",
        "c2": "the slot causes the delay",
        "c3": "the slot model comes first",
        "c4": "calls matter as much as time",
        "gaps": "no experts from the Saint Petersburg market; numbers are from memory",
        "decision": "fix the slot model before the route algorithm",
        "check": "fewer late deliveries in the pilot districts over 4 weeks",
    }}

    def draw(self, prs, slide):
        header(slide, "EXPERT INTERVIEW · EXPERT INTERVIEW PLAN AND RESULTS",
               "{{title: who ran it, with whom, when}}")
        sh = slide.shapes
        top = [
            ("Hypothesis and decision", "{{hypothesis: what we test, and the decision it drives}}"),
            ("Experts (roles)", "{{experts: roles, how each knows consumers, count}}"),
            ("Format and collection", "{{format: interview or workshop; who led and took notes}}"),
        ]
        w, gap = 4.0, 0.165
        for i, (tag, token) in enumerate(top):
            x = 0.5 + i * (w + gap)
            text(box(sh, x, 1.25, w, 0.32, fill=ACCENT, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, 1.57, w, 0.85), token, size=10)
        cols = [("Question to the expert", "q", 4.2, INK, ["{{q1: exact wording or 'not in the source'}}", "{{q2: exact wording or 'not in the source'}}", "{{q3: exact wording or 'not in the source'}}", "{{q4: exact wording or 'not in the source'}}"]),
                ("Answer or summary (role)", "a", 4.0, INK, ["{{a1: what was said and by which role, or authors' summary}}", "{{a2: what was said and by which role, or authors' summary}}", "{{a3: what was said and by which role, or authors' summary}}", "{{a4: what was said and by which role, or authors' summary}}"]),
                ("Conclusion", "c", 3.8, BAD, ["{{c1: what follows from the answers}}", "{{c2: what follows from the answers}}", "{{c3: what follows from the answers}}", "{{c4: what follows from the answers}}"])]
        x = 0.5
        for tag, key, cw, color, hint in cols:
            text(box(sh, x, 2.55, cw, 0.32, fill=color, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            for r in range(4):
                text(box(sh, x, 2.87 + r * 0.58, cw, 0.58), hint[r], size=10)
            x += cw + 0.15
        panels = [
            ("What the data does not show", "{{gaps: what is unknown: participants, verbatim answers, caveats}}", BAD, BAD_BG),
            ("Decision", "{{decision: what we change as a result}}", GOOD, GOOD_BG),
            ("Decision check", "{{check: how we check it with consumers, and when}}", INK, None),
        ]
        for i, (tag, token, color, fill) in enumerate(panels):
            px = 0.5 + i * (w + gap)
            text(box(sh, px, 5.2, w, 0.32, fill=color, line=None), tag, size=12, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, px, 5.52, w, 1.6, fill=fill), token, size=11)

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

class FieldResearch(PptxSpec):
    @property
    def rel(self):
        return "product-research/field-research/field-research.pptx"

    example = {"text": {
        "title": "FreshDrop team, 3 families observed at home, Moscow, August 2026",
        "hypothesis": "at home the family plans the order on the phone during dinner prep and loses the slot when they forget",
        "setting": "3 homes, 2 visits each, 1.5 hours per visit",
        "role": "passive, with clarifying questions; partial immersion",
        "patterns": "all 3 families plan on the phone during cooking; 2 of 3 check the slot after work",
        "refuted": "the family does not compare prices; they choose by habit",
        "decision": "build the reminder into the cooking time; test with 10 families",
        "f1": "Tue 19:10: opened the app, typed «milk», gave up on the slot",
        "f2": "Tue 19:40: called the shop, ordered by phone",
        "f3": "Wed 07:30: checked the slot on the way to work",
        "q1": "«I just want it to come when I am home»",
        "q2": "«The slot is always gone by the evening»",
        "q3": "«I forgot again, the courier left»",
        "i1": "the family plans around the slot, not the price",
        "i2": "the phone is the planning tool at dinner prep",
        "i3": "missed slots push the family back to the shop",
    }}

    def draw(self, prs, slide):
        header(slide, "FIELD RESEARCH · FIELD OBSERVATION LOG",
               "{{title: who observed, where, whom, year}}")
        sh = slide.shapes
        top = [
            ("Hypothesis", "{{hypothesis: in situation X the person does Y because Z}}"),
            ("Place, people, time", "{{setting: where, whom, visits and hours}}"),
            ("Observer's role", "{{role: passive or with questions; full or partial}}"),
        ]
        w, gap = 4.0, 0.165
        for i, (tag, token) in enumerate(top):
            x = 0.5 + i * (w + gap)
            text(box(sh, x, 1.25, w, 0.32, fill=ACCENT, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, 1.57, w, 0.8), token, size=10)
        cols = [("Observation (fact only)", "f", 4.2, INK),
                ("The person's words", "q", 3.6, INK),
                ("Interpretation", "i", 4.2, BAD)]
        x = 0.5
        for tag, key, cw, color in cols:
            text(box(sh, x, 2.5, cw, 0.32, fill=color, line=None), tag, size=11, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            hints = {"f": ["{{f%d: what they did, where, in what order}}" % n for n in range(1, 4)],
                     "q": ["{{q%d: verbatim or 'not in the source'}}" % n for n in range(1, 4)],
                     "i": ["{{i%d: why, in the observer's view}}" % n for n in range(1, 4)]}
            for r in range(3):
                text(box(sh, x, 2.82 + r * 0.72, cw, 0.72), hints[key][r], size=10)
            x += cw + 0.15
        panels = [
            ("Repeats across visits", "{{patterns: what repeated, and how many people}}", INK, None),
            ("Not confirmed", "{{refuted: what did not match, or stayed unclear}}", BAD, BAD_BG),
            ("Decision and check", "{{decision: what we change, and how we check it}}", GOOD, GOOD_BG),
        ]
        for i, (tag, token, color, fill) in enumerate(panels):
            px = 0.5 + i * (w + gap)
            text(box(sh, px, 5.1, w, 0.32, fill=color, line=None), tag, size=12, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, px, 5.42, w, 1.8, fill=fill), token, size=11)

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

class InDepthInterview(XlsxSpec):
    @property
    def rel(self):
        return "product-research/in-depth-interview/in-depth-interview.xlsx"

    example = {"text": {
        "title": "FreshDrop, ordering habits of families, August 2026, 8 interviews",
        "hypothesis": "parents who order weekly plan the order on Sunday because the slot is fixed",
        "who": "8 weekly buyers from Moscow, found through the app survey; 45 minutes each",
        "goal": "learn how the weekly order is planned and what breaks it; the slot choice decision depends on it",
        "t1": "Weekly planning", "c1": "when the order is planned and by whom",
        "q1": "Tell me about the last time you planned the week's groceries.", "f1": "Which day? Did you check the fridge first?",
        "t2": "Slot choice", "c2": "how the delivery slot is picked and how often it is full",
        "q2": "Walk me through the last slot you booked.", "f2": "Was there a slot you wanted and could not get? What did you do?",
        "t3": "Lost orders", "c3": "orders dropped or moved to a shop",
        "q3": "Tell me about the last time an order fell through.", "f3": "How much did it cost you in time and money? Where did you buy instead?",
        "t4": "Payment", "c4": "which payment method is used and why",
        "q4": "Tell me about the last time you paid for an order in the app.", "f4": "Did you try to pay another way? Was the card form a problem?",
        "t5": "Willingness to pay", "c5": "whether a fixed slot is worth money, by past behaviour",
        "q5": "Tell me about a time you paid extra for a delivery.", "f5": "What did you pay? Would you pay again next week?",
        "findings": "6 of 8 plan on Sunday; 5 lost a slot in the last month; separately, 2 said they would pay more for a fixed slot (opinion only)",
        "decision": "hypothesis confirmed; build the slot reminder and test it with 50 buyers",
        "gaps": "no buyers from outside the Moscow ring road; no answers from non-weekly buyers",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Interview"

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        thin = Side(style="thin", color="C9CED6")
        wrap = Alignment(wrap_text=True, vertical="top")

        def note(cell, hint, height=100):
            return comment(cell, hint, height=height, width=260)

        def dv_list(values, ref):
            dv = DataValidation(type="list", formula1=f'"{values}"', allow_blank=True, errorStyle="warning",
                                showErrorMessage=True, error=f"Values: {values}")
            dv.add(ref)
            ws.add_data_validation(dv)

        def header_cell(r, c, title, hint, width=None):
            cell = ws.cell(r, c, title)
            cell.font, cell.fill = bold, head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="center")
            cell.border = Border(bottom=thin)
            note(cell, hint, 110)
            if width:
                ws.column_dimensions[cell.column_letter].width = width

        ws["A1"] = "Depth interview: {{title: research topic, segment and date}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:H1")

        top = [
            (2, "Hypothesis:", "{{hypothesis: the statement we test}}", bold),
            (3, "Respondents:", "{{who: who and how many, how selected, interview length}}", regular),
            (4, "Goal:", "{{goal: learning goal and the decision behind it}}", regular),
        ]
        for r, name, token, font in top:
            ws.cell(r, 1, name).font = muted
            c = ws.cell(r, 2, token)
            c.font, c.alignment = font, wrap
            ws.merge_cells(f"B{r}:H{r}")
            ws.row_dimensions[r].height = 32

        # guide
        ws["A6"] = "Interview guide"
        ws["A6"].font = bold
        gh = 7
        header_cell(gh, 1, "№", "Theme number. The answer log refers to the question by it.", 14)
        header_cell(gh, 2, "Theme", "Short name of a block of the conversation, for example \"payment method\", \"last time they refused\".", 22)
        header_cell(gh, 3, "What we check", "Which part of the hypothesis the theme covers. Without it the question is not needed.", 24)
        header_cell(gh, 4, "Main question", "Open question about a concrete past case: \"Tell me about the last time when...\". "
                           "Not \"did you like it\" and not \"would you...\".", 44)
        header_cell(gh, 5, "Follow-ups", "Nested questions: when it was, how much time and money it took, what they did next. "
                           "Probing \"tell me more\" prompts are not written in advance.", 36)
        for i in range(1, 6):
            r = gh + i
            ws.cell(r, 1, i).font = bold
            ws.cell(r, 1).alignment = wrap
            for c, (key, hint) in [(2, ("t", "theme name")), (3, ("c", "what exactly we check")),
                                   (4, ("q", "main question about a past case")), (5, ("f", "follow-up questions"))]:
                cell = ws.cell(r, c, f"{{{{{key}{i}: {hint}}}}}")
                cell.font, cell.alignment = regular, wrap
            ws.row_dimensions[r].height = 46

        # conclusions
        concl = [
            (14, "Findings:", "{{findings: repeated cases and separate opinions}}"),
            (15, "Decision:", "{{decision: decision taken, hypothesis confirmed or not}}"),
            (16, "What is missing:", "{{gaps: what was not clarified, uncovered roles, open numbers}}"),
        ]
        for r, name, token in concl:
            ws.cell(r, 1, name).font = muted
            c = ws.cell(r, 2, token)
            c.font, c.alignment = regular, wrap
            ws.merge_cells(f"B{r}:H{r}")
            ws.row_dimensions[r].height = 46

        # log
        ws["A18"] = "Answer log: one row is one record from an interview"
        ws["A18"].font = bold
        hr = 19
        cols = [
            ("Respondent", "Respondent code (R1, R2...), not a name. One row is one record; a respondent has many.", 14),
            ("Role", "Respondent's job title or role: roles are recorded separately, they have different emphases.", 22),
            ("Theme (no.)", "Theme number from the guide or its name; for something unexpected, \"outside the guide\".", 24),
            ("What happened", "Fact: when, what they did, how much time and money it took. Only what the person said, without your assessment.", 44),
            ("Quote", "Respondent's exact phrase. If it was not recorded verbatim, leave it empty instead of paraphrasing. Empty = no data: do not write placeholders.", 36),
            ("Signal", "Time or money spent on a solution, strong emotion (irritation, relief). "
                       "A sign that the problem is real.", 26),
            ("Data type", "Fact from the past, opinion or intention (\"we would...\", \"I usually...\"), idea or request (a request to add a feature), "
                           "compliment. Facts weigh more than the rest. Empty = no data: do not write placeholders.", 22),
            ("What it means", "Your interpretation, separate from the facts: which part of the hypothesis it confirms, refutes or leaves open.", 36),
        ]
        for i, (t, h, w) in enumerate(cols, start=1):
            header_cell(hr, i, t, h, w)
        ws.row_dimensions[hr].height = 34

        first, last = hr + 1, hr + 100
        for r in range(first, last + 1):
            for c in range(1, 9):
                ws.cell(r, c).font = regular
                ws.cell(r, c).alignment = wrap
        ws.freeze_panes = None
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'Interview'!$A${first}")
        dv_list("fact from the past,opinion or intention,idea or request,compliment", f"G{first}:G{last}")

        rng = lambda col: f"${col}${first}:${col}${last}"
        ws.column_dimensions["I"].width = 3
        ws.column_dimensions["J"].width = 34
        ws.column_dimensions["K"].width = 12
        ws["J7"] = "Totals"
        ws["J7"].font, ws["J7"].fill = bold, head_fill
        ws["K7"].fill = head_fill
        stats = [
            ("Records", f'=COUNTA({rng("D")})', "0", "How many records are in the log."),
            ("Respondents", f'=SUMPRODUCT(({rng("A")}<>"")/COUNTIF({rng("A")},{rng("A")}&""))', "0",
             "How many different codes are in the first column."),
            ("Facts from the past", f'=COUNTIF({rng("G")},"fact from the past")', "0", "Records where the person described a case, not an opinion."),
            ("Opinions and intentions", f'=COUNTIF({rng("G")},"opinion or intention")', "0", "Words about the future and \"usually\": weak data."),
            ("Ideas and requests", f'=COUNTIF({rng("G")},"idea or request")', "0", "Feature requests: find out the motive, do not just fulfil them."),
            ("Compliments", f'=COUNTIF({rng("G")},"compliment")', "0", "Praise is not evidence. A growing share is a warning sign."),
            ("Share of facts", '=IF(K8=0,"",K10/K8)', "0%",
             "Facts divided by records. A low share means the interview came down to opinions; it is not a market estimate."),
            ("Records without a quote", f'=SUMPRODUCT(({rng("D")}<>"")*({rng("E")}=""))', "0",
             "Records with an empty quote: check that the wording was not made up."),
            ("Records without a type", f'=SUMPRODUCT(({rng("D")}<>"")*({rng("G")}=""))', "0", "Should be 0: a record without a type cannot be weighed."),
        ]
        for i, (name, formula, fmt, hint) in enumerate(stats, start=8):
            a = ws.cell(i, 10, name)
            a.font = regular
            note(a, hint, 90)
            b = ws.cell(i, 11, formula)
            b.font, b.fill = bold, calc_fill
            b.number_format = fmt

class JtbdInterview(PptxSpec):
    @property
    def rel(self):
        return "product-research/jtbd-interview/jtbd-interview.pptx"

    example = {"text": {
        "title": "FreshDrop, supermarket to delivery, Moscow, Aug 2026",
        "t1": "after a long queue at the shop on a Saturday",
        "t2": "read reviews of delivery services during the evening",
        "t3": "a friend recommended a delivery service with a fixed slot",
        "t4": "compared three apps, checked slot times and the price of delivery",
        "t5": "the first free delivery offer",
        "t6": "chose FreshDrop for the fixed slot and the reminder",
        "t7": "first weekly order went well; the courier was on time; expectations matched",
        "push": "waiting in queues on Saturday cost 2 hours a week",
        "pull": "a fixed slot and a reminder before the courier comes",
        "anxiety": "fear the courier will be late and the food will not arrive in time",
        "habit": "the family is used to shopping on the way home from work",
        "insights": "the job is a dinner on time for the family; the slot is what buyers pay for",
        "decision": "build the reminder and the slot guarantee; check it by the share of weekly orders",
    }}

    def draw(self, prs, slide):
        header(slide, "JTBD INTERVIEW · PURCHASE TIMELINE AND FORCES OF CHOICE",
               "{{title: who, which purchase, date}}")
        sh = slide.shapes
        marks = [
            ("First thought", "{{t1: first thought, when and why}}"),
            ("Passive looking", "{{t2: what they noticed and read}}"),
            ("Event 1", "{{t3: what pushed them to look}}"),
            ("Active looking", "{{t4: alternatives compared, workarounds}}"),
            ("Event 2", "{{t5: last nudge before the decision}}"),
            ("Decision", "{{t6: what they chose and when}}"),
            ("Use", "{{t7: first use, against expectations}}"),
        ]
        w, gap, y = 1.7, 0.07, 1.3
        for i, (tag, token) in enumerate(marks):
            x = 0.5 + i * (w + gap)
            text(box(sh, x, y, w, 0.4, fill=ACCENT, line=None), tag, size=11, bold=True, color=WHITE,
                 align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, y + 0.4, w, 1.85), token, size=10)
        forces = [
            ("→ Push", "{{push: what was wrong with the old way}}", GOOD),
            ("→ Pull", "{{pull: what the new option promised}}", GOOD),
            ("← Anxiety", "{{anxiety: what they feared about the new option}}", BAD),
            ("← Habit", "{{habit: what kept them with the old way}}", BAD),
        ]
        fw, fg, fy = 3.0, 0.107, 3.7
        for i, (tag, token, color) in enumerate(forces):
            x = 0.5 + i * (fw + fg)
            box(sh, x, fy, fw, 1.7, line=color)
            label(sh, x + 0.05, fy + 0.03, fw - 0.1, 0.35, tag, size=12, bold=True, color=color)
            text(box(sh, x + 0.05, fy + 0.4, fw - 0.1, 1.25, line=None), token, size=10)
        panels = [
            (0.5, "What the interviews showed", "{{insights: repeated findings, job and open points}}", INK, None),
            (6.75, "Decision", "{{decision: what we change and the check metric}}", GOOD, GOOD_BG),
        ]
        for x, tag, token, color, fill in panels:
            text(box(sh, x, 5.55, 6.08, 0.32, fill=color, line=None), tag, size=12, bold=True, color=WHITE,
                 anchor=MSO_ANCHOR.MIDDLE)
            text(box(sh, x, 5.87, 6.08, 1.4, fill=fill), token, size=11)

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

class ProblemInterviewScript(XlsxSpec):
    @property
    def rel(self):
        return "product-research/problem-interview-script/problem-interview-script.xlsx"

    example = {"text": {
        "title": "FreshDrop, busy families, Moscow, August 2026",
        "person": "parents with 2+ children who order food weekly",
        "problem": "the courier comes late and the slot is lost; the order is cancelled and the family eats out",
        "cause": "slots are fixed by the shop, not by the family; no reminder",
        "motivation": "a dinner on time; the metric is orders delivered in the slot, target 90%",
        "metric": "share of orders delivered in the chosen slot",
        "hypothesis": "families lose a slot about once a month and want a reminder",
        "who": "12 parents, interviewer and note-taker from the product team",
        "extra": "they plan the week on Sunday; they check the app three times a week",
        "general": "busy, two incomes, shop by phone and by app",
        "context": "they keep a list in a messenger and call the shop when a slot is missed",
        "values": "time with the children; food that is healthy and fresh",
        "pains": "a missed slot is the worst part of the week; the courier does not call",
        "decision": "hypothesis confirmed for 9 of 12 parents; build the reminder first",
        "gaps": "no answers from parents who order only once a month",
    }}

    def draw(self, wb):
        from openpyxl.comments import Comment
        from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
        from openpyxl.workbook.defined_name import DefinedName
        from openpyxl.worksheet.datavalidation import DataValidation

        ws = wb.active
        ws.title = "Script"

        bold = Font(name=FONT, bold=True, size=11)
        regular = Font(name=FONT, size=11)
        muted = Font(name=FONT, size=11, color="6B7280")
        head_fill = PatternFill("solid", fgColor="E8F0FC")
        calc_fill = PatternFill("solid", fgColor="F3F4F6")
        thin = Side(style="thin", color="C9CED6")
        wrap = Alignment(wrap_text=True, vertical="top")

        def note(cell, hint, height=100):
            return comment(cell, hint, height=height, width=260)

        def header_cell(r, c, title, hint, width=None):
            cell = ws.cell(r, c, title)
            cell.font, cell.fill = bold, head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="center")
            cell.border = Border(bottom=thin)
            note(cell, hint, 120)
            if width:
                ws.column_dimensions[cell.column_letter].width = width

        ws["A1"] = "Problem interview script: {{title: segment and problem, date}}"
        ws["A1"].font = Font(name=FONT, bold=True, size=14)
        ws.merge_cells("A1:H1")

        # Step 1: hypothesis
        top = [
            (2, "Person (who has it):", "{{person: segment that has the problem}}"),
            (3, "Problem (what):", "{{problem: behavior and blocker metric}}"),
            (4, "Cause (why):", "{{cause: possible causes of the problem}}"),
            (5, "Motivation (what for):", "{{motivation: desired result and goal metric}}"),
            (6, "Common metric:", "{{metric: one metric for the blocker and goal}}"),
            (7, "Hypothesis:", "{{hypothesis: problem hypothesis in one sentence}}"),
            (8, "Interview:", "{{who: respondents, count, interviewer and note-taker}}"),
        ]
        for r, name, token in top:
            ws.cell(r, 1, name).font = muted
            c = ws.cell(r, 2, token)
            c.font, c.alignment = (bold if r == 7 else regular), wrap
            ws.merge_cells(f"B{r}:H{r}")
            ws.row_dimensions[r].height = 32

        # Step 2: script and answers
        ws["A10"] = "Script"
        ws["A10"].font = bold
        hr = 11
        cols = [
            ("№", "Order of questions: left to right, top to bottom.", 6),
            ("Block", "Script block: behavior, problem, goal, solution or closing.", 16),
            ("Question type", "For example: general about behavior, example, frequency, tools, emotions, presence of a blocker, impact on the goal, "
                            "current solution, \"magic wand\", reverse question.", 24),
            ("Checks", "Part of the hypothesis: Behavior, Blocker metric, Motivation or Cause. A question without a hypothesis part is not needed.", 18),
            ("Question (hypothesis check)", "Open question about a use case, for example \"When was the last time you ___? Can you give an example?\". "
                                           "Do not put the answer in the question.", 44),
            ("Follow-up (new knowledge)", "Question from the new-knowledge flow if the answer did not match the hypothesis: \"Why is ___ important to you?\", \"Who else faces this?\".", 36),
            ("Respondent answer", "Notes on what they answered. No answer: leave it empty; do not write placeholders, they are counted as an answer.", 40),
            ("Matches hypothesis", "Lowercase: yes, no or partially. Assessment of the answer; empty = not yet assessed: do not write placeholders.", 18),
        ]
        for i, (t, h, w) in enumerate(cols, start=1):
            header_cell(hr, i, t, h, w)
        ws.row_dimensions[hr].height = 34

        first, last = hr + 1, hr + 30
        for r in range(first, last + 1):
            for c in range(1, 9):
                ws.cell(r, c).font = regular
                ws.cell(r, c).alignment = wrap
        wb.defined_names["data_start"] = DefinedName("data_start", attr_text=f"'Script'!$A${first}")
        dv = DataValidation(type="list", formula1='"yes,no,partially"', allow_blank=True, errorStyle="warning",
                            showErrorMessage=True, error="Values: yes, no, partially")
        dv.add(f"H{first}:H{last}")
        ws.add_data_validation(dv)

        # Steps 3-4: extra hypotheses, persona, decision (below the 30 script rows)
        base = last + 2
        blocks = [
            ("Extra hypotheses:", "{{extra: additional hypotheses about the persona}}"),
            ("General features:", "{{general: how the persona behaves in general}}"),
            ("Context:", "{{context: how the persona copes now}}"),
            ("Values and goals:", "{{values: what they strive for and value}}"),
            ("Pains and difficulties:", "{{pains: confirmed problems, what hurts most}}"),
            ("Decision:", "{{decision: outcome for the hypothesis and next step}}"),
            ("What is missing:", "{{gaps: what is not clarified, missing answers}}"),
        ]
        ws.cell(base - 1, 1, "Results: persona description in four parts and the decision").font = bold
        for i, (name, token) in enumerate(blocks):
            r = base + i
            ws.cell(r, 1, name).font = muted
            c = ws.cell(r, 2, token)
            c.font, c.alignment = regular, wrap
            ws.merge_cells(f"B{r}:H{r}")
            ws.row_dimensions[r].height = 40

        # totals
        rng = lambda col: f"${col}${first}:${col}${last}"
        ws.column_dimensions["I"].width = 3
        ws.column_dimensions["J"].width = 30
        ws.column_dimensions["K"].width = 12
        ws["J11"] = "Answer totals"
        ws["J11"].font, ws["J11"].fill = bold, head_fill
        ws["K11"].fill = head_fill
        stats = [
            ("Questions with an answer", f'=COUNTA({rng("G")})', "0", "How many rows have notes on the answer."),
            ("Matched", f'=COUNTIF({rng("H")},"yes")', "0", "Answers that confirm the hypothesis."),
            ("Did not match", f'=COUNTIF({rng("H")},"no")', "0", "Answers that refute the hypothesis: see the new-knowledge flow."),
            ("Partially", f'=COUNTIF({rng("H")},"partially")', "0", "Partial match."),
            ("Answers without assessment", f'=SUMPRODUCT(({rng("G")}<>"")*({rng("H")}=""))', "0",
             "There is an answer but no \"matches\" assessment. Should be 0 after review."),
        ]
        for i, (name, formula, fmt, hint) in enumerate(stats, start=12):
            a = ws.cell(i, 10, name)
            a.font = regular
            note(a, hint, 80)
            b = ws.cell(i, 11, formula)
            b.font, b.fill = bold, calc_fill
            b.number_format = fmt

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
        "scenario": "what the person wants to do and where it starts and ends, in one or two lines",
        "change": "which screens are added, removed, merged or moved, and why",
        "transitions": "from → to, who triggers it: user (action) or system (event)",
        "states": "loading, data, empty, error: which screens and what is visible",
        "affected": "screens of other teams affected by the change; what did not make it onto the map",
        "decision": "what was kept, merged, removed or added, and why",
        "check": "how it was checked (test, metric) and what came out; what was not measured",
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

class StateModelling(PptxSpec):
    @property
    def rel(self):
        return "product-handoff/state-modelling/state-modelling.pptx"

    example = {"text": {
        "title": "FreshDrop order, from placed to delivered",
        "entity": "what the object is; where its lifecycle starts and ends",
        "scope": "which events change states; what is outside the model",
        "s1": "name and meaning",
        "s2": "name and meaning",
        "s3": "name and meaning",
        "s4": "name and meaning",
        "s5": "name and meaning",
        "s6": "name and meaning",
        "s7": "name and meaning",
        "e1": "final success state: name and meaning",
        "e2": "final failure state: name and meaning",
        "start": "creation event",
        "t8": "return to an intermediate state: event [condition]",
        "tc": "cancel arrows: event, from which states",
        "t1": "event [condition]",
        "t2": "event [condition]",
        "t3": "event [condition]",
        "t4": "event [condition]",
        "t5": "event [condition]",
        "t6": "event [condition]",
        "t7": "event [condition]",
        "t9": "event [condition]",
        "forbidden": "lines \"from → to → system reaction\": transitions that must not happen",
        "gaps": "states and transitions missing from the diagram or the source",
        "decision": "what was agreed: states, transition rules, where they are recorded and why",
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

class UserFlow(PptxSpec):
    @property
    def rel(self):
        return "product-planning/user-flow/user-flow.pptx"

    example = {"text": {
        "title": "FreshDrop app, buyer books a slot, 1 flow in one line",
        "goal": "what the person wants to get, as \"I want X so that Y\"",
        "scope": "where the entry is, what counts as the end, which neighboring flows are left out of the diagram",
        "start": "flow entry",
        "s1": "screen: user action",
        "s2": "screen: user action",
        "s3": "screen: user action",
        "s4": "screen: user action",
        "end": "end: the result for the user",
        "cond": "is the chosen slot still free?",
        "alt": "screen: choose another slot on the «no» branch",
        "other": "neighboring flows with their own end; alternative entries",
        "issues": "where people got lost before the changes: dead ends, extra steps, from a test or data",
        "decision": "what we merged, removed, moved and why",
        "check": "how we verified (test, metric) and what we got; what we did not measure",
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

# ---------------------------------------------------------------- pdm-brief deck slides
class IntakeTitle(PptxSpec):
    @property
    def rel(self):
        return "pdm-brief/title.pptx"

    def draw(self, prs, slide):
        label(slide.shapes, 0.5, 0.3, 12.3, 0.35, "DECK · TITLE", size=12, bold=True, color=ACCENT)
        text(box(slide.shapes, 0.5, 2.2, 12.3, 1.6), "{{title: the task in one line}}",
             size=34, bold=True, anchor=MSO_ANCHOR.BOTTOM)
        box(slide.shapes, 0.5, 3.95, 2.4, 0.06, fill=ACCENT, line=None)
        text(box(slide.shapes, 0.5, 4.2, 12.3, 0.8), "{{subtitle: audience and the decision the deck prepares}}", size=16)
        label(slide.shapes, 0.5, 6.2, 6.0, 0.35, "Date", size=11, bold=True, color=MUTED)
        text(box(slide.shapes, 0.5, 6.5, 6.0, 0.45), "{{date: date of the deck}}", size=12)


class IntakeSources(PptxSpec):
    @property
    def rel(self):
        return "pdm-brief/sources.pptx"

    def draw(self, prs, slide):
        header(slide, "SOURCES AND DATA", "{{title: what the deck rests on}}")
        cols = [
            ("Official", "Regulator or government; with edition and date", ACCENT, ACCENT_BG,
             "{{sources_official: act or page, edition date, date read, what it confirms}}"),
            ("Corporate", "Company's own site; facts about that company only", INK, None,
             "{{sources_corporate: page, date read, what it confirms}}"),
            ("Other", "News, blogs, aggregators; leads, not confirmation", MUTED, None,
             "{{sources_other: outlet, date, what it says, not confirmed}}"),
        ]
        x, w, gap = 0.5, 3.95, 0.225
        for title, sub, color, bg, token in cols:
            head = box(slide.shapes, x, 1.3, w, 0.6, fill=color, line=None)
            text(head, title, size=14, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            p = head.text_frame.add_paragraph()
            r = p.add_run()
            r.text = sub
            r.font.size, r.font.name, r.font.color.rgb = Pt(10), FONT, WHITE
            text(box(slide.shapes, x, 1.9, w, 3.2, fill=bg, line=LINE), token, size=11)
            x += w + gap
        label(slide.shapes, 0.5, 5.3, 6.0, 0.35, "Data used", size=12, bold=True, color=INK)
        text(box(slide.shapes, 0.5, 5.65, 6.0, 1.45, line=None),
             "{{data_used: local files and data with dates; the ticket or brief as a source}}", size=11)
        label(slide.shapes, 6.8, 5.3, 6.0, 0.35, "Not confirmed", size=12, bold=True, color=BAD)
        text(box(slide.shapes, 6.8, 5.65, 6.0, 1.45, line=None),
             "{{not_confirmed: facts without an official source, and why}}", size=11)


class IntakeConclusions(PptxSpec):
    @property
    def rel(self):
        return "pdm-brief/conclusions.pptx"

    def draw(self, prs, slide):
        header(slide, "CONCLUSIONS", "{{title: the answer in one line}}")
        rows = [
            ("Decision", "{{decision: what to do, by whom, by when}}", ACCENT_BG, ACCENT, 1.3, 1.25),
            ("Why", "{{why: the two or three facts that decide it, with tier and date}}", None, INK, 2.7, 1.55),
            ("Risks and assumptions", "{{risks: the weakest assumptions and how to check them}}", None, INK, 4.4, 1.45),
            ("Open questions", "{{open_questions: what must be settled before the next step, and who settles it}}",
             None, INK, 6.0, 1.15),
        ]
        for tag, token, bg, color, y, h in rows:
            head = box(slide.shapes, 0.5, y, 2.8, h, fill=color if bg is None else bg, line=None)
            text(head, tag, size=13, bold=True, color=WHITE if bg is None else ACCENT, anchor=MSO_ANCHOR.MIDDLE)
            text(box(slide.shapes, 3.45, y, 9.38, h, line=LINE), token, size=12, anchor=MSO_ANCHOR.MIDDLE)


class IntakeAssumptions(PptxSpec):
    @property
    def rel(self):
        return "pdm-brief/assumptions.pptx"

    def draw(self, prs, slide):
        header(slide, "ASSUMPTIONS", "{{title: what was taken as given without the PM's answer}}")
        cols = [
            ("Not answered", "Question the PM did not settle", ACCENT, ACCENT_BG,
             "{{questions: each open question, one per line}}"),
            ("Assumed instead", "What the deck takes as true until checked", INK, None,
             "{{assumptions: the assumption behind each question, same order}}"),
            ("Who confirms", "Owner and the moment it must be settled", MUTED, None,
             "{{confirm: owner and by when, same order}}"),
        ]
        x, w, gap = 0.5, 3.95, 0.225
        for title, sub, color, bg, token in cols:
            head = box(slide.shapes, x, 1.3, w, 0.6, fill=color, line=None)
            text(head, title, size=14, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
            p = head.text_frame.add_paragraph()
            r = p.add_run()
            r.text = sub
            r.font.size, r.font.name, r.font.color.rgb = Pt(10), FONT, WHITE
            text(box(slide.shapes, x, 1.9, w, 4.3, fill=bg, line=LINE), token, size=11)
            x += w + gap
        label(slide.shapes, 0.5, 6.35, 12.33, 0.3,
              "Each assumption stays in the deck until its owner confirms or rejects it", size=10, color=MUTED)


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


if __name__ == "__main__":
    import sys
    wanted = sys.argv[1:]
    specs = [cls() for cls in concrete_specs()]
    for spec in specs:
        if wanted and not any(w in spec.rel for w in wanted):
            continue
        Builder(spec).build(ROOT / spec.rel)
    print("ok", len(specs))
