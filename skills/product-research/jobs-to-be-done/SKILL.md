---
name: jobs-to-be-done
description: Find the jobs customers "hire" a product for - from interviews about recent real cases - write them as job stories ("When <situation>, I want to <action>, so that <outcome>"), pick the main jobs, attach a product solution to each, and produce a one-slide PPTX with three job stories; or review existing job stories. Use when the team needs to know why customers come to the product and what they do instead of it, when the product is overloaded and simple actions are hard, or when user descriptions by age and income lead to no decisions.
---

# Jobs-to-be-Done

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a product and research material, **review** when the user brings finished job stories.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and the decision the jobs should feed;
- the customers: who recently started using the product, left it, or solved the task another way;
- the material: interview notes or transcripts about specific recent cases, support tickets, reviews, with how many people and when;
- what customers do instead of the product today (competitors, workarounds).

Do not invent jobs, situations or quotes. If there are no interviews, offer an interview plan (whom, how many, questions about one recent case: where they were, what happened, what they tried, what stopped them) and stop.

### 2. Write job stories

One situation per story: "When <situation>, I want to <action>, so that <outcome>". Keep product features out of the story. Mark stories that rest on one interview. Merge duplicates; split stories that cover a whole area ("managing money").

### 3. Choose and solve

Rate each job by how often it occurs and how badly it is solved today, with the evidence. Pick up to three main jobs and propose a solution for each, plus the behaviour that will show it works (people do it in the product instead of the workaround).

### 4. Show, then write

Show in chat first: all job stories with sources, the ratings, the three main jobs with solutions and checks. Write a file only after the user confirms. Ask for the output path (default `jtbd-<product>.pptx` in the working directory). Save the data as JSON (the example is the Bank of Jordan case from card.md; the result is the agency's own report):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Bank of Jordan: mobile bank, UXDA scenarios",
    "job1": "Check the balance",
    "job1_when": "Shopping in the grocery store",
    "job1_want": "Quickly check how much money I have available",
    "job1_so_that": "I can be sure I have enough for everything I buy",
    "job1_solution": "Balance quick to reach, no searching in the app",
    "job2": "Pay bills",
    "job2_when": "Managing household bills",
    "job2_want": "Know which bill payments are still unpaid this month",
    "job2_so_that": "I can immediately handle them",
    "job2_solution": "Not described in the source",
    "job3": "Transfer money to family",
    "job3_when": "My daughter calls: I forgot her piano lesson money",
    "job3_want": "Quickly transfer money to her",
    "job3_so_that": "She does not have to miss the lesson",
    "job3_solution": "Transfer to a saved recipient in a few taps",
    "who": ["Typical bank clients, for example a mother of two who combines work and family", "Initially: rating 2.8, simple operations — through a branch"],
    "result": ["Google Play rating 2.8 → 4.7 over six months; App Store also 4.7", "Agency data; the relaunch date is not given", "Growth is the result of the whole redesign"]
  }
}
```

Each `jobN` is a short name (under 30 characters); each `jobN_*` field is one sentence of under 70 characters. `who` and `result` take up to five items of under 90 characters; each list item becomes its own paragraph. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/jobs-to-be-done.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's job stories in any form and check them against the common mistakes in card.md:

1. Each story describes a job, not a feature ("I want a button" is a solution).
2. Each story has a concrete situation ("when").
3. Stories come from interviews about real recent cases, with sources.
4. Stories are narrow enough to suggest a decision; area-wide ones are split.
5. Each chosen job has a solution and a behavioural check, not just "feature shipped".

Report findings as a numbered list: what is wrong, why it misleads the decision, the concrete fix. End with a verdict: "stories support the decision", "support it after fixes" or "not enough data".
