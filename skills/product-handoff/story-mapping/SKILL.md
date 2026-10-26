---
name: story-mapping
description: Build or review a story map - the product goal and whose path is mapped, the activities and their tasks left to right in the order of the path (the backbone), stories under each task ranked top to bottom by necessity, and horizontal release slices each with a target outcome, the first slice covering the whole path - and produce a one-slide PPTX; or review an existing story map or release plan. Use when a product or a large feature must be discussed as a whole, when the first version must be cut to fit a fixed deadline, or when releases must each deliver a complete path.
---

# Story Mapping

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a product, a feature or a list of stories to map, **review** when the user brings a finished map or release plan.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product goal and whose path is mapped; who took part or will take part in the session;
- what people do with the product, step by step, or the existing list of stories;
- the deadline and the team's capacity, if a release must fit them;
- for each release, the outcome the team expects and how it will be seen.

Do not invent steps, stories, estimates or outcomes. If there are only one or two small changes, say that a map is overkill: rank the changes and map each one small. Work that is not about what people do (a database move, a rebrand) goes outside the map; say so.

### 2. Map

- **Activities:** up to five big things people do, as verbs, left to right in the order of the path. **Tasks:** the steps of each activity in the same order. Do not rank activities against each other: all are needed; ranking happens among the stories under them.
- **Stories:** under each task, from what the path cannot work without (top) to improvements (bottom). If the user only has a list, place each item under its step and flag items that fit no step.

### 3. Slice releases

- Draw the first line so that release 1 covers the whole path with the minimum under every step; flag any column left empty in release 1.
- Name the outcome of every release: what changes for people and which number shows it.
- If an estimate exceeds capacity, shrink release 1 or make stories thinner rather than dropping a whole step. Check that no release depends on stories from a later one.
- Say that the map is built with the team and stakeholders, not by one person, and is updated as stories move.

### 4. Show, then write

Show in chat first: the backbone, the releases with their outcomes and the gaps. Write a file only after the user confirms. Ask for the output path (default `story-map-<topic>.pptx` in the working directory). Save the data as JSON. The JSON below shows the format only: its values are the Allegro case from card.md, not data for this map; use them only when the user explicitly asks to see an example. The source names the activities and splits only "calculating the cost" into stories, so the other cells there are gaps, not invented content:

```json
{
  "text": {
    "title": "Allegro: parcel shipping platform, 2014",
    "act1": "Create a shipment order", "act2": "Calculate the cost", "act3": "Track the order", "act4": "Personal account", "act5": "Get invoices",
    "task1": "Steps are not given in the source", "task2": "", "task3": "", "task4": "", "task5": "",
    "r1_goal": ["The whole path at minimum; shipped in June, on time", "120 SP at capacity ~80 — scope cut"],
    "r2_goal": "“Nice to have”: for product completeness",
    "r3_goal": "Long-term plans",
    "s1_1": "", "s1_2": ["Split into stories: fixed and dynamic price list", "Standard and additional services", "Price ranges, discount codes", "Which made it into release 1 — not stated"], "s1_3": "", "s1_4": "", "s1_5": "",
    "s2_1": "", "s2_2": "", "s2_3": "", "s2_4": "", "s2_5": "",
    "s3_1": "", "s3_2": "", "s3_3": "", "s3_4": "", "s3_5": ""
  }
}
```

The keys are `act1`–`act5` and `task1`–`task5` for the five columns, `r1_goal`–`r3_goal` for the three releases and `s<release>_<column>` for the stories; leave unused cells as empty strings; write a used cell with no source fact as "N/A". `act` takes under 40 characters; `task` up to two items of under 50; each `s` cell up to four items of under 50; each `r_goal` up to two items of under 45; the title under 60; each list item becomes its own paragraph. With more than five activities, merge the smallest or make a second slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/story-mapping.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's map or release plan in any form and check it against the common mistakes in card.md:

1. The map was built with the team and stakeholders, not by one person.
2. The top row holds what people do, not system modules or technical work.
3. Ranking happens among stories, not among activities.
4. Release 1 covers the whole path, with no empty step.
5. Every release has a named outcome and a way to see it.
6. The map is kept up to date and postponed stories stay visible on it.

Report findings as a numbered list: what is wrong, why it misleads the plan, the concrete fix. End with a verdict: "map supports the release plan", "supports it after fixes" or "not enough data".
