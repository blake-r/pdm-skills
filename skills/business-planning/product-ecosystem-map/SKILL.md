---
name: product-ecosystem-map
description: Build or check a Product Ecosystem Map — the products of an ecosystem with their roles (Lead, Value, Profit, Engagement, Upsale, Retention generators, touchpoints, platform, operational efficiency), role metrics, transfer value between products and a decision on the portfolio — and produce a one-slide map, or review an existing map. Use when a company with several products for one customer must decide what to launch, close or keep, or claims to be an "ecosystem".
---

# Product Ecosystem Map

The theory, roles, metrics and the worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants to build the map, **review** when the user gives an existing map or role list and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the company, the customer (one or several segments) and the date of the map;
- the list of products and the need each one solves;
- the platform: is there one shared customer profile, and what data goes between products;
- the entry points (apps, sites) and their reach;
- the metric of each role and its current value, with source;
- what decision is pending: launch, close, change a role.

If the products are only grouped by industry and share no profile or data, say that by the PAF definition this is not an ecosystem and ask whether to map it anyway as a portfolio. Never invent numbers: mark what the user did not give as unknown.

### 2. Platform and transfer value

Describe the platform and the level of transfer value: authorization, transactions or context. Write each arrow: from which product, to which, which data. No arrows means no transfer value.

### 3. Roles

For each product ask "why does the company need it": customers come for it (Value), it earns on the core (Profit), it brings new customers (Lead), it raises use of other products (Engagement), it adds revenue but nobody comes for it (Upsale), it keeps customers (Retention: retention products or next-steps products). A product may have two roles; a product with none is a candidate to close. Do not assign roles the source does not support: mark them as assumptions.

### 4. Metrics and balance

Put the PAF metric of each role next to its current value; unknown stays empty. Check the balance: is there a Lead, a Profit and a Retention product. Judge by the customer: share of wallet, LTV of the ecosystem.

### 5. Decision

Name one decision by product (launch, close, change role) and the metric by which it is checked, and by when. A loss-making product may stay if it raises an ecosystem metric.

### 6. Show, then write

Show the map in chat first as a table by template blocks: title, touchpoints, six roles with products and metric values, transfer value, platform, operational efficiency, decision. Write a file only after the user confirms. Ask for the output path (default `product-ecosystem-map-<company>.pptx`). Save the data as JSON. The example is the Tinkoff case from card.md; fields the source does not give are left out (null):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Tinkoff, Retail and SME, Strategy Day, June 2018",
    "touch": "Tinkoff app: 2.5+ million MAU, 0.8+ million DAU (slide 28)",
    "lead": "Tinkoff Journal (Lead stated directly in PAF)",
    "lead_m": "3+ million MAU (slide 27); the source gives no conversion data",
    "value": "Tinkoff Black, loans (Value, Profit; reconstruction from PAF)",
    "value_m": "North Star Metric not specified",
    "profit": "Credit cards, cash loans (reconstruction)",
    "profit_m": null,
    "engage": null,
    "engage_m": null,
    "upsale": "Insurance (assumption)",
    "upsale_m": null,
    "retain": null,
    "retain_m": null,
    "transfer": "Data transfer between products is not described in the source. Cross-sales (slide 15, our reading): share of new customer inflow to a product through Black: investments 80%, cash loans 32%, insurance 31%, SME 30% (selected)",
    "platform": "No unified profile platform in the source (slide 13 labels are SME delivery methods)",
    "ops": "Telesales and cloud service: 77% of activities, savings of ₽3 billion in 2017 (slide 33)",
    "decision": ["From 2018, the Lifestyle Banking stage (slide 12)", "Essence of the stage: slides 11, 13 and 27", "The source has no decision to launch or close a product"]
  }
}
```

Limits that fit the slide: title under 70 characters; touch under 110; each role's products under 90 (about four short lines); each metric value under 70; transfer under 230; platform under 100; ops under 100; decision up to four items under 60. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/product-ecosystem-map.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's map, role list or description and check it against the common mistakes in card.md:

1. The ecosystem exists only by name: industry showcases or a super app without a shared profile and data transfer.
2. A shared login is taken for transfer value: authorization only saves registration, the value comes from transactions and context.
3. One role per product, although a product may be Value and Profit at once (debit card versus credit card).
4. A loss-making product is closed by ordinary portfolio rules, without looking at its input to engagement and retention.
5. A role has no metric, or the metric has no current value.
6. Hypotheses are presented as facts: PAF calls the answer about the bundle subscription a hypothesis and gives the effects of the ecosystem (CAC, retention, adoption) without measurements.

Items 2, 5 and 6 usually cannot be judged from a role list: ask which data actually moves between products, which metrics are tracked, and where the effects come from. Additional advice, outside the checklist: mention if Lead, Profit or Retention products are missing, or if there is no decision with a check metric. Report findings as a numbered list: what is wrong, why it matters, the concrete change to the map. End with a verdict: "map manages the ecosystem", "works after changes" or "not an ecosystem yet: start with the platform and data transfer".

Example: a bank lists a debit card, a mortgage and a travel app as "Value" and says all are linked by one login. Findings: item 2 — a login is not transfer value, name data that moves between products; item 3 — the mortgage earns, add Profit; item 5 — no metrics. Verdict: "works after changes".
