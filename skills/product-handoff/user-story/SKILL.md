---
name: user-story
description: Write or review a user story - the role, what the person wants and why ("As a <role>, I want <goal>, so that <benefit>"), notes from the team conversation, acceptance criteria as Given/When/Then examples including errors and defaults, the INVEST check (independent, negotiable, valuable, estimable, small, testable) and the team's size estimate - and produce a two-slide PPTX (the card face and its back); or review existing stories and acceptance criteria. Use when a need must be handed to a team before development, when a task will be picked up by someone without context, or when a requirement can be read in several ways.
---

# User Story

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a need, a feature idea or a draft to turn into a story, **review** when the user brings finished stories or acceptance criteria.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- who has the need: a concrete role or segment, not "a user";
- what the person wants to achieve and why, in their words; what is known about the problem (research, complaints, numbers);
- known limits, edge cases, errors and defaults; what is out of scope;
- whether the team has discussed it and estimated it.

Do not invent the role, the benefit, criteria or an estimate. If the work has no user (a library upgrade, a server move), say that a story format would only mask it and suggest a plain task.

### 2. Write the story

- **Role:** a concrete role. **Goal:** what the person wants, without the solution ("add a button" is a solution). **Benefit:** the "so that" part; say it guides how to build the feature.
- **Notes:** what the conversation settled: limits, open questions, what is out of scope. The card is a reminder for a conversation, not a full specification; if the team has not talked yet, list the questions for that conversation.

### 3. Acceptance criteria and INVEST

- Write one to four Given/When/Then examples: the main case, the default when something is missing, the error. Each "Then" is an observable result.
- Check INVEST and tick only what holds. If the story is not small or not estimable, propose a split along paths, interfaces, data or rules, and say the split is decided with the team, not by the product owner alone. Record the team's estimate with its unit; leave it empty if there is none.

### 4. Show, then write

Show in chat first: the story, the notes, the criteria and the INVEST gaps. The file has two slides: the face holds the title, role, goal, benefit and estimate; the back holds the title again, the notes, the criteria and INVEST. Write a file only after the user confirms. Ask for the output path (default `user-story-<topic>.pptx` in the working directory). Save the data as JSON (the example is the GOV.UK Pay case from card.md; what the source does not give is marked so, not filled in):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "GOV.UK Pay: payment in Welsh, published 29.07.2019",
    "role": "Connected service of a government body (not formulated in the source)",
    "goal": "Create a payment in Welsh or English",
    "benefit": "The benefit is not recorded in the source",
    "notes": ["Which language codes are supported: en, cy", "No code — the default language is English", "Unsupported code — error 422 with a message", "The source gives no “As…, I want…” wording and no estimate"],
    "given1": "Service sends a request to create a payment", "when1": "In the request \"language\": \"cy\"", "then1": "Payment created with Welsh language, standard response",
    "given2": "Service sends a request to create a payment", "when2": "No language property in the request", "then2": "Payment created with English language, standard response",
    "given3": "Service sends a request to create a payment", "when3": "In the request \"language\": \"cym\"", "then3": "Payment not created, 422 response and error text",
    "given4": "", "when4": "", "then4": "",
    "i": "", "n": "", "v": "", "e": "", "s": "", "t": "✓",
    "size": "Not stated in the source"
  }
}
```

Put "✓" in each INVEST key that holds and an empty string in the others; leave unused criteria rows empty. The example ticks only "t" because the source shows testable criteria and says nothing on the rest. `role`, `goal` and `benefit` take under 110 characters; each `given`, `when` and `then` under 80; `notes` up to eight items of under 70, each its own paragraph; `size` under 40; the title under 60. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/user-story.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's stories in any form and check each against the common mistakes in card.md:

1. The role is concrete, not "a user".
2. There is a "so that" with a real benefit.
3. The goal is a need, not a ready solution.
4. Acceptance criteria are concrete and cover errors and defaults.
5. The story is small enough to estimate and finish in a short time; if not, propose a split.
6. The story was discussed with the team, not handed over as a finished task.

Report findings as a numbered list: what is wrong, why it misleads the team, the concrete fix (rewrite the story or criteria). End with a verdict: "ready for development", "ready after fixes" or "needs a conversation first".
