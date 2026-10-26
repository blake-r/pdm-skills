---
name: objectives-and-key-results
description: Set Objectives and Key Results (OKR) for a company, department, team or person - three to five qualitative objectives, about three measurable key results each with a start and target value, committed or aspirational type, owners and actions - align them across levels, and produce an XLSX that computes progress; or review existing OKRs, or grade them at the end of a period on Google's 0-1.0 scale. Use when choosing the few main priorities for a quarter, half-year or year, when teams pull in different directions, or at a mid-period check-in or end-of-period grading.
---

# Objectives and Key Results (OKR)

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a strategy, priorities or a draft of goals, **review** when the user brings finished OKRs or asks to grade them.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the level (company, department, team, person) and the period;
- the strategy or the higher-level OKRs these must support;
- the current values of the metrics that may become key results, with sources;
- who owns what, and which goals must be met in full.

Do not invent current values or targets. If a start value is unknown, mark the key result as needing a baseline first.

### 2. Objectives

Propose three to five objectives: qualitative, clear without explanation, ambitious. For each, ask "what would have to be true to get there?".

### 3. Key results

For each objective, write about three key results: a number with a start and a target value, or a milestone "launch X". Reject tasks posing as results: an action goes to the actions column.

### 4. Type and alignment

Mark each objective committed (expected grade 1.0) or aspirational (expected average 0.6 to 0.7). Check that each objective supports one at the level above, and name the owner of each key result.

### 5. Show, then write

Show in chat first, row by row as in the spreadsheet: level, objective, type, key result, unit, start, target, current, owner, actions. Write a file only after the user confirms. Ask for the output path (default `okr-<team>-<period>.xlsx` in the working directory). Save the data as JSON (the example is the Nubank case from card.md; the source gives no key results, so the numeric cells stay empty):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {"title": "Nubank, 2020", "why": "From a credit card company to a full-cycle bank outside Brazil"},
  "rows": [
    ["company", "Free 100 million customers from financial complexity", "aspirational", "Not given in the source", null, null, null, null, null, "Expansion to Mexico; OKRs not tied to Brazil"]
  ]
}
```

A row is ten values, columns A to J: level, objective, type, key result, unit, start, target, current, owner, actions. Do not pass the progress: the spreadsheet computes it in column K with a live formula. `type` must be exactly `committed` or `aspirational`. Use `null` for an unknown value. Repeat the objective in each of its key-result rows. Rows beyond the 30 prepared ones get the formula but no input validation. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/objectives-and-key-results.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's OKRs in any form and check them against the common mistakes in card.md:

1. Key results are measurable results, not tasks.
2. OKRs are not used to evaluate employees.
3. Each objective is marked committed or aspirational, and grades are read against the right expectation.
4. There are check-ins during the period, not only the final grade.
5. There are three to five objectives with about three key results each.

Item 4 usually cannot be judged from the OKRs alone: ask the user instead of reporting a finding. When asked to grade, grade each key result from 0 to 1.0, then each objective as a rough average, and say what the grades mean for the next period. Report findings as a numbered list: objective or key result, what is wrong, why it matters, the concrete fix. End with a verdict: "OKRs are ready", "ready after fixes" or "not enough data".
