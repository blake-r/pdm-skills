---
name: elevator-pitch
description: Build or check a product elevator pitch using Geoffrey Moore's positioning template (for whom, need, product category, key benefit, main alternative, difference) and produce a one-slide pitch sheet, or review an existing pitch. Use when someone must explain a product in seconds to an investor, executive or new team, or has a vague product description.
---

# Elevator Pitch

The theory, the template fields, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user needs a pitch written, **review** when the user shows an existing pitch and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and the audience of the pitch (investor, executive, new team);
- who the target customers are, concretely;
- the customer's need or opportunity, from the customer's side;
- the product category: what the listener should compare it with;
- what customers use today instead (the main alternative), even if it is manual or free;
- the one difference that matters to the customer;
- whether the pitch was ever told to someone and what they answered.

If a field cannot be filled, say it is a knowledge gap and propose research instead of inventing. Do not invent numbers or facts: mark what the user did not give as unknown.

### 2. Fill the six fields

Customer, need, product with category, key benefit, main alternative, difference. One alternative, one difference. Check that substituting another product makes the wording wrong: if it still fits, it is too general.

### 3. Say it aloud

Write the spoken version in one or two plain sentences, up to 30 seconds, without the template's connecting words.

### 4. Check and decide

Ask the user to tell the pitch to a person outside the topic and to note whether they could retell it. Record the answer in the check block. The decision: keep the wording, rewrite it, or run research for a field that has no data. If a decision was already made on the pitch (for example an investor's), record that decision and what it rests on.

### 5. Show, then write

Show the sheet in chat first as a table by template blocks: title, the seven rows (for, who, the, is a, that, unlike, our product), spoken version, check, decision. Write a file only after the user confirms. Ask for the output path (default `elevator-pitch-<product>.pptx` in the working directory). Save the data as JSON. The example is the Airbnb case from card.md; fields the source does not give are null (here `diff`: the slide "Competitive Advantages" is only a list of six headings, not a difference; say so in chat):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "AirBed&Breakfast, first investor pitch deck",
    "target": "price-sensitive travelers and people with spare space who want to rent it out",
    "need": "a hotel cuts you off from the city; there is no simple way to rent a room from a local or to become a host",
    "product": "AirBed&Breakfast",
    "category": "a web platform where users rent out their space to visitors",
    "benefit": "save money on a trip, earn money from renting, feel the city (Save money, Make money, Share culture)",
    "alt": "Craigslist and Hotels.com (the main competitors according to BI's summary)",
    "diff": null,
    "spoken": "Book rooms with locals, rather than hotels. (subtitle of the first slide)",
    "check": "No check: the source does not report one",
    "decision": "The sources contain no decision on the pitch: Paul Graham's letter to Fred Wilson of 23.01.2009 is a recommendation to the investor, not a decision on the pitch"
  }
}
```

Limits that fit the rendered slide: title under 65 characters; each of the seven rows under 110 characters; spoken version under 200; check under 220; decision under 260. A list of strings becomes lines. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/elevator-pitch.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's pitch and check it against the common mistakes in card.md:

1. Fields are filled with general words that fit any product.
2. The alternative is "nobody" or one the customer does not compare the product with.
3. The template is read aloud as written, stiff and too long.
4. Several differences are listed instead of one.
5. The benefit gives no reason to choose the product ("convenient").
6. The pitch was never told to a person outside the topic.
7. The pitch is taken as proof that customers need the product.
8. A field is missing, or the spoken version does not fit 30 seconds.

Items 6 and 7 usually cannot be judged from the text alone: ask whom it was told to and what evidence of demand exists, instead of reporting a finding. Report findings as a numbered list: what is wrong, why it matters to the listener, the concrete rewrite. End with a verdict: "pitch works", "works after changes" or "needs customer facts first".

Example: "For small businesses who need efficiency, our platform is a solution that improves results." Findings: item 1 — the customer and the need fit any product, name a concrete customer and a concrete task; item 2 — no alternative is named, ask what customers use now; item 5 — "improves results" gives no reason to choose. Verdict: "needs customer facts first".
