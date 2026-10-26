---
name: usp-maxwell-formula
description: Build or check a USP (unique selling proposition) phrase by the Dane Maxwell formula "end result + time to get it + answer to the customer's objection", and produce a one-slide template, or review an existing USP phrase. Use when someone needs a headline, ad line or landing-page promise, wants to add a time and a guarantee to a vague promise, or asks to check a slogan.
---

# USP Maxwell formula

The theory, the limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user needs a phrase, **review** when the user shows an existing phrase and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the offer and the customer: who buys, what the product or service is;
- the end result the customer wants, in the customer's words;
- the time in which the result can be delivered, and how often that time is really kept (data, not hope);
- the main objection or fear: what stops the customer from believing or buying, and where it was heard (interviews, support, reviews);
- what the company can promise on the objection: remove the unpleasant part or take the risk (guarantee, refund), and what it costs;
- where the phrase will stand (page, ad, email).

Do not invent numbers, terms or guarantees. Mark what the user did not give as unknown and say what must be checked.

### 2. Three parts

Write the result, the time as a number, the answer to the objection. For each part give one sentence of check: is it the customer's word, is the number confirmed by data, is the objection real. Say if a guarantee has no cost estimate.

### 3. Phrase

Join the parts into one phrase. Give two or three wordings and point to the best one. Do not claim that the phrase differs from competitors: the formula does not prove it.

### 4. Risk, check, decision

Name what can break the promise (weather, peak load, limits of the guarantee), what will be counted after launch (share of misses, share of guarantee payouts) and when it is reviewed. State the decision to take and what data is missing.

### 5. Show, then write

Show the filling in chat first as a table by template blocks: title, result, time, objection, phrase, risk, check, decision. Write a file only after the user confirms. Ask for the output path (default `usp-maxwell-formula-<name>.pptx` in the working directory). Save the data as JSON. The example is the Checkers Sixty60 case from card.md; what the source does not give is null:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Checkers Sixty60 (Shoprite, South Africa): app delivery, release 27.03.2023",
    "result": "Products the buyer wants",
    "time": ["Delivery in 60 minutes, fee R35", "Share of deliveries kept on time: not given"],
    "objection": ["Difficulty from the release: traffic, rain", "Answer (our conclusion): free if late by more than 30 minutes", "or fewer than 80% of first-choice items delivered"],
    "phrase": "Groceries in 60 minutes, or we refund R35 if we are 30+ minutes late or deliver under 80% of items",
    "risk": ["The R35 fee is returned to the app wallet", "It is spent on orders within a week", "Guarantee costs not given"],
    "check": ["Late deliveries and payouts: not in the release", "Sales after launch: not in the release"],
    "decision": "Guarantee introduced 27.03.2023; phrase reconstructed from the release, slogan \"It's great, or it's free\"; no result"
  }
}
```

Limits that fit the rendered slide: title under 90 characters; result, time and objection up to three lines under 70 characters each; phrase under 110 characters; risk and check up to three lines under 55; decision under 130. A list of strings becomes lines, one thought per item. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/usp-maxwell-formula.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's phrase and its context and check it against the common mistakes in card.md:

1. Result without a time, or a time without a result.
2. The objection is invented, not taken from customers.
3. The time is taken from the best day, not from the worst conditions.
4. The guarantee is blurred: conditions in small print become a new objection.
5. Three parts are glued into one long phrase that does not read in one breath.
6. There is no check after launch: nobody counts how often the promise is broken.
7. The cost of the guarantee is not counted.

Items 2, 3, 6 and 7 usually cannot be judged from the phrase alone: ask where the objection came from, what share of orders meets the time in bad conditions, who counts the guarantee payouts and what they cost, instead of reporting a finding. Report findings as a numbered list: what is wrong, why it matters, the concrete rewrite. End with a verdict: "phrase holds", "works after changes" or "needs customer data first".

Example: "Fast delivery, best prices". Findings: item 1 — no number and no result; item 2 — no objection is answered; item 4 — no guarantee at all. Verdict: "needs customer data first".
