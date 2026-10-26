---
name: impact-mapping
description: Build an impact map (Gojko Adzic) that links a business goal with a metric to the actors who affect it, the behaviour changes needed from them and the deliverables that could cause those changes, choose which branch to build first, and produce a one-slide PPTX; or review an existing impact map or a feature list against its goal. Use at the start of a product or initiative, when stakeholders bring ready-made features, when the team must pick what to build first, or when the goal changes.
---

# Impact Mapping

The theory, levels, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a goal or a list of wishes to sort out, **review** when the user brings a finished map or a feature list with a goal.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the business goal, the metric, its current value, the target and the date;
- who uses the product, who pays, who can help or block the goal;
- the features or wishes already on the table, and who asked for them;
- what is already known about these people's behaviour, with sources.

Do not invent metrics, numbers or research findings. Mark every behaviour change without data as a hypothesis.

### 2. Why

State the goal as a change in a business metric with a number and a date. If the user gives a feature as the goal, ask why it is needed until a metric appears.

### 3. Who and how

List two to four actors, including those who can block the goal. For each, write one or two behaviour changes: what they should start, stop or do differently. A behaviour change is not a feature.

### 4. What

For each behaviour change, list one or two deliverables that could cause it. Attach the user's existing features to the branches; features that fit no branch are candidates to drop — name them.

### 5. Choose

Recommend one or two branches to build first, with the reason: the size of the expected shift, the cost, the evidence. Say how to check the choice: the metric, the expected shift and the date.

### 6. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, the goal, the metric, then each actor with its behaviour changes and deliverables. Write a file only after the user confirms. Ask for the output path (default `impact-map-<initiative>.pptx` in the working directory). Save the data as JSON (the example is the UPI case from card.md):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "UPI: a billion transactions a day",
    "goal": "1 billion UPI transactions a day within 3–5 years",
    "metric": ["Transactions per day", "2021: about 100 million", "Target: 1 billion by 2025–2027"],
    "actor1": "People without a smartphone or without screen skills",
    "impact1_1": "Start paying via UPI from a feature phone",
    "deliv1_1": ["UPI 123PAY: call, missed call", "Built-in app, audio signal"],
    "impact1_2": "Pay by voice",
    "deliv1_2": ["Hello! UPI: Hindi and English"],
    "actor2": "Smartphone users",
    "impact2_1": "Pay small amounts via UPI instead of cash",
    "deliv2_1": ["UPI Lite: up to 200 rupees without a PIN"],
    "impact2_2": "Pay with a credit card via a UPI QR code",
    "deliv2_2": ["RuPay cards in UPI"],
    "actor3": "Merchants",
    "impact3_1": "Accept UPI instead of cash",
    "deliv3_1": ["Zero fee for accepting payments"],
    "impact3_2": "Pay a fee on payments above 2,000 rupees",
    "deliv3_2": ["0.4% fee, cap 300 rupees", "From 15 October 2026"]
  }
}
```

Keys are `actor1`…`actor3`, `impact<actor>_<n>` and `deliv<actor>_<n>` with up to two behaviour changes per actor; leave unused keys out (the script leaves them empty and names them in a warning). Keep the title under 50 characters, the goal under 70, the metric to three items of under 35, each actor under 40, each behaviour change under 60, each deliverable to two items of under 45; list the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/impact-mapping.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's map or feature list in any form and check it against the common mistakes in card.md:

1. The goal is a change in a business metric with a number and a date, not a feature.
2. The "how" level holds behaviour changes, not features.
3. Actors include those who can block the goal or on whom the result depends.
4. Every deliverable traces back to the goal through an actor and a behaviour change; name the ones that do not.
5. One or two branches are chosen first, with a way to measure the shift.

Item 3 often needs the user's knowledge of the market: ask instead of reporting a finding when unsure. Report findings as a numbered list: level and branch, what is wrong, why it matters for the choice, the concrete fix. End with a verdict: "map is ready", "map is ready after fixes" or "not enough data".
