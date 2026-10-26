# Quality gate for cards

Criteria that determine whether a tool card for product managers is ready. A card is a self-contained reference for a mixed audience: a newcomer must be able to understand the tool and apply it, while an experienced reader must be able to find non-obvious limitations and nuances.

## Pass rule

Each criterion K1–K8 is scored on a 0–2 scale. **A card passes the gate only if every criterion scores 2.** The total score is used only to decide what to improve first.

An agent scores against the anchors below; the user spot-checks the results.

## Card reference

### Location

```
<function>-<stage>/<tool>/
  card.md         — card (in English)
  SKILL.md        — agent skill (in English)
  <tool>.pptx     — artifact template, if the tool has a visual form
  <tool>.xlsx     — artifact template, if the tool is tabular
```

All directory names under `skills/` are in kebab-case: lowercase Latin letters, digits and hyphens. The tool's directory name matches the `name` field in SKILL.md. Functions and stages are described in the [Catalogs](#catalogs) section.

Each tool has exactly one template: `<tool>.pptx` or `<tool>.xlsx`. Shared fill scripts are in `scripts/`.

After all cards pass the gate, the set is rebuilt into the Claude Code plugin `pdm-skills`: category directories move to `skills/`, and `.claude-plugin/` and `LICENSE` appear in the root (content — CC BY-SA 4.0, code — MIT). Until then, work continues in the current structure.

### card.md sections

The H1 heading is the original name of the tool. Then come eight H2 sections, strictly in this order:

1. **Essence** — what the tool is and what task it solves, in 1–3 sentences.
2. **When to use and when not to** — the situation, the required inputs, the boundaries of applicability.
3. **Scheme** — the abstract template of the tool: a table, a diagram, a sequence of steps, a meeting agenda.
4. **How to apply** — the step-by-step procedure: inputs, steps, formulas and scales, interpretation of the result.
5. **Example** — a real public case, with a link (e-commerce and fintech are preferred; any other industry is allowed). The tool is shown applied in it, and the case is brought to an accepted decision.
6. **Common mistakes** — pitfalls and wrong interpretations.
7. **Source** — the author (or organization), the year, the context of appearance, and at least one working link to the primary source or an authoritative description. If there is no single author, the origin of the method is described.
8. **See also** — tools of this set that are linked to this one, each with how to use them together. Format: one bullet per tool, `- <Phrase> <Tool name>: <how to use them together, one sentence>`. The phrase is one of: `Enhanced by` (the two work well together), `Alternative to` (the other tool solves the same problem differently), `Preceded by` (the other tool is done before this one), `Followed by` (the other tool is done after this one), `Improved by` (the other tool makes this one better, one-way), `Used to improve` (this tool makes the other one better, one-way). The tool name is the H1 of that tool's card, exactly. The section is checked by `build/quality_gate.py`: every name must match an existing card.

All sections are mandatory; marking a section as "not applicable" is not allowed. Other tools of the set are named in "See also". Outside that section, a specific neighbouring tool is named only when the tool cannot be used without it (a hard dependency); a mere pointer to a related tool belongs in "See also". There are also no "Category" or "Image" fields: the folder sets the category.

## Catalogs

The directory name is `<function>-<stage>`. Only non-empty directories are created.

### Functions

| Function | What it covers |
|---|---|
| `business` | Market and money: markets and niches, customer segments, competitors (by revenue, share, niches, USP), revenue, profit, investments, product portfolio. |
| `product` | Product features, including from the point of view of user interests: user value, the user's path and perception, functionality, product development. |
| `development` | Software development (not product development): processes, rituals and artifacts of the engineering team. |

Strategy is not a separate function. A strategic tool belongs to `business` if the decision concerns the market and money, and to `product` if it concerns features.

### Stages

