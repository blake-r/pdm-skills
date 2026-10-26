---
name: business-model-canvas
description: Describe a company's or a new line of business's business model in the nine blocks of Osterwalder and Pigneur's Business Model Canvas - customer segments, value proposition, channels, customer relationships, revenue streams, key resources, key activities, key partners, cost structure - check the links between blocks, pick the assumptions to test first, and produce a one-slide PPTX; or review an existing canvas. Use when launching a new line of business, comparing the current business model with a new one, or looking for a new revenue stream for existing resources.
---

# Business Model Canvas

The theory, blocks, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a company, a product or an idea, **review** when the user brings a filled canvas.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the company or the new line of business and the date of the canvas;
- the customers it serves or plans to serve;
- what is already known: prices, costs, channels, partners, resources, with sources;
- whether this is the current model or a new one.

Do not invent revenues, costs or partners. Mark everything not confirmed by data as an assumption.

### 2. Right side

Fill in order: customer segments; the value proposition for each segment; channels; customer relationships; revenue streams. If segments need different propositions, suggest a canvas per segment.

### 3. Left side

Fill key resources, key activities, key partners, then the cost structure.

### 4. Links

Check that each proposition is backed by resources and activities, that each brings revenue, and that revenues can cover costs. Name every broken link.

### 5. Assumptions

List the main assumptions: demand, willingness to pay, cost of resources. Say which to test first and what result would change which block.

### 6. Show, then write

Show in chat first, block by block as they will appear on the slide, then the broken links and the assumptions. Write a file only after the user confirms. Ask for the output path (default `business-model-canvas-<company>.pptx` in the working directory). Save the data as JSON (the example is the M-Pesa case from card.md; empty blocks stay empty, as on the published canvas):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Safaricom: M-Pesa, 2007",
    "partners": [],
    "activities": [],
    "resources": ["Existing telecom network", "Subscriber base"],
    "value": ["Money transfers via phone"],
    "relationships": [],
    "channels": ["Agent network"],
    "segments": ["Mobile phone users"],
    "costs": [],
    "revenues": ["Transaction fees"]
  }
}
```

Keep the title under 45 characters. Keep `partners`, `value` and `segments` to eight items of under 40 characters; `activities`, `resources`, `relationships` and `channels` to four items of under 40; `costs` and `revenues` to four items of under 90. Leave a block as an empty list when it is not filled. List the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/business-model-canvas.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's canvas in any form and check it against the common mistakes in card.md:

1. Customer segments are specific, not "everyone".
2. The links between blocks are stated: resources and activities behind each proposition, revenue from each.
3. Assumptions are marked as assumptions, with the first one to test named.
4. The canvas is dated and matches the current model.

Report findings as a numbered list: block, what is wrong, why it matters for the business, the concrete fix. End with a verdict: "model is coherent", "coherent after fixes" or "not enough data".
