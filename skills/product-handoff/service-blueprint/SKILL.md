---
name: service-blueprint
description: Map one service scenario as a service blueprint — customer actions with the frontstage, backstage and support processes behind each step, the lines of interaction, visibility and internal interaction, physical evidence, failure points and time — and produce a filled blueprint slide, or review an existing blueprint. Use when a service spans several teams or systems, complaints repeat for hidden reasons, or a new service must be designed and handed to teams.
---

# Service Blueprint

The theory, layers, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user describes a service or brings research about it, **review** when the user brings a blueprint.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the service and one scenario in it, with a start and an end;
- the customer segment the scenario is for;
- current state or future state;
- the goal of the blueprint: remove duplication, cut waiting, fix a failure, design something new;
- what the user knows from research: observation of employees, interviews, support tickets, logs, process documents — and which of it is first-hand.

If the user names several services or scenarios, pick one with them and list the others as separate blueprints. If the backstage comes only from documents or guesses, say so and mark those cells as unverified; suggest observing the people who do the work before relying on them. Never fill a layer with a plausible guess: leave it empty and list the question.

### 2. Customer actions first

Write the customer's steps in order, from the start to the end of the scenario. Aim for five steps or fewer; the sixth column is for an end-to-end scope only. Merge or split so each column is one customer action. Keep the customer in focus: a step that is only internal belongs in a lower layer.

### 3. Fill the layers under each step

For each step: what employees or systems do in front of the customer (frontstage), what happens out of sight (backstage) and who owns it, which systems, data, teams and partners support it. Draw the three lines: interaction, visibility, internal interaction.

### 4. Failure points and time

For each step, record where it breaks, how long it takes and which metric shows it. Use the user's numbers; if there are none, name the metric to collect instead of inventing a value.

### 5. Evidence last

Add what the customer sees or holds at each step: screens, emails, documents, receipts.

### 6. Decide

Rank the failure points by frequency and severity, propose the fixes and who owns each, and say whether a future-state blueprint is needed. Keep current and future state on separate slides.

### 7. Show, then write

Show the blueprint in chat first as a table: steps as columns, layers as rows, then the ranked failure points and decisions. Write a file only after the user confirms. Ask for the output path (default `service-blueprint-<service>.pptx` in the working directory). Save the data as JSON. Keys: `title`; `s1`–`s6` step names; then for each step number `e` evidence, `c` customer actions, `f` frontstage, `b` backstage, `p` support processes, `x` failure points and time. The example is the Airbnb case from card.md, reconstructed as a future-state blueprint from the release notes. The sources describe the blueprint but do not show it, so only the cells the release notes support are filled and the rest are left out:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Airbnb: Summer Release 2023 changes (future state)",
    "s1": "Booking",
    "s2": "Trip",
    "s3": "Check-out",
    "e1": "Check-out instructions on the listing page",
    "c1": "Reads check-out instructions before booking",
    "c2": "Calls support during the trip",
    "c3": "Gets a reminder and checks out",
    "f2": "24/7 priority support for guests on a trip",
    "f3": "Reminder to the guest before check-out",
    "x1": "Support requests broken down by all steps; figures by step not published",
    "x2": "Goal: answer 90% of calls in English within 2 min"
  }
}
```

Omit a key or pass an empty string to leave a cell empty. Keep the title under 60 characters, step names under 22 and every cell under 90; list the rest and the decisions in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/service-blueprint.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint. The script warns about keys you left out; that is expected.

## Mode: review

Take the user's blueprint in any form and check it against the common mistakes in card.md:

1. The backstage is based on observation or first-hand data, not on assumptions.
2. The customer stays in focus: every column is a customer step.
3. One scenario and one customer segment, not several services.
4. The lines of interaction, visibility and internal interaction are drawn.
5. Failure points, time and metrics are marked.
6. Current and future state are not mixed on one blueprint.
7. The blueprint has an owner and is kept up to date.

Items 1 and 7 usually cannot be judged from the blueprint alone: ask the user instead of reporting a finding. Report findings as a numbered list: step and layer, what is wrong, why it matters for the service, the concrete fix. End with a verdict: "blueprint is ready", "ready after fixes" or "needs research first".

Example, built from the Airbnb case in card.md with planted mistakes: columns "Registration", "Booking", "Trip", "Check-out"; the customer row says "Chooses accommodation" and "Lives in the property", which no source states; the frontstage holds "After: 24/7 priority support" next to current-state cells; "Registration" has no customer action. Findings: item 1 — customer actions are guesses, replace them with what the release notes say or mark them unverified; item 6 — current and future state are mixed, split into two slides; item 2 — a column without a customer action, remove it or add the action. Verdict: "ready after fixes".
