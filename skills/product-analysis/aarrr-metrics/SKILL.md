---
name: aarrr-metrics
description: Lay out a product's metrics across the five AARRR stages (acquisition, activation, retention, referral, revenue), compare each with a benchmark, find the bottleneck and produce a one-slide PPTX with the funnel and the decision, or review an existing AARRR dashboard. Use when the team must decide which stage of the customer path to work on next.
---

# AARRR Metrics

The theory, stages, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings product data or asks where to focus, **review** when the user brings a filled funnel or a decision drawn from one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and the customer path: what "first value" and "coming back" mean for it;
- the period;
- per stage: the metric with its exact definition and its value for that period;
- a benchmark per stage: previous period, target, competitors or market, with the source.

Do not invent values or benchmarks. If a stage has no data, keep it in the funnel as "no data" and say what to measure.

### 2. Check the metrics

- One definition per metric, one period for all stages.
- Replace vanity counts (downloads, sign-ups) with rates that show value.
- Point out stages where the company's metric only approximates the stage.

### 3. Find the bottleneck

Compare each stage with its benchmark as a share of it or a multiple, since the units differ. The bottleneck is the stage with the largest gap, not the smallest number. If two stages lag equally, prefer the earlier one in the customer's path unless retention is failing: fixing acquisition while customers leave wastes money.

### 4. Decide

Name one change for the bottleneck stage, the metric that will show the result and the date to check it. Suggest how to find the cause (interviews, cohorts, tests) if it is unknown. Do not promise effects.

### 5. Show, then write

Show in chat first: the five stages with metric, value and benchmark, the bottleneck and the decision. Write a file only after the user confirms. Ask for the output path (default `aarrr-<topic>.pptx` in the working directory). Save the data as JSON:

```json
{
  "text": {
    "title": "…",
    "acquisition": "…", "acquisition_compare": "…",
    "activation": "…", "activation_compare": "…",
    "retention": "…", "retention_compare": "…",
    "referral": "…", "referral_compare": "…",
    "revenue": "…", "revenue_compare": "…",
    "bottleneck": "…",
    "decision": ["Change: …", "Check: … by …"]
  }
}
```

Keep each stage value under about 90 characters and each comparison under about 110 so they fit their boxes. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/aarrr-metrics.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's funnel in any form and check it against the common mistakes in card.md:

1. Every stage has a metric with a clear definition, and all use the same period.
2. Metrics show value (rates, money), not vanity counts.
3. Every metric has a benchmark with a source.
4. The bottleneck is chosen by the gap to the benchmark.
5. The team works on one stage, not all at once.
6. Acquisition is not being scaled while retention fails.
7. The decision names a metric and a date to check it.

Item 3 often needs the user's knowledge: ask where a benchmark came from instead of reporting a finding. Report findings as a numbered list: stage, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
