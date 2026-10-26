# MoSCoW Prioritization

## Essence

MoSCoW sorts requirements, user stories or tasks into four groups for one timeframe: Must Have, Should Have, Could Have and Won't Have this time (the lower-case "o" letters only make the acronym pronounceable). It answers one question: what do we guarantee, and what do we drop first if time runs out. Time and cost stay fixed; the scope flexes through the Should and Could groups.

## When to use and when not to

Use it when the deadline or the budget is fixed and the scope is negotiable: a release, an increment, a sprint, a tender. Inputs: a list of requirements, a rough effort estimate for each, and a business owner who can explain why something is a Must.

Do not use it to rank items inside a group or to choose between competing ideas by value: MoSCoW has no order within a group and no score. Use a scoring tool for that.

Limitations:

- **The categories mean "for this timeframe".** A requirement can be a Must for the project, a Should for the first increment and a Won't for a given timebox (a fixed-length work period).
- **Should versus Could is subjective.** The handbook says to agree objective boundaries (for example, the number of affected people) before collecting requirements.
- **Lists without effort hide the real balance.** The handbook's guideline is by effort, not by count: a Must list that is half of the items can be most of the work.
- **The 60% limit is a guideline.** Above it the risk grows, unless estimates are accurate, the approach is well known, the team is mature and the environment is low-risk.

## Scheme

```
Timeframe: project | increment | timebox
Must Have      ≤ ~60% of effort   guaranteed (minimum usable subset)
Should Have                       important, a workaround exists
Could Have     ~20% of effort     contingency, dropped first
------------------------------------------------ line of scope
Won't Have this time              recorded, excluded from effort
```

## How to apply

1. **Fix the timeframe** (project, increment or timebox) and the deadline. Each requirement gets a priority for that timeframe only.
2. **Agree the boundary between Should and Could** before listing requirements, for example by number of affected users or business value.
3. **Start from Won't Have.** Move an item up only with a reason that links it to a project objective.
4. **Test each Must:** "What happens if it is not delivered?" If the answer is "cancel", it is a Must; if a workaround exists, even a manual one, it is not. Also: "Would we stop the deployment the night before without it?" A Must may depend only on other Musts.
5. **Break down large items.** If everything looks like a Must, the items are too coarse; split them and prioritise the parts. Acceptance criteria may differ: restore within 4 hours is a Should, within 24 hours a Must.
6. **Estimate effort** and check the balance: Musts at most about 60%, Coulds about 20%. Won't Haves are excluded.
7. **Record the Won't Haves** in the list so they do not return informally.
8. **Review** at least at the end of each timebox and increment. Unfinished items are re-prioritised.

Reading the result: the business can expect all Musts and Shoulds, and Coulds in the best case. When the deadline is at risk, drop Coulds first, then Shoulds; never negotiate the date.

## Example

Case: MoreThan TALK, a student project at the University of Southampton (2018): a website for finding people to practise speaking languages with. The team published its functional specification as a 48-row MoSCoW table, grouped by function (sign-up, profile, search, monetisation, administration).

Counts from the table: 25 Must, 12 Should, 5 Could, 3 Won't; 3 rows are not rated. Examples: Must: login with username and password, search for users by language, country and interest, third-party ad blocks. Should: login via Google or Facebook, automatic translation of profiles. Could: email alert on a new message. Won't: lock the account after three failed logins; user-created page layout.

What the case lacks: no effort estimates, so the 60% check cannot be run (by count, Musts are 52%); no timeframe; no decision on what is built first or dropped; two heading rows and one rating are empty; it is a coursework project, not a product. Only the form of the tool is visible, so this is a weak case. A real public case with a decision was not found.

Case source: [«Specifying the Functional Specification»](https://generic.wordpress.soton.ac.uk/group1/?p=374), MoreThan TALK project blog, University of Southampton, May 2018.

## Common mistakes

- **Everything is a Must.** No contingency is left; the date will slip. Break items down.
- **Priorities by count, not by effort.** Check the shares of work, not the number of lines.
- **Inflated Musts by pressure.** Ask the cancel test and the workaround test for each one.
- **No Won't Have list.** Dropped items come back through the back door.
- **One priority for all timeframes.** A project Must can be a Should in the first increment.
- **Must depends on a Should.** If the Should is cut, the Must fails.
- **Set once and forgotten.** Priorities need review after every timebox.
- **Ranking inside a group.** MoSCoW does not order items within a group.

## Source

Dai Clegg (Oracle UK), with Richard Barker, [«Case Method Fast-Track: A RAD Approach»](https://folio.caval.edu.au/Record/c000181229), Addison-Wesley, 1994: the origin of MoSCoW, per the record and secondary sources (the book itself was not opened, and the Agile Business Consortium pages do not name Clegg). The rules, the 60% and 20% guideline and the tips are from Agile Business Consortium, [«What is MoSCoW Prioritization?»](https://www.agilebusiness.org/resource/what-is-moscow-prioritization/), 2026, and chapter 10 of the [DSDM Agile Project Framework Handbook](https://www.agilebusiness.org/wp-content/uploads/2026/05/DSDM-Agile-Project-Framework-Handbook.pdf) (© 2014). DSDM is the Dynamic Systems Development Method. There is no description in PAF (Product Architecture Framework, productframework.ru).

## See also

- Followed by Product Backlog: record the priorities and Won't Haves in the backlog and review them each timebox.
- Alternative to Impact / Effort Matrix: use the matrix to compare ideas by value; MoSCoW to fix scope against a date.
- Alternative to RICE Scoring: score reach, impact, confidence and effort to rank; MoSCoW only classifies for a deadline.
- Enhanced by Kano Model: classify features by user satisfaction first, then choose Musts with the Kano result.
- Enhanced by Story Mapping: slice the map by release and give each slice its own MoSCoW priorities.
- Followed by Sprint: take the Musts and Shoulds of the timebox into the sprint plan.
