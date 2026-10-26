"""Mechanical checks of every card against build/quality_gate.md.

Usage (from the repository root): uv run -q python3 build/quality_gate.py [card.md ...]

Without arguments checks every skills/<category>/<tool>/card.md. Prints one line per
problem and a final count; prints nothing else for cards that pass.

Checks: exactly one H1; the eight H2 sections in the required order; word limit per
section; "See also" bullets name existing tools of the set with a relation and a way to use
them together; SKILL.md present, its name equals the directory, not hidden from the model;
template named <tool>.pptx or <tool>.xlsx.
Without arguments also checks the navigator skills/ask-pdm/SKILL.md (N1-N3) and the intake skill
skills/pdm-brief/SKILL.md (I1-I4).
"""

import glob
import json
import os
import re
import sys

H2 = ["Essence", "When to use and when not to", "Scheme", "How to apply", "Example", "Common mistakes", "Source", "See also"]
# Bullet form in "See also": "<Phrase> <Tool name>: <how to use them together>"
PHRASES = {"Enhanced by": "complements", "Alternative to": "alternative",
           "Preceded by": "precedes", "Followed by": "follows",
           "Improved by": "improved_by", "Used to improve": "improves"}
BULLET = re.compile(r"^- (" + "|".join(PHRASES) + r") (.+?): (.+)$", re.M)
# Per-section word limits; the rule behind the numbers is in build/section_stats.py.
LIMITS = {"Essence": 200, "When to use and when not to": 300, "Scheme": 200, "How to apply": 400,
          "Example": 400, "Common mistakes": 200, "Source": 200}
# Each "See also" bullet, counted after the phrase and the tool name.
LINK_LIMIT = 15
PURPOSE_LIMIT = 15  # words in an ask-pdm table purpose
WORD = r"[A-Za-z0-9]+(?:[-–][A-Za-z0-9]+)*"


def count(text):
    return len(re.findall(WORD, text))


def tool_names(cards):
    names = {}
    for card in cards:
        h1 = re.findall(r"^# (.+)$", open(card, encoding="utf-8").read(), re.M)
        names[h1[0].strip() if h1 else os.path.basename(os.path.dirname(card))] = os.path.dirname(card)
    return names


# Runs in its own environment (uv --with), because the repo env has no python-pptx or openpyxl.
# It lists the placeholder keys of one template, with the same token syntax as the fill scripts.
PROBE = r'''
import json, re, sys
TOKEN = re.compile(r"\{\{\s*([A-Za-z0-9_]+)\s*(?::([^}]*))?\}\}")
path, keys = sys.argv[1], set()
if path.endswith(".pptx"):
    from pptx import Presentation
    def texts(shapes):
        for s in shapes:
            if hasattr(s, "shapes"):
                yield from texts(s.shapes)
            if s.has_text_frame:
                yield s.text_frame.text
            if getattr(s, "has_table", False) and s.has_table:
                for row in s.table.rows:
                    for cell in row.cells:
                        yield cell.text
    for slide in Presentation(path).slides:
        for t in texts(slide.shapes):
            keys.update(m.group(1) for m in TOKEN.finditer(t))
else:
    import openpyxl
    for ws in openpyxl.load_workbook(path).worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str):
                    keys.update(m.group(1) for m in TOKEN.finditer(c.value))
print(json.dumps(sorted(keys)))
'''


def example_problems(template, data):
    """example.json "text" must give a value for every placeholder of the template and nothing else."""
    import subprocess
    run = subprocess.run(["uv", "run", "-q", "--with", "python-pptx", "--with", "openpyxl",
                          "python3", "-c", PROBE, template], capture_output=True, text=True)
    if run.returncode != 0:
        return [f"cannot read placeholders of {os.path.basename(template)}: {run.stderr.strip().splitlines()[-1:]}"]
    placeholders = set(json.loads(run.stdout))
    given = set(data.get("text", {}))
    out = []
    if placeholders - given:
        out.append("example.json has no value for placeholder(s): " + ", ".join(sorted(placeholders - given)))
    if given - placeholders:
        out.append("example.json gives a value for key(s) with no placeholder in the template: "
                   + ", ".join(sorted(given - placeholders)))
    if not out:
        out += fill_problems(template)
    return out


def fill_problems(template):
    """Filling the template with its example must not fail and must not warn that text does not fit."""
    import subprocess
    import tempfile
    folder = os.path.dirname(template)
    script = "scripts/fill_pptx.py" if template.endswith(".pptx") else "scripts/fill_xlsx.py"
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, os.path.basename(template))
        run = subprocess.run(["uv", "run", "-q", script, template, os.path.join(folder, "example.json"), out, "--force"],
                             capture_output=True, text=True)
    if run.returncode != 0:
        return [f"filling the example fails: {run.stderr.strip().splitlines()[-1:]}"]
    misfits = [line for line in run.stderr.splitlines() if "does not fit" in line]
    if misfits:
        return [f"filling the example leaves {len(misfits)} text(s) that do not fit the box, first: {misfits[0][:120]}"]
    return []


