---
name: product-backlog
description: Build or tidy a product backlog — one ordered list of features, bugs, technical work, learning and requirements under a product goal — and produce a filled backlog spreadsheet with live health checks, or review an existing backlog. Use when the user has a pile of tasks and requests for one product and needs a single ordered, groomed list for the team.
---

# Product Backlog

The theory, DEEP, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings tasks, requests or ideas to turn into a backlog, **review** when the user brings an existing backlog.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and the team that works on it;
- the product goal for the next two to six months — a future state, specific and checkable;
- the items: tasks, requests, bugs, technical work, with whoever asked for each and, if known, when it was added;
- who orders the list (the product owner) and who sizes items (the people who will do the work);
- the team's average capacity per sprint in the units it sizes in, if it sizes at all.

If there is no product goal, do not invent one: help the user phrase it first, or record that it is missing and say that the list cannot be checked against it. If the items belong to several products, build one backlog per product. If the user mainly wants a scored ranking, offer `rice-scoring` or `ice-scoring` for that step and bring the resulting order back here.

### 2. One list

Merge everything into a single list: features, bugs, technical work, learning and requirements together. Merge duplicates. Split items that hide several pieces of work. Give each item a type.

### 3. Link to the goal

For every item, write in one phrase how it moves the product towards the goal. Leave the field empty when there is no link — that marks a candidate for removal, not a mistake to hide.

### 4. Order

Put the items in one order, top first, no ties. For each, write why it sits there: value, risk, deadline, dependencies. The order is the product owner's decision; propose it, do not impose it. Requirements with a hard deadline (regulator, contract) go where the deadline puts them, not where a score would.

### 5. Detail the top, size, mark ready

Make the top items small and clear, leave the bottom coarse. Sizes come from the team: if the user gives none, leave the field empty and say who should fill it. Mark an item ready only when the team is confident it fits one sprint: it is understood, sized and not blocked. Never mark readiness on the team's behalf.

### 6. Prune

Propose a decision for each item: keep, postpone or delete. Delete candidates are items with no link to the goal and old items nobody has moved. Show them as a separate list so the product owner can confirm.

### 7. Show, then write

Show the table in chat first: place, item, type, link to the goal, why here, size, ready, decision. Above it, the product goal. Below it, the health of the list: number of items, items without a link to the goal, items without a size, ready items and how many sprints they cover.

Write a file only after the user confirms. Ask for the output path (default `backlog-<product>.xlsx` in the working directory). Save the data as JSON. The example is the YooKassa case from card.md. The source gives no order, sizes, readiness, dates or capacity, so the rows follow the article and those fields are null; with a real team, fill them, or the health checks for size, readiness and age stay meaningless:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "YooKassa, core team: maintenance and tech backlog, 2023",
    "goal": "Stability of the core functions of the payment system: API operation, payment processing, reconciliation (in the article this is the team's area of responsibility; there is no product goal)",
    "unit": "story points"
  },
  "cells": {"C3": null},
  "rows": [
    ["Fix a bug in the payment flow", "bug", "removes errors for 5% of payments", "high value for small effort: the developer has already looked at the code and knows how to fix it", null, null, null, null, "keep"],
    ["Add an index on a column", "tech work", "queries stop failing on timeout", "strong impact on processes, high confidence: the code has been reviewed", null, null, "developer", null, "keep"],
    ["Reduce the logging volume", "tech work", "disk space will not run out", "important, but there is room for half a year — schedule it", null, null, "tech lead", null, "postpone"]
  ]
}
```

Rows go in backlog order, top first. Each row has nine values: item, type, link to the goal, why here, size, ready, requested by, added, decision. Do not pass the place: the spreadsheet numbers rows itself. Use null, not an empty string, for unknown values. Allowed words: type — `feature`, `bug`, `tech work`, `learning`, `requirement`; ready — `yes` or `no`; decision — `keep`, `postpone`, `delete`. The health formulas count these exact words, so check the spelling. Size is a number. Pass the date added as a formula, `"=DATE(2026,4,1)"`, so the age check can compare it. Pass the team capacity as a number in `cells` → `C3`; with null, the sprints-of-ready-work check stays empty. The sheet prepares 100 rows. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/product-backlog.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's backlog in any form and check it against the common mistakes in card.md:

1. The list is not a dumping ground: it is short enough that the top is visible, and old untouched items get removed.
2. There is a product goal, and every item links to it; items without a link are named.
3. The order is real: one item per place, no "everything high priority".
4. Detail matches position: the top is small and clear, the bottom is coarse.
5. One product has one list: bugs and technical work are ordered together with features.
6. Sizes come from the people who will do the work.

Ask the user instead of reporting a finding when the backlog alone cannot show it: who sized the items, and whether there are other lists for the same product. Report findings as a numbered list: item or field, what is wrong, why it matters for the next planning, the concrete fix. List the items you would delete or merge. End with a verdict: "backlog is ready for planning", "ready after fixes" or "needs a product goal first".
