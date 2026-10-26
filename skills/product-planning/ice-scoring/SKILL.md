---
name: ice-scoring
description: Prioritize hypotheses, growth experiments or features with ICE (Impact, Confidence, Ease on 1–10 scales) and produce a filled ICE spreadsheet, or review an existing ICE table. Use when the user needs a quick ranking of many ideas against one metric without solid reach or effort data.
---

# ICE Scoring

The theory, scales, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a list of ideas, **review** when the user brings scored rows.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the list of ideas (one change for the user per row);
- the goal and the single metric that Impact is judged against;
- what is known about each idea: data, research, customer feedback, results of past tests;
- rough effort from the team for each idea;
- the calculation method: average of the three scores (the default) or their product (Itamar Gilad's definition).

If the ideas serve different metrics, say that their Impact is not comparable and score each metric's list separately. If the user has audience sizes and effort in person-months for every row, suggest the `rice-scoring` skill instead; for a visual split into quick wins and big bets, `impact-effort-matrix`.

### 2. Agree on scales

Before scoring, write down with the user what 1, 5 and 10 mean for Impact and Ease in their context. Default anchors for Ease: 10 — under a day, 5 — about a week, 1 — more than a quarter. Default anchors for Confidence (a simplified team convention, not Gilad's Confidence Meter): an opinion — 1–2, a few customer comments — 3–4, analytics data — 5–7, a test result — 8–10. If the user follows Gilad, use his stricter meter from the source in card.md. Keep the agreed anchors for the whole list.

### 3. Score

For every row, agree on Impact, Confidence and Ease and record the reason in one short phrase. Confidence follows the evidence, not the enthusiasm: raise it only when the user names data. Do not invent numbers; if the user cannot justify a score, take the lower value and say so.

### 4. Interpret

Sort by ICE and comment on the top of the list:

- with the average, a gap of one to two points is a tie; with the product, compare ratios rather than differences; name the extra criterion that should break a tie;
- a high-Impact, low-Confidence idea near the top should get a cheap test first, then a new Confidence score;
- strategic bets that sink because of low Ease belong in a separate plan; say so instead of editing the numbers.

### 5. Show, then write

Show the table in chat first: idea, I, C, E, ICE, rank, and the one-phrase reasons. State the method and the anchors above the table. Then the interpretation.

Write a file only after the user confirms. Ask for the output path (default `ice-<topic>.xlsx` in the working directory). Save the data as JSON:

```json
{
  "text": {"title": "…", "method": "average"},
  "rows": [["Idea", 7, 6, 5]]
}
```

`method` must be exactly `average` or `product`, in lower case: the spreadsheet template switches its formula on this literal word and silently falls back to the average on any other value, so check the spelling before running the script. Do not pass the score or the rank: the spreadsheet computes them with live formulas. Rows beyond the 30 prepared ones get formulas but no input validation. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/ice-scoring.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's table in any form and check it against the common mistakes in card.md:

1. One goal metric for all rows.
2. Scales are agreed and written down; the same number means the same thing in every row.
3. Confidence reflects evidence, not how much someone likes the idea.
4. Ease covers the whole team and the launch, not development only.
5. One calculation method for the whole list, and the arithmetic is right.
6. Scores come from more than one person, or from a joint discussion.
7. Scores are fresh: ideas were rescored after tests or new data.
8. Near-ties and low-Confidence leaders are called out instead of treated as final.

Items 6 and 7 usually cannot be judged from the table alone: ask the user instead of reporting a finding. Report findings as a numbered list: row and field, what is wrong, why it changes the ranking, the concrete fix. Recalculate the affected scores and show how the order changes. End with a verdict: "ranking holds", "ranking changes after fixes" or "not enough data to rank".
