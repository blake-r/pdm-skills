---
name: feature-canvas
description: Describe a new product feature before design and development with Nikita Efimov's Feature Canvas (analysis area - idea, why, contextual situations, problems to solve, affected customers, current behaviour, value, restrictions, capabilities; planning area - customer tasks, awareness, support needed, business goals, success criteria, key activities) and produce a one-slide PPTX, or review an existing feature canvas or feature brief. Use when an idea for a new feature arrives and the team must decide whether to build it and in what minimal form, or when the team lacks a shared view of the problem.
---

# Feature Canvas

The theory, blocks, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a feature idea, **review** when the user brings a filled canvas or a feature brief.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the idea and where it came from: customers, management, competitors;
- what is known about the problem and its sources: support requests, analytics, interviews;
- who is affected and how customers cope today;
- known technical, legal or time limits, and what the company already has that helps.

Do not invent facts, numbers or customer quotes. Mark every answer without data as "hypothesis" and name what would confirm it.

### 2. Analysis area

Fill in order: idea in two or three sentences; why it matters to customers and to the business, down to the root cause; situations; problems with their sources; affected customers; current behaviour; value; restrictions; capabilities. If the problems or situations stay vague, stop and say what to find out before planning.

### 3. Planning area

Only if the analysis holds: customer tasks, how customers will learn about the feature and where they will look for it, where they need help and which mistakes are likely, business goals, success criteria with the data needed to judge them, and the key activities - the minimum for the first version and what comes later.

### 4. Decision

Recommend build, change or drop, and name the blocks the recommendation rests on and the hypotheses still open.

### 5. Show, then write

Show in chat first, block by block as they will appear on the slide. Write a file only after the user confirms. Ask for the output path (default `feature-canvas-<feature>.pptx` in the working directory). Save the data as JSON (the example is the Monzo case from card.md):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Monzo: blocking gambling payments",
    "idea": ["The customer blocks gambling payments themselves"],
    "why": ["We help when debts already exist", "We want to prevent them"],
    "context": ["The decision to gamble is often impulsive"],
    "problems": ["80% of those seeking help are in debt", "Customers ask for the feature"],
    "affected": ["Over 5 thousand customers (bank estimate)"],
    "behavior": ["Website-blocking programs", "Self-exclusion with bookmakers"],
    "value": ["The block is applied directly on the bank account"],
    "restrictions": ["Some merchants use wrong codes", "Workaround: cash and transfers"],
    "capabilities": ["Merchant category code on every transaction"],
    "tasks": ["Turn the block on", "Later, possibly turn it off"],
    "awareness": ["A toggle in the settings"],
    "support": ["Removal via chat, after 48 hours"],
    "goals": ["A customer without debts means fewer losses"],
    "success": ["Not named: to be clarified"],
    "activities": ["List of gambling merchant codes", "Testing with the customers who asked for it"]
  }
}
```

Keep the title under 50 characters. Keep `why` and `context` to five items, `idea`, `restrictions`, `capabilities`, `tasks`, `goals`, `success` and `activities` to four items, `problems`, `affected`, `behavior` and `value` to three items, `awareness` and `support` to two items; every item under 40 characters. List the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/feature-canvas.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's canvas or brief in any form and check it against the common mistakes in card.md:

1. The problems and situations are concrete, not only the idea.
2. Every problem names its source and how often it is reported.
3. Answers without data are marked as hypotheses.
4. Success criteria are named, with the data needed to judge them.
5. Key activities single out the minimum for the first version.
6. The decision - build, change or drop - follows from the blocks.

Item 2 often needs the user's data: ask instead of reporting a finding when unsure. Report findings as a numbered list: block, what is wrong, why it matters for the decision, the concrete fix. End with a verdict: "ready to decide", "ready after fixes" or "not enough data".
