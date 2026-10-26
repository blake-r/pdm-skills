# Feature Canvas

## Essence

The Feature Canvas is a sheet of 15 blocks on which a team describes a new feature before design and development. The analysis area (9 blocks): which problem we solve, for whom, in which situations, how customers cope now, what gets in the way and what helps. The planning area (6 blocks): what customers will do with the feature, why the business needs it, how to measure success, and what minimum work to do. Problem and context come first, then the solution; an empty block shows what the team does not yet know.

## When to use and when not to

Use it when there is an idea for a new feature and you need to decide whether to build it and in what minimal form; at the start of work, so that the team and the client share the same understanding of the problem.

Do not use it for small changes and bug fixes. The canvas does not replace research: it shows which data is missing, but does not collect it.

Limitations:

- **Blocks are easy to fill with assumptions.** An answer without data is marked as a hypothesis.
- **The full version is heavy.** For a quick assessment the author offers a basic version: seven analysis blocks.

## Scheme

| Area | Block | Main question |
|---|---|---|
| Analysis | **Idea description** | the idea in 2–3 sentences |
| | **Why?** | why it matters to customers and the business; the root cause of the idea |
| | **Contextual situations** | when and where the need arises, who else is involved |
| | **Problems to solve** | what we solve, how we know about it, how often it is reported |
| | **Affected customers** | who is affected, how often, how critical it is |
| | **Current behavior and habits** | how they cope now and what does not suit them |
| | **Value proposition** | what customers will get, why they will choose the new solution |
| | **Restrictions and Limitations** | what gets in the way: technology, habits, time, money |
| | **Capabilities** | what already exists and will help |
| Planning | **Customers tasks** | what customers will do with the feature |
| | **Awareness** | how they will learn about the feature, where they will look for it |
| | **Support needed** | where help will be needed, what mistakes are possible |
| | **Business goals** | why release the feature |
| | **Success criteria** | how we will know the feature is useful, what data is needed |
| | **Key activities** | the minimum for the first version and development later |

## How to apply

1. **Write down the idea** in 2–3 sentences and why it matters to customers and the business.
2. **Fill in the analysis area,** naming the source for each problem.
3. **Mark blocks without data:** they are checked before development.
4. **If the idea passed the analysis, fill in the planning area;** add the data needed to check the success criteria.
5. **Single out the key activities:** the minimum for the first version and what to add later.
6. **Decide:** build, change or drop.

## Example

Monzo, a British digital bank, in 2018 gave customers a block on payments to bookmakers and casinos. The bank did not use the canvas; its published decisions are laid out by block.

| Block | Monzo |
|---|---|
| **Idea description** | the customer blocks gambling payments for themselves, online and offline |
| **Why?** | it helped such customers only after debts appeared; it wanted to prevent them |
| **Problems to solve** | 80% of those who sought help for gambling addiction were in debt (GambleAware); customers asked for the feature |
| **Affected customers** | 0.8% of British adults are problem gamblers; by the bank's estimate, over 5 thousand of its customers |
| **Contextual situations** | gambling can be an impulse; switching the block off must not be impulsive either |
| **Current behavior and habits** | website-blocking programs (through the GamCare organization), self-exclusion with casinos and bookmakers |
| **Value proposition** | the block is applied directly on the bank account |
| **Capabilities** | every transaction has a merchant category code, which the bank already used to sort spending |
| **Restrictions and Limitations** | the block relies on merchant codes, so a payment tagged incorrectly gets through; it is bypassed by cash withdrawals and transfers |
| **Customers tasks** | turn the block on; later, possibly turn it off |
| **Awareness** | a toggle in the app settings or via support |
| **Support needed** | support helps turn the block on and provides links to external help; removing it is possible only via chat and after 48 hours |
| **Business goals** | a customer without debts means fewer losses for the bank |
| **Success criteria** | not named in the publications |
| **Key activities** | a list of gambling merchant codes; testing with the customers who asked for the feature |

Decision: on 16 May 2018 the bank put the idea up for discussion with customers, and on 19 June it launched the feature. A gambling spending limit and approval of bets by a trusted person were not included in the first version.

Result: by July 2020, 222,993 customers had turned the block on, and 8% of them had turned it off. In 2023 the bank reported close to 100 thousand users in 10 months and over 200 thousand blocked payment attempts; it extended the pause before removal to up to one year. According to the bank's [feature page](https://monzo.com/gambling-block), over 700 thousand customers had used the block in total.

Sources of the case: Monzo blog — [idea](https://monzo.com/blog/2018/05/16/gambling-self-exclusion) (16 May 2018), [launch](https://monzo.com/blog/2018/06/19/gambling-block-self-exclusion) (19 June 2018), [improvement](https://monzo.com/blog/weve-improved-our-gambling-block) (13 September 2023); [iGB](https://igamingbusiness.com/tech-innovation/222993-use-monzo-gambling-block-since-june-2018-launch/) (22 July 2020).

## Common mistakes

- **Starting with the solution.** The idea is described in detail, the problems in general words.
- **Problems without a source.** It is not written where the problems are known from and how often they are reported.
- **Empty success criteria.** The feature was released, but it cannot be said whether it succeeded.
- **Key activities — everything at once.** The minimum for the first version is not singled out.

## Source

Nikita Efimov, [Feature Canvas](http://web.archive.org/web/20190730023745/http://featurecanvas.com/), featurecanvas.com, February 2018, licence CC BY-SA 4.0 (archived copy).

## See also

- Followed by Awesome Problem Interview Script: Run problem interviews to fill the blocks the canvas marks as missing.
- Alternative to Lean UX Canvas: Use it to turn a feature into testable hypotheses in a shorter sheet.
- Preceded by Impact Mapping: Link business goals to the behaviour changes the feature should cause first.
- Followed by Experiment Card: Test each unverified block, such as success criteria, on its own experiment card.
