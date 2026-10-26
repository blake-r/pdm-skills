---
name: empathy-map
description: Build an empathy map on Dave Gray's canvas - the goal (who we study and what they need to do), the observable sectors (what the person sees, says, does, hears) and the head in the middle (what they think and feel, their pains and gains) - from interviews and observations, name the product decision it feeds, and produce a one-slide PPTX; or review an existing empathy map. Use after user interviews or observations, when the team pictures the user differently, or before ideation so that ideas answer real pains.
---

# Empathy Map

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings research material, **review** when the user brings a finished map.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the person to map (one role or type) and their situation;
- what they need to do: the task, the decision, how they will know they succeeded;
- the material: interview notes or transcripts, observations, support tickets, reviews, with how many people and when;
- the product decision the map should feed.

Do not invent quotes, behaviour or feelings. If there is no material, say the map would record the team's guesses, offer an interview plan (whom, how many, which questions per sector) and stop.

### 2. Fill the observable sectors

Go clockwise as on the canvas: sees, says, does, hears. One point per item, with a verbatim quote or an observed action and its source. Mark where the person says one thing and does another.

### 3. Fill the head

Write what the person thinks and feels, the pains (fears, frustrations) and the gains (wants, hopes). Tie each item to something in the outer sectors; drop items that rest on nothing.

### 4. Decide, show, then write

Pick the pains the product will address and how the choice will be checked. Show in chat first: the goal, the sectors with sources, the head, the contradictions, the decision. Write a file only after the user confirms. Ask for the output path (default `empathy-map-<persona>.pptx` in the working directory). Save the data as JSON (the example is the Light Bank case from card.md; sectors the source does not retell are marked so, not filled in):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Light Bank, UXDA concept: future clients of a mobile bank",
    "who": ["Student, sales manager, entrepreneur", "Follow trends, value beauty"],
    "need_to_do": "Not retold in the source",
    "see": "Not retold in the source",
    "say": "Not retold in the source",
    "do": "Not retold in the source",
    "hear": "Friends recommend neobanks",
    "pains": "Hard to make sense of outdated bank design",
    "gains": "Not retold in the source",
    "think_feel": "Want to use neobanks",
    "decision": ["Design must be emotionally engaging", "Delightful and easy to use", "Innovative"],
    "result": ["iF and Red Dot 2019 shortlists", "Concept: no clients or metrics"]
  }
}
```

A value may be a string or a list; each list item becomes its own paragraph. Keep `pains`, `gains` and `think_feel` to three items of under 40 characters (they sit inside the head), the outer sectors to four items of under 50 characters, `decision` and `result` to five items of under 45 characters. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/empathy-map.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's map in any form and check it against the common mistakes in card.md:

1. The map rests on interviews or observations, with sources, not on the team's memory.
2. The outer sectors were filled before the head, and each item in the head ties to something observed.
3. One role or type per map.
4. The goal (who and what they need to do) is stated.
5. A product decision refers to the map.

Report findings as a numbered list: what is wrong, why it misleads the decision, the concrete fix. End with a verdict: "map supports the decision", "supports it after fixes" or "not enough data".
