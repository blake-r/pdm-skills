# Definition of Done

## Essence

Definition of Done (DoD) — a list of conditions that work must meet to count as finished. In the Scrum Guide 2020 (Scrum — an approach to development in short iterations), the DoD is a commitment for the increment, that is, the ready part of the product. Work that does not meet the DoD is not part of the increment and must not be released: it goes back to the common list of work.

## When to use and when not to

Use it when "done" is understood differently by different people; not as reporting. According to Garda, a developer may consider a task finished after review (a colleague's check of the code), unit tests (automated checks of functions) and merging the code, while a tester waits for documentation as well.

Limits:

- **Not acceptance criteria.** Acceptance criteria are separate for each task; the DoD is one for all. Mike Cohn: both sets are needed.
- **Not Definition of Ready.** Definition of Ready (DoR) — conditions under which a task is taken into work. The Scrum Guide 2020 has no DoR.
- **Own or shared.** The organisation's standard is the minimum; otherwise the team writes its own. Teams of one product — one DoD.
- **Benefit measured weakly.** Survey by Kopczyńska et al. (137 practitioners, self-assessment): 93% consider the DoD useful, but implementation difficulties and inaccurate items occur in 70% of projects or more. Schwaber and Starr: at least half of unfinished work remains in the released product; the method is not described.

## Scheme

```
 Work on a task
                │
┌───────────────▼────────────────────┐
│ DoD — one list for all tasks       │
│ ☑ code   ☑ review   ☑ tests        │
└──────┬─────────────────────┬───────┘
 all ☑ │                     │ any ☐
       ▼                     ▼
 increment: can be     back to the common
 released              list of work
```

## How to apply

Inputs: the team's roles; the tracker and CI/CD; the organisation's standard.

1. **Write the list together with the whole team.**
2. **Write checkable items:** an item is yes or no, with a note on how it is checked.
3. **Start small.** Garda: three criteria that are kept are better than fifteen that are ignored.
4. **Build checks into the process.** CI/CD (automatic build, testing and rollout of code) can block a rollout when an item is not met.
5. **If at least one item is not met — it is not "done".**
6. **Review regularly.** Atlassian: once a quarter; Garda: or by triggers the team defines.

## Example

No case from e-commerce or fintech with a DoD list, a decision and figures before and after was found: below are the best real ones.

**The list.** Garda, a cybersecurity vendor. In Jira (a task tracking system) tasks had the status "done", but what had actually been done was found out by asking colleagues; they decided to introduce DoR and DoD. Garda gives an example checklist of seven items in the article; the article does not say that this is their adopted list: code written and compiles; review passed; unit tests passed; planned tests executed; no critical comments; demo (showing the result to the customer) held; documentation updated.

Garda suggests automation: CI/CD may not let code into the stable branch (the main version of the code) if the merge request (a request to merge) has no task link, unit tests or review.

**Second list example.** The author from Gazprombank.Tech calls the team checklist "roughly like this": analysis and mockups agreed, grooming and slicing of tasks, code implemented and tested, highest-priority comments closed.

**Mechanism.** Schwaber and Starr: a gas pipeline company, a royalty payment system. Anna's department wanted to start using three parts of the system that had already been shown: the team's "done" meant "shown". The plan required 8 units of work (a conventional measure of volume) per iteration; unfinished work added 14. Anna counted 3/10 of all the work as done; the deadline was revised to 20 months, with launch in 22. Decision: strengthen skills and autotests so that the team's "done" became Anna's "done".

What the case lacks: Garda and Gazprombank.Tech have no decision on the DoD and no figures. Anna has no DoD list and no original deadline.

## Common mistakes

- **Ticks instead of checks.** Garda: it happens that a reviewer skims the code and writes "OK".
- **Too many, unachievable or vague.** An item that cannot be met for every task slows work; fifteen items get ignored; "code tested" is read differently by each person.
- **The list is imposed from above or agreed with part of the team.** Garda: such rules do not work.
- **The list is out of date.** Garda's example: they decided to drop manual linking of a merge request to a task, but it stayed in the list.
- **An item without training.** Garda recalls a case: "T-shirt sizing" (sizing tasks as S, M, L) was not explained, and the team sabotaged it.
- **The DoD is not proof of correctness.** Atlassian: a passed list does not mean the task is implemented correctly.
- **Unfinished work passed off as done.** Schwaber and Starr: technical debt (postponed unfinished work) hides the real progress.

## Source

K. Schwaber, J. Sutherland, [The Scrum Guide](https://scrumguides.org/scrum-guide.html), 2020; K. Schwaber, D. Starr, "Done and Undone", Scrum.org, 2012, [copy](https://learn.microsoft.com/en-us/previous-versions/visualstudio/visual-studio-2012/hh765983%28v=vs.110%29); article on the Mountain Goat Software website (Mike Cohn), [link](https://www.mountaingoatsoftware.com/blog/clarifying-the-relationship-between-definition-of-done-and-conditions-of-sa); Atlassian, [article](https://www.atlassian.com/agile/project-management/definition-of-done); K. Kopczyńska et al., [survey](https://arxiv.org/abs/2208.04003), 2022; A. Shilnikova, [Garda](https://habr.com/ru/companies/garda/articles/1006382/), Habr, 6 March 2026; D. Korchuganova, development team lead at Gazprombank.Tech (IT_ONE), [article](https://habr.com/ru/articles/899474) on the Gazprombank blog on Habr, 18.04.2025.

## See also

- Enhanced by Product Backlog: Mark an item done only when it meets the DoD, which is one shared list.
- Preceded by Test Case: Run the test cases first; the item is done when they pass.
- Enhanced by Sprint: The DoD sets the sprint increment bar; work that misses it returns to the backlog.
- Enhanced by Team Canvas: Record the agreed finish conditions here so they match the team canvas rules.
- Enhanced by User Story: Pair this list with acceptance criteria per story: those cover behaviour, this covers shared conditions.
