---
name: bcg-matrix
description: Place a company's products, markets or business units on the BCG growth-share matrix - market growth against relative market share, circle size by revenue - sort them into stars, cash cows, question marks and dogs, decide what to fund, hold, harvest or exit, check that the cash cows can pay for the choices, and produce a one-slide PPTX with the bubble chart; compare your products with competitors' products in one market on the same grid to see where to attack and defend; or review an existing BCG matrix. Use when a company with several products or markets decides where to invest and what to exit, when one business funds the others, or when a team wants to see its products against competitors in one market.
---

# BCG Matrix

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a company and its units, **compare** when the user brings one market with their products and competitors' products, **review** when the user brings a filled matrix.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the company, the units (products, countries, segments) and the year;
- for each unit: its market, the market's growth rate, the unit's market share and the largest competitor's share, and revenue, with sources;
- the growth threshold, if the user has one (default 10% a year);
- how much cash each unit makes or burns.

Do not invent shares or growth rates. If a unit has no data, place it only if the user accepts a stated estimate, and say in `scales` that the position is an estimate.

### 2. Markets and positions

Define each unit's market explicitly. Compute relative share as the unit's share divided by the largest competitor's share (for the leader, divided by the second-largest). Place each unit: share on the horizontal axis, growth on the vertical, circle size by revenue.

### 3. Decisions

Per quadrant: stars — hold and invest; cash cows — take cash, do not grow share; question marks — pick the few to fund to leadership, exit the rest; dogs — sell or close. Then check the balance: can the cows' cash pay for the chosen stars and question marks, and how fast is the cows' market slowing.

### 4. Show, then write

Show in chat first: a table of units (market, growth, relative share, revenue, quadrant), then the decisions and the cash flow. Write a file only after the user confirms. Ask for the output path (default `bcg-matrix-<company>.pptx` in the working directory). Save the data as JSON (the example is the Sea Limited case from card.md; Sea does not publish market shares or market growth by unit, so the positions are estimates by quadrant and the circles are equal):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Sea Limited, end of 2021",
    "scales": ["Placement is conditional: Sea does not publish market shares or growth by segment", "Quadrants are our estimate based on reports"],
    "decision": ["Shopee in Asia: hold", "Shopee's new markets: exit France, Latin America except Brazil, Poland", "SeaMoney: fund", "Garena: take cash"],
    "cash": ["Garena: EBITDA $2.8 bn for 2021", "Shopee: −$2.6 bn; positive in Q4 2022"]
  },
  "charts": {
    "matrix": {
      "points": [
        {"label": "Garena", "x": 2.5, "y": 0},
        {"label": "Shopee, Asia", "x": 2.5, "y": 20},
        {"label": "Shopee, new markets", "x": 0.25, "y": 20},
        {"label": "SeaMoney", "x": 0.5, "y": 24}
      ]
    }
  }
}
```

`x` is relative share (0.1 to 10, logarithmic axis, high share on the left as in BCG's original; the script mirrors it, pass the share as is, values outside the range are drawn at the edge), `y` is market growth in percent (-10 to 30). Add `"size"` to each point (for example revenue in one currency) to scale the circles; the circle area is then proportional to it. The share axis is fixed. If growth falls outside the vertical axis, pass `"value_axis"` with `minimum` and `maximum`, and move the borders with `"lines"` in the same units as the points: `{"Share border": [[1, ymin], [1, ymax]], "Growth border": [[0.1, g], [10, g]]}` where `g` is the growth threshold. The `lines` keys are the series names of the template chart and must match them exactly: `Share border` and `Growth border`. The quadrant names `Stars`, `Question marks`, `Cash cows` and `Dogs` are also keys in `lines`, one point each (stars at share above 1, question marks below). Keep the title under 35 characters, `scales` and `cash` to three items of under 80 characters, `decision` to four items of under 80. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/bcg-matrix.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: compare

Use it for one market only. Ask in one message for: the market and the year; the players and their main products in it; for each product, its share of the market and the leader's share, and its revenue measure; the market's growth rate. Competitors rarely publish these numbers: mark each one as "published", "estimate" or "unknown", and do not place a product whose share is unknown without the user accepting an estimate.

Compute relative share against the market leader (for the leader, against the second). Place every product on the grid. Show in chat first: a table (product, owner, growth, relative share, revenue measure, quadrant, source or estimate), then the three attack and defense moves: which competitor star to hold against, which own question mark to fund against which competitor cash cow, which own dog to give up. Do not draw a cash plan: the matrix does not show competitors' cash. Write the slide only after the user confirms, the same way as in mode do. Use the same template and `fill_pptx.py` call; in `scales` name the revenue measure and state which values are estimates; keep the owner in the point `label`, for example "Our product · Competitor X".

## Mode: review

Take the user's matrix in any form and check it against the common mistakes in card.md:

1. Each unit's market is defined, and not drawn narrow to make the unit a leader.
2. Share is relative to the largest competitor, not absolute.
3. Dogs are not kept for accounting profit.
4. Money goes to a few chosen question marks, not a little to each.
5. The cash cows' future is checked: how fast their market slows.

Report findings as a numbered list: unit, what is wrong, why it matters for the investment decision, the concrete fix. End with a verdict: "portfolio decisions are sound", "sound after fixes" or "not enough data".
