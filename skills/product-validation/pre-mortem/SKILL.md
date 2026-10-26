---
name: pre-mortem
description: Run or review a pre-mortem (Gary Klein) — assume a plan has already failed, list the reasons, change the plan — and produce a one-slide record, or review an existing one. Use before a launch, migration, pricing change or big feature, when the team feels overconfident, nobody voices doubts, or the user says "what could kill this plan", "premortem", "imagine it failed", "risks before launch".
---

# Pre-mortem

The theory, the steps and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user is preparing or has run a session and wants it recorded, **review** when the user shows a finished pre-mortem and wants it checked. If there is no written plan yet, say the tool checks a plan and ask for the plan first. If the user wants a broad list of strengths and threats, point to SWOT Analysis; to turn top reasons into tests, point to Experiment Card.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the plan under review: what, who, when, what is already committed;
- who will take part (people who know the work, not only the author) and who leads;
- the reasons the team already named, if a session was held;
- the changes and the decision, if any.

You cannot run the silent writing for the team. Offer a session script: briefing, "the plan has failed" statement, two minutes of silent writing, a round-robin of one reason each starting with the leader, no debate. Do not invent reasons the team did not give; mark gaps N/A.

### 2. Reasons and changes

Put each reason as one short sentence. Merge duplicates. For each reason the team takes up, write a change to the plan: a prevention, a check, a stop trigger or a response plan, with an owner when known. Use up to six rows.

### 3. Decision

State whether the plan goes ahead, changes or stops, and when the list is revisited.

### 4. Show, then write

Show the record in chat first as a table by template blocks: title, imagined failure, six rows of reason and change, decision. Write the file only after the user confirms. Ask for the output path (default `pre-mortem-<project>.pptx` in the working directory). Save the data as JSON.

The JSON below shows the format only. Its values come from the example case in card.md, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Client of a subscription-app consultancy, new subscription tier, pre-mortem before launch (2025)",
    "scenario": "The new subscription tier has been launched and has failed",
    "r1": "Existing customers feel cheated when new customers get a better deal",
    "r2": "N/A", "r3": "N/A", "r4": "N/A", "r5": "N/A", "r6": "N/A",
    "a1": "Position the existing tier, not only the new one; add a feature to the higher tier against cannibalization; tell existing customers first; brief support",
    "a2": "N/A", "a3": "N/A", "a4": "N/A", "a5": "N/A", "a6": "N/A",
    "decision": "Launch the tier with the four changes (the risk could not be removed: the tier had to offer more value). Outcome reported: fewer complaints than expected, MRR up"
  }
}
```

Limits that fit the slide: title under 100 characters; scenario under 90; each reason (r1..r6) under 80; each change (a1..a6) under 150; decision under 200. Put the rest in chat. Run from the repository root:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example; otherwise fill the placeholders with the user's own data.

```bash
uv run scripts/fill_pptx.py <this skill dir>/pre-mortem.pptx data.json <output>.pptx
```

`uv run scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's pre-mortem (list, notes, slide) and check it against the common mistakes in card.md:

1. The question was "what could go wrong" and not "the plan has failed".
2. Reasons were debated while being collected.
3. The sponsor or senior person spoke first or last, or commented.
4. The session came too late to change the plan.
5. Reasons have no change, owner or date.
6. The list is treated as complete and is never revisited.

Items 2, 3 and 4 usually cannot be seen from the list: ask how the session ran, who spoke first and what was already committed, instead of reporting a finding. Also check that the reasons are about this plan and not generic risks, and that a decision is recorded. Report findings as a numbered list: what is wrong, why it matters, the concrete fix. End with a verdict: "plan was changed by it", "works after changes" or "a risk list, not a pre-mortem".

Example: a list of ten generic risks ("budget", "delays") with no changes and no decision. Findings: item 5, no changes or owners, so the list does not move the plan; generic reasons, rerun with the concrete plan. Verdict: "a risk list, not a pre-mortem".
