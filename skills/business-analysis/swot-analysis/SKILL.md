---
name: swot-analysis
description: Assess a company, product or option through strengths, weaknesses, opportunities and threats, then cross internal and external factors into SO, ST, WO and WT strategies (the TOWS matrix), pick the strategies to act on, and produce a one-slide PPTX; or review an existing SWOT. Use before a strategic decision - entering a market, launching a line of business, choosing between options - or when a team needs to agree on what is strong and what holds it back.
---

# SWOT Analysis

The theory, limits and a worked case are in [card.md](card.md); the factor variants for both lists are in [factors.md](factors.md). Read both before either mode and do not contradict them. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a company, product or decision, **review** when the user brings a filled SWOT.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- what is assessed and for which decision, and the date;
- the competitors to compare against;
- market data: size, growth, regulation, trends, with sources;
- internal data: metrics, costs, capabilities, known problems.

Do not invent market facts or competitor data. A factor without a source is marked as an assumption.

### 2. Factors

Sort each factor: internal and under the company's control goes to S or W, external goes to O or T. A growing market is an opportunity, not a strength. Strengths and weaknesses are stated against competitors. A factor sits on one list only, and its verdict comes from the comparison, not from the factor.

Offer the variants from factors.md and let the user pick; if the user has a list, use it. The catalog is too long for one question, so ask through AskUserQuestion in two rounds. First, which groups matter (internal: product, customers and sales, finance, technology, people and organization, brand, operations; external: market and customers, competitors, regulation and politics, economy, technology, society). Then the factors inside the chosen groups, as a multiple choice, with the proposed set first and marked "(Recommended)". Without AskUserQuestion, offer the same two steps in one message.

### 3. Rank

Keep three to five main factors per quadrant, most important first. List the dropped ones in chat.

### 4. Strategies

For each crossing SO, ST, WO, WT, write one to three strategies, each naming the pair of factors it rests on. Then pick the strategies to act on: what is feasible and gives most, with an owner and a date.

### 5. Show, then write

Show in chat first: the four quadrants, then the strategies per crossing, then the chosen ones. Write a file only after the user confirms. Ask for the output path (default `swot-<company>.pptx` in the working directory). Save the data as JSON (the example is the Ozon case from card.md; the prospectus names no weakness-based strategies, so those cells stay empty):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Ozon, IPO, November 2020",
    "opportunities": ["Online share 6.0% in 2019, expected 8.1% in 2020", "The pandemic accelerated the shift to online"],
    "threats": ["Wildberries, Beru and other players"],
    "strengths": ["Marketplace — 45% of GMV for 9 months of 2020", "18.1 thousand sellers, >85% of the assortment"],
    "weaknesses": ["Loss of RUB 19.4 bn for 2019"],
    "so": ["Expand the assortment and categories through the marketplace", "Build logistics with a focus on the regions", "Develop advertising and services around retail"],
    "st": [],
    "wo": [],
    "wt": []
  }
}
```

Keep the title under 35 characters. Keep `opportunities` and `threats` to four items of under 60 characters, `strengths` and `weaknesses` to five items of under 40, and each strategy cell to three items of under 100. Leave a cell as an empty list when it is not filled. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/swot-analysis.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's SWOT in any form and check it against the common mistakes in card.md:

1. Strategies are formulated on the crossings, not just four lists.
2. Each factor sits on the right list: no outside factor among strengths or weaknesses, no inside factor among opportunities or threats.
3. The internal-external split holds: no factor stands on both lists.
4. No verdict is fixed to a factor: the same factor is judged anew for each company, not copied from a generic list.
5. Strengths and weaknesses are stated against competitors.
6. Each quadrant is ranked to three to five main factors.
7. Opportunities and threats have sources.

Report findings as a numbered list: quadrant or strategy, what is wrong, why it matters for the decision, the concrete fix. End with a verdict: "ready for the decision", "ready after fixes" or "not enough data".
