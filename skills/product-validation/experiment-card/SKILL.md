---
name: experiment-card
description: Fill an experiment card for one hypothesis - the question, the hypothesis, the success condition set in advance (metric and threshold), people and materials, the procedure, then the observations and the verdict (validated, invalidated or uncertain) with the decision - and produce a one-slide PPTX; or review an existing experiment plan or report. Use before a product experiment when the team must agree in advance what counts as success, when experiment results get lost in chats, or when the decision will be made by people who did not run the test.
---

# Experiment Card

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a hypothesis to test or results to record, **review** when the user brings a finished plan or report.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the decision the experiment feeds and the question behind it;
- the hypothesis and why the team believes it;
- the metrics available, their current values and the traffic or number of people the test can reach;
- who runs it, the budget, the time; for a finished test, the observations with numbers and dates.

Do not invent current values, results or thresholds. If the question would not change any decision, say so and stop.

### 2. Fill the plan (fields 1-5)

- **Question:** one sentence; the answer must change a decision.
- **Hypothesis:** one statement that can be proved wrong. Split compound ones into separate cards.
- **We are right if:** the main metric, the threshold and the secondary metrics in order of priority, so a split result still leads to a verdict.
- **People and materials:** who runs it, who takes part, the variants, texts, budget.
- **Procedure:** steps, duration, the number of observations needed, when to stop. Warn against stopping on the first days' data.

### 3. Fill the result (fields 6-7)

For a finished test: the observations with numbers per metric, anything surprising, the verdict against the threshold written in field 3, and the decision (ship, rework, drop, test further). Mark "uncertain" when data are short or metrics conflict against the priority order.

### 4. Show, then write

Show in chat first: all seven fields and the decision. Write a file only after the user confirms. Ask for the output path (default `experiment-<topic>.pptx` in the working directory). Save the data as JSON (the example is the AIC bank case from card.md; values the source does not give are marked so, not filled in):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Large bank, AIC pilot: view counts on the preview, published 2019",
    "question": "Do users have reasons to choose a product other than its characteristics?",
    "hypothesis": "The number of views on the preview will push choice — by analogy with booking.com",
    "right_if": ["Threshold not given in the source", "Order of metric priority set in advance"],
    "people": "Agency analysts together with the bank's product team",
    "materials": ["Current page with the product list", "The same page with view counts"],
    "procedure": ["Show the versions to different visitors", "Collect the required volume of data", "Dates and duration not given in the source"],
    "observations": ["Metrics: time to click, share of clicks on the preview, attempts to submit an application, time on page", "Users got to the popular product faster", "More often moved from the list to the product", "No figures in the source"],
    "conclusion": ["Product popularity also affects choice", "Next: visual hints and notifications"],
    "validated": "✓",
    "invalidated": "",
    "uncertain": ""
  }
}
```

Put "✓" in exactly one of `validated`, `invalidated`, `uncertain` and an empty string in the others; leave all three empty for a plan. `question` and `hypothesis` take under 110 characters; the other fields take up to four items of under 80 characters (`people` and `materials` under 60); each list item becomes its own paragraph. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/experiment-card.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's plan or report in any form and check it against the common mistakes in card.md:

1. There is a question whose answer changes a decision.
2. The success condition (metric, threshold, priority of metrics) was written before the start.
3. The test changes one thing; compound changes are split.
4. The procedure states the duration and the number of observations and does not stop on the first days' data.
5. The verdict follows from the threshold, and an invalidated or uncertain result is recorded, not dropped.

Report findings as a numbered list: what is wrong, why it misleads the decision, the concrete fix. End with a verdict: "experiment supports the decision", "supports it after fixes" or "not enough data".
