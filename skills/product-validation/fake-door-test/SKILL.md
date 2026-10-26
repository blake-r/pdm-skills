---
name: fake-door-test
description: Plan or review a fake door test - checking a value-proposition hypothesis inside an existing product by adding a button, menu item or banner that looks like a ready feature but leads to a stub, then measuring the share of people who click - and produce a one-slide test card. Use when the user wants to know whether users want a feature before building it, asks about a fake door, painted door or "fake button" test, wants to measure demand with a stub button or banner in a live product, or brings click-through results of such a test to read.
---

# Fake door test

The definition, steps, limits, the worked case (language switcher at Notino) and the common mistakes are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants to design a test, **review** when the user brings a finished plan or results and wants them checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product, the feature idea and the benefit it promises: who needs what and why;
- the screen where users would look for the feature, and the audience (which users, what share of traffic);
- how many users see the screen per week, and the planned test length;
- what the click shows (stub text) and whether a contact is requested;
- the main product metric to watch during the test;
- the decision rule: at what share of clicks the team builds, repeats or stops.

If the product has no live traffic, say the test needs it (card.md) and ask what the user wants to learn. If the user wants to know whether people will pay, say that a click measures interest only. Do not invent numbers: mark unknown values as "not in source" or "unknown".

### 2. Hypothesis and threshold

Write the hypothesis as: users [segment] need [benefit]; at least X% will click. Set the threshold and the number of views before launch and say that numbers such as the rough 800 views for a 5% share with a +-1.5 point margin (95% confidence interval, normal approximation; about 577 views for the 3.5% share of the case) are the card author's advice, not a rule of the source. Name three zones: build, repeat with another wording or segment, stop.

### 3. Element and stub

Describe the element and its place so that it looks like the real feature but does not claim that it works. Write the stub text: say honestly that the feature does not exist yet; no reward for the click (it attracts clicks for the reward). Do not place the element in an urgent scenario. Agree how long it stays and who removes it.

### 4. Reading the result and the decision

Explain: share = clicked / saw, in total and per segment; compare with the threshold; check the main metric (it may fall during the test); then choose to build, reword or stop. Warn that a click is interest, not readiness to pay.

### 5. Show, then write

Show the card in chat first as a table by template blocks: title, hypothesis, element, stub, audience and period, up to four reaction rows (segment, saw, clicked, share), threshold and volume (set before launch; if it was not set, say so), result, decision. Write a file only after the user confirms. Ask for the output path (default `fake-door-test-<idea>.pptx` in the working directory). Save the data as JSON. The example is the Notino case from card.md; what the source does not give says "not in source"; unused table cells get "—" (null would leave an empty bordered row). There are no count columns to leave as "" in this pptx template:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Notino, language switcher on notino.ch, 2019",
    "hypothesis": "There is enough interest in French and Italian to justify a multilingual website (reconstructed from the text)",
    "element": "Language switcher on the German site with the options \"French\" and \"Italian\"",
    "stub": "A window stating that language options are not yet available (the text is not given in the source)",
    "audience": "Visitors of notino.ch; 7–21.10.2019, two weeks; preparation and launch about one and a half days",
    "g1": "All visitors: clicks on the switcher",
    "v1": "not in source",
    "a1": "not in source",
    "r1": "3.5%",
    "g2": "Chose French or Italian",
    "v2": "not in source",
    "a2": "not in source",
    "r2": "not in source",
    "g3": "—",
    "v3": "—",
    "a3": "—",
    "r3": "—",
    "g4": "—",
    "v4": "—",
    "a4": "—",
    "r4": "—",
    "threshold": "Not in source: the threshold and the number of views are not named (a deviation from step 1 of the card)",
    "result": "3.5% clicked; probably some only opened the list (the sum of language clicks is smaller). The purchase share after the test was slightly above average",
    "decision": "The decision about the site is not named in the source; the author's conclusion: adding languages will not increase the number of purchases"
  }
}
```

Limits that fit the rendered slide: title under 60 characters; hypothesis under 130; element, stub and audience under 110 each; segments (g1..g4) under 65; saw and clicked (v, a) under 20; share (r) under 16; threshold, result and decision under 190. A list of strings becomes lines. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/fake-door-test.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's plan, element description or results and check them against the common mistakes in card.md:

1. The threshold was set after the result.
2. A click is taken for demand or readiness to pay.
3. A reward (discount, bonus) is given for the click.
4. The element misleads, or sits in an urgent scenario, or the stub does not tell the truth.
5. Too few views: the share is noisy and the difference may be random.
6. Only the total share is read, without segments.
7. The main product metric is not watched (Gousto saw a small fall in sign-ups in its first experiments; Notino checked the purchase rate).

Items 1, 5 and 7 usually cannot be judged from the description alone: ask when the threshold was written, how many users saw the element and whether anyone watched the main metric, instead of reporting a finding. Report findings as a numbered list: what is wrong, why it distorts the result, the concrete change. End with a verdict: "result can be trusted", "trusted after changes" or "repeat the test".

Example: the user says "12% clicked our fake 'Export to Excel' button, so we build it", with no threshold and no view counts. Findings: item 1 — ask when 12% was declared enough; item 2 — a click is interest, not use, so say what the 12% means; item 5 — views are unknown, so the share may be noise. Verdict: "repeat the test".
