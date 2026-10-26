# RICE Scoring

## Essence

RICE is a method of prioritizing features and product hypotheses. Each initiative is assessed on four parameters: reach (Reach), impact (Impact), confidence in the estimates (Confidence) and effort (Effort). From them comes one number — the expected return per unit of work — and the list is sorted by it.

## When to use and when not to

Use it when there are many candidates (from five to ten), the team's resources are shared, there is one target metric, and at least rough data about the audience. The main benefit: a dispute of opinions turns into a discussion of assumptions — "why a reach of 20 thousand and not 2?"

Inputs: the list of initiatives, the goal and the metric by which impact is assessed, the reach period, audience data and the team's effort estimates.

Limitations:

- **Mandatory work** (regulator's requirements, contract terms, technical dependencies) does not compete in the ranking — it is planned separately.
- **Initiatives of different teams with different metrics** cannot be compared: "impact 2" on conversion and on retention are different quantities.
- **Strategic bets** with low confidence are systematically pushed down by the formula in favour of quick wins.
- **Without an audience** (a new product, a new market) reach becomes fiction, and the number loses its meaning.

## Scheme

| Initiative | Reach (reach per period) | Impact | Confidence | Effort (person-months) | RICE Score |
|---|---|---|---|---|---|
| Initiative X | 450 | 3 | 100% | 2 | 675 |
| Initiative Y | 2,000 | 1 | 80% | 4 | 400 |
| Initiative Z | 800 | 2 | 50% | 1 | 800 |

**RICE Score = Reach × Impact × Confidence ÷ Effort.** Z wins despite low confidence because it is cheap: first check its estimates cheaply.

## How to apply

1. **Fix the goal and the period.** One metric by which impact is assessed, and one reach period for all rows — usually a quarter.
2. **Estimate the reach.** The number of people or events per period, taken from data: users, orders, transactions. Count only those who reach the place where the change is visible, not the whole audience.
3. **Estimate the impact** per reached person on the scale: 3 — massive, 2 — high, 1 — medium, 0.5 — low, 0.25 — minimal.
4. **Estimate the confidence** in the reach, impact and effort: 100% — high (there is data), 80% — medium, 50% — low. Below 50% is a blind bet.
5. **Estimate the effort** in person-months of the whole team: development, design, testing. Whole numbers, or 0.5 for work under a month.
6. **Calculate the RICE Score** and sort the list in descending order.
7. **Interpret.** The ranking is a draft of a decision. Check the top of the list for dependencies and mandatory work. A difference of 10–20% is within the margin of error of the estimates; decide such initiatives on additional considerations. Cheaply check an initiative with low confidence at the top first.

## Example

VkusVill, a mobile app for ordering groceries: about 200 participants, 12 product teams, more than 30 business customers. The teams implemented RICE with their own scales: reach in points, impact on one chosen metric for the quarter, confidence from 1 (hypothesis) to 10 (research data), effort in hours. A fragment of the real ranking of one team (task names are hidden in the source, RICE recalculated by the formula):

| Task | Reach | Impact | Confidence | Effort, h | RICE |
|---|---|---|---|---|---|
| 1 | 10 | 3 | 8 | 36 | 6.7 |
| 2 | 8 | 3 | 10 | 40 | 6.0 |
| 3 | 6 | 3 | 8 | 40 | 3.6 |
| 4 | 10 | 4 | 10 | 120 | 3.3 |

The team's conclusion: task 4 has the largest impact, but it is three times as expensive, so three lighter tasks overtook it in the ranking.

A limitation emerged later: some teams built valuable features, others small improvements from their own lists, and the tasks of different teams could not be compared by RICE. For cross-team prioritization the company moved to assessment in money.

Source of the case: [Denis Tuchin — Evolution of prioritization: how we moved from stakeholder charisma to ROI (Habr, 2026)](https://habr.com/ru/articles/1001356/).

## Common mistakes

- **Reach "all users".** Reach is inflated by including those who will never see the change, and initiatives on the most visited screens always win.
- **Different reach periods** in the rows of one ranking: a month against a quarter distorts the comparison threefold.
- **Confidence as "how much I want this feature".** Confidence reflects the quality of the data behind the estimates, not the author's enthusiasm.
- **Effort of development only.** Without design, testing and launch, initiatives with a heavy tail look cheap.
- **The ranking as a verdict.** The method shows trade-offs but does not cancel decisions on dependencies and strategy.
- **An own scale without agreement.** If everyone understands "impact 2" in their own way, the scores are incomparable — fix the scales with examples before scoring.

## Source

The method was proposed by Sean McBride, a product manager at Intercom. The team was looking for a way to compare ideas for the roadmap without relying on favourite projects and intuition. The scales and the formula are from the article [RICE: Simple prioritization for product managers](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/) on the Intercom blog: the method was developed from August 2015, and the article was published in [March 2016](https://web.archive.org/web/20160317021349/https://blog.intercom.io/rice-simple-prioritization-for-product-managers/).

## See also

- Alternative to ICE Scoring: Use ICE for a quicker ranking when no audience data exists to estimate reach.
- Preceded by Impact Mapping: Build the impact map to link goals with initiatives, then score them with RICE.
- Followed by Impact / Effort Matrix: Place the scored ideas on the impact-effort matrix.
- Preceded by Kano Model: Keep only features that pass the Kano thresholds, then rank them by RICE.
