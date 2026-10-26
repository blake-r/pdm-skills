---
name: abc-analysis
description: Rank products, customers, sellers or features by their contribution to one result - revenue, profit, units - split them into classes A, B and C by cumulative share, set a different management rule for each class, and produce an XLSX with the ranking, class summary and Pareto curve; or review an existing ABC analysis. Use when there are dozens or more objects with uneven contribution and not enough time, money or capacity to treat them all alike, or when deciding what to cut and what to protect.
---

# ABC Analysis

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings objects and values, **review** when the user brings a finished classification.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- what is ranked (products, customers, sellers, features) and by what result (revenue, profit, units), for which period;
- the values per object from one source, as a table or file;
- the class boundaries, if the user has them (default: A up to 80% of the cumulative result, B up to 95%, C the rest);
- what the classes will be used for: which resource is short.

Do not invent values. Objects without a value are left out and listed separately.

### 2. Rank and classify

Check that the objects are of one kind and the values are in one unit and period. Sort by value, descending; compute each object's share and the cumulative share. An object is in A if the cumulative share before it is below the A boundary, in B if below the B boundary, otherwise in C. Report the count and share of the result per class, and how uneven the distribution is: if A holds most objects, say that classes add little.

### 3. Rules per class

For each class, propose a concrete rule tied to the short resource: control frequency, service level, budget, review or exit. Before proposing to cut C, ask what data shows whether C objects are bought or used together with A objects.

### 4. Show, then write

Show in chat first: the class summary (objects, share of objects, share of result), the top of the ranking, the rules per class. Write a file only after the user confirms. Ask for the output path (default `abc-analysis-<subject>.xlsx` in the working directory). Save the data as JSON. The card's case has no published values, so the example below is a made-up shape of the input, not data:

```json
{
  "text": {"title": "store products by revenue, Q3"},
  "cells": {"B2": 0.8, "B3": 0.95},
  "rows": [
    ["Product 1", 1200000, ""],
    ["Product 2", 640000, ""],
    ["Product 3", 90000, "bought together with product 1"]
  ]
}
```

A row is three values, columns A to C: object, value, comment. Values are numbers, not text. `B2` and `B3` are the A and B boundaries as fractions; omit `cells` to keep 0.8 and 0.95. Do not pass columns D to G: the spreadsheet ranks, computes shares and classes, fills the class summary and draws the curve. It holds up to 500 objects; for more, aggregate or classify outside the file. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/abc-analysis.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's classification in any form and check it against the common mistakes in card.md:

1. Each class has a rule; the classification changed how work is done.
2. C is not cut wholesale without checking links to A.
3. The objects are of one kind; values in one unit and period.
4. The criterion fits the decision: profit or margin where margin matters.
5. The classes are recomputed on a schedule.

Report findings as a numbered list: what is wrong, why it misleads the decision, the concrete fix. End with a verdict: "classification is sound", "sound after fixes" or "not enough data".
