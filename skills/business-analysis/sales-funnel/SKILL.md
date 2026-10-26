---
name: sales-funnel
description: Build a sales funnel - the stages a customer passes from first contact to purchase, account opening or signed deal - with the number of customers at each stage, stage-to-stage conversion and time spent at each stage, find the bottleneck, decide what to change at that stage and how to check it, and produce a one-slide PPTX; or review an existing funnel. Use when overall conversion is low and it is unclear where customers are lost, for signup, loan application, checkout or B2B deal flows.
---

# Sales Funnel

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a flow and its data, **review** when the user brings a finished funnel.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and the flow: from which first contact to which final step;
- the stages in order, and the event in the data that marks entry to each;
- the period and, for each stage, the number of customers who entered it in that period and the time they spent on it, with the source;
- a baseline to compare with: a previous period or a similar product.

Do not invent numbers. A stage without data stays empty, and say so in `scope`.

### 2. Compute

Take customers who entered the funnel in one period and follow the same customers through the stages. For each stage compute conversion from the previous stage and time on the stage (median if the distribution is skewed). If a stage hides several steps, split it.

### 3. Bottleneck and decision

Name the transition with the largest loss of customers or the longest wait against the baseline. State what is known about why, and what data would confirm it. Propose one change at that stage, the metric that shows it worked, and the check that quality after the stage did not drop.

### 4. Show, then write

Show in chat first: the stage table (stage, customers, conversion, time), the bottleneck and the decision. Write a file only after the user confirms. Ask for the output path (default `sales-funnel-<product>.pptx` in the working directory). Save the data as JSON (the example is the Monzo case from card.md; Monzo did not publish stage-by-stage numbers, so only the entry and the end are filled):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Monzo US, sign-up, October 2023",
    "stage_1": "Downloaded the app",
    "count_1": "100%",
    "days_1": "17 min on average",
    "stage_2": "Opened an account",
    "count_2": "9%",
    "conv_2": "9%",
    "days_2": "—",
    "scope": ["Monzo blog, 2024", "39 screens, 210 taps; per-screen numbers not published"],
    "bottleneck": ["One check caused 40% of the funnel drop-off", "Address entry: takes longest and has the most typos"],
    "decision": ["Address autofill and hints", "Low risk per Alloy rules: check skipped", "Result: 40% opened an account, median 7 min"]
  }
}
```

Keys per stage `n` from 1 to 6: `stage_n` (name), `count_n` (customers, a number or a share of entry), `conv_n` (conversion from stage `n-1`, from stage 2 on), `days_n` (time on the stage with its unit). Stages 1 and 2 are required; fill stages 3 to 6 in order, and those left without keys are removed from the slide. Keep stage names under 20 characters, `scope` to two items and `bottleneck` and `decision` to three items of under 60 characters each; one thought per item, each becomes its own paragraph. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/sales-funnel.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's funnel in any form and check it against the common mistakes in card.md:

1. Conversion is shown per stage, not only overall.
2. The stages come from events in the data, and the counts are for customers of one period.
3. Time on each stage is counted.
4. One change at the bottleneck, not several at once, and not more traffic at the entry instead.
5. Quality after the stage is checked, not only conversion.

Report findings as a numbered list: stage, what is wrong, why it misleads the decision, the concrete fix. End with a verdict: "funnel supports the decision", "supports it after fixes" or "not enough data".
