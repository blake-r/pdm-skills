# pdm-skills

A Claude Code plugin for product work. You describe a product task in plain words; the plugin picks the right method from more than 100 product-management tools, asks only for what is missing, and gives you a short deck and a written brief with sources and assumptions.

It is for product managers and leads, business analysts, heads of business units, executives, and startup CPOs and CEOs. You do not need to know any of the methods in advance.

## Start here

1. **Install** (once, see below).
2. **Describe the task** in your own words, for example:
   > Use pdm-brief. We want to remove the limit on the number of cards a client can hold. Prepare a decision for the management team.
3. **Answer the questions.** The plugin asks what result you need, who reads it, and what data you have. You choose a quick conclusion (one page for a manager) or a full analysis. If a fact is missing, you pick one of: find it on the web, continue without it, or give it yourself.
4. **Get the result** in a new folder: `deck.pptx` (title, tool slides, conclusions, sources, assumptions) and `brief.md`.

If you only want to know which method fits a question, ask `ask-pdm`.

## What you get

- A deck with a conclusion first, the facts it rests on with source tier and date, and a separate slide with the assumptions taken where nobody answered.
- No invented numbers. A missing value is `N/A`, and the assumption used instead is listed on the assumptions slide.
- Regulatory facts are marked confirmed only when an official source supports them.

## Data the plugin can work with

| Mode | What it means |
|---|---|
| None | Your knowledge and assumptions only. The plugin picks methods that stay honest without numbers. |
| Local files | Documents, tables and decks in a folder you name. |
| Web | Public facts, each with a source tier (official, corporate, other) and a date. |
| Entered by hand | Company numbers you type as aggregates (indicator, value, period, unit). Raw rows, personal data and source code are never needed or accepted, so this works even when security policy forbids sharing real metrics. |

Methods that need numbers are not picked when the run has none. The plugin asks once whether to add a data mode; if you decline, the brief says "not picked: needs data".

## Install

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/), the only tool the scripts need:
   - macOS or Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
2. In Claude Code add this repository as a plugin marketplace and install the plugin: `/plugin marketplace add blake-r/pdm-skills`, then `/plugin install pdm-skills@pdm-skills`. From a local copy of the repository use `/plugin marketplace add ./` (or the full path to the folder) instead. To try it for one session only, without installing, start Claude Code with `claude --plugin-dir <path to the folder>`.
3. `pdm-brief` interviews you before it picks tools. It uses the `grilling` skill from the [mattpocock skills](https://github.com/mattpocock/skills) marketplace if you have it, any other installed grilling skill if not, and a bundled copy of the mattpocock grilling skill as the last resort, so nothing else has to be installed. On the first run it checks for `uv` and tells you the exact steps if it is missing.

Check the install: from the repository root run `uv run scripts/smoke_test.py`. It fills three templates, merges them, checks the layout and runs the catalog checks, with no network and no model. Expected last line: `smoke test passed`.

## What is inside

- `skills/<category>/<tool>/`: for each tool a card (`card.md`: theory, limits, a worked case), a `SKILL.md` with two modes (do and review), a PPTX or XLSX template and an `example.json`. The cases in cards and examples show the format; they are not data for your product.
- `skills/ask-pdm`: finds the tool for a question.
- `skills/pdm-brief`: runs the whole flow from a task to a deck and a brief.
- `product_notes.md`: the catalog, the Selection table (which tool works with which data), the Gaps list and the Chains of tools.
- `scripts/`: filling, merging and checking decks. `build/`: how templates are generated and how cards are checked (`uv run build/quality_gate.py`).

## Missing a method?

If a decision your team must make is covered by no card, `pdm-brief` says "not covered" in the brief. Maintainers add a card only when a primary source exists (the method's author or publisher, or the official page of a standard); otherwise the case goes to the Gaps list in `product_notes.md`. See `build/card_brief.md`.

## Licence

Content CC BY-SA 4.0, code MIT. See `LICENSE`.

### Third-party material

`skills/pdm-brief/third-party/mattpocock-grilling/grilling.md` is the `grilling` skill by Matt Pocock (https://github.com/mattpocock/skills, version 1.2.3, MIT licence, copyright (c) 2026 Matt Pocock), copied unchanged except for the removed frontmatter. His licence text is in the same folder. It is used only when no grilling skill is installed.
