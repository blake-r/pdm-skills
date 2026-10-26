---
name: pdm-brief
description: Turn a product task into a short research or strategy deck built from PAF tools. Interviews the product manager through AskUserQuestion about the desired output, picks PAF tools from this plugin along their chains, collects local and web context (audience, industry, niche), stress-tests the conclusions with the grilling skill, and assembles a mini-presentation from the tools' PPTX templates plus a markdown brief. Use when a product manager asks for research, a strategy, a market or competitor analysis, or a product decision, or asks to build a mini-deck from a task.
---

# PDM Brief

Orchestrates the flow: task -> grilling -> tool selection -> data -> roast -> deck.

The product manager needs no knowledge of the tools or of PAF. They describe the task and the result they want in their own words; you pick the tools. Never ask the PM to name a method.

"You" in this file means the assistant that runs this skill in the product manager's session. It is not the plugin's developer. Every path that starts with `<base dir>` is resolved from the directory this skill was invoked from, never from the PM's working directory: the PM's folder may hold an unrelated project.

Language rules:
- Everything you write to files (SKILL.md, scripts, manifests) is in English.
- Everything you say to the product manager, and every deliverable meant for them (the deck, `brief.md`, the context file, the sources list), is in the language the PM uses with you.

Ask every question through AskUserQuestion, never as plain text. Put the recommended option first and label it "(Recommended)". Max 4 questions per call; split longer rounds. If AskUserQuestion is not available in the session, use the fallback in section 1 and keep going; the fallback narrows what the result can claim, it does not stop the flow.

The skill base directory is given when this skill is invoked. Scripts live at `<base dir>/../../scripts/`. PAF tools are sibling skills at `<base dir>/../<category>/<tool>/`.

## 0. Check the grilling dependency and uv

Run `uv --version`. If `uv` is missing, tell the PM it is the only tool the scripts need and give the install command for their system (macOS or Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`; Windows PowerShell: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`); offer to run it for them through AskUserQuestion. Do not continue without `uv`.

Choose the grilling method once per run, in this order, and record the choice in the context file:

1. The `mattpocock-skills:grilling` skill, if it is installed (it comes from the mattpocock marketplace, `https://github.com/mattpocock/skills`).
2. Any other installed skill that interviews the user about a plan until nothing is left open (its name usually contains "grill"). Read its description first and use it only if it does that.
3. The copy of the mattpocock grilling skill that ships with this plugin: `<base dir>/third-party/mattpocock-grilling/grilling.md` (MIT licence, the licence file is next to it). Read it and follow it as if it were the skill. The flow never stops for lack of a grilling skill. Do not download a grilling skill from the internet during a run: unpinned instructions from the network would steer the interview, and a PM behind a corporate firewall may have no access.

Tell the PM in one line which method is used. Offer to install option 1 only if the PM asks.

## 1. Grill: output and level

Run the chosen grilling method on the task, with one added rule that overrides the method's own format: every question goes through AskUserQuestion (the recommended answer first and labelled "(Recommended)", at most 4 questions per call), never as plain text. Ask first:

