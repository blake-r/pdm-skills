---
name: soft-launch
description: Plan or review a Soft Launch - checking a solution (and business model) hypothesis by releasing the real solution in a different packaging to a limited, similar audience, region or channel without loud advertising, then deciding to scale, rework or close - and produce a one-slide soft launch card. Use when the user wants to release a product in a test market or to a small group before the full launch and read retention, conversion or revenue per user.
---

# Soft Launch

The definition, steps, the worked case (Supercell, Squad Busters, 2023-2025) and its limits are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language. The card avoids the word "prototype" and other tools' names; keep to that wording when quoting it.

Pick the mode from the request: **do** when the user plans a soft launch, **review** when the user brings a plan or results and wants them checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the solution and the hypothesis: which audience gets which benefit; whether the solution, the business model or both are checked;
- what will differ from the main launch (name, design, price, offer wording, channel) and what must stay;
- the test audience, region or channel, and how it resembles the target one;
- success measures (2-3, for example retention, conversion, revenue per user), thresholds, term and the decision owner;
- whether analytics is ready and what the closing and client-migration plan is.

If the solution cannot yet work for real users, say that a soft launch needs a working solution (card.md: high cost) and ask whether to continue. Do not invent numbers: mark unknown values "not in source" or "unknown".

### 2. Packaging and audience

Separate what may change (items that do not affect the target metrics) from what must not (core value, key characteristics). Record how the test audience differs from the target one (for a business model PAF names a market different from the target but close on key traits).

### 3. Criteria and term

Thresholds and term are set before launch; say that this is the card author's recommendation. The term must cover the horizon of the main metric (author's recommendation). Retention is the share of users who come back on day N after first use.

### 4. Run and read

No loud advertising and no fixed global date before the result. Numbers show what happened, feedback shows why. Above the threshold: scale, carrying the findings into the main product; near it: rework and repeat; below: close and migrate clients. Warn that similar audiences and big samples do not guarantee the same behavior globally.

### 5. Show, then write

Show the card in chat first as a table by template blocks: title, hypothesis, packaging, audience, term and conditions, criteria, result in numbers, result in feedback, decision. Write a file only after the user confirms. Ask for the output path (default `soft-launch-<product>.pptx` in the working directory). Save the data as JSON. The example is the Supercell case from card.md; what the source does not give says "not in source":

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Squad Busters (Supercell), soft launch 2024",
    "hypothesis": "Not in source; the team wanted a game \"for everyone\" (Joas)",
    "packaging": "Not in source",
    "audience": "iOS and Android: Canada, Finland, Denmark, Norway, Sweden, Spain, Mexico, Singapore",
    "term": "From 23.04.2024, about a month; global launch 29.05.2024 announced 25.04.2024",
    "criteria": "Not in source: thresholds not published (D7 29% in the 2023 test named below target, target not named)",
    "numbers": "Soft launch: no figures. 2023 tests: D1 61%, D3 44%, D7 38%. Later: 40 million pre-registrations, 75 million downloads in the first year",
    "feedback": "Paananen: \"not a lot of those players stuck around\"; Joas: players \"didn't find what they were looking for\"",
    "decision": "Global launch 29.05.2024; the basis from the soft launch results is not named in the source (Paananen: pressure in favour of bold risks). On 30.10.2025 Mobilegamer reported the game was being shut down. Supercell's conclusion: a longer third test was needed"
  }
}
```

Limits that fit the rendered slide: title under 60 characters; hypothesis under 130; packaging, audience and term under 110 each; criteria, numbers and feedback under 130 each; decision under 260. A list of strings becomes lines. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/soft-launch.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's plan or results and check them against the common mistakes in card.md:

1. No thresholds set before launch.
2. The test audience is taken for the market; similar countries or big samples are treated as proof.
3. The term and metrics are shorter than the decision needs (only early retention, no long-term retention or monetization).
4. Loud advertising and a fixed global date before the result, so the test becomes the launch.
5. Something significant was changed in the packaging (price, key benefit), so the result does not transfer.
6. No analytics and no exit plan (closing, client migration).

Items 1 and 3 usually cannot be judged from a description alone: ask when the thresholds were set and which metrics and how many days were measured. Report findings as a numbered list: what is wrong, why it distorts the result, the concrete change. Also check that the hypothesis names an audience and a benefit and that numbers are paired with feedback. End with a verdict: "result can be trusted", "trust after changes" or "repeat the soft launch".

Example: a team soft-launched in two countries with a global date announced in advance, measured D7 only and set no thresholds. Findings: item 1 - set thresholds; item 3 - add long-term retention and revenue; item 4 - the date makes the test a formality. Verdict: "trust after changes".
