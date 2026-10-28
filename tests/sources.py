# /// script
# requires-python = ">=3.10"
# ///
"""Register of sources that could not be checked. No LLM, no network.

Usage (from the repository root):
    uv run tests/sources.py

The cards carry no "not opened" or "not verified" marks. Every source whose full text
was not read lives here instead, as a test with the status KNOWN FAILURE. A source counts as
checked only when its full text was read; a link that opens an abstract, a paywall or a login
page is a failure, and the entry names what to find instead (exact title, ISBN, DOI).

Checks:
  1. every card named in an entry exists and still contains the entry's `cite` string,
     so an entry does not outlive the citation it describes;
  2. every KNOWN FAILURE entry has a `need` with at least one search hint;
  3. no card Source section and no Note cell of product_notes.md carries a verification mark again.

Known failures are listed and do not fail the run. The run exits with 1 only for a broken
entry or a mark that came back. When a source is finally read, delete its entry here and let
the card state what was read.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Each entry: cards (paths under skills/), cite (a string the card must contain),
# source (the citation), need (what to obtain, with hints), why (how it failed).
KNOWN_FAILURES = [
    {
        "cards": ["business-planning/balanced-scorecard"],
        "cite": "Measures That Drive Performance",
        "source": "R. S. Kaplan, D. P. Norton, \"The Balanced Scorecard - Measures That Drive Performance\", Harvard Business Review 70(1), Jan-Feb 1992, pp. 71-79.",
        "need": "Full text from HBR or a library database (reprint number 92105 is reported by search snippets only, unconfirmed).",
        "why": "hbr.org page is paywalled.",
    },
    {
        "cards": ["business-planning/balanced-scorecard"],
        "cite": "Strategic Management System",
        "source": "Kaplan, Norton, \"Using the Balanced Scorecard as a Strategic Management System\", HBR 74(1), Jan-Feb 1996, pp. 75-85.",
        "need": "Full text (reprint number 96107 is reported by search snippets only, unconfirmed).",
        "why": "paywalled.",
    },
    {
        "cards": ["business-planning/balanced-scorecard"],
        "cite": "1996 book",
        "source": "Kaplan, Norton, The Balanced Scorecard: Translating Strategy into Action, Harvard Business School Press, 1996.",
        "need": "The book, pages on the strategy map. ISBN 0-87584-651-3.",
        "why": "book, no open copy.",
    },
    {
        "cards": ["business-planning/rapid-decision-rights"],
        "cite": "Who Has the D?",
        "source": "P. Rogers, M. Blenko, \"Who Has the D? How Clear Decision Roles Enhance Organizational Performance\", HBR 84(1), January 2006.",
        "need": "Full text from HBR or a library database (reprint R0601D, 11 pages).",
        "why": "hbr.org and store.hbr.org show the abstract only; the Wyeth case and role definitions are corroborated by three Bain pages cited in the card.",
    },
    {
        "cards": ["business-planning/rapid-decision-rights"],
        "cite": "Decide & Deliver",
        "source": "M. Blenko, M. Mankins, P. Rogers, Decide & Deliver: 5 Steps to Breakthrough Performance in Your Organization, Harvard Business Press, 2010.",
        "need": "The book; chapters on RAPID roles.",
        "why": "book, no open copy.",
    },
    {
        "cards": ["product-handoff/service-blueprint"],
        "cite": "Designing Services That Deliver",
        "source": "G. L. Shostack, \"Designing Services That Deliver\", HBR 62(1), Jan-Feb 1984, pp. 133-139.",
        "need": "Full text from HBR or a library database (reprint number 84115 is unconfirmed).",
        "why": "hbr.org page is paywalled; Wikipedia and an NTNU review confirm the citation (62(1), pp. 133-139) but not the text.",
    },
    {
        "cards": ["business-analysis/ge-mckinsey-matrix"],
        "cite": "Industry Attractiveness-Business Strength Matrix",
        "source": "A. C. Hax, N. S. Majluf, \"The Use of the Industry Attractiveness-Business Strength Matrix in Strategic Planning\", Interfaces 13(2), 1983, pp. 54-71. DOI 10.1287/inte.13.2.54.",
        "need": "Full text with the procedure and examples (the companion paper on the growth-share matrix is Interfaces 13(1), pp. 46-60, not this one); or a textbook chapter by the same authors (Hax, Majluf, Strategic Management: An Integrative Perspective, Prentice Hall, 1984).",
        "why": "pubsonline.informs.org shows the abstract; the PDF link needs a login.",
    },
    {
        "cards": ["business-analysis/ge-mckinsey-matrix"],
        "cite": "What's Watt",
        "source": "M. G. Allen, \"Diagramming GE's Planning for What's Watt\", Planning Review 5(5), May 1977, pp. 3-9. DOI 10.1108/eb053813.",
        "need": "Full text.",
        "why": "emerald.com shows the abstract; the article is pay-per-view. A 1977 Fortune interview with Allen (digital.weber.edu, item 43882) confirms the GE background only.",
    },
    {
        "cards": ["business-analysis/value-chain-and-nets"],
        "cite": "Competitive Advantage",
        "source": "M. E. Porter, Competitive Advantage: Creating and Sustaining Superior Performance, The Free Press, 1985, chapter 2 \"The Value Chain\".",
        "need": "The book, chapter 2 \"The Value Chain and Competitive Advantage\" (pp. 33-61 reported by catalogues; IfM Cambridge cites it as ch. 1, pp. 11-15, a conflict to settle). ISBN 0-02-925090-0 is confirmed by Open Library.",
        "why": "book, no open copy; the activity list is taken from the IfM Cambridge page and matches.",
    },
    {
        "cards": ["business-analysis/value-chain-and-nets"],
        "cite": "Co-opetition",
        "source": "A. Brandenburger, B. Nalebuff, Co-opetition, Currency Doubleday, 1996.",
        "need": "The book, chapters on the value net and the roles.",
        "why": "book; the four roles are corroborated by the authors' strategy+business article (1997) and TechTarget.",
    },
    {
        "cards": ["business-planning/risk-register"],
        "cite": "Circular A-11",
        "source": "OMB Circular No. A-11, section on enterprise risk management (the definition of a risk register quoted by NIST IR 8286r1).",
        "need": "The current A-11 text of the section that defines the risk register; Fig. 4 of NIST IR 8286r1 viewed as an image.",
        "why": "the NIST quote of the definition (\"a repository of risk information...\") was not found in the A-11 texts of 2020 and 2025 (checked in full; likely an older edition); Fig. 4 is an image, known by its caption and Table 1. A-11 (2025) Capital Programming Guide p. 916 has its own risk register table.",
    },
    {
        "cards": ["product-analysis/rfm-analysis"],
        "cite": "Strategic Database Marketing",
        "source": "A. M. Hughes, Strategic Database Marketing, Probus, 1994 (Open Library OL1182563M).",
        "need": "The book, chapter on RFM, to confirm the five levels per attribute and 125 cells; and a source naming the origin of RFM in direct-mail catalog retail.",
        "why": "book; Wikipedia confirms the catalog industry and five bins (125 segments), not the origin or the book; the origin of the method has no primary source.",
    },
    {
        "cards": ["product-planning/elevator-pitch"],
        "cite": "Crossing the Chasm",
        "source": "G. A. Moore, Crossing the Chasm, HarperBusiness, 1991 (positioning chapter, the \"For ... who ...\" statement).",
        "need": "The book, exact wording, chapter and page of the positioning statement; state the edition.",
        "why": "book; retellings differ in wording (MIT CSAIL: \"who ... need or opportunity\"; others: \"who are dissatisfied with\"); one blog cites p. 186 of the 3rd edition (2014).",
    },
    {
        "cards": ["product-planning/ice-scoring"],
        "cite": "Hacking Growth",
        "source": "S. Ellis, M. Brown, Hacking Growth, Crown Business, 2017.",
        "need": "The book, the passage on ICE scoring: how the three scores are combined (average or product).",
        "why": "book; the average variant is confirmed by a book summary and growthmethod.com, the product formula comes from Itamar Gilad.",
    },
    {
        "cards": ["product-planning/moscow-prioritization"],
        "cite": "Case Method Fast-Track",
        "source": "D. Clegg, R. Barker, Case Method Fast-Track: A RAD Approach, Addison-Wesley, 1994.",
        "need": "The book, the passage that introduces MoSCoW; or an Agile Business Consortium page that names Clegg.",
        "why": "book; Wikipedia (names the book, 1994) and a Pearson-hosted footnote (names Clegg, Oracle UK) agree; no Agile Business Consortium page names Clegg.",
    },
    {
        "cards": ["product-planning/opportunity-solution-tree"],
        "cite": "Continuous Discovery Habits",
        "source": "T. Torres, Continuous Discovery Habits, Product Talk, 2021.",
        "need": "The book, the chapters on the opportunity solution tree.",
        "why": "book; the steps are taken from producttalk.org.",
    },
    {
        "cards": ["product-planning/pugh-matrix"],
        "cite": "Concept selection",
        "source": "S. Pugh, \"Concept selection - a method that works\", Proceedings of ICED 81, Rome, Tecniche Nuove, 1981, pp. 497-506.",
        "need": "The paper.",
        "why": "no open copy; cited from the bibliography of Total Design.",
    },
    {
        "cards": ["product-planning/storytelling"],
        "cite": "Resonate",
        "source": "N. Duarte, Resonate: Present Visual Stories that Transform Audiences, Wiley, 2010.",
        "need": "The book; the scheme is checked against the TED talk transcript only.",
        "why": "book.",
    },
    {
        "cards": ["product-research/expert-interview"],
        "cite": "Interviewing Experts",
        "source": "A. Bogner, B. Littig, W. Menz (eds.), Interviewing Experts, Palgrave Macmillan, 2009; M. Meuser, U. Nagel, \"The Expert Interview and Changes in Knowledge Production\", pp. 17-42, DOI 10.1057/9780230244276_2.",
        "need": "Text of the 2009 chapter. The 1991 German chapter is open at ssoar.info/ssoar/handle/document/2402 and is cited in the card.",
        "why": "publisher pages show details only.",
    },
    {
        "cards": ["product-validation/packaging-offer-test"],
        "cite": "4-Hour Workweek",
        "source": "T. Ferriss, The 4-Hour Workweek, Crown, 2007 (the title test).",
        "need": "The book, the passage on testing the title with AdWords; the number of titles tested (sources diverge: six or more than a dozen).",
        "why": "book; the case is known from retellings.",
    },
    {
        "cards": ["business-planning/business-model-patterns"],
        "cite": "business_model_research",
        "source": "Miro board linked from the PAF page on business model research.",
        "need": "The board content, or a PAF statement of where the patterns come from.",
        "why": "the board needs a login.",
    },
    {
        "cards": ["business-planning/usp-4u"],
        "cite": "Masterson",
        "source": "M. Masterson, the text that introduces the 4 U's (book Ready, Fire, Aim, 2008, or an earlier AWAI text).",
        "need": "The primary text that names the four features; the link between the formula and the book.",
        "why": "only secondary retellings found.",
    },
    {
        "cards": ["business-planning/usp-aida"],
        "cite": "Sheldon",
        "source": "A. F. Sheldon, Successful Selling, 1911; Barry, Howard, \"A review and critique of the hierarchy of effects in advertising\", Int. J. of Advertising 9(2), 1990.",
        "need": "The book (the card cites Wikipedia for it) and the article (AIDAS variant). Strong 1925 was read in full and is cited in the card.",
        "why": "no open copy found; the dates come from Wikipedia.",
    },
    {
        "cards": ["business-planning/usp-habitual-without-habitual"],
        "cite": "familiar",
        "source": "The primary source of the \"familiar thing without a familiar element\" formula.",
        "need": "Any publication that names the author and year of the formula.",
        "why": "a search by the exact phrase shows neither an author nor a publication.",
    },
    {
        "cards": ["product-validation/hadi-canvas"],
        "cite": "HADI",
        "source": "The original note with the canvas layout (lanes and period data).",
        "need": "A public primary source of the canvas layout.",
        "why": "none found.",
    },
]

# Phrases that mark a source as unchecked. They must not appear in a card's Source section
# or in the Note cell of a catalog row.
MARKS = [
    "not opened", "was not opened", "were not opened", "not verified", "could not be verified",
    "could not be accessed", "could not be opened", "was not read", "were not read",
    "not read (", "paywalled", "text not opened", "was not checked", "were not checked",
    "unverified", "was not viewed", "not consulted", "not cross-checked",
]


def source_section(text):
    m = re.search(r"## Source\n(.*?)\n## See also", text, re.S)
    return m.group(1) if m else ""


def main():
    problems = []

    for i, e in enumerate(KNOWN_FAILURES, 1):
        for key in ("cards", "cite", "source", "need", "why"):
            if not e.get(key):
                problems.append(f"entry {i}: missing '{key}'")
        for c in e.get("cards", []):
            path = ROOT / "skills" / c / "card.md"
            if not path.exists():
                problems.append(f"entry {i}: no card {c}")
                continue
            body = path.read_text()
            if e["cite"] not in body:
                problems.append(f"entry {i}: card {c} does not contain '{e['cite']}'")

    for path in sorted((ROOT / "skills").glob("*/*/card.md")):
        low = source_section(path.read_text()).lower()
        for mark in MARKS:
            if mark in low:
                problems.append(f"{path.relative_to(ROOT)}: Source section carries the mark '{mark}'")

    for n, line in enumerate((ROOT / "product_notes.md").read_text().splitlines(), 1):
        if line.startswith("| ["):
            cells = line.split("|")
            note = cells[-2].lower() if len(cells) > 2 else ""
            for mark in MARKS:
                if mark in note:
                    problems.append(f"product_notes.md:{n}: Note carries the mark '{mark}'")

    for e in KNOWN_FAILURES:
        print(f"KNOWN FAILURE  {e['source']}")
        print(f"    cards: {', '.join(e['cards'])}")
        print(f"    failed: {e['why']}")
        print(f"    need: {e['need']}")
    print(f"\n{len(KNOWN_FAILURES)} known failures (sources not read in full).")

    if problems:
        print("\nPROBLEMS:")
        for p in problems:
            print(" -", p)
        return 1
    print("Register is consistent; no verification marks in cards or notes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
