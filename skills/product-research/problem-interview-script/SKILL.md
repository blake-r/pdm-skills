---
name: problem-interview-script
description: Build a problem interview script from a problem hypothesis (Person + Problem + Cause + Motivation), record answers against it and describe the persona, or review an existing script, question list or interview notes. Use when the team needs to confirm or reject an assumed customer problem through conversations, or when interview questions are a loose list not tied to a hypothesis.
---

# Awesome Problem Interview Script

The theory, the limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants a script or wants to record interview results, **review** when the user brings a script, a question list or notes to check.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the assumed problem and the segment it happens to (Person);
- what the person does and which result it blocks (Problem, Motivation);
- the suspected causes (Cause);
- who the respondents are, how many, who leads and who takes notes;
- for finished interviews: the notes.

If the problem is not known yet, or the user wants to check a solution, say that the card excludes both cases and ask what the team wants to find out. Do not invent answers, quotes or numbers: mark what the user did not give as "not in the source" in text fields. Numbers of interviews and a confirmation threshold are not set in the source; propose them as the card author's recommendation.

### 2. Hypothesis

Write Person, Problem (behavior plus a blocker metric), Cause (one or several), Motivation (desired result plus a goal metric). Use one metric for the blocker and the goal. Check that the behavior is a problem only because of the goal.

### 3. Script

Build the verification flow by blocks: behavior and problem questions from Problem, goal questions from Motivation, solution questions from Cause, then the closing questions. Mark which part of the hypothesis each question checks. Add a follow-up from the new-knowledge flow for questions where an answer may differ from the hypothesis. Questions are open and ask about cases of use; none contains a possible answer.

### 4. Additional hypotheses and results

List additional hypotheses by the card's patterns. For finished interviews put the answer next to each question, mark `yes`, `no` or `partially` in "Matches hypothesis" only when the notes show it, then describe the persona in four parts: general features, context, values and goals, pains. State the decision: hypothesis confirmed, rejected or a new one needed. Mark conclusions that the notes cannot support as the card author's judgment.

### 5. Show, then write

Show the result in chat first as a table by template blocks: title, Person, Problem, Cause, Motivation, metric, hypothesis, interview, script rows, extra hypotheses, persona, decision, gaps. Write a file only after the user confirms. Ask for the output path (default `problem-interview-script-<topic>.xlsx` in the working directory). Save the data as JSON. The example is the Karat case from card.md. The source has no script, so one row holds what creators asked for, and the empty fields say "not in the source":

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Karat: creators, financing (Stripe, no date)",
    "person": "Creators (content creators)",
    "problem": "Need money in advance to cover upcoming invoices; the source gives no metric",
    "cause": "not in the source",
    "motivation": "not in the source",
    "metric": "not in the source",
    "hypothesis": "The team's initial assumption: creators need tax software; the hypothesis in formula form is not in the source",
    "who": "not in the source: number of conversations, selection, lead",
    "extra": "not in the source",
    "general": "not in the source",
    "context": "not in the source",
    "values": "not in the source",
    "pains": "Need a loan of 5,000 or 10,000 dollars in advance to cover invoices",
    "decision": "First a merchant cash advance (did not work), then a business card with revenue-based financing from digital platforms",
    "gaps": "No questions, number of conversations, Cause, Motivation, metrics, publication date"
  },
  "cells": {},
  "rows": [
    ["1", "not in the source", "not in the source", "not in the source", "not in the source", "not in the source", "Creators asked for a loan of 5,000 or 10,000 dollars in advance to cover upcoming invoices", ""]
  ]
}
```

Warning: the template has live formulas that count column G ("Respondent answer") and column H ("Matches hypothesis"). Never write "not in the source" or any placeholder in G or H when there is no answer or no assessment: leave them empty (`""`), otherwise a placeholder counts as an answer or hides an unrated row. In the example G is filled from the source and H is empty, so the totals show 1 answer and 1 answer without assessment. The assessment is not made because the source gives no hypothesis in the formula. In other columns write "not in the source".

Length limits that fit the template:

| Field | Limit |
|---|---|
| `title` | up to 100 characters |
| `person`, `metric` | up to 100 characters each |
| `problem`, `cause`, `motivation`, `hypothesis`, `who` | up to 200 characters each |
| `extra`, `general`, `context`, `values`, `pains`, `decision`, `gaps` | up to 250 characters each |
| script: number, block | up to 6 and 16 characters |
| script: type of question, "Checks" | up to 40 and 25 characters |
| script: question, follow-up | up to 150 characters each |
| script: answer | up to 200 characters |

The template has room for 30 script rows; the summary blocks are below them, so more rows would overwrite them. A list of strings in `text` becomes lines. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/problem-interview-script.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the table columns with their hints. The totals block counts answers, matches, mismatches, partial matches and answers without assessment.

## Mode: review

Take the user's hypothesis, script or notes and check them against the common mistakes in card.md:

1. Behavior is passed off as a problem: there is no goal that the behavior blocks.
2. The blocker metric and the goal metric differ, so the hypothesis cannot be measured.
3. The questions are not derived from the hypothesis: Cause or Motivation is left unchecked.
4. The questions are closed or ask for an "ideal" instead of open questions about cases of use.
5. An answer is placed inside the question (anchor effect).
6. The interviewer interrupts and rushes: the respondent has no time to recall.
7. Only one hypothesis is checked, and interviews run in a series without breaks.
8. The script is used to search for a problem that is not known yet.

Items 5 and 6 usually cannot be judged from a question list alone: ask for notes or a recording and report only what the text shows. Item 7 needs the plan of interviews. Also check that the persona is described in four parts and that the conclusion follows from the answers. Report findings as a numbered list: what is wrong, where (question or field), why it spoils the data, a rewritten question or a concrete fix. End with a verdict: "script is ready", "ready after fixes" or "rewrite from the hypothesis".

Example: the user brings the hypothesis "Accountants want to earn more" and the question "Would it be convenient for you if we showed tasks with high pay?". Findings: item 1 — "earn little" is a state, name the behavior and the blocked result; item 2 — no metric, say what is measured; item 4 and 5 — the question is closed and contains the idea; replace with "When did you last take a task that paid less than you expected? Tell me how it went". Verdict: "rewrite from the hypothesis".
