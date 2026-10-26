---
name: segment-scoring
description: Score customer segments on several criteria - by default segment size, ability to pay, pain and accessibility on a 1-3 scale - combine the scores as a product or a weighted sum, pick the segment to focus on and check the leader for weak spots, and produce an XLSX that computes the score and rank; or review an existing segment scoring. Use when choosing the first segment for a new product or market entry, when splitting sales and marketing effort between segments, or when a team argues about which segment matters most.
---

# Segment Scoring

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a product and candidate segments, **review** when the user brings a filled scoring.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and what the choice is for: first segment, market entry, sales focus;
- the candidate segments, or what is known about the customers;
- data behind the scores: market sizes, prices, interviews, channel costs, with sources;
- whether some criterion must knock a segment out.

Do not invent scores or market data. A score without a fact behind it is marked as an assumption in the rationale.

### 2. Segments

Describe three to seven segments: who the customer is and in what situation. Merge overlapping ones; split "everyone".

### 3. Criteria and method

Propose the default four criteria or the user's own, at most four. Agree what 1, 2 and 3 mean for each before scoring. Pick the product when a weak criterion must knock a segment out, the weighted sum when criteria are unequal; set the weights before scoring.

### 4. Score and check

Score each segment with a fact per score. Check the leader for a low score on a critical criterion; call scores within a point a tie and name how to break it with customers.

### 5. Show, then write

Show in chat first: the scale definitions, then the table row by row as in the spreadsheet (segment, the scores, rationale), the resulting order and the chosen segment. Write a file only after the user confirms. Ask for the output path (default `segment-scoring-<product>.xlsx` in the working directory). Save the data as JSON (the example is the Amazon case from card.md: its own criteria replace the default headers, the unused fourth criterion stays empty, and no scores are published, so they stay empty):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {"title": "Amazon: first category, 1994", "method": "product"},
  "cells": {"B4": "Number of items", "C4": "Mail catalog", "D4": "Suppliers", "E4": ""},
  "rows": [
    ["Books", null, null, null, null, "More than 3 million in print; catalog too large to mail; wholesalers already have electronic warehouse lists"],
    ["Music CDs", null, null, null, null, "About 200 thousand items"],
    ["Computers", null, null, null, null, "Not in the sources"],
    ["Software", null, null, null, null, "Not in the sources"],
    ["Video", null, null, null, null, "Not in the sources"]
  ]
}
```

A row is six values, columns A to F: segment, the four scores (whole numbers 1-3 or `null`), rationale. Do not pass the score and rank: the spreadsheet computes them in columns G and H with live formulas, from the filled criteria only. `method` must be exactly `product` or `weighted sum`: the spreadsheet formula compares it with these strings. For the weighted sum, write the weights to `B3`-`E3` through `cells` (they default to 1). To rename a criterion, write its header to `B4`-`E4`; leave an unused criterion empty in every row. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/segment-scoring.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's scoring in any form and check it against the common mistakes in card.md:

1. Every score has a fact behind it.
2. Segments are specific and do not overlap.
3. Weights and scale definitions were set before scoring.
4. The method fits: a product where a weak criterion must knock a segment out.
5. The winner is not decided by a one-point difference on a coarse scale.

Report findings as a numbered list: segment or criterion, what is wrong, why it matters for the choice, the concrete fix. End with a verdict: "choice is sound", "sound after fixes" or "not enough data".
