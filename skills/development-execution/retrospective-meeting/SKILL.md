---
name: retrospective-meeting
description: Prepare, facilitate or review a team retrospective (what went well, what went badly, how to improve) and produce a filled retrospective slide with agreed actions. Use when a team wants to look back at an iteration, release, incident or project and decide what to change.
---

# Retrospective Meeting

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants to prepare or run a retrospective or turn raw notes into its outcome, **review** when the user brings a finished retrospective outcome.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the team and the period under review;
- the facts for the period: dates, metrics, incidents, customer complaints, what was planned and what was delivered;
- the actions from the previous retrospective and whether they were done;
- the format: prepare an agenda for a live meeting, or process notes (stickers) the team already wrote.

If the team cannot change its own process, say that the meeting will mostly collect frustration, and suggest escalating the issues to whoever decides.

### 2. Prepare or process

For a live meeting, give an agenda with timeboxes along Derby and Larsen's five stages, with a check of previous actions after the first: set the stage; gather data (silent writing into "good" and "bad"); generate insights (vote with three dots each, discuss the top two or three themes); decide what to do; close. Scale to at most three hours for a month-long period.

For collected notes:

1. Group stickers into themes; keep the team's own words.
2. Rewrite blame into facts about the process ("review waited four days", not a name).
3. Rank themes by votes; if there were no votes, ask the user to rank rather than guessing.
4. For the top themes, gather improvement ideas into "how to improve".
5. Agree on one to three actions, each with an owner, a deadline and a sign of success.

If one theme is a deep failure with unclear causes, suggest a separate root-cause session with the `five-whys` skill. To test an improvement as a hypothesis, suggest `hadi-canvas`.

Do not invent stickers, votes or owners; ask.

### 3. Show, then write

Show the result in chat first: the three columns as a table with votes, then the actions list (what — who — by when — how we will know).

Write a file only after the user confirms. Ask for the output path (default `retro-<team>-<period>.pptx` in the working directory). Save the data as JSON:

```json
{
  "text": {
    "title": "Payments team, 1–14 March",
    "good": ["Release went out without rollbacks (+3)"],
    "bad": ["Review waited 4 days on average (+5)"],
    "improve": ["Review slot every morning"],
    "actions": ["Daily review slot — Anna — from 18.03 — review wait < 1 day"]
  }
}
```

Each list item becomes one line on the slide. Keep five to seven stickers per column; merge the rest into themes. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/retrospective-meeting.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's retrospective outcome in any form and check it against the common mistakes in card.md:

1. Previous actions were checked.
2. Items are facts about the process, not blame of people.
3. Priorities come from the whole team (votes), not from the loudest voices.
4. Improvement ideas address the top-voted problems.
5. There are one to three actions, not a long wish list.
6. Each action has an owner, a deadline and a sign of success.
7. Actions are within the team's control; external issues are escalated.
8. The format varies between meetings, or the answers show no sign of going stale.
9. Items cover the whole period, not only its last days.
10. Top-voted themes are backed by facts, not only by popularity.

Items 1 and 8, and whether someone who evaluates the participants was in the room, cannot be judged from one artifact: ask the user about them instead of reporting a finding. Report findings as a numbered list: where (column or action), what is wrong, why it matters, the concrete fix. End with a verdict: "ready to act", "actions need owners or deadlines" or "no actionable outcome", and the single most important fix.
