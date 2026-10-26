# Kanban Board

## Essence

A kanban board shows the flow of work: columns are the stages from start to finish, cards are units of work. Kanban Guide 2025: kanban is a strategy for optimizing the flow of value; the flow is described, actively managed and improved. The board is the visible part of this description: besides the columns it has a work-in-progress limit (WIP) and explicit rules for moving between stages.

## When to use and when not to

Use when work flows continuously and predictable timelines are needed: support, service teams, development without iterations.

Do not use it as a list of "to do / doing / done" without limits and rules: such a board does not manage the flow.

Limitations:

- **There is no single board format.** Kanban Guide: "There are no specific guidelines for how a visualization should look." The columns describe your process.
- **There are no right limits.** OTP Bank: "we do not have correct limit values for all teams". The limit is chosen and changed based on data.

## Scheme

```
           │ commitment                              finish │
Queue →    │ Analysis [N] → Work [N] → Review [N] →   Done   │
           │  exit rule     exit rule     exit rule           │
⚑ blocker — a flag on the card, not a column
Metrics: WIP · throughput · cycle time · age
```

## How to apply

1. **Describe the stages** the work really passes through, including waiting. Mark the commitment point (the Guide says "started" point) — the time is counted from it — and the finish point.
2. **Set a WIP limit** for the stages, per person or for the whole system. New work is pulled when a place frees up. Little's law: in a stable system, WIP equals throughput multiplied by the average time in the system.
3. **Write exit rules** for the stages next to the board.
4. **Mark a blocker with a flag,** with a reason and a date when it will be lifted, not by moving it to a separate column.
5. **Agree on replenishment:** when, how many cards and who puts new work in.
6. **Track the four Kanban Guide metrics:** WIP, throughput (how many were finished in a period), age of started work, cycle time (from start to finish). A percentile is the time within which a given share of cards fits: the 85th percentile is the time for 85% of cards. Take the expected time from past data: "85% of cards in N days or faster".
7. **Look for the bottleneck:** by time in statuses, find the stage where cards stay the longest. Review a card older than N days right away. Change the board or a rule and check it by the metrics.

## Example

T-Bank, seven designers serving 10 product teams, 20–30 tasks per month, no iterations. A task took from a couple of days to three months, some up to 100 days. Predictability is the ratio of the 98th percentile of completion time to the median (the 50th percentile, the middle of the series); the company's threshold is 5.6.

Status chain: Specification → To Do → Hold → Design → Customer Review → Design Review → Done. The commitment is taken on entry to Specification, the finish is at Done. To Do is a buffer, Hold is a block.

Time in statuses before the changes, days:

| Status | Median | 85% | 95% |
|---|---|---|---|
| Hold | 12.1 | 27.6 | 65.7 |
| Design | 2.7 | 13.4 | 19.9 |

Decision: "I removed the Hold column from our kanban board". Instead, a blocker flag with a reason and a lift date from the blocking party, and a blockers register. At the same time, personal limits were introduced (do not take a new task when there are three or four in progress), long tasks are reviewed once every three months, plus decomposition and a checklist for task setup.

| | Dec 2023 | Jan | Feb | Mar | Apr | May | Jun 2024 |
|---|---|---|---|---|---|---|---|
| Predictability 98/50 | 13.7 | 10.5 | 14.7 | 8.9 | 6.2 | 5.5 | 3.3 |

What the case lacks: a snapshot of the board, limits per column, and completion time in days before and after. There are several measures, and the contribution of the Hold column was not measured. T-Bank is a fintech company; the designers are a service team for internal product teams.

Case source: E. Stremousov, [«How to improve the predictability of design delivery with team performance metrics»](https://habr.com/ru/companies/tbank/articles/901798/), T-Bank blog on Habr, 21.04.2025.

## Common mistakes

- **No limits, or they are not kept.** Arto Kiiskinen (Eficode): most teams have no limit, and those that do rarely keep it. Ahmad et al.: respondents called managing the WIP limit difficult.
- **A parking column.** "Waiting" collects forgotten cards.
- **Pushing instead of pulling.** Work is passed on although there is no free place.
- **Looking only at development.** Kiiskinen: teams forget about demos and feedback.
- **No transition rules.** It is unclear when a card is ready for the next stage.
- **Not watching card age.** Kanban Guide: age is one of four mandatory metrics, and items must not age unnecessarily against the expected time; age flags a card that is overdue while still in progress.
- **Percentiles on a small sample.** With 20–30 cards per month, the 98th percentile is set by one or two of the longest cards: watch the trend over several periods.

## Source

J. Coleman, D. Vacanti, [«The Kanban Guide»](https://kanbanguides.org/english/), 2025; Kanban University, [«Official Guide to The Kanban Method»](https://kanban.university/kanban-guide/); D. (nickname next_data), senior Agile coach, [«How the Kanban method affected the bank's teams»](https://habr.com/ru/companies/otpbank/articles/802867/), OTP Bank blog on Habr, 26.03.2024; A. Kiiskinen, [«Solving the 7 most common Kanban mistakes»](https://www.eficode.com/insights/blog/solving-the-7-most-common-kanban-mistakes-that-ruin-your-development), Eficode, 2022; M. O. Ahmad et al., [«Usage of Kanban in Software Companies»](https://personales.upv.es/thinkmind/dl/conferences/icsea/icsea_2014/icsea_2014_6_20_10093.pdf), ICSEA 2014; [Little's law](https://en.wikipedia.org/wiki/Little%27s_law).

## See also

- Alternative to Sprint: A sprint fixes work length; a kanban board keeps continuous flow with WIP limits.
- Enhanced by Stand-up Meeting: walk the board at the stand-up to surface blockers and what needs help today.
- Enhanced by Retrospective Meeting: bring the board's cycle time and bottleneck data to the retrospective.
- Preceded by Product Backlog: the ordered backlog supplies the cards pulled into the first column.
- Enhanced by Gantt Chart: Track daily flow here; use the Gantt deadline view to check the schedule holds.
