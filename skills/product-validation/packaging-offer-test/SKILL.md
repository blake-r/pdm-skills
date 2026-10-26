---
name: packaging-offer-test
description: Plan or review an offer test through "packaging" - checking a value-proposition hypothesis by showing an ad, brochure or box mock-up of a product that does not exist yet and measuring the share of people who react - and produce a one-slide test card. Use when the user must choose between wordings of an offer, headline, title or promise before building anything.
---

# Packaging offer test (advertisement / brochure / packaging)

The definition, steps, the worked case (title and subtitle of a book tested with search ads) and its limits are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants to design an offer test, **review** when the user brings a finished plan or results and wants them checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the idea and the value-proposition hypothesis: who needs what and why;
- 2-4 candidate wordings of the offer (if the user has one, help write the others);
- the audience and where it can be reached: search ads, social ads, a stand, a meeting;
- the carrier: ad, brochure or box mock-up, and the non-binding action (click, tick, visit a site);
- budget and time, the target conversion and how many views are needed.

If the user wants to learn whether people will pay or whether the solution works, say that the test measures only how attractive the wording is (card.md) and ask what they want to prove. Do not invent numbers: mark unknown values as "not in source" or "unknown".

### 2. Hypothesis and measure

Write the hypothesis as: customers [group] need [benefit], and offer [text] will attract them. Choose one measure: conversion from view to click or to a mark of interest. Set the threshold and the number of views before launch and say that this is the author's advice from card.md, not a rule of the source.

### 3. Offers and packaging

Write 2-4 variants of one idea and change one variable at a time. Describe the carrier and what stands on it. Warn that one variant alone can reject a good idea (PAF calls this a type I error; usually it is a false negative; author's note). Split the audience into groups to read results by group.

### 4. Reading the result and the decision

Explain how to compute conversion per variant and per group, compare it with the threshold and choose: check the solution itself, change the wording or the group, or stop. Mention the cost of a click against the price of the product.

### 5. Show, then write

Show the card in chat first as a table by template blocks: title, hypothesis, audience and channel, packaging, non-binding action, up to four offer rows (offer, views, responses, conversion), threshold and volume (set before launch; if it was not set, say so), result, decision. Write a file only after the user confirms. Ask for the output path (default `packaging-offer-test-<idea>.pptx` in the working directory). Save the data as JSON. The example is the book case from card.md; what the source does not give says "not in source"; unused table cells get "—" (null would leave an empty bordered row):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Book title, IT readers, IT Revolution, 2012",
    "hypothesis": "The title \"The Phoenix Project\" will attract IT-professional readers more strongly than the working title \"When IT Fails\"",
    "audience": "Google AdWords: search queries of five reader groups by characters of the novel (\"agile\", \"ITIL\", \"it audit\" and others)",
    "pack": "Two Google ads: title plus a placeholder subtitle \"Creating Breakthrough Performance\"",
    "action": "Click on the ad, go to the thank-you page",
    "o1": "When IT Fails: Creating Breakthrough Performance",
    "v1": "not in source",
    "a1": "not in source",
    "r1": "not in source",
    "o2": "The Phoenix Project: Creating Breakthrough Performance",
    "v2": "not in source",
    "a2": "not in source",
    "r2": "not in source",
    "o3": "Stage 2: about 8 subtitles with the title \"The Phoenix Project\"",
    "v3": "~218k",
    "a3": "86 clicks",
    "r3": "~0.04%",
    "o4": "—",
    "v4": "—",
    "a4": "—",
    "r4": "—",
    "threshold": "Not in source: no threshold set. Stage 1 per day: ~150k views, 82 clicks, $170, CTR below 0.2%",
    "result": "The title \"The Phoenix Project\" led roughly 2:1; the security group chose \"When IT Fails\". A click cost $2.25 on average",
    "decision": "Title \"The Phoenix Project\", subtitle \"Helping Your Business Win\". Advertising as a sales channel for a $9.95 book probably will not pay off"
  }
}
```

Limits that fit the rendered slide: title under 60 characters; hypothesis under 130; audience, pack and action under 110 each; offers (o1..o4) under 65; views and responses (v, a) under 20; conversion (r) under 16; threshold, result and decision under 190. A list of strings becomes lines. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/packaging-offer-test.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's plan or results and check them against the common mistakes in card.md:

1. One offer only, and a low click is read as "the idea is not needed".
2. No threshold before launch, so any number can be explained afterwards.
3. Only the total is read, and differences between audience groups are hidden.
4. A click is taken for demand or for readiness to pay.
5. Several elements (title, subtitle, picture, audience) changed at once, so the winner's cause is unknown.
6. The cost of a click is not counted against the price of the product.

Items 2 and 6 cannot be judged from a description alone: ask when the threshold was set and what a click cost. Report findings as a numbered list: what is wrong, why it distorts the result, the concrete change. Also check that the hypothesis names a group and a benefit, that views are enough to tell variants apart, and that a decision (check the solution, change, stop) is written. End with a verdict: "result can be trusted", "trust after changes" or "run the test again".

Example: one ad "Save on transfers", 40 clicks from 5 000 views, the user writes "no demand". Findings: item 1 - a single wording, write 2-3 variants of the same idea; item 2 - ask for the threshold set before launch; item 3 - read clicks by audience group. Verdict: "run the test again".
