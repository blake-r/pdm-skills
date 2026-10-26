# Stand-up Meeting

## Essence

A stand-up is a short daily team meeting: check progress toward the shared goal, name the obstacles and adjust the plan for the day. In Scrum, an approach to development in short iterations, it is the Daily Scrum: 15 minutes every day, at the same time and place, for the people who do the work. Jeff Sutherland, in the first Scrum team (Easel, 1993), took over a meeting from Borland, where it went on "at least an hour", and cut it to 15 minutes and three questions (Scrum Guide 2017: what did I do yesterday, what will I do today, what is in my way).

## When to use and when not to

Use when the team has a shared goal and the participants' tasks depend on each other.

Do not use it as a report to a manager. Viktoria Stray, Dag I. K. Sjøberg and Tore Dybå (12 teams, 79 meetings): stand-ups are received worst when they are a report to the manager, and meetings seem frequent and long.

Limitations:

- **Size.** Satisfaction with the meeting drops noticeably when a team has more than 12 people (survey of 221 developers, Stray, Moe and Bergersen).
- **The meeting interrupts work.** Stray, Moe and Sjøberg advise meeting right before lunch, and for a team that works well together, 3–4 times a week.
- **The three questions are not mandatory.** The Scrum Guide 2020 removed them: the team chooses the structure, as long as the meeting leads to the goal and gives a plan for the day.

## Scheme

```
Before the meeting    Stand-up, ≤ 15 minutes          After
preparation →         1 obstacles               →     plan for the day
                      2 urgent                          help
                      3 stuck                           questions taken offline
                      4 the rest by priority
```

## How to apply

Inputs: the goal of the iteration or period, the list of tasks, the participants, who are the people doing the work.

1. **Agree on time, place and limit:** the same every day, no longer than 15 minutes.
2. **Choose the structure.** Jason Yip suggests walking the board rather than the people (walk the board), in Pawel Brodzinski's order: obstacles, urgent, stuck, the rest by priority. If by person, ask about the work, not about the person.
3. **Speak to the team, not to the facilitator; rotate the facilitator.** According to Yip, without this, walking the board slides into a report to the boss.
4. **A headline, not a story.** A long discussion goes afterwards, with the right people.
5. **The outcome is the plan for the day and requests for help.**
6. **Check the format.** Time the meetings and publish the length (Yip). Periodically ask the team whether it is useful.

How to read the measurements. In Stray, Moe and Sjøberg's study (102 meetings, 15 teams), the stand-up lasted 11.7 minutes on average. Only 34% of the time went to the three questions, and almost as much, 31%, to discussing problems. The authors advise not talking about what was done yesterday: teams that tried this did not go back to that question. Longer than the limit means split the team or move discussions out; no benefit means meet less often.

## Example

PSB, Linux administrators department. In the summer of 2023 they introduced a daily stand-up with three questions, two minutes per person.

| | Before | Now, spring 2024 |
|---|---|---|
| Composition | 13, then 20 people at one meeting | the department is split into four teams |
| Length | plan — 30 minutes, sometimes up to an hour and a half | 20 minutes, in each team before 11:00 |
| Preparation | a report form every morning | a "quiet hour" 9:00–10:00 before the daily: new tasks and the report |
| Afterwards | — | a help window with the team lead the same day |

The report form from the article: yesterday's plan with statuses, today's plan; counters: tasks without a deadline, overdue, not updated for a week, moved more than twice, "where I need help". At the daily, the manager checks the report against the task table.

What the case lacks: the order of talk after the breaks, measurements other than length, a team survey, the size of the four teams. This is infrastructure operations, not a product team. And the manager checks reports during the meeting; research names this as the main cause of dissatisfaction.

Case source: A. Khusainov, [«How to tame the chaos in a distributed and fast-growing IT team»](https://habr.com/ru/articles/911170/), PSB blog on Habr, 22.05.2025.

## Common mistakes

- **A report to the boss.** Participants talk to the manager, not to each other (Yip).
- **Yesterday eats the meeting.** Telling what was done is the least liked part for participants, but it takes the most time (Stray et al.).
- **A story instead of a headline.** The rest switch off.
- **A long analysis in front of everyone.** Discussing problems is useful, but a long analysis belongs with those it concerns.
- **The stand-up opens the day.** Yip: people may not start project work until it.

## Source

K. Schwaber, J. Sutherland, [«The Scrum Guide»](https://scrumguides.org/scrum-guide.html), 2020; J. Sutherland, [«The Origin of The Daily Stand-up»](https://www.linkedin.com/pulse/20140926150354-136414-the-origin-of-the-daily-stand-up), 2014; J. Yip, [«It's Not Just Standing Up: Patterns for Daily Standup Meetings»](https://martinfowler.com/articles/itsNotJustStandingUp.html), 2016; V. Stray, D. I. K. Sjøberg, T. Dybå, [«The daily stand-up meeting: A grounded theory study»](https://doi.org/10.1016/j.jss.2016.01.004), Journal of Systems and Software, 2016; V. Stray, N. B. Moe, D. I. K. Sjøberg, [«Daily Stand-Up Meetings: Start Breaking the Rules»](https://arxiv.org/abs/1808.07650), IEEE Software, 2018; V. Stray, N. B. Moe, G. R. Bergersen, [«Are Daily Stand-up Meetings Valuable?»](https://doi.org/10.1007/978-3-319-57633-6_20), XP 2017.

## See also

- Enhanced by Kanban Board: walking the board rather than people keeps the stand-up on the flow of cards.
- Enhanced by Sprint: the daily stand-up runs inside the sprint and checks progress toward its goal.
- Preceded by Team Canvas: agree on roles and working rules on the canvas, then hold the daily to them.
