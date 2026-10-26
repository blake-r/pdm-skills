---
name: stand-up-meeting
description: Design or fix a team's daily stand-up — purpose, time, length, participants, facilitator, order of talk, preparation, what goes offline, outcome and how the format is checked — and produce a one-slide stand-up agreement, or review an existing stand-up. Use when a team's daily meeting is too long, turns into status reporting, or is being set up for a new team.
---

# Stand-up Meeting

The theory, research numbers, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user is setting up a stand-up or wants to change one, **review** when the user describes or records an existing stand-up and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the team: who does the work, how many people, where they sit (one office, remote, time zones);
- the shared goal for the current iteration or period;
- how the stand-up runs now, if it exists: time, actual length, who speaks to whom, order, who leads;
- what goes wrong: too long, status reports to a manager, problem solving during the meeting, people not listening;
- where the team keeps its tasks.

If there is no shared goal and the members' tasks do not depend on each other, say that the card advises against a daily stand-up and suggest a less frequent sync. Do not invent numbers about the team: mark what the user did not give as unknown.

### 2. Purpose

Phrase why the team meets: progress towards the shared goal, obstacles, the plan for the day. If the meeting mainly serves a manager's need for status, say so and propose another channel for status.

### 3. Time, length, people, facilitator

Same time and place every day, a limit of 15 minutes. Name who takes part — the people who do the work. With more than 12 people, propose splitting into smaller teams. Propose rotating the facilitator. If the meeting breaks the morning, mention the card's option of meeting right before lunch; for a well-communicating team, 3–4 times a week.

### 4. Order of talk and preparation

Propose walking the tasks rather than the people: obstacles, urgent, stuck since the last meeting, the rest by priority. If the team keeps questions per person, keep them about the work and suggest dropping "what I did yesterday". Decide what people prepare beforehand and where (a short written update, a board).

### 5. Offline, outcome, check

Agree how long discussions are stopped and who stays after. The outcome is the plan for the day and requests for help. Agree how the format is checked: time the meetings and share the numbers, ask the team about usefulness every few weeks, and set when to revisit.

### 6. Show, then write

Show the agreement in chat first: purpose, when, length, people, facilitator, order, preparation, offline, outcome, check, decision. Write a file only after the user confirms. Ask for the output path (default `stand-up-<team>.pptx` in the working directory). Save the data as JSON. The example is the PSB case from card.md, after the change; fields the source does not give say so:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "PSB, Linux administrators department (20 people → four teams), spring 2024",
    "purpose": "Not given in the source: the article names no goal against which progress is checked",
    "when": "Every day, in each team at a time convenient for it, before 11:00",
    "length": "20 minutes (previously a planned 30 minutes, sometimes up to an hour and a half)",
    "people": "One of the department's four teams; the size of each is not given in the source",
    "facilitator": "Not given in the source; the department head checks the reports at the meeting",
    "agenda": "The source does not say how the talk goes after the breaks; since summer 2023 — three questions, two minutes per person: what I did yesterday, whether there are problems, what I will do today",
    "prep": "«Quiet hour» 9:00–10:00 before the daily: each person looks at new tasks and fills in the report form the department had already been filling in every morning (yesterday's plan and status, today's plan, counters: no deadline, overdue, not updated for a week, moved more than twice, where help is needed), and sends it to the manager",
    "offline": "Help window after the daily: if an employee asks for help, a meeting with the team lead the same day",
    "outcome": "Not given in the source",
    "check": "Length: it was up to an hour and a half, now 20 minutes. The article does not describe a team survey",
    "decision": "Spring 2024: split the department into four teams, introduce a quiet hour before the daily and a help window after it — to reduce switching between tasks"
  }
}
```

All values are strings; a list of strings becomes lines. Missing keys stay empty. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/stand-up-meeting.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints the placeholders with their hints.

## Mode: review

Take the user's description, agreement or meeting notes and check them against the common mistakes in card.md:

1. People report to the manager instead of the team.
2. "What I did yesterday" takes most of the meeting.
3. Speakers tell the whole story instead of the headline.
4. The whole team solves one problem during the meeting instead of taking it offline.
5. The stand-up opens the day, and nobody starts work before it.

Also check the length against the limit, the number of participants against the card's threshold of 12, and whether anyone measures the meeting. Ask the user instead of reporting a finding when the material alone cannot show it: actual length, who speaks to whom, what happens after the meeting. Report findings as a numbered list: what is wrong, why it matters, the concrete change to the format. End with a verdict: "format works", "works after changes" or "needs a purpose first".
