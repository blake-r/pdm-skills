---
name: jtbd-interview
description: Plan, run and analyse a Jobs-to-be-Done (JTBD) interview, also called a Switch Interview - a conversation about a recent real purchase or switch, rebuilt as a timeline from first thought to first use, with the four forces (push, pull, anxiety, habit) - and produce a one-slide timeline with forces and a decision, or review an existing interview guide, notes or timeline. Use when the team wants to learn why customers chose, left or rejected a product.
---

# JTBD Interview

The method, the timeline, the forces, limits and the Autobooks case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants to prepare, run or analyse an interview, **review** when the user brings a guide, notes or a finished timeline to check.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and the decision to study: a purchase, a switch away, a refusal;
- who can be interviewed: people with a recent real case, how many, how they are found;
- what the team wants to decide with the result;
- raw material, if the interviews are already done: notes, recordings, transcripts.

If the question is about shares or sizes of segments, say that the card rules this out (PAF: not for quantitative assessment) and ask what the team needs instead. Do not invent answers of the customer: what the notes do not contain is marked "not in the source".

### 2. Prepare or take the notes

For preparation: write the interview plan (start from the decision point, then go back to the first thought and forward to first use; ask about events, tried options and workarounds, not about wanted features), roles (one leads, one records) and time (30 minutes to 1.5 hours per PAF). For finished notes: put every event on the seven markers and cut what is not an event.

### 3. Forces

For each interview write the four forces with the person's own words: push, pull, anxiety, habit. Mark what is a reconstruction by you and not said by the person. Compare several interviews: repeated events and forces make the finding. A single story is a hypothesis.

### 4. Findings and the decision

State what repeats, what contradicts, and one decision: raise the pull, lower anxiety or habit, or change the offer, with how to check it by customer behaviour. Do not state shares from a small number of interviews.

### 5. Show, then write

Show the result in chat first as a table by template blocks: title, seven timeline markers, four forces, findings, decision. Write a file only after the user confirms. Ask for the output path (default `jtbd-interview-<topic>.pptx` in the working directory). Save the data as JSON. The example is the Autobooks story of the lawyer Harry from card.md (the marker "Use" is the card author's addition to the site's stages; force entries are marked as reconstruction); what the source does not give says "not in the source":

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Autobooks: lawyer Harry, switching from cheques to cards (BoS 2023)",
    "t1": "A client asked if they could pay by card; he declined",
    "t2": "A friend used Square: not a fit; he also dismissed PayPal",
    "t3": "Two or three questions about the card over two weeks",
    "t4": "not in the source",
    "t5": "not in the source",
    "t6": "Connected Autobooks, offered by his bank",
    "t7": "Detailed invoice in Word; one-line invoices in Autobooks pointing to it",
    "push": "Repeated client requests to pay by card (reconstruction)",
    "pull": "The service of his own bank (reconstruction)",
    "anxiety": "not in the source",
    "habit": "Cheques from corporate clients (reconstruction)",
    "insights": [
      "Owners think about accounting twice a year, about getting money every day",
      "Some businesses do not issue invoices at all",
      "Plenty of people like Harry: detailed invoices with attachments"
    ],
    "decision": [
      "Accounting separated, a paid extension",
      "Calls to action in internet banking: \"get paid\", \"issue an invoice\"",
      "A simple payment link",
      "Results in numbers: not in the source"
    ]
  }
}
```

Limits that fit the rendered slide: title under 70 characters; each timeline marker t1..t7 under 110; each force under 120; insights: up to four items under 80 each; decision: up to four items under 70 each. A list of strings becomes lines. Use "not in the source" for an empty block, not null or an empty string. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/jtbd-interview.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's guide, notes or timeline and check them against the common mistakes in card.md:

1. The first thought is taken as the person named it, without probing further back.
2. Questions are about wanted features or the future, not about events.
3. Only people who bought were interviewed; those who left or did not decide are missing.
4. One story is taken as the rule, without repetition in other interviews.
5. Only the pull is described; anxiety and habit are missing.
6. The result is read as numbers or shares.
7. Committees or large companies were interviewed without a plan to rebuild who decided.

Items 3, 4 and 7 usually cannot be judged from one set of notes: ask who was interviewed and how many, instead of reporting a finding. Also check that every force has the person's own words and that reconstructions are marked. Report findings as a numbered list: what is wrong, why it distorts the picture, the concrete change. End with a verdict: "timeline supports a decision", "works after changes" or "needs more interviews first".

Example: notes with only the purchase date and the line "chose us for the price", with four buyers and nobody who left. Findings: item 1 — the first thought is missing, ask what happened before; item 2 — "price" is a feature, ask for events and alternatives; item 3 — no one who left, add them; item 5 — no anxiety or habit. Verdict: "needs more interviews first".
