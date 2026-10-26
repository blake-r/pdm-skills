---
name: sprint
description: Plan a Scrum sprint around one sprint goal — capacity, limit from past sprints, selected items with plans and estimates — record its outcome and keep a sprint history in a spreadsheet, or review an existing sprint plan or sprint results. Use when the user is preparing sprint planning, wants to phrase a sprint goal, or asks why the team keeps not finishing what it took.
---

# Sprint

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user is planning a sprint or recording its results, **review** when the user brings a sprint plan, a sprint goal or sprint statistics to check.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the team, the sprint number and dates, the sprint length in working days;
- the product goal the sprint should move towards;
- who is available and for how many days: holidays, training, other duties;
- the results of the last sprints, if any: taken at planning, added during the sprint, not done at the end, and whether the goal was met;
- the top of the product's ordered list of work, with the product owner's priorities;
- estimates from the people who will do the work, in one unit (hours, story points).

If the work is a stream of unrelated small requests and no single goal can be phrased, say that the card suggests a continuous flow instead of sprints, and ask whether to continue. If the team keeps changing the sprint length to fit the work, recommend fixing the length and splitting the work instead.

### 2. Capacity and limit

Compute capacity as each person's working days minus absences, times ideal hours per day (focused hours without interruptions; the card's case uses 4–5.6 of an 8-hour day), or in the team's own unit. Propose a limit from past sprints: what the team actually finished, not what it took. Without history, say that the first limit is a guess and will be corrected after the sprint. The limit is a guide, not a hard cap, and the team decides.

### 3. Sprint goal

Propose one goal: why the sprint is worth doing and what will be possible at its end. It must not restate the list of items. If the user gives several unrelated goals, ask which one matters, and treat the rest as other work. The team and the product owner own the final wording.

### 4. Select and plan items

Take items from the top of the list while the estimates fit the limit. For each: a short plan (sub-tasks or steps to a finished result), the estimate, who takes it, and whether the goal needs it. Never invent estimates: leave them empty and say who should give them. Mark work that arrives after planning as `added`.

### 5. At the end of the sprint

Fill in which items are finished by the team's own criteria, what happens to the rest (back to the list, next sprint, cancelled) and why, whether the goal was met, and what the sprint review decided. Add one row to the history.

### 6. Interpret

Read the totals: load against the limit, added work, share not done, goal items not done. More than the limit at planning means the team promises more than it delivered before. A large share not done means take less next time; a lot of added work means keep a reserve. The card's reference point: all promised work done in 8 of the last 10 sprints.

### 7. Show, then write

Show the plan in chat first: goal, limit, items with plan, estimate, owner, goal flag, origin; then the totals and the recommendation for the next limit. Write a file only after the user confirms. Ask for the output path (default `sprint-<team>-<number>.xlsx` in the working directory). Save the data as JSON. The example is the Rosbank case from card.md: the source shows statistics for sprints 62–67 but hides the sprint goal and the items, so those stay empty, and the limit of 135 ideal hours circled in the source, with no explanation of how it was derived, goes into the review text, not into the limit cell of a sprint that is not shown:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Rosbank, one of the teams: results of sprints 62–67 (sprints of 14–15 working days)",
    "goal": "The source hides the sprint goal",
    "product_goal": "Not given in the source",
    "unit": "ideal hours",
    "review": "The source circles a limit of 135 ideal hours; how it was derived is not stated"
  },
  "cells": {
    "C4": null,
    "History!A5": "62", "History!E5": 190, "History!F5": 18, "History!G5": 85,
    "History!A6": "63", "History!D6": "50–70", "History!E6": 150.5, "History!F6": 34.5, "History!G6": 30,
    "History!A7": "64", "History!D7": 100, "History!E7": 105, "History!F7": 15, "History!G7": 86,
    "History!A8": "65", "History!D8": 80, "History!E8": 150, "History!F8": 0, "History!G8": 100,
    "History!A9": "66", "History!D9": 80, "History!E9": 118.5, "History!F9": 92.5, "History!G9": 75,
    "History!A10": "67", "History!D10": 80, "History!E10": 156, "History!F10": 24, "History!G10": 27
  },
  "rows": []
}
```

Each row in `rows` has eight values: item, goal flag, plan, owner, estimate, origin, done, what next. Do not pass the number: the sheet numbers rows itself. Use null, not an empty string, for unknown values: null leaves the cell empty, as `C4` does in the example. Allowed words: goal flag and done — `yes` or `no`; origin — `planned` or `added`; in `cells`, `G4` (goal met) and the history column C — `yes`, `partially` or `no`. The template's formulas and totals match these words exactly, so check the spelling and keep them in English even when the rest of the data is in the user's language. Estimates and the limit `C4` are numbers in the unit from the `unit` field. The history sheet (`History`) takes one row per sprint from row 5 through `cells`: A sprint, B goal, C goal met, D limit, E taken, F added, G not done; columns H–J compute done, share not done and "all done". Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/sprint.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's sprint plan, goal or statistics in any form and check them against the common mistakes in card.md:

1. The goal states the reason for the sprint, not the list of items.
2. There is one goal, not several unrelated ones.
3. Success is not judged only by closed tasks and velocity: the goal and the result are checked.
4. Work does not pass between roles in sequence (analysis a sprint ahead, testing a sprint behind), leaving nothing finished for the review.
5. The plan rests on past sprints: the team does not take more than it has been finishing.

Also check the sprint length is fixed and the goal is not changed mid-sprint. Ask the user instead of reporting a finding when the material alone cannot show it: past sprint results, who gave the estimates, how work was split during the sprint. Report findings as a numbered list: what is wrong, why it matters for the next sprint, the concrete fix — for the goal, a rewritten goal. End with a verdict: "plan is ready", "ready after fixes" or "needs a goal first".
