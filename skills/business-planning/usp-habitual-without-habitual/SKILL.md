---
name: usp-habitual-without-habitual
description: Build or check a USP (unique selling proposition) phrase in the form "familiar thing without a familiar element" (for example "a bank without branches"), and produce a one-slide template, or review an existing phrase of this kind. Use when someone wants to differentiate by removing something customers consider obligatory, or asks to check such a slogan.
---

# USP "familiar without familiar"

The theory, the limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language. The author and the original source of the formula are unknown; do not attribute it to anyone.

Pick the mode from the request: **do** when the user needs a phrase, **review** when the user shows an existing phrase and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the offer and the customer: who buys, what the product or service is;
- the category as the customer names it;
- the familiar element the offer removes, and whether it is really removed and not hidden;
- how the customer gets what that element gave (replacement);
- why the element bothered customers and where this was heard (interviews, support, data);
- what tasks the element solved and what rules or limits apply;
- where the phrase will stand (page, ad, email).

Do not invent facts, numbers or quotes. Mark what the user did not give as unknown and say what must be checked.

### 2. Two parts and the support

Write the category and the removed element. For each give one sentence of check: is it the customer's word, is the element truly gone. Then write the replacement and the reason (mark as unknown if there is no evidence).

### 3. Phrase

Join into "category without element". Give two or three wordings and point to the best one. It must be clear without explanation. Do not claim that the phrase differs from competitors or that customers want it: the formula does not prove either.

### 4. Risk, check, decision

Name the tasks the removed element solved and how they are covered, what will be counted after launch (how customers complete those tasks, whether they value the removal) and when it is reviewed. State the decision to take and what data is missing.

### 5. Show, then write

Show the filling in chat first as a table by template blocks: title, category, removed, replacement, reason, phrase, risk, check, decision. Write a file only after the user confirms. Ask for the output path (default `usp-habitual-without-habitual-<name>.pptx` in the working directory). Save the data as JSON. The example is the Tinkoff Credit Systems case from card.md; what the source does not give is null:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Tinkoff Credit Systems (Russia): Retail Banker International interview, 23.10.2013",
    "habit": "Bank: license, credit cards and payments",
    "removed": "Branches",
    "replacement": ["1000 couriers in 600 cities (per the interview text)", "Direct mail: the main acquisition channel in 2007", "Online acquisition"],
    "reason": ["Wide reach without the cost of maintaining branches", "What branches bothered customers about: not stated"],
    "phrase": "A bank without branches (phrase reconstructed from the interview, not an ad text)",
    "risk": ["Deposits require an in-person meeting and signature", "People won't give money to a bank they cannot see"],
    "check": ["Customer testing: not in the source", "Share of deposits attracted online: not in the source"],
    "decision": "Online and couriers chosen for deposits; $977 million in less than 4 years after the start of online deposits; no dates"
  }
}
```

Limits that fit the rendered slide: title under 90 characters; habit and removed up to three lines under 55 characters each; replacement and reason up to three lines under 55; phrase under 110; risk and check up to three lines under 55; decision under 130. A list of strings becomes lines, one thought per item. A null value leaves the placeholder empty, so write "not in the source" in the text where the user needs the gap shown. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/usp-habitual-without-habitual.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's phrase and its context and check it against the common mistakes in card.md:

1. The removed element is something the customer needs.
2. The phrase says only what is absent, not what the customer gets.
3. The element is hidden, not removed.
4. The removal runs into rules, and the promise cannot be kept.
5. A difference is taken for an advantage: nobody checked that customers value the removal.
6. There is no check after launch: nobody counts how customers cover the tasks of the removed element.

Items 3 to 6 usually cannot be judged from the phrase alone: ask what the element did, what rules apply, what customers said, who counts what after launch, instead of reporting a finding. Report findings as a numbered list: what is wrong, why it matters, the concrete rewrite. End with a verdict: "phrase holds", "works after changes" or "needs customer data first".

Example: "Bank without the usual". Findings: item 2 — no removed element is named, so nothing is promised; item 5 — no sign that customers asked for it. Verdict: "needs customer data first".
