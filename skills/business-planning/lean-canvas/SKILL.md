---
name: lean-canvas
description: Sketch a new product or startup idea on Ash Maurya's Lean Canvas - customer segments and early adopters, top problems and existing alternatives, unique value proposition and high-level concept, solution, channels, revenue streams, cost structure, key metrics, unfair advantage - pick the riskiest assumption to test first, and produce a one-slide PPTX; or review an existing Lean Canvas. Use when an idea is new and mostly assumptions, when comparing variants of an idea, or when explaining an idea to a team or investors on one page.
---

# Lean Canvas

The theory, blocks, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings an idea or a product, **review** when the user brings a filled canvas.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the idea or product, the date and the canvas version;
- who the customers are and who has the problem most acutely;
- what is already known from customers: interviews, sales, usage, with sources;
- prices, costs and channels already tried.

Do not invent customer evidence, prices or advantages. Everything not backed by data is an assumption: say so.

### 2. Customers and problem

Fill customer segments and early adopters, then the top one to three problems and the existing alternatives, as the customers solve them today.

### 3. The rest in order

Fill the unique value proposition from the top problem, then a high-level concept ("X for Y"), solution (one per problem), channels, revenue streams, cost structure, key metrics, and the unfair advantage last. Leave a block empty when nothing is known; never fill the unfair advantage with passion, the team or features.

### 4. Riskiest assumption

Name the assumption whose failure breaks the rest of the model, and the cheapest way to test it with customers. Say which block changes depending on the result.

### 5. Show, then write

Show in chat first, block by block as they will appear on the slide, then the riskiest assumption and how to test it. Write a file only after the user confirms. Ask for the output path (default `lean-canvas-<product>.pptx` in the working directory). Save the data as JSON (the example is the TodayLaunch case from card.md; the blocks the post does not state stay empty):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "TodayLaunch, spring 2012",
    "problem": ["Running social media for a business is hard", "The tools are confusing and do not teach"],
    "alternatives": ["HootSuite and similar services"],
    "solution": [],
    "metrics": ["They use the product as intended", "Would be upset if the service shut down"],
    "uvp": ["One social media inbox, as simple as email"],
    "concept": ["Mailbox for social media"],
    "advantage": [],
    "channels": ["Meetings with local businesses", "Live training courses"],
    "segments": ["Small firms running their own social media"],
    "early_adopters": ["Those who do not choose the best-known tool"],
    "costs": [],
    "revenues": ["Paid access"]
  }
}
```

Keep the title under 35 characters. Keep `problem`, `segments` and `uvp` to three items of under 45 characters; `solution`, `metrics`, `advantage` and `channels` to three items of under 40; `alternatives`, `concept` and `early_adopters` to two items of under 45; `costs` and `revenues` to three items of under 90. Leave a block as an empty list when it is not filled. List the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/lean-canvas.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's canvas in any form and check it against the common mistakes in card.md:

1. The canvas starts from customers and their problem, not from the solution.
2. Early adopters are named, not "everyone".
3. The unfair advantage is real or left empty, not passion, the team or features.
4. The canvas is dated, versioned and updated after customer conversations.
5. The riskiest assumption is named and is tested first.

Report findings as a numbered list: block, what is wrong, why it matters for the idea, the concrete fix. End with a verdict: "canvas is ready to test", "ready after fixes" or "not enough data".
