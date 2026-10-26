---
name: unit-economics
description: Calculate unit economics of a business model — CAC (cost to acquire a customer), contribution margin per unit, LTV (lifetime value), LTV/CAC and CAC payback — per channel or scenario, check against thresholds, and produce an XLSX with live formulas; or review an existing unit-economics calculation. Use when someone asks whether a business model, channel, price or delivery condition pays back before scaling, how much a customer can cost to acquire, or why the numbers "work" on paper but the cash runs out.
---

# Unit Economics

The theory, the formulas, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants a calculation built, **review** when the user brings a finished calculation or a table of unit numbers.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the unit: customer, order or item; for a customer, whether purchases repeat;
- the period: month, quarter or an observation window, and where the numbers come from;
- per scenario (channel, price option, period): spend on acquisition, new customers, revenue per customer in the period, contribution margin (what remains after cost of goods, delivery, payment fees, support, returns), churn per period if known;
- the horizon in periods, if churn is unknown, and why that number;
- thresholds the business wants to use for LTV/CAC and payback, and the decision the numbers should serve.

Do not invent numbers. Mark what the user did not give as unknown and leave the cell empty. If there are no repeat purchases or fewer than a few dozen new customers, say that CAC and churn will swing and mark every result as a rough estimate. If the user gives revenue instead of contribution margin, ask for the margin: LTV on revenue overstates value (card.md, mistakes).

### 2. Name the version of the formulas

Say which version is used: card.md follows David Skok (CAC, lifetime = 1 / churn, LTV = ARPA x margin / churn, payback = CAC / (ARPA x margin)). Skok's own thresholds (LTV/CAC above 3, payback up to 12 months) are for SaaS with margin of 80% and more; propose the user's own thresholds and write them down before looking at results.

### 3. Calculate by scenario

One row per scenario, never an average across channels. The template computes CAC, contribution per period, lifetime, LTV, LTV/CAC and payback. Without churn, the horizon replaces lifetime: label the result "estimate for the window", not LTV.

### 4. Interpret and decide

Below 1: does not pay back, change channel, price or costs. Between 1 and the threshold: pays back slowly, check whether cash lasts until payback. Above the threshold: scale while CAC does not grow. Compare totals as well as ratios: the best ratio is not always the best sum. Propose one decision and a date to check it.

### 5. Show, then write

Show the table in chat first: scenario, CAC, contribution per period, lifetime, LTV, LTV/CAC, payback, verdict, then the unit, period and decision. Write a file only after the user confirms. Ask for the output path (default `unit-economics-<business>.xlsx` in the working directory). Save the data as JSON. The example is the Wayfair case from card.md (S-1, 2014); the source gives no churn, LTV or threshold, so churn is `null`, the horizon is 1 window and the thresholds stay empty. Note that Wayfair's CAC counts advertising only, below Skok's version:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Wayfair, North America: customer acquisition spend, Q3 2011 and Q3 2013 (S-1, 15.08.2014)",
    "unit": "Customer: first purchase on one of the sites in the quarter or in the next 180 days",
    "period": "Observation window: the quarter and the next 180 days; one period in the table — the whole window (horizon 1). Data from S-1, pp. 58–59",
    "decision": "Wayfair closed more than 240 niche sites in favor of Wayfair.com and began acquiring customers with higher lifetime value, accepting a longer payback. The source contains no LTV/CAC threshold and no review date"
  },
  "cells": {},
  "rows": [
    ["Q3 2011", 8797000, 244778, 265, 0.2, null, 1, "S-1, pp. 58–59: advertising $8,797 thousand, customers 244,778, revenue per customer $265; 20% margin — Wayfair's assumption"],
    ["Q3 2013", 20966000, 451750, 311, 0.2, null, 1, "S-1, pp. 58–59: advertising $20,966 thousand, customers 451,750, revenue per customer $311; 20% margin — Wayfair's assumption"]
  ]
}
```

Each row has eight values in this order: scenario, acquisition spend, new customers, revenue per customer per period, contribution margin (share, 0.2 for 20%), churn per period (share), horizon in periods, basis. Margin and churn are shares from 0 to 1 (0.2, not 20), not percents. Use `null`, not an empty string, for unknown values. Columns I to O are formulas: do not put values there, the script copies them for extra rows. The sheet has 30 prepared rows; thresholds R7 (LTV/CAC) and R8 (payback, periods) are empty: the user sets them before looking at results, e.g. `"cells": {"R7": 2, "R8": 12}`; without them the verdict says only whether the unit pays back. Expected result for the example: CAC about 35.9 and 46.4, LTV/CAC 1.47 and 1.34, verdict `pays back, LTV/CAC threshold not set` for both. The verdict strings are written by the spreadsheet formulas. Zero churn with a horizon of 12 gives lifetime 12, not an empty cell.

Length limits that fit the sheet: title under 105 characters; unit under 100; period under 130; decision under 220; scenario under 40; basis under 130. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/unit-economics.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints every column and its hint.

## Mode: review

Take the user's calculation (table, formulas, or description) and check it against the common mistakes in card.md:

1. LTV is computed on revenue, not on contribution margin.
2. A threshold from another industry is used (Skok's 3 and 12 months come from SaaS with margin of 80% and more, LTV without margin). Never offer Skok's numbers as defaults.
3. The best ratio is taken as the best decision: totals after acquisition are not compared.
4. Lifetime is unbounded: churn near zero gives 1 / churn growing without limit, with no horizon set as an assumption.
5. Periods differ: monthly revenue with annual churn.
6. Channels are averaged, so a channel that does not pay back is hidden.
7. The unit is wrong: for repeat purchases the unit is the customer, not the order.

Items 3 and 6 usually need the raw rows: ask for the numbers per channel or period instead of reporting a finding. Also check that CAC includes all sales and marketing spend, not advertising alone, and that the thresholds were set before the results. Report findings as a numbered list: what is wrong, how it changes the decision, the concrete correction. End with a verdict: "unit pays back", "works after changes" or "numbers do not support scaling".

Example: a table gives LTV = revenue per customer x 24 months = 7200, CAC 1500, ratio 4.8, "scale". Margin is 25%, never mentioned. Findings: item 1 — on contribution margin LTV is 1800 and the ratio 1.2, so it pays back barely; item 2 — ask which threshold and where it comes from; item 4 — ask where 24 months comes from. Verdict: "works after changes".