def check(card, names):
    problems = []
    d = os.path.dirname(card)
    tool = os.path.basename(d)
    text = open(card, encoding="utf-8").read()
    body = re.sub(r"\(http[^)]*\)", "", text)  # links do not count as words or mentions

    if len(re.findall(r"^# .+$", text, re.M)) != 1:
        problems.append("H1 must appear exactly once")
    heads = re.findall(r"^## (.+)$", text, re.M)
    if heads != H2:
        problems.append("H2 sections must be: " + " | ".join(H2) + f"; found: {' | '.join(heads)}")
    for part in re.split(r"^## ", body, flags=re.M)[1:]:
        name, _, section = part.partition("\n")
        name = name.strip()
        n = count(section)
        if name in LIMITS and n > LIMITS[name]:
            problems.append(f"section '{name}' has {n} words, limit {LIMITS[name]}")

    skill = os.path.join(d, "SKILL.md")
    if not os.path.exists(skill):
        problems.append("SKILL.md is missing")
    else:
        s = open(skill, encoding="utf-8").read()
        m = re.search(r"^name:\s*(\S+)", s, re.M)
        if not m or m.group(1) != tool:
            problems.append(f"SKILL.md name must be '{tool}'")
        if "disable-model-invocation" in s:
            problems.append("SKILL.md must not set disable-model-invocation")
        for mode in ("Mode: do", "Mode: review"):
            if mode not in s:
                problems.append(f"SKILL.md must contain '{mode}'")
        if "explicitly asks to see an example" not in s:
            problems.append("SKILL.md must say that example.json is used only when the user explicitly asks to see an example")

    templates = glob.glob(os.path.join(d, "*.pptx")) + glob.glob(os.path.join(d, "*.xlsx"))
    names_t = [os.path.basename(t) for t in templates]
    if not names_t:
        problems.append("template is missing")
    elif f"{tool}.pptx" not in names_t and f"{tool}.xlsx" not in names_t:
        problems.append(f"template must be named {tool}.pptx or {tool}.xlsx; found {', '.join(names_t)}")
    example = os.path.join(d, "example.json")
    if templates and not os.path.exists(example):
        problems.append("example.json is missing next to the template")
    elif os.path.exists(example):
        try:
            data = json.load(open(example, encoding="utf-8"))
            if not isinstance(data, dict) or not ({"text", "rows", "cells", "charts"} & set(data)):
                problems.append("example.json must hold fill data: text, rows, cells or charts")
            elif templates:
                problems += example_problems(templates[0], data)
        except ValueError as e:
            problems.append(f"example.json is not valid JSON: {e}")

    own_dir = os.path.abspath(d)
    for part in re.split(r"^## ", text, flags=re.M)[1:]:
        if part.partition("\n")[0].strip() == "See also":
            section = part.partition("\n")[2]
            bullets = BULLET.findall(section)
            for phrase, name, how in bullets:
                if count(how) > LINK_LIMIT:
                    problems.append(f"'See also': the text for '{name}' has {count(how)} words, limit {LINK_LIMIT}")
                if name not in names:
                    problems.append(f"'See also': '{name}' is not the H1 of a card in the set")
                elif os.path.abspath(names[name]) == own_dir:
                    problems.append(f"'See also': '{name}' is this tool itself")
    return problems


INVERSE = {"precedes": "follows", "follows": "precedes", "complements": "complements", "alternative": "alternative",
           "improved_by": "improves", "improves": "improved_by"}


def links_of(card):
    """'See also' bullets of one card as {target H1: (relation, text)}."""
    text = open(card, encoding="utf-8").read()
    if "\n## See also\n" not in text:
        return {}
    section = text.split("\n## See also\n", 1)[1]
    return {m.group(2): (PHRASES[m.group(1)], m.group(3)) for m in BULLET.finditer(section)}


def check_pairs(cards, names):
    """Compare each link with the link back. Returns {card: [problems]}.

    A link whose reverse exists with a non-matching relation is a contradiction (error).
    A link with no reverse is reported only with --reciprocal, since one-way links are allowed.
    """
    all_links = {}
    for card in cards:
        h1 = next((n for n, d in names.items() if os.path.abspath(d) == os.path.abspath(os.path.dirname(card))), None)
        if h1:
            all_links[h1] = (card, links_of(card))
    out = {}
    for name, (card, links) in all_links.items():
        for target, (rel, _) in links.items():
            if target not in all_links:
                continue
            back = all_links[target][1].get(name)
            if back is None:
                if RECIPROCAL:
                    out.setdefault(card, []).append(f"'See also': no link back from '{target}'")
            elif back[0] != INVERSE[rel]:
                out.setdefault(card, []).append(
                    f"'See also': '{target}' is '{rel}' here but '{back[0]}' back; expected '{INVERSE[rel]}' back")
    return out


