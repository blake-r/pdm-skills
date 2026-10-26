---
name: competitor-analysis-template
description: Build or check a competitor profile using the PAF competitor analysis template — business model, market size, product, pricing and sales, users, value proposition, functionality, key screens and customer reviews, each value with a source, a date and a confidence mark — and save it as a spreadsheet, or review an existing competitor analysis. Use when the user is entering a market, launching a feature, revising prices or positioning and needs to describe a competitor, or asks why a competitor table is useless.
---

# Competitor Analysis Template

The theory, limits and the example are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user needs a competitor profiled, **review** when the user brings a ready analysis or table to check.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the decision the analysis serves: enter a niche, set a price, choose how to differ;
- our product in a few lines, to compare against;
- the competitor and its type: direct (same problem, same way), indirect (same problem, other way), displacer (fights for the customer's money or time) or channel competitor (fights for access to customers);
- sources the user already has: links, screenshots, interviews, reports, reviews;
- which blocks to drop or add for this market.

If the competitors are not named yet, say that the card needs them first and ask who they are; do not guess. If the user has no sources, say what can be found openly (site, tariffs, app stores, review sites, filings, trial use) and offer to work only from what the user pastes. Do not invent figures: a fact needs a source and a date.

### 2. Fill the profile by blocks

Go through the blocks of the card: business model, market size, contacts, product, competition, pricing and sales (with the five stages of the customer path: acquisition, activation, revenue, retention, referral), users, offer (value proposition, functionality, key screens), reviews. For each parameter write the data, the source with a date, and a confidence mark: `fact` (confirmed by the source), `estimate` (your own, with the reasoning in the data), `no data` (nothing found). Leave a parameter empty if nothing is known. Revenue growth, market share and audience of private companies are usually closed: mark them as an estimate or no data.

### 3. Conclusion

Answer in three lines: where the competitor is strong; where it is weak and whether its customers complain about it; what it does not look at. Then say where our place is and which decision follows. Offer a review date.

### 4. Show, then write

Show the profile in chat first as a table: block, parameter, data, source and date, confidence; then the conclusion and the counts of gaps. Write a file only after the user confirms. Ask for the output path (default `competitor-<name>.xlsx` in the working directory). Save the data as JSON. The example is the Evstratov case from card.md; the source gives no names, values or decision, so those say so and everything else is left out:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "online grocery store (Products Moscow meetup, 2017)",
    "decision": "Perception map: how buyers perceive stores, where competitors are concentrated, where competition is lower; the decision is not stated in the source",
    "kind": "Competitors of an online grocery store; types are not named in the source",
    "conclusion": "Not given in the source"
  },
  "cells": {
    "C44": "Store is passive (only informs) or interactive (collects data, speeds up choice): values for competitors are not given in the source",
    "D44": "Evstratov, Habr, 26.04.2017",
    "E44": "no data",
    "C46": "Number of screens before the \"Pay for order\" button in trial orders; values are not given in the source",
    "D46": "Evstratov, Habr, 26.04.2017",
    "E46": "no data"
  },
  "rows": []
}
```

Values go into columns C, D, E (data, source and date, confidence) of the parameter rows that the template already lists. Write them either in `cells` by address, as above, or as `rows` from the first parameter row (a row is `[data, source, confidence]`, `null` for an unknown value; every parameter row must have an entry, in template order). Use `null`, not an empty string. Confidence takes only `fact`, `estimate` or `no data`: the totals count them. The 44 parameter rows run from row 7 to row 50 (business model 7–15, market size 16–23, contacts 24–27, product 28–32, competition 33–35, pricing and sales 36–42, users 43, offer 44–47, reviews 48–50). To drop a block, delete its rows after filling.

Length limits that fit the template: `title` up to 100 characters; `decision`, `kind`, `conclusion` up to 200 each; data up to 300 characters per cell; source and date up to 120. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/competitor-analysis-template.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints. The totals block counts parameters, filled ones, filled without a source (must be 0), estimates, gaps, and filled without a confidence mark (must be 0).

## Mode: review

Take the user's competitor analysis in any form (a table, a document, notes) and check it against the common mistakes in card.md:

1. Only functions are compared; prices, sales process, channels and reviews are missing, so the reasons for the competitor's success are not visible.
2. Data have no source and no date, so it is impossible to check what is outdated.
3. Unavailable figures are invented: market share, revenue growth, audience with no stated method.
4. The competitor's strengths are copied, instead of looking for what it does badly or does not do.
5. Only direct competitors are taken; displacers, indirect competitors and channel competitors are missing.
6. The analysis is done once and has no review date; tariffs, functions and ratings may be outdated.

Also check that the decision the analysis serves is stated, that site claims are checked against reviews or trial use, and that reviews are counted by repetition, not by single vivid ones. Items 2, 3 and 6 can often be seen from the document; ask the user instead of reporting a finding when the material alone cannot show it (where a figure comes from, when it was collected). Report findings as a numbered list: the block and parameter, what is wrong, why it matters, the concrete fix. End with a verdict: "profile is ready", "ready after fixes" or "collect data again".

Worked example. The user brings a table: columns "Features" and "Price" for three direct competitors, no dates, a "Market share" row with round numbers and no source. Findings: 1 — only features and price; add the sales process, channels and reviews; 2 — no source or date, add both for each value; 3 — the market share has no method, mark it as an estimate with the reasoning or `no data`; 5 — all three are direct, add an indirect one and a displacer. Item 6: ask when the table was collected. Verdict: "ready after fixes".
