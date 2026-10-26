---
name: in-depth-interview
description: Plan and record a depth interview (CustDev interview) with consumers or customers — a hypothesis, an interview guide of past-experience questions, a log of answers typed as fact, opinion, idea or compliment, and a decision — or review an existing guide, question list or interview notes. Use when the team needs to learn why customers behave a certain way, check a hypothesis about customers through conversations, or suspects that interviews only collect praise.
---

# In-Depth Interview

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants to prepare interviews or record their results, **review** when the user brings a guide, a question list or notes of finished interviews to check.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the hypothesis in the form "role does X because Y", or the decision the interviews should inform;
- who the respondents are: segment, roles, how many, how they are found, how long one interview takes;
- what the team already knows (metrics, support requests) and what it does not know;
- for a finished series: the notes, with quotes if they were taken.

If the user wants numbers ("how many customers do this"), say that the card treats the interview as qualitative and offer to turn the findings into a hypothesis for a numeric check. Do not invent answers, quotes or counts: mark what the user did not give as "not in the source" in the file.

### 2. Goal and hypothesis

Write a concrete goal and the hypothesis. A goal like "learn about users" is too broad: narrow it to a behavior or a decision.

### 3. Guide

Build 3–5 themes. For each: what it checks, one open main question about a concrete past case ("Tell me about the last time when…"), nested follow-ups (when, how long, how much money, what next). Drop questions about the future, opinions and "would you" questions; do not describe the team's idea in the questions. Probing phrases such as "tell me more" are not written in advance.

### 4. Log of answers

For finished interviews, split the notes into records, one fact per row: respondent code, role, theme, what happened, the exact quote, the signal (time or money spent, strong emotion), the type of data (`fact from the past`, `opinion or intention`, `idea or request`, `compliment`), and your interpretation in a separate column. Keep facts and interpretation apart.

### 5. Findings and decision

A hypothesis holds when several respondents independently described the same behavior with concrete cases; opinions and compliments alone do not support it. Name what stayed open and which roles are not covered. State the decision or the numeric check that follows; mark judgments that the data cannot support as the author's recommendation.

### 6. Show, then write

