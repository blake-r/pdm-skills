---
name: abcdx-segmentation
description: Split paying customers into A, B, C, D and X segments by how much they need the product, compare the shares of customers, revenue and support load, sort requests by segment and produce a filled spreadsheet, or review an existing ABCDX segmentation. Use when the team must decide whose requests to build first, whom to acquire and whom to serve cheaply.
---

# ABCDX Segmentation

The theory, segments, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings customer data or requests to prioritize, **review** when the user brings a segmentation or a decision built on one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product, the period, and whether revenue or margin is counted;
- per paying customer: revenue or margin, number of purchases, and if available the sales cycle and support requests;
- what sales and support say distinguishes the best customers;
- the requests, tickets or feature asks that need prioritizing, if any.

If the base is far below the card's limits (about 10,000 paying customers in B2C, 100 in B2B), say the segments will be anecdotal and continue only as a hypothesis. Do not invent customers or counts.

### 2. Find the segment traits

Rank customers by revenue or margin and purchase frequency. For the top and the bottom, ask what they have in common: need, situation, channel, region, company size. Propose one or two traits per segment and agree them with the user. Traits, not amounts, define a segment: a new customer with A traits is A.

### 3. Tag and compare

Tag every customer A, B, C, D or X with a short reason. Compare shares of customers, revenue and support requests per segment. Point out where C and D take more support than they bring revenue, and name the X customers separately.

### 4. Sort requests and decide

If there are requests, split each by the segments that raised it and rank by the count from A and B, not by the total. State the decision: which requests go first, whom to acquire, what to automate for C and D, what to decide about X. Do not promise effects.

### 5. Show, then write

Show in chat first: the traits, the segment table with shares, the requests by segment and the decision. Write a file only after the user confirms. Ask for the output path (default `abcdx-<topic>.xlsx` in the working directory). Save the data as JSON:

```json
{
  "text": {
    "title": "…",
    "criteria_a": "…", "criteria_b": "…", "criteria_c": "…", "criteria_d": "…", "criteria_x": "…",
    "strategy_a": "…", "strategy_b": "…", "strategy_c": "…", "strategy_d": "…", "strategy_x": "…",
    "decision": ["First: …", "Postpone: …"]
  },
  "cells": {"Segments!A16": "Search filter does not work well", "Segments!C16": 12, "Segments!D16": 27},
  "rows": [["client-001", 31000, 5, null, 1, "A", "pays for the subscription, no questions"]]
}
```

Each row is the customer, revenue or margin, purchases, sales cycle in days (`null` if unknown), support requests, segment letter, reason. The sheet “Segments” computes the shares. `cells` fills the request table on “Segments”: rows 16–25, column A the request, C the count from A and B, D the count from C and D; the share and the total are computed. Order the rows by column C, not by the total. The template prepares 300 customer rows and the summary counts up to 5,000; aggregate larger bases in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/abcdx-segmentation.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's segmentation in any form and check it against the common mistakes in card.md:

1. The base is large enough, and only paying customers (plus heavy non-payers as D) are segmented.
2. Segments are defined by traits, not by revenue alone.
3. Tags match the traits, and the shares add up.
4. Requests are ranked by A and B demand, not by total count.
5. C and D service is automated or limited, not ignored or over-served.
6. X has an explicit decision.
7. Segments are reviewed regularly.

Items 1 and 7 often cannot be judged from the table alone: ask the user instead of reporting a finding. Report findings as a numbered list: segment or customer, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
