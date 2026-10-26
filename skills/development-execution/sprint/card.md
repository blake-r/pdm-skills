# Sprint

## Essence

A sprint is a stretch of work of constant length, no longer than a month, at the end of which the team has a finished result that can be used — an increment. A sprint has one goal: it explains why the sprint is needed and leaves the team freedom to choose the specific work. This is the core cycle of Scrum, an approach built on such iterations. Ken Schwaber described it at the OOPSLA'95 workshop: "usually from one to four weeks".

## When to use and when not to

Use when a permanent team builds the product and the result can be released in parts. Scrum Guide 2020: short sprints give more learning cycles and less risk.

Do not use when the work is a flow of unrelated small requests: support, checks, audit requests. Roman Pichler told a maintenance team of a financial institution that Kanban, a continuous flow, might suit it better than Scrum.

Limitations:

- **The goal is a commitment, the scope of work is not.** Changes that threaten the goal and a drop in quality are unacceptable. The scope is clarified with the product owner, the person responsible for value and the order of work. Only they can cancel the sprint, if the goal is obsolete.
- **A short sprint puts pressure on experiments.** Mike Cohn: an unsuccessful experiment can break the sprint's promise; he estimates that a team that stretches and reaches falls short about 20% of the time, and calls it acceptable.

## Scheme

```
┌─ Sprint: 1–4 weeks, fixed length ───────────────┐
│ Planning         Work                Review     │
│ why? → goal      ● items for the goal  increment │
│ what? → items    ○ other items         results  │
│ how? → plan      + added work                   │
└───────────── next sprint right away ─────────────┘
```

## How to apply

1. **Choose the length and do not change it** from sprint to sprint. PSB: "adjusting the sprint size to fit what needs to be done is a big mistake"; split the tasks instead.
2. **Calculate capacity:** each person's working days without vacations and training × ideal hours per day. An ideal hour is work on a task without distractions; Rosbank takes 4–5.6 such hours out of an 8-hour day. Set the limit from past sprints: by what was done, not by what was taken. It is a guideline.
3. **Planning answers the three questions of the Scrum Guide:** why the sprint is valuable, what can be done, how. The goal is one and speaks about the result; it does not list items.
4. **Take items from the top of the ordered list of work.** For each, make a plan and get an estimate from the people who will do it. Mark the items without which the goal will not be reached. Keep to the limit.
5. **During the sprint,** discuss the scope with the product owner, but do not touch the goal. Mark incoming work as added.
6. **The sprint review** is a working session, not a presentation. The review is not a gate to releasing value: ready work may be released earlier (Scrum Guide 2020).
7. **Record the results:** whether the goal was met, how much was taken, added and not done. Cohn's benchmark for Rosbank: all promised work was done in 8 of the last 10 sprints. A lot not done means take less next time; a lot added means keep a reserve.

## Example

Eight Rosbank teams plan this way, with sprints of three weeks.

The form from the article: sprint 57, 06–26.06.2022: six people, 64 person-days after vacations and training × 8 h × 50–70% = 256–358.4 ideal hours.

Statistics of sprints 62–67 of one team, in ideal hours ("Added" also counts raised estimates of subtasks):

| Sprint | 62 | 63 | 64 | 65 | 66 | 67 |
|---|---|---|---|---|---|---|
| Taken at the start | 190 | 150.5 | 105 | 150 | 118.5 | 156 |
| Added | 18 | 34.5 | 15 | 0 | 92.5 | 24 |
| Removed and remaining | 85 | 30 | 86 | 100 | 75 | 27 |
| Done | 123 | 155 | 34 | 50 | 136 | 153 |
| Limit | — | 50–70 | 100 | 80 | 80 | 80 |

In the limit row after sprint 67, "135 IH" is circled: the agreed limit. How it was derived is not stated.

Year total for one team (whether it is the same team is not stated): in the first three sprints since February 2022, 113 of the 213 hours taken (53%) were not done; a year later, 13 of 114 (11%) were not done.

What the case lacks: the sprint goal (it is hidden in the screenshot from the task tracking system; the author only writes that the goal usually covers 3–4 of the 10–20 items). There is no share of achieved goals and no justification for the limit.

Case source: S. Kazachenko, [«Short-term and long-term planning in Scrum and agile»](https://habr.com/ru/companies/rosbank/articles/744246/), Rosbank blog on Habr, 07.07.2023.

## Common mistakes

- **The goal restates the items.** Pichler: the goal often repeats the task list rather than the reason for the sprint.
- **Several unrelated goals.** Feedback is hard to link to the work.
- **The sprint as a checklist.** Cohn: success is measured by closed tasks and velocity.
- **Mini-waterfall.** Mark Levison: team members work in sequence (analysts a sprint ahead, testers a sprint behind), and the review shows half-done work.
- **Promising more than was done.** The plan does not rest on past sprints.

## Source

K. Schwaber, J. Sutherland, [«The Scrum Guide»](https://scrumguides.org/scrum-guide.html), 2020; K. Schwaber, [«SCRUM Development Process»](http://jeffsutherland.org/oopsla/schwapub.pdf), OOPSLA'95; R. Pichler, [«The Product Owner's Guide to Effective Sprint Goals»](https://www.romanpichler.com/blog/effective-sprint-goals/), 2012, and [«A Template for Formulating Great Sprint Goals»](https://www.romanpichler.com/blog/sprint-goal-template/), 2014; M. Cohn, [«When Do Agile Teams Make Time for Innovation?»](https://www.mountaingoatsoftware.com/agile/when-do-agile-teams-make-time-for-innovation), 2023; M. Levison, [about scrummerfall](https://agilepainrelief.com/blog/scrum-team-scrummerfall/), Agile Pain Relief, page updated 2026; M. Lyutsau, [«Seven Scrum implementation problems we did not know about»](https://habr.com/ru/company/psb/blog/420265/), PSB blog on Habr, 2018.

## See also

- Preceded by Product Backlog: take the sprint's items from the top of the ordered backlog.
- Enhanced by Stand-up Meeting: the daily stand-up checks progress toward the sprint goal.
- Followed by Retrospective Meeting: Review this sprint's results and pick changes for the next.
- Alternative to Kanban Board: a kanban board suits flow work without fixed iterations.
- Preceded by Objectives and Key Results (OKR): Take the actions under each key result as sprints of constant length.
- Enhanced by Definition of Done: Use the DoD as the increment bar; unfinished work returns to the backlog.
- Alternative to Gantt Chart: Use fixed-length sprints instead of exact Gantt dates when the scope is unclear.
