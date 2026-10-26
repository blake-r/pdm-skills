---
name: lean-ux-canvas
description: Turn a feature request or a vague goal into a business problem, measurable outcomes, users and their benefits, solution ideas, hypotheses, the riskiest assumption and the smallest experiment to test it, using Jeff Gothelf's Lean UX Canvas (v2), and produce a one-slide PPTX; or review an existing Lean UX Canvas or hypothesis backlog of a team. Use at the start of an initiative, when a team is handed a ready-made solution, when it must agree what to test first, or after an experiment to refill the canvas for the next iteration.
---

# Lean UX Canvas

The theory, boxes, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings an initiative, a feature request or a goal, **review** when the user brings a filled canvas or a set of hypotheses.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the initiative and who asked for it;
- the business problem behind it and the metric that shows it;
- who the users and customers are, and what is known about their behaviour, with sources;
- the iteration number and what previous experiments showed, if any.

Do not invent metrics, research findings or experiment results. Everything on the canvas is an assumption until tested: say so.

### 2. Boxes 1-4

Fill in order: the business problem; the business outcomes as changes in what people do, with a metric; the users to focus on first; their benefits and the behaviour change that shows they got them. If the user starts with a solution, ask which problem it solves before going on.

### 3. Box 5

List solution ideas without choosing yet, including the one the user came with.

### 4. Box 6

Combine boxes 2-5 into hypotheses: "We believe that [business outcome] will be achieved if [user] attains [benefit] with [feature]". One feature per hypothesis.

### 5. Boxes 7-8

For the most important hypothesis, name its riskiest assumption - early on, a risk to value, not to feasibility. Design the smallest experiment that shows whether it holds: what to do, with whom, for how long, and which result confirms or refutes it.

### 6. Show, then write

Show in chat first, box by box as they will appear on the slide. Write a file only after the user confirms. Ask for the output path (default `lean-ux-canvas-<initiative>.pptx` in the working directory). Save the data as JSON (the example is the Etsy case from card.md):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Etsy: photo as the first step · iteration 1",
    "problem": ["Not named in the source", "Changes should help sales or simplify the tools"],
    "outcomes": ["Sellers finish listings faster", "Sellers create more listings"],
    "users": ["Sellers who create listings"],
    "benefits": ["Time saved", "Sellers check against the photo while writing the description"],
    "solutions": ["Uploading a photo is the first step"],
    "hypotheses": ["Photo as the first step will save sellers time"],
    "riskiest": ["The result comes precisely from moving the photo"],
    "experiment": ["Several days, three groups of sellers", "25%: photo at the top, 25%: at the bottom", "50%: in the middle, as before"]
  }
}
```

Keep the title under 45 characters. Keep `problem`, `outcomes`, `users` and `benefits` to four items, `solutions` to eight, `hypotheses` and `experiment` to three, `riskiest` to two; every item under 60 characters, in `solutions` and `riskiest` under 40, in `hypotheses` under 110. List the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/lean-ux-canvas.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's canvas or hypotheses in any form and check them against the common mistakes in card.md:

1. Boxes 1 and 2 are filled before box 5, and the business outcome has a metric.
2. Each hypothesis follows the formula and holds one feature.
3. The riskiest assumption concerns value, not only feasibility, at an early stage.
4. The experiment is the smallest one that confirms or refutes that assumption, with a result that decides.
5. After an experiment, the canvas is refilled with the next iteration number.

Item 5 usually cannot be judged from one canvas: ask the user instead of reporting a finding. Report findings as a numbered list: box, what is wrong, why it matters for what the team will learn, the concrete fix. End with a verdict: "ready to test", "ready after fixes" or "not enough data".
