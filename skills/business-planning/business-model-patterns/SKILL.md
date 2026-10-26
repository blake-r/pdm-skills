---
name: business-model-patterns
description: Apply a business model pattern (St. Gallen Business Model Navigator, 55 patterns such as Flat Rate, Razor and Blade, Freemium, Subscription, Cross Selling) to a company's model — compare the model before and after along Who, What, How, Value, and produce a one-slide pattern sheet with a decision — or review an existing pattern analysis. Use when the user looks for a new way to earn money, wants to test an idea like "what if we sold by subscription", or has a pattern analysis to check.
---

# Business Model Patterns

The theory, the four dimensions, steps, limits and a worked case (Amazon Prime, Flat Rate) are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants to try a pattern on a model, **review** when the user brings a finished pattern analysis.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the company and product, the customer and who pays;
- the current model by Who, What, How, Value, and what blocks growth;
- which pattern the user has in mind; if none, propose two or three (one near, one far from their industry) and say the user chooses;
- known numbers for the "before" state and their sources.

Do not invent numbers or company examples. The pattern name, the number in the 55-pattern list and its example companies must come from the St. Gallen working paper (link in card.md); if you cannot check them, say so and write "Not described in the sources" in the field.

### 2. Compare along four dimensions

For the chosen pattern write what changes in Who, What, How, Value, before and after. Where the source gives nothing, write the string "Not described in the sources" in the cell, never null or an empty cell.

### 3. Consistency, decision, check

Check fit with the company's competencies, competitors and the customer's perceived value. Formulate one decision with a measurable assumption and a date, and a pilot with real customers. Do not present a business case as proven.

### 4. Show, then write

Show the sheet in chat first as a table by template blocks: title, pattern card, four dimension rows (before and after), decision, check and risks. Write a file only after the user confirms. Ask for the output path (default `business-model-patterns-<company>.pptx`). The example is the Amazon Prime case from card.md; where the source gives nothing the cell says "Not described in the sources":

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Amazon, Prime program, February 2005",
    "pattern": "#15 Flat Rate",
    "logic": "A single fee for the service regardless of usage: simpler for the customer, a steady revenue stream for the company",
    "examples": "SBB 1898, Buckaroo Buffet 1946, Sandals Resorts 1981, Netflix 1999, Next Issue Media 2011",
    "now_who": "Amazon.com buyers",
    "new_who": "Not changed (Amazon.com buyers)",
    "now_what": "Delivery is paid, free with promotions",
    "new_what": "Unlimited free two-day delivery on more than a million items; next day for $3.99",
    "now_how": "Not described in the sources",
    "new_how": "Not described in the sources; rising delivery costs are a consequence, see Value",
    "now_value": "Q1 2004: delivery revenue $94 million, expenses $137 million, loss $43 million",
    "new_value": "Fee $79 per year; Q1 2005, Prime was in effect since February: $108 million, $163 million, loss $55 million",
    "decision": ["Launch Prime at $79 per year", "The sources do not name success metrics or timing", "The sources do not mention a pilot"],
    "check": ["Fortune, 10 years later: $538 vs $320 a year, RBC self-assessment", "Delivery losses ≥ $1 billion per year — Forrester analyst estimate", "The comparison is retrospective, reconstructed from the sources"]
  }
}
```

Limits that fit the slide: title under 60 characters; pattern under 35; logic under 150; examples under 110; each of the eight before/after cells under 130; decision up to three items under 70; check up to four items under 70. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/business-model-patterns.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Check the user's pattern analysis against the common mistakes in card.md:

1. Nobody counts the load of unlimited use: heavy users cost more than light ones (our conclusion, not from the source).
2. Only the price changed: it is not described what the pattern changes in What (our conclusion, not from the source).
3. A business case is computed before a pilot.
4. Others' success is taken as a guarantee: no fit with the company's competencies and customer value.
5. An analyst's estimate or a survey self-report is presented as company data.

Items 3 and 4 usually cannot be judged from the text alone: ask whether a pilot is planned and what the fit rests on. Also check that the pattern name and examples match the working paper, and that the decision has a measurable assumption and a date. Report findings as a numbered list: what is wrong, why it matters, the concrete change. End with a verdict: "ready for a pilot", "works after changes" or "start with the current model first".

Example: "We add a subscription, price is 20% lower, margin will be 15%." Findings: item 2 — only the price is described; item 3 — the 15% margin is computed without a pilot; ask about item 1. Verdict: "works after changes".
