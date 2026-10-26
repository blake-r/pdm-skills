---
name: customer-journey-map
description: Map the path a customer takes to a goal through contact with the company as stages × four rows (goals and expectations, touchpoints and scenarios, experience and problems, insights and opportunities), find the bottleneck, choose one opportunity and how to check it, and produce a one-slide PPTX, or review an existing journey map. Use when the customer path spans several steps and channels, customers drop off for unclear reasons, or the team must choose which stage to improve first.
---

# Customer Journey Map

The theory, rows, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings research data about a customer path, **review** when the user brings a finished map or a decision drawn from one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the customer type and the scenario: who goes the path and to what goal;
- the stages as the customer sees them, if the user has them;
- the data per stage: interviews, surveys, reviews, support contacts, step conversion; source and date for each;
- the goal of the work, for example fewer drop-offs at checkout.

Do not invent emotions, problems or numbers. If a cell has only the team's guess, mark it "hypothesis" and say how to check it.

### 2. Set the stages

Name 3–5 stages by what the customer does ("chooses a size"), not by company departments ("logistics"). One map covers one customer type and one scenario; if the data mixes new and returning customers, make two maps.

### 3. Fill the rows

For each stage write the goals and expectations, the touchpoints and what the customer does there, the experience and problems with the source in brackets, and the insights and opportunities. Leave a cell empty with "no data" rather than filling it with a guess.

### 4. Decide

Name the bottleneck stage and the evidence: step conversion, share of complaints, quotes. Choose one opportunity, a test on part of the customers, the metric, the expected change and the date of the check. Say that the bottleneck may move after the fix. Do not promise effects.

### 5. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, the customer and scenario, the stages with four rows each, and the decision. Write a file only after the user confirms. Ask for the output path (default `customer-journey-map-<scenario>.pptx` in the working directory). Save the data as JSON:

```json
{
  "text": {
    "title": "…",
    "actor": ["Footwear buyer", "Goal: buy a pair"],
    "stage1": "Awareness",
    "goals1": ["Wants comfortable shoes"],
    "touch1": ["Ads, marketplaces"],
    "exp1": ["No data"],
    "ins1": ["No data"],
    "stage2": "Decision",
    "goals2": ["Find the right size"],
    "touch2": ["Product page, reviews"],
    "exp2": ["Do not know their size (reviews)"],
    "ins2": ["Size chart in emails"],
    "decision": ["Bottleneck: size at the decision stage", "Test: size chart in abandoned-cart emails", "Metric: email-to-order conversion, check in a month"]
  }
}
```

The template has five stages (`stage1`…`stage5` with `goals`, `touch`, `exp`, `ins` for each). Leave out the keys of unused stages: the script leaves them empty and names them in a warning. Keep the actor to two lines of up to about 20 characters, stage names to one or two short words of up to about 12 characters each and cells to about three lines of under 30 characters and up to four lines in the decision; list the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/customer-journey-map.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's map in any form and check it against the common mistakes in card.md:

1. The map covers one customer type and one scenario.
2. Stages are named by what the customer does, not by departments.
3. Experience and problems come from data with sources, not from the team's guesses.
4. Every stage has touchpoints and problems, not only goals.
5. A bottleneck is named, with evidence.
6. One opportunity is chosen, with a test, a metric and a date to check.
7. The map has a date and a plan to update it after the change.

Items 1 and 3 often need the user's knowledge: ask instead of reporting a finding. Report findings as a numbered list: stage or row, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
