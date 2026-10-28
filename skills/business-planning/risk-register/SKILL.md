---
name: risk-register
description: Build or check a risk register - one row per risk with risk statement, cause and effect, owner, likelihood and impact on a 1-5 scale, score computed by formula, response (accept, transfer, mitigate, avoid), status and review dates (NIST IR 8286r1; OMB Circular A-11 definition) - and produce an XLSX with live formulas; or review an existing register. Use when a launch, migration, partnership or product line has more risks than people can track, when risks have no owners or review dates, or when the user says "risk register", "risk log", "risk list", "risk matrix", "risk owners", "реестр рисков".
---

# Risk Register

The theory, scheme and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants to build or update a register, **review** when the user brings a finished one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the objective or project the register covers, and who reviews it;
- the risks known so far (sources: pre-mortem, incident history, audits, interviews) and who owns each;
- the scales: what each level 1-5 of likelihood and impact means, and the score bands for High and Medium (template default: High from 15, Medium from 6);
- what is already in place (controls) and what is planned, for the response;
- review dates, if any.

Do not invent risks, owners, scores or dates. A blank owner or response stays blank and is counted in the summary.

### 2. Write and score

Write each risk as an event with a cause and an effect, one owner, and the current likelihood and impact (with existing controls). Do not fill score, rating, priority rank or review flag: the spreadsheet computes them. Choose a response type for the risks above the threshold: accept, transfer, mitigate, avoid (for opportunities: realize, share, enhance, accept).

### 3. Decision

For the top-ranked risks write the decision: respond, escalate, accept with a monitored trigger, or close. Put it in the "decision" field. A register with no decision for its top risks is only a list.

### 4. Show, then write

Show the register in chat first (a table of risks with the scores and ratings you computed by hand, then the decision). Write a file only after the user confirms. Ask for the output path (default `risk-register-<topic>.xlsx` in the working directory).

The JSON below shows the format only. Its values come from the example case in card.md (Highland Community Planning Partnership, Strategic Risk Register, January 2026), not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill the fields with the user's facts.

```json
{
  "text": {
    "title": "Highland Community Planning Partnership, Strategic Risk Register as at January 2026",
    "scope": "Delivery of the Highland Outcome Improvement Plan (HOIP) 2024-2027, reported to the Board on 10 March 2026",
    "decision": "Board noted the update and agreed the revised approach, including the Risk Appetite Statement applied to all strategic risks; funding (02/26), policy implementation (07/26) and data sharing (08/26) seen above appetite"
  },
  "rows": [
    ["Risk 02/26", "Partnership may be unable to sustain long-term financial viability or align funding streams",
     "Reducing or unpredictable budgets, competing demands, short-term or ring-fenced funding, little flexibility to redirect money",
     "Constrained delivery, hindered strategic planning, less ability to invest in preventative or joint approaches",
     "People, Place, Prosperity", "CPP Senior Officers Group", 4, 5, null,
     "Agree budget arrangements beyond May 2027 and partner contributions; align funding streams; explore joint investment, bids and pooled resources",
     null, null, null, null]
  ]
}
```

Row format, in column order: ID, risk statement, cause, effect, category, owner, likelihood (whole number 1-5), impact (whole number 1-5), response type (Accept, Transfer, Mitigate, Avoid, Realize, Share or Enhance; null if not set), response, status (Open, In progress or Closed), date raised, last reviewed, next review (dates as Excel serial numbers, days since 1899-12-30, for example `(date(2026, 3, 10) - date(1899, 12, 30)).days`; null if unknown). Use null for blanks, not "". Do not pass score, rating, priority rank or review flag. Limits: title under 90 characters; scope under 160; decision under 250; ID under 12; risk statement under 110; cause and effect under 130 each; category under 30; owner under 40; response under 160. Up to 50 risks. The "High from" and "Medium from" cells (U6 and U7) can be set with `"cells": {"U6": 12, "U7": 5}`.

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data. Run from the repo root:

```bash
uv run scripts/fill_xlsx.py <this skill dir>/risk-register.xlsx data.json <output>.xlsx
```

`uv run scripts/fill_xlsx.py <template> --list` prints the columns with their hints.

## Mode: review

Take the user's register in any form and check it against the common mistakes in card.md:

1. A risk has no named owner (blank, a group, "everyone").
2. A risk statement is vague and cannot be scored: no event, cause or effect.
3. Scores are not reviewed: no last-reviewed or next-review date, or the date has passed.
4. The score is read as a verdict: high-score risks are treated alike without comparing them with the risk appetite.
5. Inherent and current scores are mixed: it is not stated whether controls are counted, or rows use different bases.
6. The register is a long tail with no ranking or threshold, so the few important risks are buried.
7. A risk has no response, or a response with no cost, owner or date.
8. The table holds scenario detail, assumptions and history that belong in a separate detail record, or the register is treated as the only record.

Items 4 and 5 usually cannot be judged from the table: ask what appetite or threshold applies and whether controls were counted, instead of reporting a finding. Also check that likelihood and impact use the same written scale in every row. Report findings as a numbered list: what is wrong, why it matters, the concrete change. End with a verdict: "register is usable", "usable after fixes" or "not enough to act on".

Example: eight risks, two of them scored 20, no owner is a person, no review dates, no response types. Findings: item 1 - owners are groups; item 3 - no review dates; item 7 - responses are planned actions with no dates. Verdict: "usable after fixes".
