---
name: cost-benefit-analysis
description: Compare the costs and benefits of a feature or its alternatives period by period, find when each option breaks even, and produce a one-slide PPTX with the cumulative benefit/cost chart and the decision, or review an existing cost-benefit analysis. Use when the user must decide whether to launch, choose between options, or keep or close a feature.
---

# Cost / Benefit Analysis

The theory, chart, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a decision and estimates, **review** when the user brings a finished calculation or a decision based on one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the decision and the options, including "change nothing";
- the horizon and the period step (month, quarter, year);
- per option and period: costs (one-off and recurring) and benefits (extra revenue, saved costs, reduced losses), each with its source;
- a discount rate if the horizon is longer than a year.

Do not invent numbers. If the user has only a single figure, ask for a cautious and an optimistic value.

### 2. Clean the estimates

- Count benefits only above "change nothing".
- Remove transfers counted on both sides (a payment from one party to another is not a net cost or a net benefit to the whole).
- Make sure recurring costs (support, infrastructure) continue through the horizon.
- Keep non-monetary effects as a short list next to the numbers.

### 3. Calculate

Per option and period: cumulative costs, cumulative benefits, their ratio, and net benefit. Discount future periods when a rate is given. Report the payback period (first period where the ratio reaches 1.0), the final ratio and the net benefit, for both the cautious and the optimistic case. Show the calculation with code if there are many figures.

### 4. Decide

Compare options by net benefit and ratio together; if they point to different options, say so and choose by net benefit within the budget. State the decision and the condition for revisiting it: which actual figure, by which period, would change it. If the options swap places between the cautious and optimistic cases, say the decision depends on that estimate and suggest how to check it cheaply.

### 5. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, the assumptions, the totals, the decision and the chart series (the table of cumulative figures and ratios). Write a file only after the user confirms. Ask for the output path (default `cost-benefit-<topic>.pptx` in the working directory). Save the data as JSON:

```json
{
  "text": {
    "title": "…",
    "assumptions": ["Horizon: 5 quarters", "Discount rate: 15% per year", "Benefits are measured above \"change nothing\""],
    "totals": ["A: pays back in quarter 3, ratio 1.8", "B: …"],
    "decision": ["Launch A", "Revisit: if the ratio is below 0.9 by quarter 3"]
  },
  "charts": {
    "ratio": {
      "categories": ["Q1", "Q2", "Q3", "Q4", "Q5"],
      "series": [
        {"name": "Break-even (1.0)", "values": [1, 1, 1, 1, 1]},
        {"name": "Option A", "values": [0.4, 0.9, 1.3, 1.6, 1.8]}
      ],
      "value_axis": {"minimum": 0, "maximum": 2.0, "major_unit": 0.5, "number_format": "0.0"}
    }
  }
}
```

Keep the break-even series first with 1.0 in every period: the template draws it as a dashed line. Add at most four options after it; group the rest in chat. Chart at least two periods: if the user has only totals for the whole horizon, ask for the profile by period and do not spread the totals yourself. Always set `maximum` to four times `major_unit` (2.0 with 0.5, 4.0 with 1, 8.0 with 2), choosing the smallest pair above the largest ratio: some viewers, such as Keynote, always split the axis into four steps and otherwise put the ticks off 1.0; with the cautious and optimistic cases, chart the cautious one and give both in `totals`. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/cost-benefit-analysis.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's calculation in any form and check it against the common mistakes in card.md:

1. Benefits are counted above "change nothing".
2. No transfer or effect is counted twice.
3. Recurring costs run through the whole horizon.
4. Estimates are ranges with sources, not single figures.
5. The arithmetic, cumulative sums and discounting are right.
6. The horizon fits the decision and is the same for all options.
7. The decision states a condition for revisiting it.
8. Options are compared by net benefit as well as by ratio: a small option with a higher ratio can bring less net benefit.

Items 1 and 4 often need the user's knowledge: ask instead of reporting a finding when the source of an estimate is unknown. Report findings as a numbered list: option or line, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
