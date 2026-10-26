---
name: rice-scoring
description: Prioritize features or product hypotheses with RICE (Reach × Impact × Confidence ÷ Effort) and produce a filled RICE spreadsheet, or review an existing RICE table. Use when the user needs to rank a list of initiatives against one goal.
---

# RICE Scoring

The theory, scales, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a list of initiatives, **review** when the user brings scored rows.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the list of initiatives (one change for the user per row);
- the goal and the single metric that Impact is judged against;
- the reach period, one for all rows (default: a quarter);
- the data behind Reach: audience sizes, funnel steps, event counts;
- effort estimates from the team, in person-months, covering development, design and testing.

Before scoring, filter out mandatory work (regulatory, contractual, hard dependencies) and list it separately: it does not compete in the ranking. If the initiatives belong to teams with different metrics, say that their Impact is not comparable and score each team's list separately.

### 2. Score

For every row, agree on each value and record the reason in one short phrase:

1. **Reach**: people or events per period from data; count only those who reach the place where the change is visible.
2. **Impact** per reached person: 3, 2, 1, 0.5 or 0.25 (card.md scale).
3. **Confidence** in the three other estimates: 100%, 80% or 50%. Tie it to the evidence, not to enthusiasm. If the user wants less than 50%, flag the row as a moonshot.
4. **Effort**: person-months, whole numbers or 0.5.

Do not invent numbers. If data is missing, give a range, pick the conservative end and lower Confidence.

If the team already scores with its own scales (Reach in points, Confidence 1–10, Effort in hours, Impact above 3), keep them rather than converting: remapping values or rounding Effort changes the ratios and can reorder close rows. Enter Confidence as a share of the scale's maximum (8 of 10 → 0.8) and Effort in the team's unit; the ranking depends only on ratios. Name the units in the title (for example, "Effort in hours, Confidence 1–10"). Scores then differ in scale from the card's example (0.67 instead of 6.7 when Confidence 8 of 10 becomes 0.8); only the order matters. The spreadsheet warns about values outside the card's scales; accept the warning.

If Reach cannot be estimated at all (no audience yet), say RICE will mislead and suggest the `ice-scoring` skill. For cross-team comparison in money, suggest `cost-benefit-analysis`; for a quick visual split into quick wins and big bets, `impact-effort-matrix`.

### 3. Interpret

Sort by score and comment on the top of the list:

- scores within 10–20% of each other are a tie; name the extra criterion that should break it;
- a low-Confidence row near the top should be validated cheaply before it is built;
- dependencies or strategy may move a row; say so explicitly instead of editing the numbers.

### 4. Show, then write

Show the table in chat first: initiative, R, I, C, E, score, rank, and the one-phrase reasons. Then the interpretation.

Write a file only after the user confirms. Ask for the output path (default `rice-<topic>.xlsx` in the working directory). Save the data as JSON:

```json
{
  "text": {"title": "…", "reach_period": "quarter"},
  "rows": [["Initiative", 1200, 2, 0.8, 3]]
}
```

Confidence goes in as a fraction (0.8 for 80%). Rows beyond the 30 prepared ones get formulas but no input validation. Do not pass score or rank: the spreadsheet computes them with live formulas. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/rice-scoring.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's table in any form and check it against the common mistakes in card.md:

1. One goal metric and one reach period for all rows.
2. Reach comes from data and counts only people who meet the change, not the whole audience.
3. Impact uses the agreed scale; the team shares the meaning of each value.
4. Confidence reflects the evidence behind the estimates.
5. Effort covers the whole team, not development only.
6. The arithmetic is right: R × I × C ÷ E.
7. Mandatory work and cross-team rows are not mixed into one ranking.
8. Near-ties and low-Confidence leaders are called out instead of treated as final.

Report findings as a numbered list: row and field, what is wrong, why it changes the ranking, the concrete fix. Recalculate the affected scores and show how the order changes. End with a verdict: "ranking holds", "ranking changes after fixes" or "not enough data to rank".