def check_plugin_manifest():
    """P1: .claude-plugin/plugin.json lists every skill folder under skills/ and no other."""
    import glob
    import json
    listed = set(json.load(open(".claude-plugin/plugin.json", encoding="utf-8"))["skills"])
    found = {"./" + os.path.dirname(f) for f in glob.glob("skills/*/*/SKILL.md")} | {"./skills/ask-pdm", "./skills/pdm-brief"}
    return ([f"plugin.json: skill folder {x} is not listed" for x in sorted(found - listed)]
            + [f"plugin.json: {x} has no SKILL.md" for x in sorted(listed - found)])


def check_navigator():
    """Checks of skills/ask-pdm/SKILL.md (N1, N2, N3). Returns problem lines."""
    path = "skills/ask-pdm/SKILL.md"
    if not os.path.exists(path):
        return ["skills/ask-pdm: SKILL.md is missing"]
    text = open(path, encoding="utf-8").read()
    rows = re.findall(r"^\| `([^`]*)` \| ([^|]*?) \| (.*?) \|$", text, re.M)
    problems = []
    folders = {}
    for skill in sorted(glob.glob("skills/*/*/SKILL.md")):
        m = re.search(r"^name:\s*(\S+)", open(skill, encoding="utf-8").read(), re.M)
        d = os.path.dirname(skill)
        folders[m.group(1) if m else os.path.basename(d)] = os.path.basename(os.path.dirname(d))
    folders["pdm-brief"] = "-"  # the orchestrator sits directly in skills/, outside any category
    listed = {name for name, _, _ in rows}
    for name, folder in folders.items():
        if name not in listed:
            problems.append(f"skills/ask-pdm: skill '{name}' (skills/{folder}/{name}) is not in the navigator table")
    seen_names = set()
    seen_purpose = {}
    for name, folder, purpose in rows:
        if name not in folders:
            problems.append(f"skills/ask-pdm: row '{name}' names no skill of the set")
        elif folders[name] != folder.strip():
            problems.append(f"skills/ask-pdm: row '{name}' has folder '{folder.strip()}', the skill is in '{folders[name]}'")
        if name in seen_names:
            problems.append(f"skills/ask-pdm: skill '{name}' has more than one row")
        seen_names.add(name)
        if len(purpose.split()) > PURPOSE_LIMIT:
            problems.append(f"skills/ask-pdm: purpose of '{name}' has {len(purpose.split())} words, limit {PURPOSE_LIMIT}")
        key = purpose.strip().lower()
        if key in seen_purpose:
            problems.append(f"skills/ask-pdm: '{name}' has the same purpose as '{seen_purpose[key]}'")
        seen_purpose.setdefault(key, name)
    # N3: exactly five routing examples, each naming an existing tool
    sec = re.search(r"^## Routing examples\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not sec:
        problems.append("skills/ask-pdm: section 'Routing examples' is missing")
    else:
        bullets = [l for l in sec.group(1).splitlines() if l.startswith("- ")]
        if len(bullets) != 5:
            problems.append(f"skills/ask-pdm: 'Routing examples' must have exactly 5 bullets, found {len(bullets)}")
        for b in bullets:
            m = re.search(r"`([^`]+)`\s*$", b)
            if not m or m.group(1) not in folders:
                problems.append(f"skills/ask-pdm: routing example does not end with an existing tool in backticks: {b[:60]}")
    return problems


INTAKE_STEPS = [("grilling dependency", r"grilling dependency"), ("grill on output", r"grill.*output"),
                ("pick tools", r"\btools?\b"), ("context", r"context"), ("roast", r"roast"), ("build the deck", r"deck")]


def check_intake():
    """Checks of skills/pdm-brief/SKILL.md (I1-I4, I6). Returns problem lines."""
    d = "skills/pdm-brief"
    path = os.path.join(d, "SKILL.md")
    if not os.path.exists(path):
        return [f"{d}: SKILL.md is missing"]
    text = open(path, encoding="utf-8").read()
    front = text.split("---")[1] if text.startswith("---") else ""
    problems = []
    m = re.search(r"^name:\s*(\S+)", front, re.M)
    if not m or m.group(1) != os.path.basename(d):
        problems.append(f"{d}: SKILL.md name must be '{os.path.basename(d)}'")
    if not re.search(r"^description:\s*\S", front, re.M):
        problems.append(f"{d}: description is missing")
    if "disable-model-invocation" in front:
        problems.append(f"{d}: SKILL.md must not set disable-model-invocation")
    for f in sorted(set(re.findall(r"scripts/([\w.-]+\.\w+)", text))):
        if not os.path.exists(os.path.join("scripts", f)):
            problems.append(f"{d}: scripts/{f} does not exist")
    if "product_notes.md" in text and not os.path.exists("product_notes.md"):
        problems.append(f"{d}: product_notes.md does not exist")
    for p in sorted(set(re.findall(r"\bskills/[\w./-]+", text))):
        if not os.path.exists(p.rstrip(".")):
            problems.append(f"{d}: {p} does not exist")
    for cat, tool in sorted(set(re.findall(r"\b((?:business|product|development)-[a-z]+)/([a-z0-9-]+)", text))):
        if not os.path.isdir(os.path.join("skills", cat, tool)):
            problems.append(f"{d}: tool '{cat}/{tool}' is not an existing skill")
    for rel in sorted(set(re.findall(r"<base dir>/((?:\.\./)+[^<\s`)]*)", text))):
        if not os.path.exists(os.path.normpath(os.path.join(d, rel))):
            problems.append(f"{d}: <base dir>/{rel} does not resolve")
    for rel in sorted(set(re.findall(r"<base dir>/((?:\.\./)+)<", text))):
        if not os.path.isdir(os.path.normpath(os.path.join(d, rel))):
            problems.append(f"{d}: <base dir>/{rel}<...> does not resolve")
    heads = re.findall(r"^## (.+)$", text, re.M)
    pos = -1
    for label, pat in INTAKE_STEPS:
        idx = next((i for i, h in enumerate(heads) if i > pos and re.search(pat, h, re.I)), None)
        if idx is None:
            problems.append(f"{d}: step '{label}' is missing or out of order in the headings")
        else:
            pos = idx
    if "AskUserQuestion" not in text:
        problems.append(f"{d}: the text does not mention AskUserQuestion")
    return problems


DATA_MODES = {"none", "web", "local", "manual"}
STAGES = {"research", "analysis", "planning", "validation", "execution", "handoff"}


def check_selection_table():
    """Checks the Selection table of product_notes.md: one row per tool skill, allowed modes and stage."""
    if not os.path.exists("product_notes.md"):
        return ["product_notes.md is missing"]
    text = open("product_notes.md", encoding="utf-8").read()
    m = re.search(r"^## Selection table\n(.*?)(?=^## )", text, re.M | re.S)
    if not m:
        return ["product_notes.md: section 'Selection table' is missing"]
    rows = {}
    problems = []
    for line in m.group(1).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5 or not cells[0].startswith("`"):
            continue
        tool = cells[0].strip("`")
        if tool in rows:
            problems.append(f"Selection table: duplicate row for {tool}")
        rows[tool] = cells
        modes = [x.strip() for x in cells[1].split(",")]
        if not modes or not set(modes) <= DATA_MODES:
            problems.append(f"Selection table: {tool}: data modes must be from {sorted(DATA_MODES)}, got '{cells[1]}'")
        if cells[2] not in STAGES:
            problems.append(f"Selection table: {tool}: unknown stage '{cells[2]}'")
        if not cells[3]:
            problems.append(f"Selection table: {tool}: input needed is empty")
        if cells[4] not in ("draft", "reviewed"):
            problems.append(f"Selection table: {tool}: status must be draft or reviewed, got '{cells[4]}'")
    skills = {}
    for card in glob.glob("skills/*/*/card.md"):
        folder = os.path.dirname(card)
        skills[os.path.basename(folder)] = os.path.basename(os.path.dirname(folder))
    for tool in sorted(set(skills) - set(rows)):
        problems.append(f"Selection table: no row for {tool}")
    for tool in sorted(set(rows) - set(skills)):
        problems.append(f"Selection table: row for unknown tool {tool}")
    for tool, cells in rows.items():
        if tool in skills and cells[2] != skills[tool].split("-", 1)[1]:
            problems.append(f"Selection table: {tool}: stage '{cells[2]}' differs from its folder '{skills[tool]}'")
    return problems


def main():
    global RECIPROCAL
    RECIPROCAL = "--reciprocal" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--reciprocal"]
    cards = args or sorted(glob.glob("skills/*/*/card.md"))
    names = tool_names(glob.glob("skills/*/*/card.md"))
    pairs = check_pairs(sorted(glob.glob("skills/*/*/card.md")), names)
    failed = 0
    for card in cards:
        problems = check(card, names) + pairs.get(card, [])
        if problems:
            failed += 1
            for p in problems:
                print(f"{os.path.dirname(card)}: {p}")
    extra = []
    if not args:
        extra = check_navigator() + check_intake() + check_selection_table() + check_plugin_manifest()
        for p in extra:
            print(p)
    print(f"cards: {len(cards)}, with problems: {failed}")
    if failed or extra:
        sys.exit(1)


RECIPROCAL = False


if __name__ == "__main__":
    main()
