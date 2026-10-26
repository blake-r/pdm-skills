---
name: ab-testing
description: Plan or read an A/B test (controlled experiment) - the hypothesis, one primary metric chosen before launch, guardrail metrics, the randomization unit, the sample size and whole-week duration from baseline conversion and minimum detectable effect, the decision rule; then the results per variant with relative difference, p-value, confidence interval, a sample-split check and a verdict - and produce an XLSX with live formulas; or review an existing test plan or report. Use before changing a product for part of the users, when the team argues about which version is better, or when a finished test must be read without fooling yourself.
---

# A/B Testing

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a change to test or test results to read, **review** when the user brings a finished plan or report.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the change and the hypothesis behind it;
- the decision the test feeds and the candidate metrics with their current values;
- how many users (or sessions, stores) per day reach the changed place, and how traffic can be split;
- for a finished test: users and conversions per variant, the planned split, start and end dates.

Do not invent baselines, traffic or results. If the user cannot say which metric decides, stop and settle that first.

### 2. Plan

- **Hypothesis:** "if we change X, metric Y changes because ..."; one change per variant.
- **Primary metric:** one, fixed before launch. Guardrails: what must not get worse (revenue, bounce, speed, complaints).
- **Unit:** usually the user, so each person sees one version for the whole test.
- **Size and duration:** the spreadsheet computes users per variant from the baseline, the minimum detectable effect, α = 0.05 and power 0.8, then days and whole weeks from daily traffic. Round up to whole weeks, at least one, better two. If it needs months, say the test is not feasible as planned and suggest a bigger effect, a more frequent metric or no test.
- **Decision rule:** what happens on "better", "worse" and "difference not proven", written now.

### 3. Read the results

Enter users and conversions per variant, control first. The spreadsheet computes conversion, relative difference, p-value (two-sided z-test of two proportions), the confidence interval of the difference and a verdict per variant, plus a sample-split check (chi-square p below 0.001 means the split is broken and the result is not usable). Then apply the decision rule. Warn when the test was stopped early, ran for partial weeks, the metric was picked after the fact or several variants were compared without correction.

### 4. Show, then write

Show in chat first: the plan, the size and duration, and for a finished test the table and the verdict. Write a file only after the user confirms. Ask for the output path (default `ab-test-<topic>.xlsx` in the working directory). Save the data as JSON (the example is the Etsy case from card.md: Etsy published rates, not user counts or daily traffic, so `rows`, `mde` and `daily` stay empty rather than invented; the baseline is the control's purchases-from-search rate):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Etsy: infinite scroll in search, talk 2012",
    "hypothesis": "If more items are shown faster, purchases from search will grow: the premise \"more and faster is better\"",
    "metric": "The primary metric is not named in the source; clicks, favorites and purchases from search were published",
    "guardrails": "Overall purchases — not set in advance in the source",
    "audience": "Control: search with pages; variant: infinite scroll. Unit and shares not given",
    "duration": "Not given; the slides have dates 6–9 February",
    "decision_rule": "Not written down; after the test the feature was removed and the premises were checked with separate tests"
  },
  "cells": {"B22": 0.0164},
  "rows": []
}
```

With counts, `rows` holds one list per variant: name, users, conversions, control first, for example `[["A: pages", 524, 38], ["B: scroll", 504, 30]]` (illustrative numbers, not Etsy's). Up to five variants. `cells` sets the sample-size inputs: `B22` baseline and `B23` minimum detectable effect as fractions (0.05 for 5% relative), `B26` users per day; α and power sit in `B10` and `B11`. Do not pass computed columns. Values set through `cells` replace the `{{baseline}}`, `{{mde}}` and `{{daily}}` tokens, so the script's "no value" warning for them is expected. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/ab-testing.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's plan or report in any form and check it against the common mistakes in card.md:

1. One primary metric was chosen before launch; guardrails are named.
2. The sample size was computed in advance and reached; a difference within the noise is not called an effect.
3. The test ran whole weeks and was not stopped at the first significant day.
4. The actual split matches the planned one.
5. Each variant changes one thing, so the result has a cause.
6. The decision follows the rule written before launch.

Report findings as a numbered list: what is wrong, why it misleads the decision, the concrete fix. Recompute p-value and interval when counts are given. End with a verdict: "test supports the decision", "supports it after fixes" or "not enough data".
