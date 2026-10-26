---
name: technology-adoption-lifecycle
description: Describe who adopts a new technology or product in five groups - innovators, early adopters, early majority, late majority, laggards - and what each group needs, find which group buys now and whether growth is stuck before the mainstream (the chasm), pick one pragmatist niche as a beachhead and the whole product it needs, and produce a one-slide PPTX; or review an existing adoption plan. Use when first customers exist but growth has stalled and it is unclear why the rest do not buy, or when choosing the next segment and what to add to the product for it.
---

# Technology Adoption Lifecycle

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a product and its customers, **review** when the user brings a finished plan.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the technology or product, the market, and who decides on the purchase;
- who bought first, who buys now, who does not buy yet, with numbers and dates if there are any;
- what customers say they lack, from interviews, lost deals or support requests;
- the candidate segments for the next step and what the user knows about each.

Do not invent customers or numbers. A group with nothing known stays marked "no data".

### 2. Describe the groups

For each of the five groups, write who they are in this market and what they need to buy. Use the textbook shares only as a rough guide, not as a measurement. Name the group buying now, with the share or count and the date.

### 3. Beachhead and whole product

If growth is stuck before the early majority, propose one pragmatist niche: where the problem hurts most and where customers talk to each other. List what the niche needs beyond the core technology: integrations, support, pricing, guarantees, references. Name the metric and the date that show the beachhead is taken. If there is no sign of a stall, say so and do not force a beachhead.

### 4. Show, then write

Show in chat first: the five groups, where the product is now, the beachhead and the whole product. Write a file only after the user confirms. Ask for the output path (default `technology-adoption-<product>.pptx` in the working directory). Save the data as JSON (the example is the Square case from card.md; the group marking is ours, not Square's):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Square, card acceptance for sellers, US, 2015",
    "innovators": "Small sellers without bank acquiring",
    "early_adopters": "Small business: connected at once, 2.75%",
    "early_majority": "Large sellers from $125k a year",
    "late_majority": "no data",
    "laggards": "no data",
    "now": ["Q4 2014: large sellers — 33% of volume", "Q4 2015: large sellers — 39% of volume"],
    "beachhead": ["Large sellers, no single niche", "Retail, restaurants, services all at once"],
    "whole_product": ["Sales team, individual rates", "Registers for retail and restaurants", "Result: Q4 2019 — 55% of volume"]
  }
}
```

Keep `title` under 50 characters and each group under 45 characters. Keep `now`, `beachhead` and `whole_product` to three items of under 40 characters each; one thought per item, each becomes its own paragraph. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/technology-adoption-lifecycle.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's plan in any form and check it against the common mistakes in card.md:

1. The pitch to the mainstream differs from the pitch to enthusiasts: a ready solution and a reference from a similar customer.
2. One niche is chosen, not all at once.
3. The plan lists the whole product, not only the core technology.
4. Early sales are not taken as proof of mainstream demand.
5. The niche's share has a metric and a check date.

Report findings as a numbered list: what is wrong, why it misleads the decision, the concrete fix. End with a verdict: "plan supports the decision", "supports it after fixes" or "not enough data".
