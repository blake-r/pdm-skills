---
name: product-lifecycle
description: Place a product or category on the product lifecycle - introduction, growth, maturity, decline - from its sales history over several years, name the current stage and the evidence for it, choose the decision that fits the stage (invest, extend with a new use, market or price, or harvest and exit) and how to check it, and produce a one-slide PPTX with the curve; or review an existing lifecycle assessment. Use when growth has slowed and it is unclear whether this is a dip or maturity, or when one line in a portfolio takes resources without return.
---

# Product Lifecycle

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a product and its history, **review** when the user brings a finished assessment.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product, category or line, and the market;
- one metric by year (revenue, transaction volume, active customers) for every year of the product, from one source, and any change in how it was counted;
- supporting signs: margin, share of new customers, number of competitors;
- the decision the user faces and the resource at stake.

Do not invent values. A year without data stays out of the series; say so in `stages`.

### 2. Mark the stages

Check that the metric is comparable year to year; if accounting changed, switch to a comparable metric or mark the break. Mark each stage by the growth rate and the supporting signs. Do not call a stage from one year, and check whether a one-off event (season, regulation, a crisis) explains the change. Say that the stage is only visible in hindsight, and how sure the call is.

### 3. Decision

Propose the decision that fits the current stage: invest to grow, extend (new use, market or price), or harvest and exit. At maturity, consider extension before harvesting. Name the numbers and the date by which the decision will be checked.

### 4. Show, then write

Show in chat first: the series by year, the stage marking with its evidence, where the product is now, and the decision. Write a file only after the user confirms. Ask for the output path (default `product-lifecycle-<product>.pptx` in the working directory). Save the data as JSON (the example is the Groupon case from card.md; the stage marking is ours, not Groupon's):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Groupon, deal volume through the platform, 2009–2023",
    "stages": ["Introduction 2009, growth 2010–2013", "Maturity 2014–2017, peak $6.3 bn in 2015", "Decline from 2018; marking is ours"],
    "now": ["2019: $4.6 bn, down 11% from 2018", "Goods: 40% of impressions, 20% of gross profit", "Goods profit falling for 4 quarters"],
    "decision": ["February 2020: exit goods", "Focus on local services", "Goal: return to growth by 2022"],
    "result": ["Goods moved to a third-party marketplace model, 2020–21", "2022: $1.8 bn, growth did not return", "The pandemic cannot be separated from the decision"]
  },
  "charts": {
    "curve": {
      "categories": ["2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"],
      "series": [
        {"name": "Deal volume, $ bn", "values": [0.03, 0.75, 3.99, 5.4, 5.8, 6.2, 6.3, 5.7, 5.6, 5.2, 4.6, 2.6, 2.3, 1.8, 1.6]}
      ],
      "value_axis": {"number_format": "0", "major_unit": 1}
    }
  }
}
```

`curve` takes the years as `categories` and one or two series of numbers, one value per year; put the unit in the series name. Keep `title` under 60 characters, and `stages`, `now`, `decision` and `result` to three items of under 40 characters each; one thought per item, each becomes its own paragraph. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/product-lifecycle.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's assessment in any form and check it against the common mistakes in card.md:

1. The stage rests on several years, not one.
2. Product, category and brand are not mixed.
3. The metric is comparable across years.
4. The stage led to a decision with a check date.
5. At maturity, extension was considered before harvesting.

Report findings as a numbered list: what is wrong, why it misleads the decision, the concrete fix. End with a verdict: "assessment supports the decision", "supports it after fixes" or "not enough data".
