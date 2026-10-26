---
name: morphological-analysis
description: Generate and choose product, feature, pricing-plan or business-model variants with morphological analysis (Zwicky's morphological box) - split the object into independent properties, list values for each, drop incompatible or unfit values with a reason, assemble combinations of one value per property, pick by stated criteria, and produce a one-slide PPTX, or review an existing morphological table. Use when a team rebuilds a product, plan line-up or channel, keeps circling two or three familiar options, or needs to show how variants differ.
---

# Morphological Analysis

The theory, steps, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings an object to rebuild, **review** when the user brings a finished table or a decision drawn from one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the object: a product, plan line-up, feature or channel, and whom it is for;
- the goal of the search: what the new variants should achieve;
- the constraints: budget, regulation, technology, partners;
- what is known about customers and competitors, with sources.

### 2. Properties

Propose four to six properties that do not depend on each other and matter to the customer or the business. If two properties move together (price and plan level), merge them and say why.

### 3. Values

For each property list two to four values: the current one, those seen at competitors, and at least one unusual value. Mark values taken from the user's facts and those you propose as ideas. Do not invent competitors' offers.

### 4. Drop

Mark incompatible pairs and drop values that fail the goal, the cost or the constraints. Write each reason in one phrase.

### 5. Combine and choose

Assemble two to four meaningful combinations, one value per property, including at least one unfamiliar combination; a property may stay unset if the variant does not need it. Agree the criteria with the user, compare the combinations against them and choose. Say how to check the choice: the metric, the expected result and the date. Do not promise effects.

### 6. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, up to five properties with up to four values each, the combinations, the dropped values and the decision. Write a file only after the user confirms. Ask for the output path (default `morphological-<object>.pptx` in the working directory). Save the data as JSON (the example is the Monzo case from card.md; `£15, previous tariff` and `Travel, previous tariff` are past values shown for comparison):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Bank paid plans: new line-up",
    "prop1": "Price per month",
    "v1_1": "£3", "v1_2": "£7", "v1_3": "from £17", "v1_4": "£15, previous tariff",
    "prop2": "Money management",
    "v2_1": "Basic", "v2_2": "Extended: other banks, cards",
    "prop3": "Savings",
    "v3_1": "Standard rate", "v3_2": "Better rate 3.25%",
    "prop4": "Perks",
    "v4_1": "None", "v4_2": "Greggs bakery items, train discount", "v4_3": "Business lounges, cashback on transfers",
    "prop5": "Insurance",
    "v5_1": "None", "v5_2": "Travel, previous tariff", "v5_3": "Phone, travel, roadside assistance",
    "combos": ["Extra = 1.1 + 2.2 + 3.1 + 4.1 + 5.1", "Perks = 1.2 + 2.2 + 3.2 + 4.2 + 5.1", "Max = 1.3 + 2.2 + 3.2 + 4.2 + 5.3"],
    "excluded": ["Metal card: expensive, better to offer varied benefits", "Business lounges and cashback: only a small share of customers got the benefit"],
    "decision": ["Three plans instead of two", "Check: paying customers over a year"]
  }
}
```

Keys are `prop1`…`prop5` and `v<row>_<col>` with up to four values per row; leave unused keys out (the script leaves them empty and names them in a warning). Keep the title under 50 characters, each property under 25, each value under 35, the combinations and the decision to four items of under 40 characters each, the dropped values to three items of under 80 characters; list the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/morphological-analysis.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's table in any form and check it against the common mistakes in card.md:

1. The object and the goal are stated.
2. Properties do not depend on each other.
3. Values go beyond the familiar ones.
4. Incompatible values are dropped before combining, each with a reason.
5. Combinations take one value per property and include at least one unfamiliar one.
6. The choice follows stated criteria and has a check: metric, expected result, date.

Item 2 often needs the user's knowledge of the product: ask instead of reporting a finding when unsure. Report findings as a numbered list: property or combination, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
