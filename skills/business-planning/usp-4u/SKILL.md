---
name: usp-4u
description: Build or check a USP (unique selling proposition) phrase against the 4U checklist (useful, unique, ultra-specific, urgent) and produce a one-slide template, or review an existing headline, ad line or subject line. Use when someone needs a headline with a measurable promise, wants to know which of the four features a draft lacks, or asks to check a slogan.
---

# USP 4U

The theory, the limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user needs a phrase, **review** when the user shows an existing phrase and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the offer and the customer: who buys, what the product or service is;
- the benefit for the customer, in the customer's words;
- the mechanism: what in the product or model produces the benefit;
- a number (percent, money, pieces, minutes), its data source and the conditions under which it holds ("on average" or "up to");
- a real deadline or reason to act now, if there is one;
- where the phrase will stand (page, ad, email).

Do not invent numbers, terms or deadlines. Mark what the user did not give as unknown and say what must be checked. If the user's "unique" means "different from competitors" rather than "how the benefit is achieved", name which meaning is used (card.md, limits).

### 2. Four features

For each of the four features write one sentence: what the draft says, and one sentence of check (is the number confirmed by data, is the deadline real). Write an absent feature as an explicit statement, not an empty block; urgency may legitimately be absent.

### 3. Phrase

Join the features into one phrase. Give two or three wordings and point to the best one. Do not claim that the phrase differs from competitors: the checklist does not prove it.

### 4. Gaps, check, decision

Name what is missing or unconfirmed, what will be counted after publication and when it is reviewed. State the decision to take and what data is missing.

### 5. Show, then write

Show the filling in chat first as a table by template blocks: title, useful, unique, specific, urgent, phrase, risk, check, decision. Write a file only after the user confirms. Ask for the output path (default `usp-4u-<name>.pptx` in the working directory). Save the data as JSON. The example is the Wise case from card.md; what the source does not give is stated in words (the phrase is our reconstruction from the headline, as the source has no ad line):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Wise (fintech, transfers): blog post dated 21.09.2020; 4U breakdown is ours",
    "useful": "Transfers are cheaper",
    "unique": ["More customers, higher efficiency", "Faster transfers, lower costs"],
    "specific": ["76% of customers; avg -15%, up to -30%", "£1000 to IDR: fee £5.21 → £3.62"],
    "urgent": "No urgency: no deadline in the source",
    "phrase": "Transfers are cheaper for 76% of customers: on average by 15%, in some cases up to 30%",
    "risk": ["No urgency", "No methodology for the '8x cheaper than a bank' claim"],
    "check": ["The source does not name verification metrics;", "To set: response to the phrase, review date"],
    "decision": "Transfer prices cut from 21.09.2020 (USD, GBP and a number of currencies); the phrase is reconstructed from the headline"
  }
}
```

Limits that fit the rendered slide: title under 90 characters; useful, unique, specific and urgent up to three lines under 40 characters each; phrase under 110 characters; risk and check up to three lines under 55; decision under 130. A list of strings becomes lines, one thought per item. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/usp-4u.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's phrase and its context and check it against the common mistakes in card.md:

1. A number without grounds: no data, conditions or "average/up to" distinction.
2. A benefit without a mechanism: nothing says how it is achieved.
3. An invented urgency: a deadline that is not real or is always extended.
4. All four features forced into one phrase that does not read in one breath.
5. The meanings of "unique" are mixed: mechanism versus difference from others.
6. There is no check after publication: nobody counts what drove the response.

Items 1, 3 and 6 usually cannot be judged from the phrase alone: ask where the number comes from, whether the deadline is real and who counts the response, instead of reporting a finding. Report findings as a numbered list: what is wrong, why it matters, the concrete rewrite. End with a verdict: "phrase holds", "works after changes" or "needs data first".

Example: "The best service, order now!". Findings: item 1 — no number; item 2 — no mechanism; item 3 — "now" has no real deadline. Verdict: "needs data first".
