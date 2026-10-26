---
name: cohort-analysis
description: Build and read a cohort table (retention or spend by cohort and period) and produce a filled spreadsheet with a normalized heatmap, or review an existing cohort table and its conclusions. Use when the user needs to see whether newer customers behave better than older ones, whether a change worked, or why a total metric hides churn.
---

# Cohort Analysis

The theory, reading directions, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings raw data or counts by cohort, **review** when the user brings a built table or a conclusion drawn from one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the question the table must answer;
- the cohort attribute and the period step (first purchase month, install week);
- the metric and the definition of "active" or of what counts as spend;
- the data: either per-customer events with dates, or already aggregated values per cohort and period, plus cohort sizes.

If the user gives raw events, aggregate them yourself (with code if a file is attached) and show the aggregation rule. Do not invent values; missing periods stay empty.

### 2. Choose the normalization

- Retention or any count of customers: share of the cohort size.
- Spend, orders or revenue: index to period 0.
- Losses, repayments or any amount measured against what the cohort received (for example, loan vintages): share of the cohort size, where the size is the original amount issued.

State the choice and why. The spreadsheet takes one normalization for the whole table. The colour scale paints higher values green; for losses or churn, where higher is worse, say so in the title and in chat.

If a source publishes only the latest value of each cohort at different ages, put each value in the column of its age and do not compare values across columns: that is one diagonal, not a cohort comparison.

### 3. Read the table

Read in the three directions from card.md and report each:

- rows: how a single cohort lives;
- columns: whether newer cohorts do better at the same age;
- diagonals: whether one calendar period hit every cohort at once.

Flag cohorts that are too small to trust (say, under a few hundred customers for retention) and the incomplete right edge. Name the alternative explanations the user must rule out: channel mix, seasonality, price changes, events.

### 4. Conclude

Give the conclusion as an answer to the user's question and the decision it supports. If the evidence is only a correlation, say what check (for example, splitting cohorts by channel) would make it stronger.

### 5. Show, then write

Show the normalized table in chat first, with the three readings and the conclusion. Write a file only after the user confirms. Ask for the output path (default `cohorts-<topic>.xlsx` in the working directory). Save the data as JSON:

```json
{
  "text": {"title": "…", "metric": "…", "normalization": "share of cohort size"},
  "rows": [["2026-01", 1000, 1000, 420, 350, 310]]
}
```

Each row is the cohort label, the cohort size (customers or the original amount), then the raw values for period 0, 1, 2… Leave the size as `null` for index normalization if it is unknown. `normalization` must be exactly `share of cohort size` or `index to period 0`. The template's formulas compare against these exact literals, and any other value falls back to the share, so check the spelling. The template holds 24 cohorts and periods 0–12; the sheet “Cohorts” computes the normalized heatmap. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/cohort-analysis.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints. Apple Numbers does not render the colour scale; Excel, Google Sheets and LibreOffice do.

## Mode: review

Take the user's table or conclusion in any form and check it against the common mistakes in card.md:

1. Cohorts are compared at the same age (same column), not at the same calendar date.
2. One definition of active or of spend across the whole table.
3. Normalization fits the metric, and the arithmetic is right.
4. Small cohorts and the incomplete right edge are not used for conclusions.
5. Column trends and diagonal events are not confused.
6. Alternative explanations (channel, season, price) are named and checked.
7. The conclusion answers a stated question and leads to a decision.

Items 2 and 6 often cannot be judged from the table alone: ask the user instead of reporting a finding. Report findings as a numbered list: cells or cohorts, what is wrong, why it changes the conclusion, the concrete fix. End with a verdict: "conclusion holds", "conclusion changes after fixes" or "not enough data to conclude".
