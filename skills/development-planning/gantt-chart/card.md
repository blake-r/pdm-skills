# Gantt Chart

## Essence

A Gantt chart is a project plan on a timeline: tasks run down the vertical axis, time runs along the horizontal axis, and each task is shown as a bar from its start date to its end date. It shows what is done, when, and by whom, and which tasks set the deadline for the whole project.

## When to use and when not to

Use it in projects with a known set of work, dependencies between the tasks, and an external deadline: a launch by a regulator's date, a system migration, an integration with a partner, or several teams working toward one result.

Inputs: the list of work, its durations, dependencies (what follows what), owners and their load, and external dates, i.e. milestones.

Do not use it:

- **when the set of work is unknown**: in a research task the plan goes stale faster than it can be updated;
- **for day-to-day team management**: the chart answers "are we on track for the date?", not "what should we do today?";
- **without aggregation in large projects**: hundreds of linked rows become unreadable.

The main limitation: a chart turns assumptions into dates and creates a sense of certainty. The higher the uncertainty, the more often the plan has to be revised.

## Scheme

| Task · owner | Week 1 | Week 2 | Week 3 | Week 4 | Week 5 |
|---|---|---|---|---|---|
| Task 1 · Anna | ██ | ██ | | | |
| Task 2 · Boris | | ██ | ██ | ██ | |
| Task 3 · Anna, after task 1 | | | ██ | ██ | |
| Task 4 · Vera, after tasks 2 and 3 | | | | | ██ |
| ◆ Milestone: launch | | | | | ◆ |

In a full chart, arrows connect the end of one task to the start of its dependent task. A vertical line marks today, and the completed part of each bar is filled in.

## How to apply

1. **Break the project into tasks** of a few days to two or three weeks each, with a clear result for each.
2. **Estimate durations** in calendar days and assign an owner.
3. **Record dependencies.** The main type is finish-to-start: a task starts after its predecessors finish.
4. **Build the plan** from the start date: each task is placed right after its predecessors, and rows are ordered by start date.
5. **Mark milestones**: events with no duration, such as external dates, decisions, or releases.
6. **Find the critical path**: the longest chain of dependent tasks. Its length is the project duration, and any delay to a task on it moves the finish date. Other tasks have slack: how long they can be delayed without moving the finish date.
7. **Check the load.** Two bars for the same owner at the same time: move one task or hand it to someone else.
8. **Keep the plan up to date.** Record progress once a week. If a critical-path task falls behind, decide immediately: add people, cut scope, or move the milestone.

The result is a readiness date with its rationale, and a list of the tasks that date depends on.

## Example

British Open Banking: nine of the largest banks, at the request of the competition regulator (Competition and Markets Authority, CMA), implemented open application programming interfaces (APIs) for payments and account access. The implementation plan, the CMA Order Roadmap, was drawn as a Gantt chart. Roadmap items run down the vertical axis, and months of 2020–2021 run along the horizontal axis.

In spring 2020, COVID-19 made the original dates unrealistic. The plan got a column marking the "crisis impact period" (April to June 2020). Most of the later work was tied to the end of that period: "four months after it ends", "nine months after it ends". Offset marks of +1…+18 months appeared on the timeline, and the bars that depend on them were outlined with dashed lines: "the date will move if the crisis is extended". Had the crisis been extended, the dependent dates would have shifted by the same amount without rebuilding the plan's logic.

The "Variable Recurring Payments" row after the revision consists of bars that follow one another:

| Work | Months | Shift from end of crisis |
|---|---|---|
| Draft standard | April – October 2020 | fixed date |
| Industry consultation | November – December 2020 | +5…+6 |
| Second draft | January 2021 | +7 |
| Consultation | February 2021 | +8 |
| Standard | March 2021 | +9 |

Decision: on 15 May 2020 the CMA approved the revised plan. In 2024 the regulator confirmed that all nine banks had completed the roadmap.

Case sources: [CMA approved roadmap, May 2020 (PDF)](https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/885537/Notice_of_proposed_changes_to_the_open_banking_roadmap_-_web_publication_-_cma_gov_uk_---_May_2020_-.pdf), [Open Banking news on publication of the plan](https://www.openbanking.org.uk/news/cma-publishes-approved-roadmap-for-the-final-stages-of-open-banking-implementation/), [confirmation of completion in 2024](https://www.openbanking.org.uk/news/cma-confirms-full-completion-of-open-banking-roadmap-unlocking-a-new-era-of-financial-innovation/).

## Common mistakes

- **False precision.** Exact dates for tasks whose scope is still unclear. For such tasks, aggregate the rows and build in an explicit buffer.
- **No dependencies.** The chart shows parallelism that does not exist, and the deadline looks closer than it is.
- **Ignoring the load.** One person on three simultaneous bars is a plan that will fall apart.
- **Buffer hidden in every task.** Each owner adds their own cushion and spends it. A shared buffer at the end of the critical path is visible and manageable.
- **Drawn once and forgotten.** A chart that is not updated weekly stops reflecting reality within a couple of weeks.
- **Too much detail.** Hundreds of linked rows are unreadable. Aggregate to the level at which decisions are made.

## Source

The chart is named after Henry Gantt (1861–1919), an American engineer who developed it around 1910–1915 for planning and controlling production work. A similar "harmonogram" was created by the Polish engineer Karol Adamiecki as early as 1896. The method became known through Wallace Clark's book "The Gantt Chart: A Working Tool of Management" (1922). For an overview of the history and limitations, see the [Gantt chart article on Wikipedia](https://en.wikipedia.org/wiki/Gantt_chart).

## See also

- Enhanced by Kanban Board: Use the kanban board for daily flow; the Gantt chart checks only the deadline.
- Preceded by Project Canvas: Describe goals, work and milestones on a project canvas, then make Gantt rows.
- Alternative to Sprint: With unclear scope, plan short sprints, not exact Gantt dates that give false precision.
- Preceded by SMART Goals: Plan the action steps of a dated SMART goal on the Gantt timeline.