| Stage | What it covers |
|---|---|
| `research` | Data is collected for the first time, even if it is complex, and even if the tool immediately classifies or orders it: interviews, observations, surveys, market data collection, identification of participants and competitors. |
| `analysis` | Processing of data that has already been collected — usually internal: metrics of an existing product, interview results, exports. |
| `planning` | Formulating hypotheses, ideas, goals, priorities and plans. |
| `validation` | Checking hypotheses on data or with users: experiments and tests. |
| `execution` | Running the work: processes, rituals, progress control. |
| `handoff` | Passing the result to the next link (to development, operations, sales): requirements, specifications, acceptance criteria. |

### Borderline cases

Borderline cases are considered from the point of view of product management: the catalog is determined by how the product manager uses the tool, not by the historical origin of the method or by the function (marketing, sales, development) it was originally built for. Beyond that, the function definitions apply: market and money — `business`, product features — `product`.

The stage is determined by what the tool does with the data, not by where the method originated. If the tool itself collects the data for the first time — `research`; if it processes data that has already been collected — `analysis`.

Interview and survey data: if the set contains a card describing how to collect them, a tool that sorts the collected material into a form (for example, a buyer persona) belongs to `analysis`; if the set has no collection method and the data is collected directly while the tool is being filled in — to `research`.

## Criteria

### K1. Completeness and structure

- **2** — all eight sections are present, follow the reference order and the reference headings, and each one has content. "See also" lists existing tools with a relation and a way to use them together.
- **1** — all sections are present, but at least one is formal (a single general phrase), or the order or headings are violated, or "See also" names a tool that is not in the set or gives no way to use it together.
- **0** — a section is missing or is marked "not applicable".

### K2. Factual accuracy

Checked against the primary source from the "Source" section. Checking on the internet is allowed.

- **2** — everything agrees with the primary source: the names of elements, formulas, scales, the order of steps, authorship and year are correct.
- **1** — there are inaccuracies that do not change how the tool is applied: a simplification, an imprecise date, a free translation of a term.
- **0** — there is an error that would lead to the tool being applied incorrectly; or the authorship is wrong; or the card's claims cannot be verified (there is no working link).

### K3. Clarity for a newcomer

- **2** — "Essence" is understandable without prior knowledge of the tool. Terms and abbreviations are explained at first mention. The volume is proportionate to the content; the word limit is set per section: Essence 200, When to use and when not to 300, Scheme 200, How to apply 400, Example 400, Common mistakes 200, Source 200; each "See also" bullet's text 15 words. Counted without URLs; `build/quality_gate.py` checks the limits. `build/section_stats.py` shows the length of each section across all cards and the recommended limits.
- **1** — generally understandable, but there are unexplained terms, or the card is noticeably bloated or over-compressed.
- **0** — without knowing the tool in advance, it is impossible to understand what it does.

### K4. Depth for the experienced

- **2** — the sections "When to use and when not to" and "Common mistakes" contain non-obvious content: limitations of the method, conditions under which the result misleads, nuances of interpretation.
- **1** — only common knowledge ("quality data is needed", "don't drag it out").
- **0** — these sections restate the definition.

### K5. Practicality

- **2** — "How to apply" lets the tool be applied without other sources: inputs, steps, formulas and scales are given (for meetings — participants, duration, agenda), it is described how to interpret the result and which decision follows from it. The "Example" is a real public case from any industry (e-commerce and fintech preferred) with a link, in which the tool itself is visible in its own form: a filled-in board, table, chain or plan — taken from the source or reconstructed from it without speculation. The decision made on the basis of this form is also visible.
- **1** — steps are present, but inputs or interpretation are skipped; or the example is not brought to a decision; or the tool is only mentioned in the case, or applied without a visible result in its own form.
- **0** — there are no steps; or the example is fictional or has no link to a source.

### K6. Catalog correctness

