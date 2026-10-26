---
name: financial-modeling
description: Check a business-model hypothesis by calculation before launch — build a financial (mathematical) model from business and product metrics, solve the forward problem (initial metrics to target metrics) or the inverse one (limits on initial metrics for a given target), test three scenarios against criteria set in advance, run sensitivity, and produce an XLSX with live formulas; or review an existing model. Use when someone asks whether a business model can reach its goal on paper, how much a customer or a store may cost, what the break-even point is, or which assumption matters most before spending on a real test.
---

# Financial Modeling

The theory, the formulas, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants a model built, **review** when the user brings a finished model or a table of assumptions.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the hypothesis: which conditions (initial metrics) should reach which goal (target metrics);
- the unit (customer, order, store) and the period, and where the numbers come from;
- which problem is solved: forward (initial metrics known, target computed) or inverse (target known, limits on initial metrics wanted), and boundary conditions for the inverse one;
- per assumption, for three scenarios: volume of units per period, revenue per unit, share of variable costs (cost of goods, delivery, payment fees, returns, support), one-off cost to launch a unit (acquisition or opening), fixed costs of the period;
- the criteria, set before looking at results: target profit and allowed payback in periods;
- the basis of every number: fact (source, date), estimate, company goal or hypothesis.

Do not invent numbers. Mark what the user did not give as unknown and leave the cell empty. If every number is a hypothesis, say that the model is a priori and its trust is low (card.md).

### 2. Build the chain

Walk through the seven metric groups of card.md (product creation, acquisition, sales, logistics, retention, upsell, support) and make sure no cost line is missing. The template folds them into five assumptions; if a business needs more, put the extra cost into variable or fixed costs and say so.

### 3. Calculate

The template computes per scenario: revenue, contribution of a unit per period, payback in periods, profit of a period after launch has paid back, net profit over the allowed payback term (term × period profit − volume × launch cost, so payback and profit use one horizon), break-even in units (fixed costs ÷ contribution of a unit), limits of launch cost by payback and by target profit, margin to the limit, verdicts against the criteria. The target profit is the net profit over the allowed term, so it needs the term. Sensitivity (±10% by default) works on the base scenario and ranks assumptions by the swing of net profit; equal swings share a rank, so rank 1 may belong to several assumptions. State that three scenarios, criteria before the calculation, break-even, payback, net profit and sensitivity are the card author's additions, not PAF's. If only one criterion is set, the verdict gets the mark "(one criterion)": tell the user it is checked by one criterion.

### 4. Interpret and decide

Criteria met: the hypothesis is not rejected, name what to check in the real world first (the top-ranked assumptions). Not met: change initial or target sets and recalculate, or drop the option. "Works on paper" is never "proven". Propose one decision and how and when it will be checked.

### 5. Show, then write

Show the model in chat first as a table: assumptions by scenario with their basis, then results, sensitivity and the decision. Write a file only after the user confirms. Ask for the output path (default `financial-modeling-<business>.xlsx` in the working directory). Save the data as JSON. The example is the Warby Parker case from card.md (S-1, 24.08.2021, pp. 125 and 127); the source gives no volume, launch cost, fixed costs, target profit or other scenarios, so those are `null`:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Warby Parker, retail store model (S-1, 24.08.2021)",
    "hypothesis": "A new store reaches the metrics of a mature one (sales $2,900 per sq. ft, margin 35%) and pays back in under 20 months",
    "task": "Inverse: from the payback term we find the maximum investment per sq. ft; the forward part is not disclosed in the source",
    "unit_period": "Unit: 1 sq. ft of retail space; period: year (assumption of the card author, S-1 does not state a period)",
    "decision": "S-1 names a plan: 30–35 stores in 2021; the source does not say the plan follows from a model. Potential in the US 900+ (third-party firm)"
  },
  "cells": {},
  "rows": [
    [null, null, null, "not in S-1"],
    [null, 2900, null, "S-1, p. 125: target for mature stores (12+ months)"],
    [null, 0.65, null, "Author's calculation: 1 − 35% margin of mature stores; rent and staff are variable here"],
    [null, null, null, "not in S-1; limit is in the row \"Limit of launch cost per unit\""],
    [null, null, null, "not in S-1"],
    [null, null, null, "not in S-1"],
    [null, 1.6667, null, "S-1, p. 125: target for new stores; 20 ÷ 12 ≈ 1.67 years, author's calculation"]
  ]
}
```

Seven rows go in the fixed order of the template: volume, revenue per unit, share of variable costs (a share from 0 to 1, not percent), launch cost per unit, fixed costs, target net profit over the allowed term, allowed payback term in periods (it is also the horizon of net profit). Each row has four values: pessimistic, base, optimistic, basis. Use `null`, not an empty string, for unknown values. Everything below row 14 (the calculation, sensitivity and its ±10% step in `E32`) is formulas: do not put values there; to change the step write `"cells": {"E32": 0.2}`. Expected result for the example: contribution of a unit 1015 per period, limit of launch cost 1691.7 (1.6667 × 1015) for the base scenario, verdict "no data for the criteria" because launch cost, volume and profit target are missing; sensitivity stays empty until the five numeric assumptions are filled.

Length limits that fit the sheet: title under 80 characters; hypothesis under 170; task under 150; unit_period under 130; decision under 200; basis under 110. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/financial-modeling.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints every column and its hint.

## Mode: review

Take the user's model (table, formulas, or description) and check it against the common mistakes in card.md:

1. Assumptions have no basis: numbers are invented and presented as a result.
2. There is one scenario only, no pessimistic one.
3. The criteria were set after the calculation, so the threshold fits the result.
4. A solution of the inverse problem is taken as the only one, with no boundary condition or optimization function.
5. Not all cost lines are included: advertising is there, while delivery, returns and payment fees are not.
6. Periods or units differ: monthly revenue against annual costs.
7. "Works on paper" is read as "proven": the model is not checked in the real world and not updated with facts.

Items 3 and 7 usually cannot be judged from the table alone: ask when the criteria were fixed and what real data is planned instead of reporting a finding. Also check that sensitivity was run and the top assumption is named. Report findings as a numbered list: what is wrong, how it changes the decision, the concrete correction. End with a verdict: "model supports checking in the real world", "works after changes" or "numbers do not support the hypothesis".

Example: a model with one scenario, acquisition cost of advertising only and the sentence "the model proves the business works". Findings: item 2 — add a pessimistic scenario; item 5 — add delivery, returns and payment fees to variable costs; item 7 — rephrase to "does not reject the hypothesis" and name what to check first. Verdict: "works after changes".