- What exactly should the result be (research, strategy, go/no-go decision, pitch)?
- Who is the audience for the deck, and how many slides do they expect?
- What is the business context (already operating, new market, scope)?
- How much is needed: a quick conclusion (the decision, the conditions under which it holds, the assumptions, on one page for a manager) or a full analysis (all tool slides and a full brief)? This choice is made once per run. It sets the volume of the brief and the slides; it never changes which tools are picked. If the PM names no number of slides, a quick conclusion is 4 slides (title, conclusions, sources, assumptions) and a full analysis is the title, one slide per tool, conclusions, sources and assumptions.
- What data is available (the data mode of the run): none (the PM's knowledge and assumptions only), local files, the web, or company numbers the PM enters by hand as aggregates. Several modes can apply; record them all.
- How deep is the PM's experience? Adapt: a beginner gets a one-sentence explanation of each tool and a worked example before each question; an experienced PM gets terse questions and no tutorial.

If AskUserQuestion is not available in the session:
- Start a subagent with the client's default model settings that runs the grilling. If you cannot start a subagent, run the grilling yourself from the same question list and write "grilling not independent" in `brief.md`. The subagent asks the questions above and the grilling skill's own questions, one round at a time, and returns them as a numbered list with its recommended answer for each.
- Answer each question yourself, as the PM would, using the task text, the local files and sourced web facts (grill-self). Mark every answer that is not in the task as an assumption and carry the assumptions into the open questions of `brief.md`.
- Use the same fallback for the roast (section 4) and the draft approval (section 5.2).

## 2. Pick the PAF tools

Choose tools the way `ask-pdm` does: match the task on the three axes (function, stage, situation) in the table of `<base dir>/../ask-pdm/SKILL.md`. Read `<base dir>/../../product_notes.md` (the catalog at the plugin root): one entry per tool with its category, purpose and origin, and the Chains section. Open a tool's `SKILL.md` only for the shortlisted tools, not all of them.

Filter by data. The catalog has a Selection table: for each tool, the data modes in which it gives an honest result (none, web, local, manual) and its stage. Keep only the tools whose modes include a mode the run has. A tool that needs numbers while the run has none: ask once, before the shortlist, whether to add a data mode (local files, the web, or numbers entered by hand). If the PM declines, do not pick the tool and write "not picked: needs data" in `brief.md`. Never offer an empty template with N/A as a result.

If no tool covers a decision the audience must make, say so in `brief.md` ("not covered") and do not stretch the nearest tool over it.

Chains: a chain is a list of positions. Each position may list alternatives, which are interchangeable for that position; pick the one that fits the task. When the tools you need sit in non-adjacent positions of a chain, take every position between them and one tool from each, and say why. Do not add a tool that sits in no chain with the rest of the shortlist unless the stop rule still justifies it.

Stop rule: add a tool only if it changes a decision the audience must make, or fills a gap no other tool fills. Stop when the next tool would change no decision, or has no data to fill it honestly. One tool is enough when the result is one artifact; several when the audience must decide several things. Record every skipped tool with one reason.

Show the shortlist with one line per tool and why it fits. The PM confirms, removes, or adds tools. Without AskUserQuestion, the fallback in section 1 applies.

## 3. Context: local files and the web

1. Look for the context file of this project (see step 5). If it exists, read it: use its recorded answers (data modes, output location, depth, PM's level) and skip those questions.
2. Otherwise, if `local` is among the run's data modes, ask the PM which folder holds the project's files, unless the task already names one. If `local` is not a mode of this run, skip steps 2 and 3.  Scan that folder for `.md`, `.csv`, `.xlsx`, `.pptx`, `.pdf` files (skip `.git` and `node_modules`). Show a short list grouped by type.
3. Ask ONCE how to use the local data (only when the folder holds files). Options: sync with the web and update (Recommended), use local data as-is, ignore local data and research the web, pick files manually.
4. Find what the tools still need: audience, industry, niche, size, competitors, pricing. Use the local files first, then WebSearch (standard mode; switch to extended only if the standard result is thin, off-target, or outdated). Record the source of every fact. Flag small samples explicitly.

Missing data. After the tools are confirmed, list every fact they still need that neither the task, the local files nor a search gave. Ask for them in one batch: one AskUserQuestion question per fact, at most 4 questions per call, the rest in the next call. Options for each fact:
- "Find it yourself on the web" (not offered for a company's internal numbers).
- "Continue without the data".
- "I will give it" (offered first for a company's internal numbers: revenue, conversion, CAC, estimates).

Rules for the answers:
- "Find it yourself": search, tag the source tier and date, and keep the fact unconfirmed if only the Other tier supports it.
- "Continue without the data": write N/A in the artifact, never a made-up value. Put the assumption you use instead on the assumptions slide and the fact in "not confirmed" on the sources slide.
- "I will give it": accept aggregates only, as a short form: indicator, value, period, unit. Mark every value "internal data, not verified". Say before the input that raw rows, personal data and source code are not accepted and not needed; if the PM's company forbids sharing real metrics, the PM may enter rounded or relative numbers, or choose "Continue without the data".

Write every answer in the context file so it is not asked again.

Source tiers. Tag every web fact with one tier:
- **Official**: the regulator's or government's own site, or the official legal database. Only these confirm regulatory facts (limits, deadlines, whether a requirement is in force).
- **Corporate**: a company's own site, used only for facts about that company, never for market or regulatory facts.
- **Other**: news, blogs, vendor marketing, aggregators. Use them only as a lead to find the official source. A fact that rests only on this tier stays unconfirmed in the brief and the deck.

Latest edition of a normative act. For every regulatory fact, find the latest edition yourself, do not take the first search result:
- Open the act on the official legal database or the regulator's site and read its list of editions. Open the latest one and record its date and the date you read it.
- If the list or the text does not open, search the regulator's site for the act's latest amendment and record what you found and where.
- A date later than today is an anomaly on the page: record it, do not use it as the edition date, and keep looking for the current edition.
- If the page shows no text of the act, say so; the fact stays unconfirmed.

If the official source cannot be opened, keep the fact as unconfirmed and say why. Do not promote it to confirmed. A regulator's information message (a press release, a FAQ) is an official source for the fact it states, but not for the text of the act: write "stated by the regulator, the act itself not read" and keep the status unconfirmed for any clause of the act.

5. Record the decisions (data modes, output location, depth, PM's level) and the sourced facts in a project context file named `pdm-context.md`, so they are not asked again and later runs build on them.
   - Location: the output folder (section 5.2). The context file always goes into the output folder, also when the output folder is outside the folder the PM's files are in. If the PM's project folder already has a context file, update that one and point to it from `brief.md`.
   - The plugin's `AGENTS.md` is the rule set of the plugin repository. It is not read for the PM's data and does not set where the PM's files go.

## 4. Roast

Present the draft conclusions with their sources and the weakest assumption in each. Ask the PM through AskUserQuestion where they disagree. Revise until the PM confirms. Without AskUserQuestion, the fallback in section 1 applies: the roast is run by the subagent and answered by you, and the deck and brief say that the PM did not confirm it.

## 5. Build the deck

1. Draft the content in chat first, block by block for each tool: titles, conclusions, and every JSON value in the language the PM uses. Keys and the template labels stay English; the text the PM reads is in the PM's language. Write nothing to disk yet.
2. Ask the PM through AskUserQuestion whether the draft is approved, and which folder the output goes to. Recommended: a new subfolder named after the topic, inside the folder the PM names as the project folder; if the PM names none, inside the folder the session runs in, and say that path in `brief.md`. Do not write files until the PM answers. Without AskUserQuestion, use the fallback in section 1 and the recommended folder.
3. Create the output subdirectory. Write one JSON file per tool, compose it from the tool's SKILL.md (use `null` for unknown fields, never invent values; the `example.json` next to a template is used only when the PM explicitly asks to see an example), then fill the tool's template. The template is `<tool>.pptx` (or `<tool>.xlsx`) in the tool's own directory, `<base dir>/../<category>/<tool>/`. Run from the tool's directory:
   `uv run ../../../scripts/fill_pptx.py <tool>.pptx data.json <out>.pptx`
   Run with `--list` first to see the fields. The script refuses to overwrite an existing `<out>.pptx` unless `--force` is given; a rerun needs `--force`. Use `fill_xlsx.py` for XLSX-based tools, with the same path rule. An XLSX result cannot be merged into the deck: leave the workbook next to the deck, name it in `brief.md` and on the sources slide, and put its main result (the top rows or the totals) on the conclusions slide. Do not count it as a tool slide.
4. Merge the filled tool decks into one deck, in the order the PM agreed: `uv run ../../../scripts/merge_pptx.py <out>.pptx <tool deck 1>.pptx <tool deck 2>.pptx ...`. The script copies slides, charts and embedded workbooks at the package level, so charts survive. The first deck is the base. It checks the result itself (zip integrity, a content type for every part, every relationship target present) and stops with a list of problems if the file is broken. Slide titles are conclusions, not topics. Keep the deck to the number of slides the PM agreed to, plus the slides below.
   - Title slide: every deck has one. Fill `<base dir>/title.pptx` with the task's title, the subtitle (audience and decision) and the date.
   - Sources slide: every deck has one. Fill `<base dir>/sources.pptx`: each source with its tier, its edition date and date read, and whether the fact is confirmed; plus the data used and the facts not confirmed.
   - Assumptions slide: every deck has one. Fill `<base dir>/assumptions.pptx` with each question the PM did not settle, the assumption the deck takes in its place, and who confirms it and by when (write "date N/A" when none is known). Take the rows from the brief's assumptions and open questions.
   - Conclusions slide: only for an analytical artifact. Fill `<base dir>/conclusions.pptx` with the decision, the reasons, the risks and the open questions. A non-analytical artifact (a plan, a map, a canvas) states its conclusions itself and gets no conclusions slide.
   - JSON for these four slides has the same shape as for tool templates: `{"text": {"key": "value"}}`, with the keys shown by `fill_pptx.py <template> --list`; a list-like field (questions, assumptions, who confirms) is an array of strings, one item per line, with the same number of items in each column of the assumptions slide.
   - Fill the title, conclusions (if any), sources and assumptions slides from `<base dir>` with the same `fill_pptx.py` command as the tool templates, and merge them in this order: title, the tool decks in the agreed order, conclusions (if any), sources, assumptions. For a quick conclusion there are no tool decks: the order is title, conclusions, sources, assumptions, and the tool results go into the brief.
5. Write `brief.md` next to the deck, in the PM's language: the task, the audience, the chosen tools and the chain they follow, the facts with their tiers and the edition dates, the roasted assumptions, and open questions. Flag every fact whose source is unverified or whose sample is small.
6. Check the deck with `uv run <base dir>/../../scripts/check_pptx.py <out>.pptx`, run with the deck's path as it is. It reports rough layout errors: text that probably overflows its box or the slide, words too long for their box (they break in the middle), shapes outside the slide, and template placeholders left in the deck. Fix each reported item in the JSON and fill again. Do not change the template.
   - Read the warnings `fill_pptx.py` prints to stderr. A warning `text does not fit the box even at 9 pt` names the shape and its text: shorten that text in the JSON and run the fill again; do not change the template. A warning `chart ... keeps the template's sample data` means the JSON has no `charts` entry for that chart: add its data under `charts` (the key is the chart name from `--list`) and fill again. Never ship a deck with sample chart data.
   - Do not check the slides visually: no rendering, no screenshots, no visual review. The script check is the only layout check.
7. Show the PM the list of files and the slide count before finishing.
