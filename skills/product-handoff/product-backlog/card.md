# Product Backlog

## Essence

A product backlog is a single ordered list of what needs to be done to improve the product. The 2020 Scrum Guide (the guide to Scrum, an approach in which the team works in short cycles called sprints) calls it an "emergent, ordered list" and the only source of the team's work. Above the list stands the product goal — a future state that the items lead to.

Items can be: features, bugs, technical work, learning, requirements.

Roman Pichler and Mike Cohn described a good backlog with the word DEEP:

1. **Detailed appropriately:** the top of the list is detailed, the bottom is coarse.
2. **Estimated:** items have a size estimate from those who will do the work.
3. **Emergent:** the list changes as new knowledge arrives.
4. **Prioritized:** the most valuable items are at the top and are done first.

## When to use and when not to

Use it when the product has a permanent team, there is more work than the team can get through, and requests come from users, support, the business and the team itself.

Do not use it as a warehouse for all ideas. Marty Cagan separates the opportunity backlog (a list of things to explore) from the product backlog — work that has already been decided to be done.

Limits:

- **Ordering is one person's responsibility.** According to the Scrum Guide this is the product owner; whoever wants to change the list has to persuade them.
- **A flat list hides the picture.** Jeff Patton: in a long enumeration you cannot see how items add up into the user's work.
- **Length hurts.** Pichler has come across a list of 40,000 items: such a list is hard to understand, let alone order.

## Scheme

```
Product goal: ____________________
┌────┬────────────┬────────┬────────┬────────┬────────┐
│ №  │ Item       │ Why    │ Link   │ Size   │ Ready  │
│    │            │ here   │ to goal│        │        │
├────┼────────────┼────────┼────────┼────────┼────────┤
│ 1  │ small,     │        │        │ precise│ yes    │ ← next sprint
│ 2  │ clear      │        │        │        │ yes    │
├────┼────────────┼────────┼────────┼────────┼────────┤
│ …  │ large,     │        │        │ coarse │ no     │ ← refine
│ N  │ coarse     │        │        │        │ no     │ ← delete
└────┴────────────┴────────┴────────┴────────┴────────┘
State of the list: number of items · without a link · ready
```

## How to apply

1. **Write the product goal** for the next two to six months. An item that does not lead to it is a candidate for deletion.
2. **Gather everything into one list:** features, bugs, technical work. One product — one backlog.
3. **Order it** by value, risk, deadlines and dependencies: one item per place. Write down why it sits there.
4. **Ask the team to size** the top items. A rough estimate is enough for the bottom ones.
5. **Refine the top of the list** before each planning session: split large items, remove blockers. An item is ready when the team can complete it in one sprint.
6. **Clean the tail regularly.** Delete old items that have not moved.
7. **Look at the state of the list.** Fewer ready items than one sprint — refine the top. Many items with no link to the goal — delete them or revisit the goal.

## Example

The YooKassa team is responsible for the stability of the core functions of YooMoney's payment system: the API, payment processing and reconciliation. There, "backlog" means the maintenance of existing products: bugs, incidents, technical quality.

When the team started going through the list, it had more than 300 tasks. It was split into three streams:

| Stream | What is inside | Who orders it |
|---|---|---|
| Development | ideas that should grow into projects | product manager |
| Tech backlog | code rework, technical quality | the whole team |
| Maintenance | bugs, incidents, requests from neighbouring departments | the whole team |

Items and decisions from the article:

- a bug in the payment flow: easy to fix, errors for 5% of payments go away — first priority;
- reduce the logging volume: important, but disk space is enough for half a year — schedule it;
- add an index: queries fail on timeout;
- add a shop to the blacklist, connect a new payment method: important, but not urgent.

After the initial sorting of tasks over three quarters, the backlog shrank by 50%. Then the team started ranking the remaining 100–150 tasks: a day before the meeting it estimates five to ten tasks in Jira (a task-tracking system), and at the meeting it records the reasoning. The list is filtered by direction, and the tail is closed.

What the case lacks: the list itself with its order, the product goal, item sizes and readiness. It does not show how much of the 50% was done and how much was closed without work.

Case source: L. Churkina, [“Backlog the scientific way: how prioritization helped YooMoney get rid of task chaos”](https://habr.com/ru/companies/yoomoney/articles/733564/), YooMoney blog on Habr, 05.05.2023.

## Common mistakes

- **Dumping ground.** Cohn: the backlog turns into a "dumping ground" — everything is put in and nothing is removed.
- **Wish list.** Items are not linked to the product goal, so there is nothing to argue about in their order.
- **Everything is high priority.** A "important" label on half the items means there is no order.
- **Detailed everywhere.** Detailed descriptions at the bottom of the list go stale before their turn comes.
- **Several lists for one product.** Bugs and technical work are tracked separately, and there is no shared order.
- **The team does not size the items.** According to the Scrum Guide, estimates are given by those who will do the work.

## Source

K. Schwaber, J. Sutherland, [“The Scrum Guide”](https://scrumguides.org/scrum-guide.html), 2020; R. Pichler, [“Make the Product Backlog DEEP”](https://www.romanpichler.com/blog/make-the-product-backlog-deep/), 2010, [“Seven Product Backlog Mistakes to Avoid”](https://www.romanpichler.com/blog/product-backlog-mistakes/), 2021, and [“How to Reduce the Size of Your Product Backlog”](https://www.romanpichler.com/blog/how-to-reduce-the-product-backlog-size/), 2019; M. Cohn, [“Product Backlog”](https://www.mountaingoatsoftware.com/agile/scrum/artifacts/product-backlog) and [“Make the Product Backlog DEEP”](https://www.mountaingoatsoftware.com/agile/make-the-product-backlog-deep); M. Cagan, [“The Opportunity Backlog”](https://www.svpg.com/the-opportunity-backlog/), 2012; J. Patton, [note on flat backlogs](https://jpattonassociates.com/the-new-backlog/), 2008.

## See also

- Enhanced by Story Mapping: Use a story map when a flat list hides how items serve user work.
- Enhanced by User Story: Write backlog features as user stories, so each item names who needs it and why.
- Followed by Sprint: The top backlog items that fit one sprint are taken into the sprint.
- Followed by Kanban Board: Pull the top ordered items into the first column.
- Enhanced by Definition of Done: Mark an item done only when it meets the DoD.
- Preceded by Feedback Matrix: Turn advice into ordered improvements; review suggestions by frequency.
- Preceded by Frequency / Adoption Analysis: Turn remove and rework decisions into ordered items.
- Preceded by Product Requirements Document: Turn the PRD's functions into ordered backlog items.
