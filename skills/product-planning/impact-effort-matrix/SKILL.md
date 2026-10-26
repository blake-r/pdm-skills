---
name: impact-effort-matrix
description: Sort ideas, features or tasks on a 2×2 Impact / Effort matrix (quick wins, major projects, fill-ins, thankless tasks) and produce a one-slide PPTX with the plotted matrix, or review an existing matrix. Use when the user needs to agree on the order of 10–30 ideas quickly and show the decision visually.
---

# Impact / Effort Matrix

The theory, quadrants, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a list of ideas, **review** when the user brings a matrix (an image, a board export or a list of ideas with their quadrants or scores).

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the list of ideas (one change per item);
- the goal or the single metric that impact is judged against;
- what is known about the likely effect of each idea: data, research, past tests;
- rough effort from the people who will do the work.

If the ideas serve different goals, say that their impact is not comparable and build one matrix per goal. If the user needs a numeric ranking with a confidence factor, suggest the `ice-scoring` skill; with audience sizes and effort in person-months, `rice-scoring`.

### 2. Agree on scales

Before scoring, write down with the user what 0, 5 and 10 mean for impact and for effort. Effort covers the whole team: design, development, testing, launch. Keep the scales for the whole list.

### 3. Score and place

For every idea, agree on impact and effort from 0 to 10 and record the reason in one short phrase. Do not invent numbers; if the user cannot justify a score, say so and mark the idea as a guess. Read the quadrant: impact above 5 and effort below 5 is a quick win; both above 5, a major project; both below 5, a fill-in; low impact and high effort, a thankless task. Scores of exactly 5 sit on a border.

### 4. Interpret

- Call out every point within one point of a border and ask what would move it.
- If there is no major project or every idea is a quick win, question the effort estimates.
- Quick wins with an unproven effect should launch as tests with a metric.
- Recommend at most one or two major projects at a time.

### 5. Show, then write

Show the result in chat first: a table of idea, impact, effort, quadrant and reason, grouped by quadrant, then the decision. Write a file only after the user confirms. Ask for the output path (default `impact-effort-<topic>.pptx` in the working directory). Save the data as JSON:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Partner Hub 'Join now' page: ideas (illustrative placement)",
    "scales": "Impact on clicks to start registration, 0-10; effort of the whole team, 0-10",
    "decision": ["Now: sticky registration button on mobile", "Test: button text 'Start registration'"],
    "rejected": "Steps description higher on the page: no growth in the test"
  },
  "charts": {
    "matrix": {
      "points": [
        {"label": "Sticky button", "x": 2, "y": 8},
        {"label": "Button text", "x": 1, "y": 4},
        {"label": "Steps higher", "x": 2, "y": 3}
      ]
    }
  }
}
```

The example uses the ideas from the Booking.com case in card.md; the source publishes no scores, so the positions are illustrative and must be said to be so in chat.

`x` is effort and `y` is impact, both from 0 to 10. Keep labels under 25 characters; the chart shows them next to the points. Labels sit to the right of their points. If two points are closer than about 0.5 on effort and 0.3 on impact, shift one of them by up to 0.3 or shorten its label so both stay readable; for effort above 8.5 keep the label under 15 characters so it does not run past the chart edge. Mention every shift in the chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/impact-effort-matrix.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's matrix in any form and check it against the common mistakes in card.md:

1. One goal behind all impact scores.
2. Scales are agreed and written down.
3. Effort covers the whole team, not development only.
4. Quadrants are read correctly from the scores.
5. The matrix is not all quick wins; major projects exist and have a plan slot.
6. Border points are discussed, not decided by their quadrant alone.
7. Quick wins with an unproven effect are planned as tests.
8. Scores come from more than one person and are fresh.

Item 8 usually cannot be judged from the matrix alone: ask the user instead of reporting a finding. Report findings as a numbered list: idea, what is wrong, why it changes the decision, the concrete fix. Show which ideas move to another quadrant after the fixes. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
