---
name: field-research
description: Plan, run notes for, or review a field observation study (field research, contextual inquiry, observing people in their natural environment such as a store, home, bank branch or app use) to test hypotheses about customer behaviour, and produce a one-slide observation log. Use when the team needs to see what people actually do, not what they say, or when someone brings visit notes to check.
---

# Field Research

The theory, limits and a worked case (Bank of America and IDEO, Keep the Change) are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user is preparing or summarising a field study, **review** when the user brings notes, a log or a plan and wants them checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the hypothesis: "in situation X the person does Y because Z";
- the place where this really happens and who the people are;
- the role of the observer: silent, or asking short clarifying questions; full or partial immersion;
- permissions: participants, owners of the place, rules for other observers;
- what has been observed already: visit notes, recordings, quotes.

If the user wants shares or numbers ("how many customers do this"), say that the card does not give quantities and offer to describe the behaviour only. Never invent observations or quotes: what the user did not give is marked "not in the source".

### 2. Plan the visit

Give a short plan: research question, place, role, how long a visit lasts (an hour or two up to several days, NN/g), what to watch (order of actions, words, workarounds) and how facts and interpretations are written apart.

### 3. Fill the log

For each observation write three things: the fact (what was done, where, in which order), the person's own words (verbatim or "not in the source") and the interpretation, marked as the observer's conclusion. Do not mix them.

### 4. Patterns, refuted, decision

State what repeated across visits and how many people, what did not match the hypothesis or stayed unclear, and one decision with a check by behaviour. Do not state shares.

### 5. Show, then write

Show the result in chat first as a table by template blocks: title, hypothesis, setting, observer role, three log rows, patterns, refuted, decision. Write a file only after the user confirms. Ask for the output path (default `field-research-<topic>.pptx` in the working directory). Save the data as JSON. The example is the Bank of America and IDEO case from card.md; details from secondary retellings are marked, and what the source does not give says "not in the source":

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "IDEO and Bank of America: observing women with children, 2004",
    "hypothesis": "not in the source (the case studied how the bank underserves this group)",
    "setting": "Atlanta, Baltimore, San Francisco; per a retelling — about a dozen families, shopping and eating; no number of visits given",
    "role": "Observation of shopping and eating; the immersion format is not in the source",
    "f1": "Many people round payments up to the dollar",
    "f2": "A woman from Atlanta wrote rounded amounts into her chequebook (retelling)",
    "f3": "Many mothers find it hard to save",
    "q1": "No participant words; Brown: \"we saw how many people were rounding up\"",
    "q2": "not in the source",
    "q3": "not in the source",
    "i1": "The habit can be linked to the debit card (IDEO's conclusion via Brown)",
    "i2": "Rounding simplifies the accounting and provides a buffer (retelling)",
    "i3": "No money or no self-control (interpretation of sources)",
    "patterns": "Number of people who round up: not in the source",
    "refuted": "not in the source",
    "decision": [
      "Keep the Change: purchases made with a Visa debit card are rounded up to the dollar",
      "The difference goes from the account to a savings account",
      "The sources disagree on results: 2.5 million clients (Core77, 2007), 10 million (Brown, 2010), 12 million (2018)"
    ]
  }
}
```

Limits that fit the rendered slide: title under 70 characters; hypothesis, setting and role under 110; each of f1..f3 and i1..i3 under 90; q1..q3 under 80; patterns and refuted under 120; decision: up to three items under 110. A list of strings becomes lines. Use "not in the source" for an empty block, not null or an empty string. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/field-research.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's visit plan, notes or log and check them against the common mistakes in card.md:

1. Interpretation is written on the spot instead of the fact.
2. The study relies on what people say, not what they do.
3. One person's case is taken as the rule.
4. Shares or numbers are read from a few visits.
5. The observer effect is ignored.
6. Permissions and rules for observers are missing.
7. The log ends without a decision and a way to check it.

Items 3 and 5 usually cannot be judged from the notes alone: ask how many people were seen and how the observer was present, instead of reporting a finding. Also check that the hypothesis, the observer's role and the place are named. Report findings as a numbered list: what is wrong, why it distorts the picture, the concrete change. End with a verdict: "log supports a decision", "works after changes" or "needs more visits first".

Example: notes "the user was annoyed by the form", one visit, no quotes, no decision. Findings: item 1 — "annoyed" is an interpretation, write what he did; item 3 — one visit, add more; item 7 — no decision. Verdict: "needs more visits first".
