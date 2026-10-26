---
name: competition-map
description: Map everyone who competes for a product's customer along the steps of the customer's key scenario - direct competitors, indirect competitors, displacers competing for the same money or time, and channel competitors competing for access to the customer - pick the main competitor at each step and what to do about it, and produce a one-slide PPTX; or review an existing competitor map or competitive analysis. Use when entering a market, when customers leave and it is unclear where to, or when the product covers only part of the scenario.
---

# Competition Map

The theory, types, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a product to map, **review** when the user brings a filled map or a competitor list.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and the customer it serves;
- the customer's key scenario, from the first need to the result;
- known competitors and where customers go instead, with sources: churn surveys, interviews, search and traffic data;
- the market and the country.

Do not invent competitors or market shares. If the user has no data on where customers go, name how to find out and mark the map as a draft.

### 2. Scenario

Write the scenario as three to five steps, including steps the product does not cover.

### 3. Competitors by step

For each step, list who else helps the customer through it: companies, services, do-it-yourself solutions.

### 4. Types

Sort each competitor into one type with the questions from card.md: the same problem, the same way, what exactly it competes for. A player can have different types at different steps: name the step.

### 5. Main competitor and action

For each step, name the main competitor, the one customers go to most often, and the action: outflank, cover the step yourself, partner, or accept losing the step.

### 6. Show, then write

Show in chat first: the scenario, the competitors by type as they will appear on the slide, then the main competitor and action per step. Write a file only after the user confirms. Ask for the output path (default `competition-map-<product>.pptx` in the working directory). Save the data as JSON (the example is the Amazon case from card.md):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Amazon: buying a product, 2019",
    "steps": ["Find", "Buy", "Receive"],
    "direct": ["Online stores", "Omnichannel", "Manufacturers"],
    "indirect": ["Offline stores", "Grocery stores"],
    "displace": ["Not named"],
    "channel": ["Search engines", "Price sites", "Social networks", "Portals"],
    "insight": ["Find: search engines → ads in Amazon search", "Buy: assortment, price, delivery"]
  }
}
```

Keep the title under 45 characters and `steps` to five items of under 12 characters. Keep `direct`, `indirect`, `displace` and `channel` to four items of under 16 characters each, `insight` to three items of under 45. List the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/competition-map.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's map or list in any form and check it against the common mistakes in card.md:

1. The map includes indirect competitors, displacers and channel competitors, not only direct ones.
2. The scenario includes the steps the product does not cover.
3. Each step has a main competitor and an action.
4. Displacers competing for the customer's money or time are considered.
5. Types are assigned per step, and sources show where customers actually go.

Report findings as a numbered list: step or type, what is wrong, why it matters for the decision, the concrete fix. End with a verdict: "map is sound", "sound after fixes" or "not enough data".
