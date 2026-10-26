---
name: storytelling
description: Build or review the story structure of a product pitch or launch talk using Nancy Duarte's Presentation Sparkline - alternating "what is" and "what could be", a call to action at the end and a "new bliss" - and produce a one-slide story map. Use when someone prepares a pitch, product presentation, launch talk or initiative defence and needs it to persuade, or wants an existing talk checked.
---

# Storytelling

In card.md the points marked "Card author's conclusion" are the card author's conclusions, not Duarte's; say so when you rely on them. The theory, limits and the worked Apple Pay case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user is preparing a story about a product or idea, **review** when the user brings a ready outline or text and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the audience: who listens, what keeps them up at night, what they already tried without success, what is at stake if nothing changes;
- the decision the speaker wants from them (it becomes the call to action);
- the facts of today: numbers or observations the audience can check, with sources;
- what the product changes, as concrete pairs to today's facts;
- the setting and length: pitch, launch, internal defence.

If the user has no verifiable facts for "what is", say so and ask for them; do not invent figures. If the goal is only to hand over data (a spec, a report), say that the card does not fit.

### 2. Beginning

Write one fact about the world today and set it against the world with the product. Make the gap as wide as the facts allow.

### 3. Middle

Write up to four pairs "today - with the product" and alternate them. A side without a fact stays empty. Do not put all the problems first and all the solutions after.

### 4. End

Put the call to action last. Then one sentence describing the world once the problem is solved (the new bliss), not a list of features.

### 5. Self-check

Mark each beat as "what is" or "what could be". There must be alternation, a gap at the start and the call at the very end. Say what is missing: for example a source for a figure.

### 6. Show, then write

Show the story in chat first as a table plus the order of beats for the line: audience, beginning, four middle pairs, call, new bliss, decision. Write a file only after the user confirms. Ask for the output path (default `storytelling-<topic>.pptx`). Save the data as JSON. The example is the Apple Pay talk from card.md; the "decision" field is the launch that followed:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Apple Pay: presentation on 9 September 2014",
    "audience": "Customers and partners: banks, networks, shops. A card is easy to lose, payment is insecure. A mobile wallet has long failed to arrive",
    "a1": "In the US $12 billion a day, more than 200 million transactions a day; the magnetic stripe is five decades old",
    "b1": "Cook's vision: replace the wallet, starting with payments",
    "a2": "The mobile wallet (New York Times) was long considered a matter of the near future, but it stayed elusive",
    "b2": "iPhone 6 with NFC (contactless communication) and Touch ID (fingerprint sensor)",
    "a3": "A card is easy to lose, the cashier sees the name and number",
    "b3": "Secure Element (chip for payment data); one-time number; Apple does not know what was bought",
    "a4": "Online in the US: more than $1 billion a day through long forms",
    "b4": "Payment with one touch",
    "a5": null,
    "b5": "More than 220,000 contactless payment points; banks — more than 80% of US card volume",
    "call": "Launch in the US next month, free iOS 8 update (the iPhone system)",
    "bliss": "Cook: Apple Pay will forever change the way all of us buy things",
    "decision": "Launch in the US on 20.10.2014 with iOS 8.1 (Apple release of 16.10); the case has no data on what persuaded the banks"
  },
  "charts": {
    "sparkline": {
      "categories": ["vision", "figures", "stripe", "NYT", "Apple Pay", "security", "stores", "online", "tap", "call"],
      "series": [{"name": "Story", "values": [1, 0, 0, 0, 1, 1, 1, 0, 1, 1]}]
    }
  }
}
```

The `sparkline` chart is the line of the story: one value per beat in the order the beats are really told, 0 = what is, 1 = what could be; up to 10 beats, category names under 14 characters. It may differ from the order of the table pairs. Limits that fit the rendered slide: title under 60 characters; audience under 170; each a1..a5 and b1..b5 under 90; call and bliss under 130; decision under 150. Put the rest in chat. Empty cells: `null`, not `""`. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/storytelling.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's outline, text or slides and check them against the common mistakes in card.md:

1. The story is only about the product: there is no "what is" side, so no gap and no reason to act.
2. (author's conclusion in card.md) "What is" is neutral: the status quo is described without a cost to the audience.
3. One switch instead of alternation: all the problem first, then all the solution.
4. The call to action is not at the end: it is missing or comes in the middle.
5. (author's conclusion) The end is a list of features, with no picture of the world after the problem is solved.
6. The pain is not verifiable: figures without a source, or sources only from the company itself.
7. (author's conclusion) Structure instead of proof: the story is smooth, but nothing shows that the solution works.

Items 6 and 7 cannot be judged from structure alone: ask where the figures come from and what shows the solution works. Report findings as a numbered list: what is wrong, why it weakens the story, the concrete fix. End with a verdict: "story persuades", "works after changes" or "needs facts and a decision first".

Example: a pitch opens with a feature list, mentions the user's problem once at the end and finishes with "thank you". Findings: item 1 and 2, no "what is" in the beginning, add a checkable fact and set the product against it; item 3, alternate pairs in the middle; item 4, the ask is missing, state the decision wanted; item 5, finish with the world after the solution. Verdict: "needs facts and a decision first".