Show the result in chat first as a table by template blocks: title, hypothesis, respondents, goal, guide (theme, what is checked, main question, follow-ups), log, findings, decision, gaps. Write a file only after the user confirms. Ask for the output path (default `in-depth-interview-<topic>.xlsx` in the working directory). Save the data as JSON. The example is the A3 payment service case from card.md. The source gives themes of the questions and a summary of insights, not answers by respondent, so the log holds one summary row per insight, and empty fields say "not in the source":

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "A3 payment service: interviews outside housing and utilities (ZhKU), published 10.12.2024",
    "hypothesis": "The product is of interest to companies outside ZhKU, and their pains overlap with ZhKU pains (a \"role does X because Y\" form is not in the source)",
    "who": "24 respondents: an online foreign language school, foundations, accommodation booking, travel agencies, kindergartens, online shops, online psychotherapy; selection and duration: not in the source",
    "goal": "Understand how interesting the product is to companies outside ZhKU and find overlapping pains",
    "t1": "Way of accepting payments", "c1": "not in the source", "q1": "How payments are accepted (the source wording is a topic)", "f1": "not in the source",
    "t2": "Payment acceptance partners", "c2": "not in the source", "q2": "Who they work with for payment acceptance and why", "f2": "not in the source",
    "t3": "Additional functionality", "c3": "not in the source", "q3": "What additional functionality they use: instalment payments, payment hold, SBP, SberPay", "f3": "not in the source",
    "t4": "Related services", "c4": "not in the source", "q4": "What related services they use: online accounting, website builders", "f4": "not in the source",
    "t5": "not in the source", "c5": "not in the source", "q5": "not in the source", "f5": "not in the source",
    "findings": "Common pains in ZhKU and other industries; roles have similar needs, with different emphases",
    "decision": "Positioning and communication by role; new niches as a direction; a payment widget on the website for those who gave up acquiring",
    "gaps": "No answers by respondent, quotes, wording of questions, or results of decisions; numbers were not verified"
  },
  "cells": {},
  "rows": [
    ["summary of 24", "not in the source", "Additional functionality", "Some companies are considering instalment payments; not all are ready because of the high commission", "", "not in the source", "", "Commission named as a constraint (source conclusion)"],
    ["summary of 24", "not in the source", "Additional functionality", "A number of companies are considering BNPL; a high interest rate is a constraint", "", "not in the source", "", "Rate named as a constraint (source conclusion)"],
    ["summary of 24", "not in the source", "not in the source", "There is a need to optimise the payment process, including the amount of information collected", "", "not in the source", "", "Information is specific to some markets (source conclusion)"],
    ["summary of 24", "not in the source", "Related services", "Integrating acquiring with CRM slows down processes; switching to a new system is labour-intensive", "", "not in the source", "", "Labour intensity of the switch named as the reason (source conclusion)"],
    ["summary of 24", "not in the source", "not in the source", "Cross-border payments are relevant", "", "not in the source", "", "not in the source"],
    ["summary of 24", "owners, product managers, accountants, sellers", "not in the source", "Roles have similar needs; emphases and possible USPs differ", "", "not in the source", "", "Use in positioning (source conclusion)"]
  ]
}
```

Allowed values for "Data type" (the totals count them, check the spelling): `fact from the past`, `opinion or intention`, `idea or request`, `compliment`. The four types are an adaptation by the card's author (see card.md). Warning: in the columns "Quote" (E) and "Data type" (G) never write "not in the source" or any placeholder; leave them empty (`""`). The totals treat any text there as filled, so a placeholder would hide records without a quote or a type. In text fields and other log columns write "not in the source". Fill G only when the notes show the type. Because a summarized source has no respondent codes, the totals of respondents and facts do not describe such a case: say so. In this example "Records without a quote" and "Records without a type" are 6 and 6, as they should be.

Length limits that fit the template:

| Field | Limit |
|---|---|
| `title` | up to 100 characters |
| `hypothesis`, `who`, `goal` | up to 200 characters each |
| `findings`, `decision`, `gaps` | up to 250 characters each |
| guide: theme `t1..t5` | up to 40 characters |
| guide: checks `c1..c5` | up to 70 characters |
| guide: main question `q1..q5` | up to 150 characters |
| guide: follow-ups `f1..f5` | up to 150 characters |
| log: respondent | up to 14 characters |
| log: role | up to 60 characters |
| log: theme | up to 40 characters |
| log: what happened, quote, interpretation | up to 200 characters each |
| log: signal | up to 80 characters |

The template has five guide themes and room for 100 log rows. A list of strings in `text` becomes lines. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/in-depth-interview.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the log columns with their hints. The totals block counts records, respondents, records by type, the share of facts, records without a quote and without a type.

## Mode: review

Take the user's guide, question list or notes and check them against the common mistakes in card.md:

1. The idea is told to the respondent and the question is "would you buy": the answers are compliments and promises.
2. Questions ask for opinions and forecasts instead of a concrete past case.
3. A feature request is taken for a need: nobody asked "why".
4. The interviewer presses or prompts: leading questions, an answer is pulled out of the respondent (the query effect).
5. Shares or numbers are drawn from a few dozen interviews.
6. Roles are mixed in one summary, so the different emphases are lost.
7. The stories are not checked against real behavior, for example product usage statistics.

Items 4 and 7 usually cannot be judged from a question list alone: ask for a recording or notes, and whether anyone compared the stories with usage data, instead of reporting a finding. Also check that the goal is concrete, the guide has 3–5 themes with follow-ups, quotes are verbatim and the interpretation is kept apart from facts. Report findings as a numbered list: what is wrong, where (question or record), why it spoils the data, a rewritten question or a concrete fix. End with a verdict: "guide and notes are ready", "ready after fixes" or "rewrite the guide".

Example: the user brings the question "Would it be convenient for you to pay in instalments?" and the note "Everyone said the idea is great, we will build it". Findings: item 1 — a question that describes the idea and asks about the future gives compliments; replace with "Tell me about the last time a client asked to pay in instalments. What did you do?"; item 2 — the question asks for an opinion, not a past case; item 5 — "everyone" from a handful of talks is not a share. Items 4, 6 and 7: ask for the notes by role and whether usage data was checked. Verdict: "rewrite the guide".
