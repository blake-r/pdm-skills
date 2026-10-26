---
name: value-proposition-canvas
description: Match what a product offers to what one customer segment needs on the Value Proposition Canvas (customer side - jobs, pains, gains; value map - products and services, pain relievers, gain creators), judge the fit, decide what to build, drop and test, and produce a one-slide PPTX, or review an existing canvas. Use when designing a new product or major feature from customer research, when an offer does not sell, or when every feature must be tied to a pain or gain.
---

# Value Proposition Canvas

The theory, blocks, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings research about a segment and an offer or idea, **review** when the user brings a filled canvas or a decision drawn from one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the one segment the canvas is for;
- the research data: interviews, surveys, analytics, support requests; source and date for each;
- the current or planned products and services;
- the alternatives the customers use now.

If the data covers several segments, say that their jobs and pains differ and build one canvas per segment. Do not invent jobs, pains or gains. If a block has only the team's guesses, mark them "hypothesis" and say how to check them.

### 2. Fill the customer side first

Write the jobs, pains and gains in the customers' words, each with its source. Rank jobs by importance, pains from extreme to moderate and gains from essential to nice-to-have, and say what the ranking rests on: frequency in interviews, survey share, money or time lost.

### 3. Fill the value map

List the products and services. For each important pain write what relieves it; for each important gain write what creates it. Keep pairs explicit: every reliever and creator names the pain or gain it answers.

### 4. Judge the fit and decide

Name the important pains and gains that nothing answers, and the features that answer nothing. Decide what to build, what to drop and how to check that customers care: a test, the metric, the expected change and the date. Say that the fit on paper is a hypothesis until behaviour confirms it.

### 5. Show, then write

Show in chat first as a table with one row per slide block: the title, the segment, six blocks, the fit and the decision. Write a file only after the user confirms. Ask for the output path (default `value-proposition-canvas-<segment>.pptx` in the working directory). Save the data as JSON (the example is the Monzo Flex case from card.md; the team did not use the canvas):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Monzo Flex: buy now, pay later",
    "segment": "Monzo customers who use credit cards or buy-now-pay-later services",
    "jobs": ["Pay for a purchase later", "Wait for a refund"],
    "pains": ["Individual purchases are not visible", "The minimum payment confuses", "An application for each purchase"],
    "gains": ["Know the limit in advance", "See repayment progress"],
    "products": ["Flex in the Monzo app"],
    "pain_relievers": ["3, 6 or 12 payments with an end date", "One limit without new applications"],
    "gain_creators": ["The customer chooses the limit", "Progress for each purchase"],
    "fit": ["Covered: certainty, control, visibility, convenience"],
    "decision": ["Launch Flex with these features", "Always-on research programme", "Metrics: product NPS, ease of use"]
  }
}
```

Keep the title to one line of under 70 characters and the segment to one line of under 100. Each canvas block takes up to four list items: pain relievers and gain creators under 35 characters, gains and pains under 28 (they sit inside the circle), jobs and products under 25 (their columns are narrow). The fit and the decision take up to four items of under 60 characters each; list the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/value-proposition-canvas.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's canvas in any form and check it against the common mistakes in card.md:

1. The canvas covers one segment.
2. Jobs, pains and gains come from data with sources, not from the team's guesses.
3. Pains and gains are ranked.
4. Every pain reliever and gain creator answers a named pain or gain.
5. No feature answers nothing; important pains without an answer are named.
6. The decision has a test, a metric and a date.

Item 2 often needs the user's knowledge: ask instead of reporting a finding. Report findings as a numbered list: block, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
