---
name: ge-mckinsey-matrix
description: Place business units, product lines or candidate markets on the GE-McKinsey nine-box matrix - industry attractiveness against the unit's competitive strength, each axis a weighted score over factors the user picks and rates - read the zone (invest and grow, selective, harvest or divest), decide where the money goes, and produce a one-slide PPTX; or review an existing GE-McKinsey or nine-box analysis. Use when a company with several businesses decides where to invest, which to run for cash and which to sell, when markets are compared before entry, or when the user mentions the GE matrix, McKinsey matrix, nine-box or business screen.
---

# GE–McKinsey Matrix

The theory, limits and a worked case are in [card.md](card.md); the factor variants for both axes are in [factors.md](factors.md). Read both before either mode and do not contradict them. Reply in the user's language.

Pick the mode from the request: **do** when the user brings units and wants them placed, **review** when the user brings a finished matrix or scoring table.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the units, each able to be sold and survive alone, and the decision at stake (invest, run for cash, sell, or enter a market), with the horizon;
- the factors for each axis: offer the variants from factors.md and let the user pick; if the user has a list, use it. Hold to 10 or fewer per axis;
- the weights, which the user sets (percent, 100 per axis) from their own expertise, and the rating scale (1 to 5 or 0 to 10);
- the ratings per unit and factor, with the basis of each (a fact, or a judgment).

Do not invent ratings or market numbers. Hard market data is not required: weights and ratings are the method. A rating the user cannot give stays "N/A", and the unit is not placed until it is given.

### 2. Check the factors

Before computing, check that: attractiveness factors describe the market, not the company, and strength factors describe the unit against its rivals; no factor stands on both axes (for example, the company's own share belongs to strength only); overlapping factors are merged; every scale points one way, with high = better for the unit ("few competitors" and "low external risk" score high); the weights on each axis sum to 100.

### 3. Compute and place

Per axis, sum weight times rating for each unit. Ask the user to fix the cut-offs for low, medium and high before showing results; if the user has none, propose thirds of the scale (on 1 to 5: 2.33 and 3.67), or rounding the total to a whole number with bands on 0 to 10 of 0-3 low, 4-7 medium, 8-10 high, and say that these are conventions. Place each unit and name its zone: invest and grow (high-high and the two cells beside it), selective (the diagonal), harvest or divest (the rest). Test the weights: shift each by a few points and say which placements change zone.

### 4. Decision

Give a posture and a next step per unit, tied to money and a date to revisit. Say that the grid ignores price, synergies and how much to invest, and name those that matter for the decision.

### 5. Show, then write

Show in chat first: the two scoring tables per unit (factor, weight, rating, result, sum), the placement, the decision. Write a file only after the user confirms. Ask for the output path (default `ge-mckinsey-matrix-<company>.pptx`). Save the data as JSON; the example is the eBay case from card.md, where the scoring is ours:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "eBay, three reportable segments, end of 2019 (our scoring)",
    "mh": "Marketplace: 3.15 / 3.80",
    "mm": "Classifieds: 3.40 / 3.55",
    "lm": "StubHub: 2.25 / 2.65",
    "attr": ["Size 20%, growth 25%, few rivals 25%, entry barriers 15%, low external risk 15%", "Scores: Marketplace 3.15, Classifieds 3.40, StubHub 2.25"],
    "strength": ["Share 30%, brand 15%, margin 20%, momentum 20%, fit with the rest 15%", "Scores: Marketplace 3.80, Classifieds 3.55, StubHub 2.65"],
    "scale": "Ratings 1 to 5, high = better for the unit. Cut-offs fixed before scoring: 2.33 and 3.67",
    "decision": ["Marketplace: invest, it is the core", "StubHub: sold to viagogo, $4.05 bn, Feb 2020", "Classifieds: sold to Adevinta, about $9.2 bn, June 2021"],
    "risk": ["Ratings are ours; eBay did not use the matrix", "The grid ignores price and the buyer's synergies"]
  }
}
```

Cells are named by attractiveness then strength: `hh` is high-high, `ml` is medium attractiveness and low strength, and so on, nine in all (`hl hm hh ml mm mh ll lm lh`). Leave a cell empty (null or omitted) when no unit is in it. Limits that fit the slide: title under 60 characters; each cell up to three lines under 30 characters, in the form "unit: attractiveness / strength"; attr and strength up to three lines under 75 characters; scale up to two lines under 80; decision up to four lines under 70; risk up to three lines under 60. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/ge-mckinsey-matrix.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

### When called from pdm-brief

Run steps 1 to 5 of do mode with the PM through AskUserQuestion; the factors, weights and ratings are the PM's, and you only propose.

- **Factors.** The catalog in factors.md is too long for one question, so ask in two rounds. First, which groups matter for the units (market, trends and risks, customers, technology and regulation; for strength, group the list by theme). Then the factors inside the chosen groups, as a multiple choice of 5 to 7 per axis, with the proposed set first and marked "(Recommended)". Hold the 10-per-axis limit and merge overlaps.
- **Weights.** The PM sets them or accepts a proposal; the sum is 100 on each axis.
- **Ratings.** The PM gives them, each marked as a fact or a judgment. Every judgment goes on the assumptions slide.
- **Weight test.** After placement, shift each weight by a few points; if a unit changes zone, make this the weakest point named in the roast.
- **No AskUserQuestion.** Weights and ratings are assumptions: mark all of them as "not confirmed by the PM" on the assumptions slide, and write on the conclusions slide that the zone is not confirmed.

## Mode: review

Take the user's analysis in any form and check it against the common mistakes in card.md:

1. Units are separate sellable businesses, not one cell for the whole company.
2. No factor stands on both axes (own share and brand on the strength axis only).
3. Each axis has 10 factors or fewer, and none overlap.
4. The weights were set before the units were scored, and the user can say why the top factors weigh most.
5. Attractiveness is more than growth: margins, capital needs, buyer power or competition appear too.
6. All scales point one way, high = better for the unit.
7. Every rating has a stated basis, a fact or a judgment.
8. The cell is not read as a verdict: price, synergies and how much to invest are named.
9. A revisit date exists.

Also check that the weights sum to 100 on each axis, that the cut-offs were fixed before the results, and that the weight test was run. Item 4 cannot be judged from the table alone: ask when the weights were set. Report findings as a numbered list: what is wrong, why it changes the decision, the concrete fix. End with a verdict: "placement supports the decision", "works after fixes" or "ratings need a basis first".

Example: "Our share is 40%" in the attractiveness table and "brand" in strength, weights summing to 110, one cell for the whole group. Findings: item 2 - move the share to strength; item 1 - split by business unit; the weights must sum to 100. Verdict: "works after fixes".
