---
name: metric-pyramid
description: Break a product's main metric into a top-down tree (North Star, Key metrics whose product equals the level above, Traction marks on the Key metrics that move the top most, Pulse user-behaviour metrics, plus the levers the team controls), tie ideas to branches, and produce a one-slide PPTX, or review an existing metric tree. Use when a team must agree on the metric it works on and the path to move it, filter ideas that do not affect the goal, or find which component moved the main metric.
---

# Metric Pyramid

The theory, levels, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a product and its data, **review** when the user brings a metric tree or a decision drawn from one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and its main goal;
- the metrics the team already tracks, with current values for several periods and the source;
- the ideas or initiatives the tree should help sort, if any.

Do not invent numbers. Leave a missing value as "N/A" and say how to get it. Numbers in the examples of this file are not data for the user's product. If this skill runs inside pdm-brief, the questions above are answered by pdm-brief's fallback.

### 2. Choose the top

Propose the North Star: a metric that reflects value for the customer and grows with the business. If the user picks revenue or turnover, say that it reflects customer value only indirectly and keep it only if the user agrees.

### 3. Decompose

Split the top into two to four Key metrics whose product equals it, for example active buyers × orders per buyer × average order value. Check the formula on the user's numbers and show the check; a gap of a few percent from rounding or from components counted over different windows is acceptable if you name it. Where components influence each other (more buyers may lower the average order), say so. Go one level deeper only where the team cannot act on a Key metric directly.

### 4. Traction and Pulse

Traction is a mark on Key metrics, not a separate level. Mark two or three and explain the choice from the data: the growth of the top equals the product of the components' growth, (1 + g) = Π(1 + gᵢ), and a component's share of the shift is ln(1 + gᵢ) / ln(1 + g). Show the shares; name a falling component as the cost of the others' growth. Under each Key metric list the Pulse metrics: user behaviour such as passing the steps to purchase, the share of users of a feature, averages. List the levers the team controls separately, in the decision.

### 5. Decide

Tie each idea to the branch it should move; name the ideas that move nothing. Say which metric the team bets on, what it changes, the expected shift and when to check it. Do not promise effects.

### 6. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, the North Star, three Key metrics, three Pulse blocks, Traction and the decision. Write a file only after the user confirms. Ask for the output path (default `metric-pyramid-<product>.pptx` in the working directory). Save the data as JSON. The JSON below shows the format only: its values are the Ozon case from card.md, not data for this pyramid; use them only when the user explicitly asks to see an example:

```json
{
  "text": {
    "title": "Ozon 2021: GMV growth",
    "nsm": ["GMV incl. services", "RUB 445 bn, ×2.26"],
    "key1": ["Active buyers", "25 million, ×1.81"],
    "key2": ["Orders per buyer", "8.5 in Q4, +60%"],
    "key3": ["Turnover per order", "RUB 2,020, −24%"],
    "pulse1": ["No data in the source"],
    "pulse2": ["Ozon card holders: 4× in 2021"],
    "pulse3": ["No data in the source"],
    "traction": ["Buyers: ~70% of growth", "Frequency: ~60% of growth"],
    "decision": ["Bet: frequency (our reading)", "Levers: range, warehouses", "Check: frequency each quarter"]
  }
}
```

The example is the Ozon case from card.md. The company published no pyramid, no Pulse by branch and no stated decision, so the Pulse blocks say so and the bet is marked as a reading; say this in chat.

The template has exactly three Key metrics. If the decomposition has two, leave `key3` and `pulse3` out (the script leaves them empty and names them in a warning) and say so in chat; if it has four, merge two or list the fourth in chat. Keep the North Star and each Key metric to two lines of under 25 characters, each Pulse block to four items of under 40 characters, Traction and the decision to four items of under 35 characters each, and the title to one line of under 60 characters; list the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/metric-pyramid.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's tree in any form and check it against the common mistakes in card.md:

1. The top reflects value for the customer, not just what is easy to count.
2. Each level multiplies into the level above; the formula holds on real numbers.
3. Influences between components are noted where they exist.
4. Traction marks two or three Key metrics, chosen from their share of the shift in the top.
5. Pulse metrics describe user behaviour and sit under the Key metric they drive; levers are listed separately.
6. Every idea is tied to a branch; ideas that move nothing are named.
7. The decision names the metric, the expected shift and the date to check.

Item 1 often needs the user's knowledge of the product: ask instead of reporting a finding. Report findings as a numbered list: level or branch, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