- **2** — the function and stage match the definitions in the [Catalogs](#catalogs) section; a borderline case is resolved from the point of view of product management, by the rule in the [Borderline cases](#borderline-cases) section.
- **1** — the choice can be defended, but by the definitions another catalog fits better.
- **0** — the catalog contradicts the definitions, or the folder name does not follow the scheme `<function>-<stage>/<tool>/`.

### K7. Agent SKILL

SKILL.md is written in English. The trigger phrases in `description` cover the user's language(s): a model understands trigger phrases in any language, so no particular language is required. The skill answers in the user's language. The `name` in the frontmatter matches the tool's directory name. The skill is invoked by the model; `disable-model-invocation` is not set. It works in two modes:

- **do** — apply the tool together with the user and produce a filled artifact;
- **review** — review the user's finished artifact.

The artifact of "do" mode is built on the tool's template. First the skill shows the filling in the chat as text (a table by template blocks), and writes the file only after the user confirms: `uv run scripts/fill_pptx.py` or `uv run scripts/fill_xlsx.py`. The dependencies of the scripts are declared in the scripts themselves (PEP 723).

Unlike the card, the skill may name neighboring tools of the set — in `description` and in the body, for example "if there is no data for RICE, start with ICE".

Checks:

- **a. Trigger.** From `description` in the frontmatter, the agent understands when to invoke the skill: the tool's name, the application situation and typical user phrases are given.
- **b. Modes step by step.** For "do", it is described which inputs to request, which steps to go through, how to show the filling in the chat and how to write the file from the template. For "review", there is a checklist based on "Common mistakes" and a format for remarks.
- **c. No duplication.** The skill takes the theory from `card.md` by link, contains only the procedure, and does not contradict the card.
- **d. Trial run.** In "do" mode, the agent runs the skill on the input data of the case from "Example" and gets a result comparable to the case's conclusions, including the file filled in from the template. In "review" mode, the agent gets the artifact from "Example" with one typical mistake planted in it, and finds it.

Scores:

- **2** — all four checks are passed.
- **1** — the trial run is passed, but one of checks a–c is passed only partially.
- **0** — SKILL.md is missing, or the trial run is not passed, or the skill contradicts the card.

### K8. Template

The template is `<tool>.pptx` or `<tool>.xlsx` in the tool's directory.

- **pptx** — for tools with a visual form: canvases, matrices, maps, boards, chains, trees. Usually one slide; more only if the original is structured that way (a User Story has a front and a back — two slides). Elements that change with the data (bars of a Gantt chart, points on matrices and maps) are native PowerPoint charts.
- **xlsx** — for tabular tools: headers, hints in cell comments, live formulas for calculations.

Placeholders have the form `{{key}}` and explain what to write into the block. Templates are built by a script on python-pptx or openpyxl and checked with `officecli` (a developer-side check): `validate`, `view issues`, `view screenshot`. Slides with native charts are additionally opened in Keynote or PowerPoint: the HTML rendering of `officecli` shows them inaccurately. The end user does not need `officecli`.

- **2** — the layout and block names match the original template from the primary source; the template presents the result, not the method: its static text is only the artifact's own labels, axes, legends and titles, with no instructions, process steps, method description or calculation notes (a placeholder hint saying what goes into a block is allowed); each placeholder explains the content of its block; `officecli validate` and `officecli view issues` are clean both for the empty template and for the file from the K7 trial run; no `{{…}}` remains in the filled file; `example.json` next to the template gives a value for every placeholder of the template and for no other key (checked by `quality_gate.py`), so the filled example shows the result; the screenshot of the filled slide is legible: the text does not go beyond the blocks, and the charts show the case's data.
- **1** — the file is valid and fills in, but the layout noticeably departs from the original, or some placeholders do not explain the content, or on the screenshot the text goes beyond the blocks, or one static text element describes the method or the process (for example, a footer with filling instructions).
- **0** — there is no template, the file fails `validate`, the fill script crashes, or the wrong format is chosen (a table on a slide, a canvas in xlsx). Also 0 if the template is mostly method description (explanatory text blocks instead of the result's own form).

## ask-pdm navigator

The navigator `ask-pdm/SKILL.md` picks a suitable tool for a task described in plain words and hands the work over to that tool's skill. It is invoked only by the user (`disable-model-invocation: true`). K1–K8 do not apply to it. It is checked by the criteria below.

- **N1. Coverage.** Every skill of the set (`skills/*/*/SKILL.md`, including `skills/pdm-brief`) has exactly one row in the table, and every row names an existing skill with its folder. Checked by `build/quality_gate.py`: missing rows and extra rows are both problems.
- **N2. Distinct purposes.** Each row's purpose is under 15 words and differs from every other row; the purpose says what the tool does and when to pick it over its neighbours, not only the tool's topic. Checked by `build/quality_gate.py` for length and duplicates; the wording is reviewed by reading.
- **N3. Routing.** Five fixed example tasks (listed in the navigator's SKILL.md under "Routing examples", each with the expected tool) route to the expected tool by reading the table. A task that routes to a neighbour is a failure of N2.
- **N4. Procedure.** The procedure in SKILL.md asks one clarifying question when two tools fit, and names neighbours only as alternatives after the main answer.

Score: 2 — all four pass; 1 — N1 passes, one of N2–N4 is partial; 0 — N1 fails.

## Selection table (the data filter of pdm-brief)

`product_notes.md` holds a Selection table: for each tool skill one row with the data modes in which its result stays honest (`none`, `web`, `local`, `manual`), its stage, the input it needs and a status (`draft` until the maintainer has reviewed the row). Checked by `build/quality_gate.py`:

- **S1. Coverage.** Every tool skill has exactly one row, and every row names an existing tool.
- **S2. Values.** Modes come from the allowed set, the stage equals the second word of the tool's folder, the input needed is not empty, the status is `draft` or `reviewed`.

A new card is not finished until its row is added.

## pdm-brief (the intake skill)

`skills/pdm-brief/SKILL.md` turns a product task into a short deck built from PAF tools. It is not a tool card: it has no `card.md` and no template, so K1–K6 and K8 do not apply. It is checked as an intake skill by the criteria below.

- **I1. Trigger and invocation.** `name` equals the directory (`pdm-brief`); `description` gives English trigger phrases for research, strategy, market or competitor analysis, product decisions and mini-deck requests; `disable-model-invocation` is not set (the model may invoke it).
- **I2. Flow.** The SKILL.md body has the steps in this order: grilling dependency check, grill on output and level, pick 3–5 tools, context from local files and the web, roast, build the deck. Each step is present and nothing is skipped.
- **I3. Questions.** Every question to the product manager goes through AskUserQuestion, with the recommended option first and labelled "(Recommended)". The rule is stated in the skill.
- **I4. References resolve.** Every script and file the skill names exists: `scripts/fill_pptx.py`, `scripts/fill_xlsx.py`, `scripts/merge_pptx.py`, `product_notes.md` at the repository root. Every tool it may pick is an existing skill with its template. Checked by `build/quality_gate.py`.
- **I5. Trial run.** The build step is run on two filled tool decks from `skills/` (fill, then merge): the merged deck passes `officecli validate` and has no `{{` left.
- **I6. Language.** The skill's files are in English; the text shown to the product manager follows the manager's language, as the skill states.

Score: 2 — all six pass; 1 — one of I2–I6 is partial; 0 — I1, I2 or I4 fails.

## Assessment report format

The assessment report is written by `build/record.py` to a temporary directory outside the repository; it is not stored in `docs/`. The format itself is as follows.

Summary table:

```markdown
| Card | K1 | K2 | K3 | K4 | K5 | K6 | K7 | K8 | Result |
|---|---|---|---|---|---|---|---|---|---|
| product-planning/rice-scoring | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | fail |
```

Below the table comes a block for each score below 2:

```markdown
### product-planning/rice-scoring — K3 = 1

- **Fact:** "Confidence" is used without explanation (section "Essence").
- **Fix:** explain the term at its first mention.
```

Each score below 2 is backed by a quote from the card or a verifiable fact (for K2 — a link to a source that contradicts the card) and a concrete fix action.

## Plugin manifest

P1: `.claude-plugin/plugin.json` lists every skill folder under `skills/` (including `skills/ask-pdm`) and no folder without a `SKILL.md`. A new card is not available to users until it is listed.
