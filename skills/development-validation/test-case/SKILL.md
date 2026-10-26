---
name: test-case
description: Write test cases for a requirement or user story — name as a goal, preconditions, steps in the form "action → expected result", overall expected result, source of the expectation, type and priority — and keep them in a spreadsheet with run results, or review existing test cases. Use when the user needs test cases for a feature or API method, wants to turn acceptance criteria into checks, or asks why their test cases are vague or never find bugs.
---

# Test Case

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user needs test cases written or recorded, **review** when the user brings existing test cases to check.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the requirement or story the cases are derived from: text, acceptance criteria, a link to the documentation;
- the risk: what happens to the user or the business if this breaks;
- the environment: test environment, build or version, required data and access;
- test data and states that must exist before a check (an account, an application, a signed contract);
- the existing format or regulation for cases, if the team has one: naming, fields, where cases live.

If the requirement does not say what the result should be, ask for it. Do not infer the expected result from the code or from what the system happens to do: the card names the code as the wrong oracle. If the user cannot say, leave the expectation empty and mark the case as open. If the user wants to explore a feature without a script, say that the card treats a case as a help for the tester, not as the test, and ask whether cases are needed at all.

### 2. Choose what to check

List the things worth checking in the requirement: a function, an operation, a quality attribute. For each, cover the case types of the Banki.ru prompt: main scenario, negative cases (wrong action, refusal), input validation and boundary values (the card names the ISTQB boundary value analysis for the edges of ranges). Split input data into classes the system treats the same way and take one check per class, plus the edges of ranges. Order by the risk from step 1. The Banki.ru prompt asks for 2–3 main, 3–4 negative, 2–3 validation and 1–2 edge cases per task: a point of comparison, not a rule. Do not pad: a case that checks nothing new is waste.

### 3. Write each case

- **Name:** the goal in one line, what is checked and under which condition. Not "check that the method works correctly".
- **Preconditions:** the state of the environment and data before the first step, or a reference to the case that prepares it.
- **Steps:** one action and its expected result per line, "action → expected result", with concrete values (status code, message text, field names). Do not tie steps to interface details that change soon.
- **Expected result:** the overall outcome, taken from the requirement.
- **Basis:** where the expectation comes from: a requirement item, documentation, an agreement. Do not infer it: if the user has not named a source, write that the source is not given.
- **Type and priority:** type is one of the allowed words below; priority only if the user wants it, from the risk.

Never invent values, error texts or endpoints. Mark the missing ones as unknown.

### 4. At a run

Fill the result (`passed`, `failed`, `skipped`) and the actual result. For a failed case, say whether it points at a defect or at a mistake in the case itself.

### 5. Show, then write

Show the cases in chat first: a table with ID, name, type, priority, preconditions, steps, expected result, basis; then the counts by type and what is still open. Write a file only after the user confirms. Ask for the output path (default `test-cases-<feature>.xlsx` in the working directory). Save the data as JSON. The example is the Banki.ru case from card.md: the source shows no ID, type, priority or run result, no risk and no environment description, so those are `null` or say that the source does not give them:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Banki.ru: test case from the article about the test case generation bot, 9.06.2026",
    "item": "Method /depositAccount: request the client's bank details by leadId; the case description links to the method documentation in Confluence",
    "risk": "Not given in the source",
    "env": "Not stated in the source; in the preconditions: a deposit application and a signed contract, for example for Sinara Bank"
  },
  "cells": {},
  "rows": [
    [
      null,
      "/depositAccount - Request the client's bank details by leadId with an active contract",
      null,
      null,
      "A deposit application is created and a contract is signed, for example for Sinara Bank",
      "Send POST /depositAccount with the leadId of an active contract → Response code 200\nCheck that the accountNumber, bik, bankName fields are present in the response body → All fields are present and not empty\nCheck the record in the midb.deposit_account table → The record matches the API response",
      "The method returns the correct client bank details with code 200",
      "Reference to the documentation in the case description; link to the outcome is not given in the article",
      null,
      null
    ]
  ]
}
```

Each row in `rows` has ten values in this order: ID, name, type, priority, preconditions, steps, expected result, basis, result, actual result. Put the steps of one case in one string, separated by `\n`, each as "action → expected result". Use `null`, not an empty string, for unknown values: `null` leaves the cell empty. The template has no formula columns, so every value is yours. Allowed words, which the totals count, so check the spelling: type — `main`, `negative`, `validation` or `boundary`; priority — `high`, `medium` or `low`; result — `passed`, `failed` or `skipped`.

Length limits that fit the template columns:

| Field | Limit |
|---|---|
| `title`, `item`, `risk`, `env` | up to 200 characters each; `title` up to 100 |
| ID | up to 12 characters; do not change it later |
| name | up to 100 characters |
| preconditions | up to 300 characters |
| steps | up to 6 lines, each up to 150 characters |
| expected result, actual result | up to 200 characters each |
| basis | up to 120 characters |

The template has room for 50 cases. For more, split by feature into several files. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_xlsx.py <this skill dir>/test-case.xlsx data.json <output>.xlsx
```

`uv run ../../../scripts/fill_xlsx.py <template> --list` prints the columns with their hints. The totals block counts cases by type, cases with an empty "Expected result" (must be 0), cases run, failed and the share passed.

## Mode: review

Take the user's test cases in any form (a table, an export from a test management system, text) and check them against the common mistakes in card.md:

1. The expected result is vague ("check that the method works correctly") instead of a concrete value, status or error text.
2. A step holds several actions, or the result is given only at the end, so it is unclear where the case failed.
3. The expected result is taken from the system's current behavior or code, not from the requirement; no basis is given.
4. The cases are treated as the test itself, and their count as the measure of work: no exploration, coverage judged by number of cases.
5. The cases are not revisited: old regression cases that pass for years with no code changes are kept without a review.

Also check for the missing types: only main scenarios, no negative or boundary cases. Ask the user instead of reporting a finding when the material alone cannot show it: where the expectation comes from, how long the cases have been passing, how coverage is judged. Report findings as a numbered list: the case and the field, what is wrong, why it matters, the concrete fix with a rewritten text. End with a verdict: "cases are ready", "ready after fixes" or "rewrite the cases".

Worked example. The user brings this case:

> Name: /depositAccount - check. Steps: 1. Send POST /depositAccount, check the response fields and the table record. Expected result: the method works correctly.

1. Mistake 1, field "Expected result": "the method works correctly" can be neither passed nor failed. Fix: "The method returns the client's bank details with code 200".
2. Mistake 2, field "Steps": one step holds three actions and no result after each. Fix: split into "Send POST /depositAccount with the leadId of an active contract → Response code 200", "Check that the accountNumber, bik, bankName fields are present in the response body → All fields are present and not empty", "Check the record in the midb.deposit_account table → The record matches the API response".
3. The name does not say the condition. Fix: "/depositAccount - Request the client's bank details by leadId with an active contract". There are no preconditions: add the application and the signed contract.

Mistakes 3–5 cannot be judged from one case: ask where the expectation comes from. Verdict: "ready after fixes".
