---
name: strategy-canvas
description: Compare an offering with its competitors and alternatives on the factors the industry competes on, draw their value curves on Kim and Mauborgne's Strategy Canvas, find a distinct curve by deciding what to eliminate, reduce, raise and create, and produce a one-slide PPTX with a native line chart; or review an existing strategy canvas. Use when a product is lost among similar offers and competition comes down to price, when entering a market and looking for how to stand out, or when showing a team or investors how the offer differs from alternatives.
---

# Strategy Canvas

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a product and a market, **review** when the user brings a filled canvas.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the market and the user's offering;
- two or three main competing offers, including what buyers do instead of buying anything;
- the factors the industry competes on and invests in, if the user has a list, and what buyers said about them;
- facts per offer and factor: prices, terms, speed, range, with sources.

Do not invent competitors' prices or terms. If a fact is missing, name where to find it or mark the level as an assumption to check.

### 2. Factors

List five to ten factors buyers pay for, not internal features. Add factors that no one offers yet only in step 5.

### 3. Levels

Rate every offer on every factor on one scale, 0 (none) to 5 (high), and write the fact behind each rating. Price is rated as its level: high price, high level.

### 4. Curves

Compare the curves and name where they coincide: that is where competition is fought.

### 5. New curve

Decide what to eliminate, reduce, raise and create so that the new curve differs from the others and lowers costs, not only raises them. Add created factors to the list with level 0 for current offers.

### 6. Show, then write

Show in chat first: the factor table with levels and facts, then the four actions. Write a file only after the user confirms. Ask for the output path (default `strategy-canvas-<market>.pptx` in the working directory). Save the data as JSON (the example is the Nickel case from card.md; levels are an estimate):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Nickel and French banks, 2014 · estimate",
    "factors": ["Price — annual account fee", "Accessibility — can anyone open it", "Speed — from arrival to working card"],
    "moves": ["Eliminate: overdraft, credit, cheques", "Reduce: price, client requirements", "Raise: speed of opening", "Create: opening at a tobacco kiosk"]
  },
  "charts": {
    "canvas": {
      "categories": ["Price", "Overdraft", "Cheque book", "Accessibility", "Speed", "Tobacco kiosk"],
      "series": [
        {"name": "Nickel", "values": [2, 0, 0, 5, 5, 5]},
        {"name": "French banks", "values": [5, 5, 5, 1, 1, 0]}
      ]
    }
  }
}
```

Keep the title under 45 characters. On the chart, keep at most eight categories with short names of under 15 characters, and at most three series with names of under 30. Keep `factors` to six items of under 45 characters and `moves` to four items of under 45. List the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/strategy-canvas.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's canvas in any form and check it against the common mistakes in card.md:

1. Factors are what buyers pay for, not internal features.
2. Every level has a fact behind it.
3. The new curve eliminates or reduces some factors, not only raises all of them.
4. The number of factors keeps the canvas readable.
5. The comparison includes the alternatives buyers use now, not only direct competitors.

Report findings as a numbered list: factor or curve, what is wrong, why it matters for the strategy, the concrete fix. End with a verdict: "canvas is sound", "sound after fixes" or "not enough data".
