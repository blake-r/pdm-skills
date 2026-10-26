---
name: scamper-method
description: Generate ideas for changing an existing product, feature or process with the seven SCAMPER questions (substitute, combine, adapt, modify, put to other uses, eliminate, reverse or rearrange), shortlist them against a goal, choose what to test first, and produce a one-slide PPTX, or review an existing SCAMPER list. Use when there is a concrete object to improve and the team is stuck on the same solutions, needs many options before selection, or moves a product to a new channel or audience.
---

# SCAMPER Method

The theory, questions, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings an object to improve, **review** when the user brings a finished list of SCAMPER ideas or a decision drawn from one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the object: a specific screen, feature, tariff or process, not "the product in general";
- the goal: which customer or business problem the change should solve;
- the constraints: budget, deadline, regulation, technology;
- what is known about what does not work now, with sources.

If the problem itself is unclear, say that SCAMPER gives options, not a diagnosis, and suggest finding out what goes wrong first.

### 2. Go letter by letter

For each of the seven letters ask its question from card.md about the object and write two to four concrete ideas, each a change understandable without explanation. Do not judge ideas at this step. If a letter gives nothing sensible for this object, leave it empty and say so; do not force it. Mark ideas that depend on facts you do not have as assumptions.

### 3. Shortlist

Agree on the selection criterion with the user: fit with the goal, effort, risk. Pick two to four ideas and give the reason for each in one phrase. Do not invent effects or numbers.

### 4. Decide

Choose what to do first, how to test it (a rough version of the screen or a release to part of the customers), the metric, the expected change and the date of the check.

### 5. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, seven letters, the shortlist and the decision. Write a file only after the user confirms. Ask for the output path (default `scamper-<object>.pptx` in the working directory). Save the data as JSON (the example is the T-Bank case from card.md; the team did not use SCAMPER, its documented decisions are placed by letter, and P and R stay empty because the article has no data):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "T-Bank web account for customers without the app",
    "s": ["PIN code login instead of SMS code and password"],
    "c": ["Desktop and mobile web built together"],
    "a": ["Mobile web as a PWA, close to the app", "Card details, QR scan, contact picker, tab bar"],
    "m": ["Components moved from grey to white, as in the app"],
    "p": [],
    "e": ["Dropped turning the phone over to hide balances"],
    "r": [],
    "shortlist": ["PWA for the mobile version", "Desktop and mobile built together"],
    "decision": ["Goal: mobile web matches the app", "Desktop supports the system with its own specifics", "Metric: conversion into sections (not published)"]
  }
}
```

Keep the title under 75 characters, each letter to three list items of under 45 characters, the shortlist and the decision to four items each; list the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. An empty list leaves the letter blank on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/scamper-method.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's list in any form and check it against the common mistakes in card.md:

1. The object is concrete, and the goal is stated.
2. All seven questions were asked; empty letters are empty for a reason, not skipped.
3. Each idea is a concrete change, not a slogan.
4. No idea is stretched to fill a letter.
5. The shortlist has a stated criterion.
6. The first idea to do has a test, a metric and a date.

Item 2 usually cannot be judged from the list alone: ask the user instead of reporting a finding. Report findings as a numbered list: letter or idea, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
