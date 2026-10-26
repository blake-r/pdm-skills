---
name: usp-aida
description: Write or check the text of an offer (USP) in the AIDA(s) structure - Attention, Interest, Desire, Action, satisfaction - and produce a one-slide template, or review an existing ad, email, landing-page screen or product-card text. Use when someone needs a multi-sentence offer text, wants to know which step a draft lacks, or asks to check the order of an ad. Not for one-line slogans.
---

# USP AIDA(s)

The theory, the limits, the origin dispute and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language. AIDA here is the structure of an offer text, not a model of how a customer decides.

Pick the mode from the request: **do** when the user needs an offer text, **review** when the user shows an existing text and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the audience and its problem or situation, in the customer's words;
- the mechanism: what in the product produces the benefit;
- a number or proof (percent, money, pieces, minutes) and the data behind it;
- the offer terms: where to act, price, discount, deadline (only real ones);
- what the buyer gets afterwards and what backs it up (return, guarantee, support);
- the channel and the length limit.

Do not invent numbers, terms, deadlines or guarantees. Mark what the user did not give as unknown. If the place fits fewer than five sentences, say so and keep the steps that matter.

### 2. Five steps

Write one sentence per step: attention (the customer's situation), interest (why a solution exists and how it works), desire (what the customer gets, with proof), action (one step with terms), satisfaction (the outcome and what makes the promise keepable). Say which meaning of "s" is used (card.md, limits). Write a missing step as an explicit statement, not an empty block.

### 3. Whole text

Join the sentences into one text in the order of the steps. Give two wordings and point to the best one. Do not claim the structure makes it sell better.

### 4. Gaps, check, decision

Name what is missing or unconfirmed, what will be counted after publication (response, returns, repeat purchases) and when it is reviewed. State the decision and what data is missing.

### 5. Show, then write

Show the filling in chat first as a table by template blocks: title, attention, interest, desire, action, satisfaction, offer, risk, check, decision. Write a file only after the user confirms. Ask for the output path (default `usp-aida-<name>.pptx` in the working directory). Save the data as JSON. The example is the Dollar Shave Club case from card.md; where the source has nothing the text says "not in the source":

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Dollar Shave Club, e-commerce, launch 2012; AIDA(s) breakdown is ours",
    "attention": "not in the source",
    "interest": ["Comparison with $20 a month", "for well-known razor brands"],
    "desire": ["Simple price", "Home delivery"],
    "action": ["Humble Twin: $1 a month", "+ delivery, 5 cartridges", "Executive: $9 + delivery"],
    "satisfaction": "not in the source",
    "offer": "The full text of the offer is not in the sources; not restored",
    "risk": ["Attention and satisfaction are not confirmed", "Structure's effect on the result not measured"],
    "check": ["Source: about 12,000 subscriptions in 48 hours", "There are no step-by-step metrics in the source"],
    "decision": "Launch via a video on 6.03.2012; about 12,000 subscriptions in 48 hours; blades on backorder until May"
  }
}
```

Limits that fit the rendered slide: title under 80 characters; each of attention, interest, desire, action and satisfaction up to four lines under 28 characters; offer under 120; risk and check up to three lines under 55; decision under 130. A list of strings becomes lines, one thought per item. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/usp-aida.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's text and its context and check it against the common mistakes in card.md:

1. There is no attention: the text opens with the company name instead of the customer's situation.
2. Interest has no mechanism: it says a solution exists but not how it works.
3. Desire has no grounds: a number without data and conditions.
4. Two actions at once: the customer is asked to buy, subscribe and call.
5. Satisfaction cannot be kept: the promise has no return, guarantee or support behind it.
6. All five steps are forced into a short text that no longer reads.

Items 3 and 5 usually cannot be judged from the text alone: ask where the number comes from and what backs the promise, instead of reporting a finding. Report findings as a numbered list: what is wrong, why it matters, the concrete rewrite. End with a verdict: "text holds", "works after changes" or "needs data first".

Example: "Best sofas in town! We know how to make your home cozy. Buy now, subscribe to the newsletter and call us. You will be happy." Findings: item 1 — the opening is a claim, not the customer's situation; item 2 — no mechanism; item 4 — three actions. Ask about item 5. Verdict: "works after changes".
