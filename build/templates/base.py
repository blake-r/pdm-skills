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

ROOT = Path(os.environ.get("BUILD_OUT", Path(__file__).resolve().parents[2] / "skills"))
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


# ---------------------------------------------------------------- gantt

def excel_serial(d):
    return (d - dt.date(1899, 12, 30)).days


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
