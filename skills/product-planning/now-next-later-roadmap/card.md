# Now-Next-Later Roadmap

## Essence

A Now-Next-Later roadmap is a plan of product direction in three columns instead of a calendar. Now holds the work the team is actively building and is confident about. Next holds the work expected once Now is done, described less finely. Later holds bigger, vaguer problems kept on the radar without detailed solutions. It shows order and certainty, not delivery dates, so stakeholders (the people who depend on or fund the product) see where the product is going without a date that will slip.

## When to use and when not to

Use when plans change faster than dates can be kept, the product is built around problems and goals, and stakeholders need direction rather than a release schedule.

Required inputs: a list of customer and business problems, the business objectives (for example, Objectives and Key Results, OKRs), and the team's honest view of how certain each item is.

Limitations:

- **The columns are not equal in size or fixed.** Items move or are dropped as the team learns; a column with one item is normal.
- **Undefined horizons turn the roadmap into a vaguer timeline.** If "Next" silently means "next quarter", the dates are back. Agree what each column means for this team and tell stakeholders.
- **It does not hold commitments.** Bastow puts accountability in OKRs, not in the roadmap. If a contract, a regulatory deadline or a launch partner needs a date, note that date on the item; do not hide it.
- **It does not replace a backlog or a delivery schedule.** It gives no capacity, sequence of tasks or dependencies between teams.

## Scheme

```
Business objectives:  A ■   B ■   C ■   (colour labels)
┌──────────────┬──────────────┬──────────────┐
│     NOW      │     NEXT     │    LATER     │
│ building,    │ after Now,   │ big problems │
│ specified    │ less detail  │ in the       │
│ problem →    │ problem →    │ distance     │
│ idea, ■      │ idea, ■      │ problem, ■   │
└──────────────┴──────────────┴──────────────┘
Certainty falls from left to right
```

## How to apply

1. **Collect problems, not ideas.** Write down the problems to solve; attach candidate ideas, features and experiments to each problem.
2. **Define the horizons.** Write one sentence per column for your team, for example "Now: in development or in active discovery with a named owner". Agree it with stakeholders.
3. **Define initiatives.** An initiative is a prototype, an experiment, a test or a final solution for a problem.
4. **Sort by urgency and certainty.** Confident, specified work goes to Now, broken into granular pieces. Work that follows from Now, or depends on what Now teaches, goes to Next, in coarser pieces. Large, vague problems go to Later without solutions.
5. **Tie each initiative to a business objective.** Show it with a colour label per objective, so the reason is visible at a glance. An item with no objective is a signal to question it.
6. **Mark a real deadline** on the item if one exists (a law, a contract), and say who set it.
7. **Review regularly.** Move items left as certainty grows, remove those that lost their reason, and tell stakeholders what changed and why.

Interpretation: read the roadmap by the left column first; if Now is overloaded or has no objective labels, the roadmap is a list of features. The decision that follows is what enters Now, what leaves, and what stakeholders are told about the horizon.

## Example

WooCommerce, an open-source e-commerce platform for WordPress, published its public roadmap on 30 May 2023 and described the stages in the announcement: Ideation (projects being planned, no work begun), Now (projects currently being worked on), Next (projects committed to but not started) and Later (projects being scoped, likely to happen). The roadmap was called a living document; office hours and community events were set to discuss its items.

Decision: publish the roadmap openly, with stages instead of dates, and keep it updated, so that developers see current work and direction.

What the case lacks (K5=1): the announcement lists no items, so a filled board is not visible here. I could not open a rendered board with items: the roadmap page at developer.woocommerce.com/roadmap showed only a list of blog posts, and ProdPad's own public roadmap page showed no items when opened. There is no objective labelling or reasons for moves either. WooCommerce also adds a fourth stage, Ideation, which is not part of the original format.

Case source: [Introducing the WooCommerce Public Roadmap](https://developer.woocommerce.com/2023/05/30/introducing-the-woocommerce-public-roadmap/), WooCommerce Developer Blog, 30.05.2023.

## Common mistakes

- **Dates under the columns.** "Now = Q1, Next = Q2" is a timeline in disguise; slips and disappointed stakeholders return.
- **Undefined horizons.** Without a shared meaning of each column, the roadmap becomes a vaguer timeline.
- **Ideas instead of problems.** A list of features gives nice-to-have items, not solutions chosen for a problem.
- **A feature factory.** Filling Now with output and no objective labels loses the link to strategy; more features do not equal more success.
- **No stakeholder talk.** The shift from dates to horizons must be explained, or people read Next as a promise.
- **Dropping accountability.** Taking dates away without OKRs leaves nothing the team answers for.
- **Equal columns.** Detailing Later like Now wastes planning on work that may never ship.

## Source

Janna Bastow, co-founder of ProdPad and creator of the format: [The Now-Next-Later Roadmap](https://www.prodpad.com/blog/invented-now-next-later-roadmap/), ProdPad blog, 18.10.2022. In a reader comment on that page she says she and Simon sketched the first version in 2012 under the names Current / Near Term / Future, and an early customer suggested the names Now-Next-Later. There is no description in PAF (Product Architecture Framework, productframework.ru) for this tool; the card is built from the primary source above. Case facts: WooCommerce Developer Blog, 30.05.2023 (link in Example). A second independent description of the method was not opened.

## See also

- Preceded by Opportunity Solution Tree: the tree yields the problems and solutions that are sorted into columns.
- Enhanced by Objectives and Key Results (OKR): OKRs carry the commitments, so the roadmap can drop dates.
- Alternative to Gantt Chart: a Gantt chart fixes dates and dependencies; this shows order and certainty only.
- Followed by Product Backlog: Now items are broken into backlog items for the team.
- Improved by RICE Scoring: score candidate initiatives to decide which enter Now.
