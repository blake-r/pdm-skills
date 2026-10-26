---
name: prototyping-process
description: Plan or record a prototype test - the hypothesis and the question the prototype must answer, the lowest sufficient fidelity (sketch, static screen mock-up, clickable mock-up, human-simulated service, live data), what the prototype contains, the participants, the tasks and what to observe, then the findings and the decision (go, iterate, drop) with the next step - and produce a one-slide PPTX; or review an existing prototype test plan or report. Use before building a feature or service that is expensive to build and may not be understood, when several interface variants must be compared before development, or when a new service should be tried without building its back end.
---

# Prototyping Process

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a solution to test or test results to record, **review** when the user brings a finished plan or report.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the solution, the decision that depends on the test and what the team is unsure about;
- who the users are and whether there are distinct groups;
- what already exists: sketches, mock-ups, a design tool file, a working build;
- for a finished test: the participants, the tasks, what they did (numbers and quotes), the dates.

Do not invent participants, findings or numbers. If the question would not change any decision, say so and stop.

### 2. Plan

- **Hypothesis and question:** one sentence each; the question asks whether people understand, find or want something.
- **Fidelity:** tick exactly one, the lowest that answers the question. Sketch for structure and flow; static screen mock-up for first-click and visibility checks; clickable mock-up for finding and understanding elements along a flow; human-simulated service for the value of a service without its back end; live data when speed or real data matter. Say that praise from a prototype does not prove demand.
- **Scope:** only the screens and steps of the tasks. Tell the team to click through it before the sessions.
- **Participants:** 5 from the target audience per round, 3–4 per group when groups differ; not colleagues. Plan more small rounds rather than one big one. First-click or other unmoderated tests may use larger samples; give the count.
- **Tasks:** goals in the user's words, with no wording copied from the interface. **Observe:** where people get stuck, where they click, what they expected.

### 3. Record the result

Write the findings as facts with counts ("3 of 5 did not find ..."), then tick one decision (go, iterate, drop) and write what changes and what the next check is. Mark "iterate" when the fix needs another round.

### 4. Show, then write

Show in chat first: the four columns and the decision. Write a file only after the user confirms. Ask for the output path (default `prototype-test-<topic>.pptx` in the working directory). Save the data as JSON (the example is the SberMarket ScanPay case from card.md; what the source does not give is marked so, not filled in):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "SberMarket: entry point to ScanPay, published 28.06.2024",
    "hypothesis": "A new location of the ScanPay entry point is more noticeable than the current one",
    "question": "Will users find the ScanPay entry with the first click",
    "sketch": "", "mockup": "✓", "clickable": "", "wizard": "", "live": "",
    "scope": ["Mock-up of the current screen", "Mock-up of the new screen", "First-click test on Useberry"],
    "participants": ["Users with different experience", "100 people per variant, each saw one"],
    "tasks": ["The exact wording of the task is not given in the source"],
    "observe": ["Where they click first", "Which sections they choose by mistake"],
    "findings": ["Current: only a third first clicked the ScanPay tile", "Current: 61% went through choosing a store", "New: 46% found the entry correctly, fewer wrong clicks", "New: through the retailer's page — 31%"],
    "go": "", "iterate": "✓", "drop": "",
    "next": ["Add an entry point on the retailer's main page", "A repeat check is not described in the source", "The launch and outcome are not described in the source"]
  }
}
```

Put "✓" in exactly one fidelity key and one decision key and empty strings in the others; leave the decision keys empty for a plan. `hypothesis` and `question` take under 110 characters; `scope` and `findings` take up to four items (under 60 and under 55 characters), `participants`, `tasks`, `observe` and `next` up to three items of under 60; the title stays under 60 characters; each list item becomes its own paragraph. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/prototyping-process.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's plan or report in any form and check it against the common mistakes in card.md:

1. The fidelity is the lowest that answers the question.
2. Findings are about behaviour, not praise, and no claim of demand rests on "they liked it".
3. Tasks do not repeat the interface's wording.
4. Participants come from the target audience, not colleagues; about 5 per round.
5. The prototype was clicked through before the sessions, so it does not break.
6. There is a decision, a change to the solution and a next round.

Report findings as a numbered list: what is wrong, why it misleads the decision, the concrete fix. End with a verdict: "test supports the decision", "supports it after fixes" or "not enough data".
