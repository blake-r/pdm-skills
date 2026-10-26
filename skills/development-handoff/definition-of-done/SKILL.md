---
name: definition-of-done
description: Draft or fix a team's Definition of Done (DoD) — the checklist of conditions that work must meet to count as finished — with how each criterion is checked, automatic checks, what happens to work that fails, who agreed and when the list is reviewed, and produce a one-slide team agreement, or review an existing DoD. Use when "done" means different things to developers, testers and the customer, when tasks are closed but turn out unfinished, or when a team is setting up its quality rules.
---

# Definition of Done

The theory, the survey numbers, limits and the worked cases are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user is writing a DoD or changing one, **review** when the user shows an existing DoD and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the team and the product: who does the work (developers, testers, analysts), what is being built;
- the release process: the path from "code written" to users, environments, who receives the result;
- tools: task tracker, code storage, build and test pipeline (CI/CD);
- existing quality rules: organisational standards, a current list, what "done" means today and for whom;
- what goes wrong: tasks closed but unfinished, returns from testing, disputes about "done";
- who must agree to the list.

If there is an organisational standard, the team's list must include it as a minimum. If several teams work on one product, they share one list. Do not invent facts about the team: mark what the user did not give as unknown.

### 2. Draft the criteria

Write each criterion as a yes-or-no condition and next to it how it is checked and by whom (a test run, a colleague's review, a pipeline rule). Reject vague wording: not "code tested" but what exactly tests it. Start small: three criteria the team really keeps beat fifteen that are ignored; the list grows later on purpose. The slide holds up to eight. Keep acceptance criteria out: they belong to each task, the DoD is the same for all tasks. Definition of Ready is a different list (when work may start) and is not part of the Scrum Guide 2020.

### 3. Checks, failures, review

- Automatic checks: which criteria the pipeline or the tracker can enforce (block a release without unit tests, a task link or a passed review).
- Failure: work that misses a criterion is not done, is not released and goes back to the common list of work. Say whether a part may be released; if the user does not know, mark it unknown.
- Review: how often (the card names a quarter or triggers the team defines) and who edits the list.

### 4. Who agreed and the decision

Name the roles that accepted the list, and the organisational standard if one exists. A list imposed from above or agreed with part of the team will not work: if someone has not seen it, say so and propose to agree it first. Phrase the decision: from which date the list applies, what is added or removed and why.

### 5. Show, then write

Show the agreement in chat first as a table by template blocks: title, scope, criteria with checks, automatic checks, failure, review, who agreed, decision. Write a file only after the user confirms. Ask for the output path (default `definition-of-done-<team>.pptx` in the working directory). Save the data as JSON. The example is the Garda checklist from card.md: a security vendor's article gives it as an example of seven items, and does not say it is the company's adopted list (not e-commerce or fintech). The source names no checkers, no failure rule, no review period of its own and no date, and the JSON says so:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Garda: example DoD checklist from an article",
    "scope": "Tasks and bugs; the article does not say who checks the items",
    "k1": "Code written",
    "h1": "Compiles, no syntax errors",
    "k2": "Code review done",
    "h2": "Code checked by a colleague, no critical comments",
    "k3": "Unit tests passed",
    "h3": "All automated tests pass successfully",
    "k4": "All planned tests executed",
    "h4": "Task tested against the requirements",
    "k5": "No open critical comments",
    "h5": "No critical or blocking problems",
    "k6": "Demo to the customer held",
    "h6": "Task shown to the potential consumer",
    "k7": "Documentation updated",
    "h7": "Updated in line with the changes",
    "k8": "",
    "h8": "",
    "auto": ["Garda suggests automation (example from the article):", "CI/CD does not let code into the stable branch if", "there is no task link, unit tests or review"],
    "fail": ["The article does not describe this"],
    "review": ["The article does not set this", "Advice: once per iteration, per quarter or by triggers"],
    "agreed": ["The article does not say who accepted the list", "Recommendation: developers, testers, analysts"],
    "decision": ["Introduced DoR and DoD so that 'done' means one thing (per the article)"]
  }
}
```

The template has eight criteria rows: leave unused ones empty (`""`). Put what the source does not give (for example who checks) into `scope` or `review`. Limits that fit the rendered slide: title under 60 characters; scope under 100; criteria (k1..k8) under 40; checks (h1..h8) under 90; automatic checks, failure and review: up to four items under 50 each; who agreed and decision: up to four items under 60 each. A list of strings becomes lines, one thought per item. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/definition-of-done.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's DoD, the description of how it is used or screenshots of the tracker and check it against the common mistakes in card.md:

1. Ticks instead of checks: a criterion is marked without a real check (a review that only scrolls the code).
2. Too many criteria, criteria that not every task can meet, or vague wording ("code tested") that two people read differently.
3. The list is imposed from above or agreed with part of the team.
4. The list is out of date: it keeps steps the process no longer has.
5. A criterion nobody was taught to meet.
6. The DoD is taken as proof of correctness: all ticks, yet nobody checked that the task solves the right problem.
7. Unfinished work is passed off as done: items closed with open defects, so progress looks better than it is.

Items 1, 3, 4, 5 and 7 usually cannot be judged from the text alone: ask who agreed the list, when it was last changed, how the criteria are checked in practice, whether the team was shown how to meet them and what happens to a task that fails, instead of reporting a finding. Also check that every criterion says how it is checked, that failed work goes back instead of being released, and that the list does not contradict an organisational standard. Report findings as a numbered list: what is wrong, why it matters, the concrete rewrite. End with a verdict: "list works", "works after changes" or "needs checkable criteria first".

Example: the list "code written, code reviewed, tested, documented", agreed by developers only, last edited a year ago, and the user says testers still return tasks. Findings: item 2 — "tested" is vague, write that all planned tests are run against the requirements; item 3 — testers did not agree, bring them in; item 4 — ask when the list was last reviewed and set a review date; item 1 — ask how "reviewed" is checked. Verdict: "works after changes".
