---
name: kanban-board
description: Design or fix a team's kanban board — columns from start to finish, WIP limits, exit rules, start and finish points, lanes, blocker handling, replenishment, flow metrics and an expected delivery time — and produce a one-slide board agreement, or review an existing board. Use when work piles up, tasks hang on the board, deadlines are unpredictable, or a board is being set up for a team with continuous work.
---

# Kanban Board

The theory, the numbers, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user is setting up a board or wants to change one, **review** when the user describes or shows an existing board and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the team: who works on the board, how many people, what kind of work (support, service, development);
- how work arrives: how often, how much, who sets it, whether it comes in a steady flow or in fixed iterations;
- the stages work really passes through, including waiting, and where it starts and where it counts as finished;
- how the board looks now, if it exists: columns, limits, rules, how blockers are shown;
- what goes wrong: tasks hang, deadlines slip, too much in progress, urgent work breaks the order;
- what data exists: dates when cards entered and left stages.

If the work does not come as a flow (a fixed plan with fixed iterations and no need to forecast), say that the card applies the board to flow work and ask what the team wants from it. Do not invent numbers about the team: mark what the user did not give as unknown.

### 2. Columns and the commitment point

List the real stages, waiting included. Mark the commitment point (the column from which time is counted) and the finish point. There is no standard board: the columns follow the team's own process.

### 3. Limits and exit rules

Set a WIP limit per stage, per person or for the whole system. Say that there are no right values for every team: propose a starting number, tell the team to watch the metrics and change it. New work is pulled only when a place frees up. For each stage write an exit rule, a short check of when a card may move on, and keep it next to the board. Give Little's law once if the team asks why: with the same throughput, less WIP means shorter time.

### 4. Lanes, blockers, replenishment

Decide whether urgent work gets its own lane and how many such cards may be in progress at once. Blockers are a flag on the card with a reason and a date when it will be lifted, not a separate column. Agree on replenishment: when, how many cards and who puts new work in the first column.

### 5. Metrics and expected time

Choose the four metrics: WIP, throughput, cycle time, age of started work. Say where they are viewed and how often. Phrase an expected time as "85% of cards in N days or faster" and take N from the team's own data. If there is no data, mark it unknown and propose to collect the dates first.

### 6. Bottleneck and the change

Name the stage where cards pile up and age. Propose one change to the board or the rules and how to check it by metrics and by when.

### 7. Show, then write

Show the agreement in chat first as a table by template blocks: title, six columns with limits and exit rules, start and finish, lanes, blockers, replenishment, metrics, expected time, decision. Write a file only after the user confirms. Ask for the output path (default `kanban-board-<team>.pptx` in the working directory). Save the data as JSON. The example is the T-Bank case from card.md; fields the source does not give say so:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "T-Bank, TWork Service designers, 2024",
    "c1": "Specification", "c2": "To Do", "c3": "Design", "c4": "Customer Review", "c5": "Design Review", "c6": "Done",
    "w1": "not specified per column", "w2": "not specified", "w3": "not specified", "w4": "not specified", "w5": "not specified", "w6": "—",
    "x1": "specification checked against the general checklist", "x2": "not described", "x3": "not described", "x4": "acceptance by the requester", "x5": "review by the design team", "x6": "—",
    "bounds": ["Start: Specification (commitment)", "Finish: Done"],
    "lanes": "Not described in the article",
    "blocked": ["Hold column removed", "Flag + reason in a comment", "Lift date set by the blocking party", "Blockers register"],
    "replenish": "Not described; 20–30 tasks per month",
    "metrics": ["Hold before changes: median 12.1, 95% — 65.7 days", "Design before changes: median 2.7, 95% — 19.9 days", "Predictability 98/50: 13.7 in Dec. → 3.3 in June"],
    "sle": ["The article gives no «X% within N days» expected time", "Spread tolerance 98/50 ≤ 5.6"],
    "decision": ["Bottleneck: waiting in Hold", "Column removed, flag and lift date introduced", "Personal limit: 3–4 tasks per designer", "Review of long tasks: longer than 10 days", "Check: predictability by month"]
  }
}
```

The template has six columns: leave unused ones empty or put "—". Limits that fit the rendered slide: title under 60 characters; column names under 18; limits (w1..w6) under 25; exit rules (x1..x6) under 45; bounds, lanes, blocked and replenish: up to four items under 40 each; metrics: up to four items under 55; expected time: up to three items under 55 (the percentile ratio such as 98/50 is a tolerance for spread, not an expected time); decision: up to five items under 45. A list of strings becomes lines, one thought per item. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/kanban-board.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's board description, photo notes or rules and check them against the common mistakes in card.md:

1. There are no limits, or they are not kept.
2. A parking column ("Waiting", "Blocked") collects cards that get forgotten.
3. Work is pushed to the next stage, not pulled, although it has no free place.
4. The board covers only development work: demos and feedback from users and stakeholders are missing.
5. There are no exit rules: it is unclear when a card is ready for the next stage.
6. Nobody watches the age of cards, although age shows that a card is past the expected time while it is still in progress.
7. Percentiles are read on a small sample: with 20–30 cards a month the 98th percentile is set by one or two of the longest cards, so watch the trend over several periods.

Items 1, 3, 6 and 7 usually cannot be judged from the description alone: ask for the limits, how often they are broken, who decides to start new work and whether anyone looks at card age, instead of reporting a finding. Also check that the commitment and finish points are marked and that metrics and an expected time exist. Report findings as a numbered list: what is wrong, why it matters for the flow, the concrete change to the board. End with a verdict: "board manages the flow", "works after changes" or "needs stages and rules first".

Example: columns "To do, Doing, Waiting, Done", no limits, no rules, and the user says the cards in "Waiting" sit for weeks. Findings: item 1 — no limits, so work piles up; set a start limit and tune it by metrics; item 2 — "Waiting" is a parking column, replace it with a blocker flag with a reason and a date; item 5 — no exit rules, write one per stage; item 6 — ask whether card age is tracked. Verdict: "works after changes".
