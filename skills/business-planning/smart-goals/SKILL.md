---
name: smart-goals
description: Write or check a goal with the SMART criteria in Doran's original form (Specific, Measurable, Assignable, Realistic, Time-related) and produce a one-slide goal sheet, or review an existing goal. Use when a goal is vague, has no owner, no number or no date, or when a goal must be agreed with an owner.
---

# SMART Goals

The theory, Doran's wording of the criteria, limits and the source example are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user has a rough goal to write down, **review** when the user shows a written goal and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the rough goal in the user's own words and whose goal it is;
- the current value of the indicator it should move;
- the resources: people, money, time;
- who will do it;
- the desired date and whether checkpoints are needed.

SMART checks wording, not whether the goal is worth setting: if the user is still choosing goals, say so and ask what they want from the sheet. Do not invent numbers, names or dates: mark what the user did not give as unknown.

### 2. Go through the five criteria

Say which version is used: Doran's original (Assignable, Realistic) unless the user asks for the later one (Achievable, Relevant, Time-bound). Then for each letter:

- S: one area of improvement; split the goal if there are two.
- M: a number and a unit, "from X to Y"; if a number is impossible, an indicator of progress and the data source.
- A: one named owner. No owner means the goal is not accepted.
- R: compare with the resources and write the resource ceiling into the goal.
- T: a date, with checkpoints for a long goal.

Then add an action plan and a decision: accepted, or returned to the author with the open criterion.

### 3. Show, then write

Show the sheet in chat first as a table by template blocks: title, goal sentence, S, M, A, R, T, action plan, decision. Write a file only after the user confirms. Ask for the output path (default `smart-goals-<owner>.pptx` in the working directory). Save the data as JSON. The example is Doran's own goal from card.md, which gives no owner, plan or decision, so those fields say so; an empty field is `null` and leaves its block empty:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Doran's example, 1981: inventory goal",
    "goal": "By December 31, 198_, implement an inventory system that reduces inventory costs by $1 million, at a cost of no more than 200 work hours and $15,000",
    "s": "Inventory costs; means: an inventory system",
    "m": "Reduce inventory costs by $1 million",
    "a": "The executor is not named in the example",
    "r": "Resource ceiling: 200 work hours and $15,000",
    "t": "By December 31, 198_ (the year is not given in the text)",
    "actions": ["Doran's example has no action plan"],
    "decision": ["Criterion A is not met: no executor", "The example has no action plan", "Return to the author with these two gaps"]
  }
}
```

Field limits that fit the slide: title under 60 characters; goal under 200; s, a under 80; m, r, t under 120; actions up to five items under 55; decision up to four items under 55. A list of strings becomes lines. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/smart-goals.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's goal and check it against the common mistakes in card.md:

1. The criteria are used in a mixed or unstated version (Doran's vs Achievable/Relevant/Time-bound); the version is not agreed.
2. The goal has no owner.
3. Measurability at any price: a number replaces the real goal.
4. The goal has no action plan.
5. A number without the starting level, so realism cannot be judged.
6. A means instead of a result: "implement a system" is not a goal.
7. Five "yes" answers are taken as proof that the goal is right.

Items 3 and 7 usually cannot be judged from the text alone: ask what the number stands for and why the goal was chosen, instead of reporting a finding. Also check that the date is a real date and that the resource ceiling is written down. Report findings as a numbered list: what is wrong, why it matters, the concrete rewrite. End with a verdict: "goal is ready", "ready after changes" or "return to the author".

Example: "Increase sales by Q4", no owner. Findings: item 2, no owner, name one; item 5, no starting level, ask for it; M has no number, write "from X to Y"; item 4, no plan. Verdict: "return to the author".
