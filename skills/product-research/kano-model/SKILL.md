---
name: kano-model
description: Design a Kano survey (a functional and a dysfunctional question per feature, five answers each), classify the answers with the Kano evaluation table into must-be, one-dimensional, attractive, indifferent, reverse and questionable, assign a category per feature, compute Berger's Better and Worse coefficients, decide what to build first, and produce an XLSX; or review an existing Kano study. Use when there is a list of candidate features and the team needs to know which users take for granted, which they value in proportion, which would delight them and which they do not care about.
---

# Kano Model

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings features or survey answers, **review** when the user brings a finished study.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product, the user segment, and the decision the survey feeds;
- the candidate features, each as a benefit a user understands without explanation;
- if the survey is done: the answers per respondent (functional and dysfunctional answer per feature) or the counts per category;
- whether the user wants the category by the most frequent answer (Berger) or by the A + O + M versus I + R + Q rule.

Do not invent answers or counts.

### 2. Survey (if not run yet)

Write two questions per feature: "If the product has <feature>, how would you feel about it?" and "If <feature> is absent, how would you feel about it?", answers: I like it; I expect it; I am neutral; I can live with it; I dislike it. Keep one segment per survey, or ask a segment question to split the results. Stop here and let the user run it.

### 3. Classify

Map each answer pair to a category with the evaluation table in card.md and count A, O, M, I, R, Q per feature. The spreadsheet assigns the category by both rules and computes Better and Worse. Flag ties, near-ties (a gap of a few answers) and features with many Q: ask again or split by segment before deciding.

### 4. Decide, show, then write

Propose: fix must-be features that are missing or weak first, invest in one-dimensional ones, add one or two attractive ones, defer indifferent ones, drop reverse ones. Show in chat first: the counts, both categories, Better and Worse, the decision per feature. Write a file only after the user confirms. Ask for the output path (default `kano-<product>.xlsx` in the working directory). Save the data as JSON (the example is the ShopeePay case from card.md; the decisions come from the paper's satisfaction map and recommendations, not from ShopeePay):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {"title": "ShopeePay, wallet users in Indonesia, 145 responses, 2020"},
  "rows": [
    ["Navigation", 49, 53, 12, 31, 0, 0, "attractive quadrant: last in priority"],
    ["Ad frequency", 26, 51, 31, 37, 0, 0, "improve: reduce dissatisfaction"],
    ["Screen quality", 29, 32, 28, 56, 0, 0, "not named in the recommendations"],
    ["Transaction security", 11, 25, 39, 69, 0, 1, "must-be quadrant: improve"],
    ["Brand image on screen", 33, 21, 25, 66, 0, 0, "not in the authors' recommendations"]
  ]
}
```

A row is eight values, columns A to H: feature, then counts A, O, M, I, R, Q (whole numbers), then the decision. Do not pass columns I to M: the spreadsheet computes the total, the category by the most frequent answer, the category by the A + O + M rule, Better and Worse. It holds up to 50 features. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/kano-model.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's study in any form and check it against the common mistakes in card.md:

1. Each feature has both the functional and the dysfunctional question.
2. One segment per result, or results split by segment.
3. Categories with near-equal counts are not treated as firm; the counting rule is stated.
4. Must-be gaps are closed before attractive features get investment.
5. The survey date is recent enough; categories are rechecked over time.

Report findings as a numbered list: what is wrong, why it misleads the decision, the concrete fix. End with a verdict: "study supports the decision", "supports it after fixes" or "not enough data".
