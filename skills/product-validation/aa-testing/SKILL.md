---
name: aa-testing
description: Plan or read an A/A test - an experiment where both groups see the same version, used to check the experimentation system itself - the goal, the metric and randomization unit of future experiments, the number of runs (live or historical re-splits), then per run the split check and p-value, and over the series the share of significant results against α, the number of split mismatches and the uniformity of p-values with a histogram - and produce an XLSX with live formulas; or review an existing A/A check. Use before the first experiment on a new system, after changes to user assignment, a new metric or a new significance formula, or when experiment results look too good to be true.
---

# A/A Testing

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a system to check or A/A results to read, **review** when the user brings a finished A/A check.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- what is being checked: user assignment, a new metric, a new significance formula; what changed recently;
- the metric and randomization unit used by future experiments, and the planned group shares;
- for results: per run, users and conversions in each group; how the runs were made (live tests or re-splits of history).

Do not invent counts or runs. If the user has one run, say that one run shows only the split check and cannot show the false positive rate; propose re-splitting history into at least 20 runs, better 100.

### 2. Plan

- **Goal:** one sentence naming what the check must prove.
- **Metric and unit:** the same as in future experiments.
- **Runs:** live runs catch assignment and data collection bugs; historical re-splits are fast and catch metric calculation problems, not live assignment bugs. Say which the plan covers.
- **Decision rule:** what happens if significant results exceed α, if the split is off, if p-values are not uniform.

### 3. Read the results

Enter one row per run. The spreadsheet computes per run the conversions, the p-value (two-sided z-test of two proportions) and the split check against the planned share of A (p below 0.001 is a mismatch). Over the series it computes the share of significant runs, the binomial probability of that many by chance, the number of mismatches with the same check, a chi-square test of p-value uniformity over ten bins (from 20 runs) with a histogram, and the verdict. Explain a failing verdict: too many significant runs points to the calculation or data, a split mismatch to assignment, non-uniform p-values to a formula that does not fit the metric. Say that after a fix the A/A check must be repeated.

### 4. Show, then write

Show in chat first: the plan and, for results, the summary and the verdict. Write a file only after the user confirms. Ask for the output path (default `aa-test-<topic>.xlsx` in the working directory). Save the data as JSON (the example is the Airbnb case from card.md: Airbnb published no counts, so `rows` stays empty rather than invented):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Airbnb: checking the experimentation system, published 27.05.2014",
    "goal": "What the system returns when there is clearly no difference",
    "metric": "Not named in the source",
    "audience": "Site visitors; split 50/50 and 75/25, one version for everyone",
    "runs": "Many live A/A tests; the number and timing are not given in the source",
    "decision_rule": "Imbalance means look for the cause; a bug was found in splitting visitors who are not logged in"
  },
  "rows": []
}
```

With counts, `rows` holds one list per run: name, users A, conversions A, users B, conversions B, for example `[["Run 1", 339, 43, 344, 42]]` (illustrative numbers from the tool's original sketch, not Airbnb's). 100 rows are prepared; more rows get the formulas copied, and the summary counts up to row 1000. For an unequal split set the planned share of A with `"cells": {"B10": 0.75}`; `B9` holds α. Do not pass computed columns. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/aa-testing.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's A/A check in any form and check it against the common mistakes in card.md:

1. There is a series of runs, not one; a single significant or clean run is not taken as proof.
2. The group shares are checked against the planned ones, not only significance.
3. Unequal splits are covered if future experiments use them.
4. The metric and the randomization unit match future experiments.
5. A found problem is fixed and the A/A check is repeated before experiments start.

Report findings as a numbered list: what is wrong, why it misleads, the concrete fix. Recompute the p-values and split checks when counts are given. End with a verdict: "system can be trusted", "trusted after fixes" or "not enough data".
