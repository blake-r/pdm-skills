---
name: adl-matrix
description: Choose a strategy for a business unit or product line with the ADL matrix (Arthur D. Little) - industry life-cycle stage (embryonic, growth, mature, aging) crossed with competitive position (dominant, strong, favorable, acceptable/tenable, weak; Wiley adds non-viable: exit at once) - and produce a one-slide matrix, or review an existing ADL analysis. Use when the user must decide whether to grow, defend, narrow to a niche, harvest or exit a business, or mentions ADL, Arthur D. Little, life cycle and competitive position.
---

# ADL Matrix

The theory, the scales and a case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants to place a business on the matrix and choose a direction, **review** when the user shows a finished analysis.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the business unit: products, customers, main competitors, price level; whether it could be sold and survive on its own;
- the industry: growth rate, growth potential, breadth of product lines, number of competitors, stability of market shares, buying patterns, ease of entry, technology;
- the unit's position: relative share, a unique advantage, a niche, dedicated resources or channels, distinctive competence;
- the decision: what the user wants to choose (invest, defend, narrow, harvest, exit).

Do not invent numbers: mark what the user did not give as unknown. If the user wants one answer for the whole company, ask to split it into business units first.

### 2. Stage and position

Judge the industry stage (embryonic, growth, mature, aging) from the eight factors and name the factors that disagree. Judge the position (dominant, strong, favorable, acceptable/tenable, weak; Wiley adds non-viable: exit at once) from qualitative evidence, one fact per rating. Say that both ratings are expert judgments.

### 3. Cell and direction

Name the cell, the family of actions (natural development, selective development, profit viability, withdrawal) and a concrete thrust (start up, keep share, content with the position, gain position gradually or aggressively, defend, harvest, exit). Give the main risk and a date to revisit the ratings.

### 4. Show, then write

Show the result in chat first as a table by template blocks: title, filled cells, business cell, stage basis, position basis, decision, risk. Write a file only after the user confirms. Ask for the output path (default `adl-matrix-<unit>.pptx`). Save the data as JSON; the example is the Amazon retelling from card.md, and fields the source does not give say so. Empty cells are null or omitted:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Amazon (e-commerce), per Think Insights, 2022",
    "c11": "Investment in platform R&D and brand",
    "c22": ["New product categories", "Expansion of the logistics network"],
    "c12": null,
    "cell": "Growth · Strong (per the source text)",
    "stage_basis": "the source does not list the factors",
    "position_basis": "the source does not give shares or advantages",
    "decision": ["Maturity: innovation (cloud, streaming) and acquisitions (Whole Foods)", "The position and decision date are not given in the source"],
    "risk": ["Stages follow the company's path", "Industry maturity: no evidence"]
  }
}
```

Limits that fit the slide: title under 60 characters; each of the 20 cells (c11 to c54: row = position from dominant to weak, column = stage from embryonic to aging) up to two lines under 35 characters; cell under 70; stage_basis and position_basis up to three lines under 45; decision up to four lines under 45; risk up to three lines under 35. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/adl-matrix.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Check the user's analysis against the common mistakes in card.md:

1. The company is rated as a whole, not a business unit.
2. The industry stage is confused with the stage of the company.
3. The position is overrated: "strong" or "dominant" has no evidence of an advantage.
4. The strategy is copied from a template cell word for word, with no check of resources.
5. The life cycle is treated as inevitable: a possible rejuvenation of the industry after a technology shift is ignored.
6. The ratings are never revisited.

Items 3 and 5 usually cannot be judged from the text alone: ask for the evidence behind the position and for signs of a technology shift instead of reporting a finding. Also check that stage factors are named, that the family of actions is stated and that a risk and a revisit date exist. Report findings as a numbered list: what is wrong, why it changes the decision, the concrete fix. End with a verdict: "direction is justified", "works after changes" or "ratings need evidence first".

Example: "The whole group is mature and strong, so we defend", with three unrelated businesses. Findings: item 1 - rate each business unit separately; item 3 - ask for the evidence of "strong"; item 6 - add a revisit date. Verdict: "ratings need evidence first".
