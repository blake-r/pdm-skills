# Opportunity Solution Tree

## Essence

An opportunity solution tree is a visual map of the paths a team could take to reach a desired outcome. At the top is one outcome, the business need the team must move. Below it are opportunities (customer needs, pain points and desires), then solutions for one chosen opportunity, and at the bottom the assumption tests that show which solutions are worth building. It keeps a product trio (product manager, designer, engineer) working from customer evidence instead of from a list of features.

## When to use and when not to

Use it in continuous discovery, when the team has an outcome and talks to customers every week, and must decide which need to address first and which of several ideas to test.

Inputs: a theory of the target customer and the value proposition, a clearly defined outcome, and at least three or four story-based customer interviews (the customer tells a real recent episode, not opinions).

Do not use it:

- Without interviews. Invented opportunities give a tree that looks like evidence and is not.
- As a company-wide tree. Use a KPI tree or an experience map instead; one team, one outcome, one tree.
- As a plan with dates. It shows options and learning, not a schedule.

Non-obvious limits:

- **Opportunities from sales calls, support tickets or analytics are inspiration for interviews, not inputs.** Source them from interviews.
- **A one-way opportunity is probably a solution in disguise.** If there is only one way to address it, rewrite it.
- **Effort stays out of the opportunity assessment.** Judging "too hard" early discards opportunities before solutions were explored.
- **A new tree is needed only when the direction of the outcome changes**, not when its target number changes.

## Scheme

```
            Outcome  (one, a product outcome)
          /     |      \
  Opportunity  TARGET   Opportunity     opportunity space
  (sub-opportunities below any of them)
          /     |      \
   Solution  Solution  Solution         for the target only
      |         |         |
  Assumption tests: the riskiest assumptions of each solution
```

Opportunities are written in the customer's words and grouped by moments of the customer experience, parents above children. Assumptions are tested across all three solutions at once.

## How to apply

1. **Check the inputs:** target customer, value proposition, outcome, and interviews already done.
2. **Put one outcome at the top.** Prefer a product outcome (customer behaviour in the product) over a business outcome or a single feature's metric. If several are requested, take the most important; teams sharing an outcome split it by customer segment or journey step.
3. **Map the opportunity space** from interview notes: write each need, pain or desire as a customer statement, then group similar ones under a parent. Start with a crummy first draft; refine the lower branches rather than rearranging the top.
4. **Choose one target opportunity.** Compare and contrast the opportunities, leaving effort out of the comparison. Work on one small opportunity at a time.
5. **Brainstorm solutions for that opportunity only,** then pick three to explore (compare and contrast; one idea gets no real comparison).
6. **Break each solution into assumptions** and rank them by risk.
7. **Test the riskiest assumptions** of all three ideas with quick experiments rather than opinion.
8. **Read the result and decide:** drop an idea, refine one for delivery, or choose a new target opportunity. Update the tree after every three or four interviews.

## Example

Grailed, a peer-to-peer fashion marketplace. Its Discovery team had spent eight months building a feed where users follow designers and sellers and curate it themselves; the response was underwhelming and the feed roughly broke even. About 10% of users arrive looking for a specific item; the team focused on the other 90%, who browse with no item in mind.

The team first captured its own assumptions in a tree, whose first version had a single node, "increase relevance". Interviews showed these statements were business statements, not user opportunities. They were replaced by customer wording: "Show me things I interact with", "Show me stuff that's popular", "There should always be new stuff when I come". The team turned low-lift opportunities into quick tests, for example adding popular items to the feed. Over about six months the feed grew from a reverse-chronological list to one with recommendations, interleaved content and tracking of seen items.

Result: discoveries and gross merchandise value (GMV) from the feed grew four to five times. Feed users, against the average user, opened the app about 30% more, made about 40% more discoveries and had about 20% higher lifetime value (LTV), mainly through retention. The team's decision was to adopt continuous discovery as a way of working. Limit of the source: the article gives no raw LTV figures, sample sizes or significance tests, and its chart shows feed users' LTV slightly below baseline at 30 days; the 20% is the product manager's estimate, not a measured experiment.

What the case lacks (K5=1): the text of the tree diagrams (versions 1 and 8) is only an image, so the outcome, the hierarchy, the target opportunity and each assumption test are not visible. The template above is filled from the prose only; the pairing of solutions with one target opportunity is our reading, and unknown cells are N/A.

Case source: Melissa Suzuno, [Product in Practice: Opportunity Mapping Led to a 20% Lift in LTV at Grailed](https://www.producttalk.org/opportunity-mapping-grailed/), Product Talk, 19 October 2022.

## Common mistakes

- **Solutions written as opportunities.** "Add a filter" is a solution; "I wish it would take less effort to find hotels that meet my preferences" (a trivago opportunity) is an opportunity.
- **Opportunities from the team's heads.** Grailed's first tree held business statements until interviews corrected it.
- **Reacting to one interview.** Wait for a pattern across several before reshaping a branch.
- **Brainstorming for the whole tree.** Solutions are for the target opportunity only.
- **Testing the idea, not its assumptions.** Build tests for the riskiest assumptions; a built feature is a slow test.
- **One tree for the company,** or a top level that keeps changing while the lower branches stay empty.

## Source

Teresa Torres, Product Talk: ["Opportunity Solution Trees"](https://www.producttalk.org/opportunity-solution-tree/) (article, undated; the method and its steps are taken from it) and her book Continuous Discovery Habits (Product Talk, 2021), the book on continuous discovery habits that Grailed's team also read. Torres is the author of the method. The tool has no page in the Product Architecture Framework (PAF, productframework.ru), so the card is built from the primary source of the method alone. The case article is on the same site; the book itself was not opened for this card, so its steps were checked only through Product Talk pages.

## See also

- Preceded by In-Depth Interview: Interview customers about real episodes; their stories become the opportunities in the tree.
- Preceded by Metric Pyramid: Take the tree's outcome from a branch the team can influence.
- Enhanced by Jobs-to-be-Done: Frame opportunities as the customer's progress and struggles in a situation.
- Enhanced by Customer Journey Map: Use journey stages to group opportunities by moments of the experience.
- Followed by Experiment Card: Write each assumption test of the chosen solutions as a card.
- Alternative to Impact Mapping: Impact mapping starts from actors and impacts; the tree starts from customer needs.
