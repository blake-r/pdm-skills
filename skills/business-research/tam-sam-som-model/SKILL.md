---
name: tam-sam-som-model
description: Size a market in three nested levels - TAM (total addressable market), SAM (serviceable available market) and SOM (serviceable obtainable market) - top-down and bottom-up, with sources and assumptions, and produce a one-slide PPTX with three nested circles; or review an existing market sizing, for example in a pitch deck or business case. Use when deciding whether to enter a market, preparing an investment or budget request, or choosing which segment or country to start with.
---

# TAM / SAM / SOM Model

The theory, levels, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a product and a market to size, **review** when the user brings a finished sizing.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product, the problem it solves and who has this problem;
- the countries, segments and channels the product serves now and plans to serve;
- the horizon for SOM (for example, three years) and the current number of customers, if any;
- data the user already has: industry statistics, prices, average purchase, conversion, with sources.

Do not invent market statistics. If a number is needed and the user has none, name the public source to look it up in, or mark the number as an assumption and say how to check it.

### 2. Unit

Choose one unit for all three levels: money per year, or purchases, trips, payments per year.

### 3. TAM, SAM, SOM

Compute top-down: TAM from industry statistics or from the number of people with the problem times their spending; SAM by removing countries, segments and channels the product does not serve; SOM as the share of SAM the company can take over the horizon, from its acquisition pace, budget and competitors' shares. Show each calculation as a chain of multiplications with sources.

### 4. Bottom-up check

Compute customers × frequency × average purchase over the horizon and compare with SOM. If they differ several times over, find the wrong assumption before going on.

### 5. Compare with the goal

Compare SOM over the horizon with the user's goal: the revenue plan or the amount requested. If SOM is below the goal, suggest another segment, channel or horizon, or dropping the market. If it is above but not backed by an acquisition pace, say it must not be promised as a plan.

### 6. Show, then write

Show in chat first: the three values, the calculation behind each, the comparison with the goal, then the sources and assumptions. Write a file only after the user confirms. Ask for the output path (default `market-size-<product>.pptx` in the working directory). Save the data as JSON (the example is the Airbnb case from card.md):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "AirBed&Breakfast: travel market, 2008",
    "tam": "1.9+ billion trips",
    "sam": "532 million trips",
    "som": "10.6 million trips",
    "tam_how": ["All trips booked worldwide"],
    "sam_how": ["Budget and online trips"],
    "som_how": ["Trips via AirBed&Breakfast", "× $20 commission = $200 million for 2008–2011"],
    "sources": ["'Market Size' and 'Business Model' slides of the first deck", "10% commission, $70 per night, three nights"]
  }
}
```

Keep the title under 45 characters, `tam` and `sam` under 25, `som` under 20. Keep `tam_how`, `sam_how` and `som_how` to three items of under 70 characters, `sources` to four items of under 80. List the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/tam-sam-som-model.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's sizing in any form and check it against the common mistakes in card.md:

1. TAM counts those who have the problem, not everyone who could theoretically pay.
2. All three levels use the same unit.
3. SOM follows from an acquisition calculation, not from "we will take 1%".
4. Every number has a source, and SOM has a horizon.
5. The top-down SOM agrees with the bottom-up check.
6. SOM is compared with the goal, and the decision follows from the gap.

Report findings as a numbered list: level, what is wrong, why it matters for the decision, the concrete fix. End with a verdict: "sizing is sound", "sound after fixes" or "not enough data".
