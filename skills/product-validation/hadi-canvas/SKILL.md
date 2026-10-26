---
name: hadi-canvas
description: Run one HADI cycle (Hypothesis, Action, Data, Insights) on a canvas - the problem in numbers, a hypothesis tied to one metric, the experiment, the metric with its threshold, the data by period, the interim and final insights with a decision (scale, rework or drop) - and produce a one-slide PPTX; or review an existing HADI cycle. Use when the team has more ideas than resources and must learn quickly which ones move a metric, when arguments about an idea rest on opinions, or when a change can be rolled out to part of the users, stores or traffic and measured within one or two weeks.
---

# HADI Canvas

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a problem or an idea to test, **review** when the user brings a planned or finished cycle.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and the metric that is bad: its current value, the period, where the number comes from;
- the idea to test and why the team expects it to move the metric;
- who or what the change can be rolled out to (share of traffic, users, stores) and how much traffic or how many orders that gives per week;
- the time the team can give the cycle.

Do not invent current values, results or traffic. If the current value is unknown, the first step of the cycle is to measure it.

### 2. Write the top lanes

- **Problem:** the metric, its value, the source.
- **Hypothesis:** "if we do X, metric Y changes by Z, because ...". One hypothesis, one metric. Drop hypotheses that are obvious or are routine work.
- **Experiment:** what changes, for whom, for how long; what stays the same so the result is not mixed with another change.
- **Metrics:** the metric, the value before, the threshold that confirms the hypothesis, and the number of observations needed to tell the effect from noise. If traffic is too low for the threshold, say so and propose a longer run, a bigger change or a different metric.

### 3. Data and insights

Split the run into periods (days or weeks). For a planned cycle leave the values empty; for a running or finished one put the user's numbers per period and an interim insight per period. The final insight states whether the threshold was reached and the decision: scale, rework (the next hypothesis) or drop.

### 4. Show, then write

Show in chat first: the four lanes, the table by period, the insights and the decision. Write a file only after the user confirms. Ask for the output path (default `hadi-<product>.pptx` in the working directory). Save the data as JSON (the example is the Carrot quest case from card.md; values the source does not give are marked so, not filled in):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Carrot quest: sign-up page, FRII workshop week, May 2015",
    "problem": "Main task — raise the sign-up conversion on the website",
    "hypothesis": "Not stated; the tested change was the headlines",
    "experiment": ["Headline with the names of client companies: Ikea, Kaspersky, Intel", "New block headings and button", "Duration — one week"],
    "metrics": ["Sign-up conversion", "Threshold: not stated for this test", "Workshop rule: about 3,000 visitors, error 1%"],
    "period1": "Before changes",
    "period2": "Test week",
    "period3": "—",
    "metric1": "Sign-up conversion",
    "m1_p1": "not specified",
    "m1_p2": "no growth",
    "m1_p3": "—",
    "metric2": "Page visitors",
    "m2_p1": "not specified",
    "m2_p2": "≈3,000 planned",
    "m2_p3": "—",
    "metric3": "—",
    "m3_p1": "—",
    "m3_p2": "—",
    "m3_p3": "—",
    "subresults": "The source has no interim conclusions",
    "results": ["No conversion growth seen: hypothesis not confirmed", "Decision: move on to the next hypotheses", "The source has no figures before and after"]
  }
}
```

Keep `title` under 80 characters. The four lanes, `subresults` and `results` take up to four items of under 60 characters; each list item becomes its own paragraph. Table cells take under 20 characters (`metricN` under 25); put "—" in unused cells. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/hadi-canvas.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's cycle in any form and check it against the common mistakes in card.md:

1. The hypothesis is not obvious and is not routine work.
2. It names one metric, the value before and the threshold that confirms it.
3. The experiment changes one thing for that metric and has enough observations to beat noise.
4. Data are recorded by period, with the source.
5. The cycle lasts one or two weeks, not a quarter.
6. The cycle ends with a decision (scale, rework, drop), not just a report; a negative result is recorded as a result.

Report findings as a numbered list: what is wrong, why it misleads the decision, the concrete fix. End with a verdict: "cycle supports the decision", "supports it after fixes" or "not enough data".
