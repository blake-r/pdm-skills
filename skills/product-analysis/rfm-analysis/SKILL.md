---
name: rfm-analysis
description: Segment customers by Recency, Frequency and Monetary value, assign an action to each segment and produce a filled spreadsheet with scores and a recency × frequency grid, or review an existing RFM segmentation and its campaign plan. Use when the user has purchase history and wants to decide whom to retain, wake up, win back or stop discounting.
---

# RFM Analysis

The theory, scales, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings customer data, **review** when the user brings segments, a grid or a campaign plan built on RFM.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the analysis period and the calculation date;
- per customer: days since the last purchase (or its date), number of orders and purchase amount in the period;
- the typical purchase cycle of the product;
- the channels available for segment actions and any budget limits on discounts.

If the user attaches raw orders, aggregate them yourself (with code) and show the rule. Do not invent customers or values. If customers buy once every few years, say that RFM will barely separate them and stop.

### 2. Set the level boundaries

Use three levels per attribute, because the template has three; level 3 is the best score. If the user's sources use 1 as the best, convert before comparing codes. Propose boundaries from the purchase cycle (for example, R = 3 within one cycle, R = 2 within three cycles) or from equal-sized groups, and agree them with the user. Write them down: they go into the spreadsheet.

### 3. Score and read the grid

Score every customer, then build the recency × frequency grid with customer counts and revenue per cell. Report where revenue concentrates, what share of frequent buyers already sleeps, and how many one-time buyers never returned. Use M to rank customers inside a cell, not to replace F.

### 4. Assign actions

For each cell give one action and one goal (retain, raise frequency, wake up, win back, stop spending). Tie every discount to a control group: a share of the segment that gets no message. Do not promise effects; state what the test will measure.

### 5. Show, then write

Show in chat first: the boundaries, the grid with counts and revenue, the action per cell. Write a file only after the user confirms. Ask for the output path (default `rfm-<topic>.xlsx` in the working directory). Save the data as JSON:

```json
{
  "text": {"title": "…", "actions": ["Recent, frequent: …", "Sleeping, frequent: …"]},
  "cells": {"C3": 30, "E3": 90, "C4": 4, "E4": 2, "C5": 20000, "E5": 5000},
  "rows": [["client-001", 12, 5, 31000]]
}
```

`cells` sets the boundaries on the sheet “Customers”: row 3 is R in days (level 3 at most C3, level 2 at most E3), row 4 is F in orders (level 3 at least C4, level 2 at least E4), row 5 is M in money (the same rule). Each row is the customer, days since the last purchase, orders, amount. Do not pass R, F, M or the segment: the spreadsheet computes them, and the sheet “Segments” builds the grid. `actions` lists one line per grid cell: action, goal, control group. The template prepares formulas for 300 customers and copies them for more rows; the grid counts up to 5,000 customers, so aggregate larger bases in chat and pass the grid-level result or a sample. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/rfm-analysis.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's segmentation in any form and check it against the common mistakes in card.md:

1. Boundaries follow the purchase cycle.
2. Period and calculation date are stated and the same for all customers.
3. Scores match the boundaries, and the arithmetic is right.
4. Frequency, not one large amount, decides whether a customer is "valuable".
5. Every segment has one action and one goal.
6. Discounts are tested against a control group.
7. Scores are recalculated regularly.

Items 6 and 7 often cannot be judged from the grid alone: ask the user instead of reporting a finding. Report findings as a numbered list: segment or customer, what is wrong, why it changes the plan, the concrete fix. End with a verdict: "plan holds", "plan changes after fixes" or "not enough data to plan".
