---
name: yc-guide-to-business-models
description: Pick the key metrics for a product or each business line from Y Combinator's guide to nine business models - SaaS, transactional, marketplace, subscription, enterprise, usage-based, e-commerce, advertising, hardtech - define each metric precisely, catch substitutions such as GMV passed off as revenue, and produce an XLSX metric sheet with the guide as a reference; or review an existing set of business metrics. Use when choosing success metrics for a product or business line, when the business model changes, or when explaining to investors or a team which numbers to judge a business by.
---

# YC Guide to Business Models

The theory, the nine models, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a product or a company, **review** when the user brings the metrics they track.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the company or product and its business lines;
- how each line makes money: who pays, for what, once or regularly;
- the metrics tracked today with their definitions and latest values, with sources;
- any planned change of model.

Do not invent metric values. A metric without a value stays empty.

### 2. Model per line

Split the business into lines that make money differently. Map each line to one of the nine models; if none fits, name the model and say why.

### 3. Metrics

For each line, take the model's primary metrics from card.md, three to four per line. Write the exact definition of each: what is included and what is not. Flag substitutions: GMV or GTV as revenue, one-off or usage revenue as recurring, registered users instead of active.

### 4. Model changes

If a line changes model, say which metrics stop describing it and which to add, and who needs to be told.

### 5. Show, then write

Show in chat first: the lines with their models, then the table row by row as in the spreadsheet (line, model, metric, definition, value, period, change, conclusion) and the substitutions found. Write a file only after the user confirms. Ask for the output path (default `business-model-metrics-<company>.xlsx` in the working directory). Save the data as JSON (the example is the Kaspi.kz case from card.md):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {"title": "Kaspi.kz, 2023"},
  "rows": [
    ["Payments", "Transactional", "TPV", "Payments and B2B operations of active customers, excluding free P2P and QR", "28,406 bn KZT", "2023", "+43%", "Volume growing, fee stable"],
    ["Payments", "Transactional", "Take rate", "Fees as a share of TPV", "1.2%", "2023", "unchanged", ""],
    ["Marketplace", "Marketplaces", "GMV", "All sales on the platform, 3P and 1P", "4,161 bn KZT", "2023", "+45%", "GMV is not revenue"],
    ["Marketplace", "Marketplaces", "Take rate", "Fees as a share of GMV of third-party sellers", "9.2%", "2023", "8.2% in 2022", "Growth driven by high-margin categories"],
    ["e-Grocery", "E-commerce", "Retail revenue", "Sale of groceries and delivery", "58.4 bn KZT", "2023", "since February 2023", "Model switched from 3P to 1P: track margin"],
    ["Fintech", "Lending", "TFV", "Volume of loans issued", "7,930 bn KZT", "2023", "+47%", "Model not in the guide"]
  ]
}
```

A row is eight values, columns A to H: line, model, metric, definition, value, period, change, conclusion. Write the model exactly as in the guide (`SaaS`, `Transactional`, `Marketplaces`, `Subscription`, `Enterprise`, `Usage Based`, `E-commerce`, `Advertising`, `Hardtech/Bio/Moonshots`) or your own name if none fits. Do not pass column I: the spreadsheet looks up the guide's metrics for the model from the "Reference" sheet and shows `not in the guide` for other models; this text is written by the spreadsheet formulas. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/yc-guide-to-business-models.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's metrics in any form and check them against the common mistakes in card.md:

1. Each business line is mapped to its own model, not one model for the whole company.
2. GMV or GTV is not reported as revenue.
3. One-off or usage revenue is not counted as recurring.
4. Active users, not registered users.
5. After a model change, the metrics changed too.

Report findings as a numbered list: line and metric, what is wrong, why it misleads, the concrete fix. End with a verdict: "metrics fit the model", "fit after fixes" or "not enough data".
