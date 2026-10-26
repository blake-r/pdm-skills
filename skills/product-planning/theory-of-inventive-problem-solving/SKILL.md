---
name: theory-of-inventive-problem-solving
description: Solve a hard product, service or process problem with TRIZ (theory of inventive problem solving) - state the contradiction where improving one property worsens another, formulate the ideal final result, list the resources already in the system, separate the conflicting requirements in time, space or conditions using a TRIZ principle, and produce a one-slide PPTX, or review an existing TRIZ analysis. Use when obvious solutions force an either-or trade-off (speed vs safety, convenience vs control, capacity vs cost) and the team is about to settle for a compromise.
---

# Theory of Inventive Problem Solving (TRIZ)

The theory, steps, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a problem, **review** when the user brings a finished TRIZ analysis or a decision drawn from one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the problem in one phrase and the system: its elements, users, processes;
- what must improve and what gets worse when it does;
- the solutions already tried or proposed, and why they do not fit;
- the resources available: data, time windows, places, participants, existing processes.

If the problem is not yet understood, say that TRIZ needs a stated conflict and suggest finding out what goes wrong first. If a known solution only lacks money or people, say that TRIZ will not add much.

### 2. State the contradiction

Name the element or parameter in conflict and write two requirements: it must be A for benefit X, and not-A for benefit Y. Check with the user that both benefits are real. If there is no conflict, only a lack of ideas, say so and stop.

### 3. Ideal final result

Write how it would be if the element itself delivered both X and Y with no harm and no cost. Use it as a direction, not a promise.

### 4. Resources

List what already exists in the system and around it: time windows when a requirement does not apply, information the system already has, idle capacity, users' own actions. Prefer free resources to new costs.

### 5. Separate and pick a principle

Find when, where or under which conditions A is needed and when not-A. Propose two or three ways to separate the requirements, each with a TRIZ principle by name (for example "preliminary action", "segmentation", "asymmetry"). Treat principles as hints: the solution still has to be designed. Do not invent effects or numbers.

### 6. Decide

Choose one solution with the user and say how to check it: the metric, the expected result and the date.

### 7. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, the element, the two requirements, the ideal final result, resources, principle, solution and check. Write a file only after the user confirms. Ask for the output path (default `triz-<problem>.pptx` in the working directory). Save the data as JSON (the example is the platform-load case from card.md):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Withstand the payday request peak early",
    "element": "Server capacity",
    "need_a": ["Lots: wave of requests at 16:00, over +500%"],
    "need_not_a": ["Little: the rest of the time — for cost and energy"],
    "ikr": ["Capacity exists exactly when it is needed"],
    "resources": ["Number of payments for tomorrow is known", "History of server load", "Traces of service calls"],
    "principle": ["Separation in time", "'Preliminary action' technique"],
    "solution": ["A plan based on a similar day in the past", "Increase capacity around noon", "Scale back after the peak"],
    "check": ["Peak without overload", "Platform costs lower"]
  }
}
```

Keep the title under 50 characters, the element under 50, each requirement and the ideal final result to two items of under 55 characters, resources, principle, solution and check to three items of under 35 characters each; list the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/theory-of-inventive-problem-solving.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's analysis in any form and check it against the common mistakes in card.md:

1. The contradiction is stated: one element, two opposite requirements, a benefit for each.
2. The solution removes the conflict instead of settling on a middle value.
3. The ideal final result is written and the solution moves toward it.
4. Resources already in the system were considered before adding new costs.
5. The separation (time, space, conditions) and the principle are named.
6. The solution has a check: metric, expected result, date.

Item 1 often needs the user's knowledge of the system: ask instead of reporting a finding when the benefits are unclear. Report findings as a numbered list: step, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
