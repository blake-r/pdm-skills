# Metric Pyramid

## Essence

The metric pyramid is a tree that breaks down the main product metric "from top to bottom". At the top is the value metric (North Star); below it are the key metrics (Key), whose product gives the metric one level up. Among them, the ones that influence the top the most are marked as Traction. At the bottom are user behaviour metrics (Pulse). The tree shows through which branch an idea can move the top, and helps discard ideas that do not affect it.

## When to use and when not to

Use it to agree on which metric the team works on; to filter out ideas that do not affect the goal; to find which component moved the main metric.

Do not use it when the product has neither users nor data: the tree becomes a set of assumptions. It does not replace testing ideas.

Inputs: the product goal, metric values for several periods.

Limitations:

- **Not all links are products.** Some metrics influence their neighbours (growth in the audience may lower the average check), and simple multiplication hides this.
- **The main metric is often debatable.** Revenue or turnover reflect value for the customer only indirectly.
- **The tree gets outdated.** It is rebuilt when the strategy changes.

## Scheme

| Level | What it is | Example for a marketplace |
|---|---|---|
| **North Star** | the main value metric of the product | turnover (GMV) per year |
| **Key** | components whose product equals the metric above | active buyers × orders per buyer × average check |
| **Traction** | not a separate level, but a mark on the key metrics that influence the top most | order frequency |
| **Pulse** | user behaviour: passing steps before purchase, share of users of a feature, averages | share of orders paid with the store card |

Levers are recorded separately — what the team changes to move a branch: range, delivery times, payment terms.

## How to apply

1. **Choose the top:** a metric that shows the product's value for the customer and grows with the business.
2. **Break it down into factors** so that their product equals the top; check the formula on real data.
3. **Break the key metrics down further** if needed, to the level the team can influence directly.
4. **Mark Traction:** two or three metrics that moved the top most in past periods.
5. **Add Pulse** under each key metric and record the levers.
6. **Tie the ideas** to a specific branch and discard those that affect nothing.
7. **Analyze every shift of the top.** The growth of the top equals the product of the growth of the factors: (1 + g) = (1 + g₁) × (1 + g₂) × (1 + g₃). A factor's share of the shift is ln(1 + gᵢ) / ln(1 + g). A falling branch is the cost of the others' growth.

## Example

Ozon, a Russian marketplace, in its reports for investors gives turnover (GMV including services), the number of orders, active buyers and order frequency. The company did not publish a metric pyramid; below, its indicators are laid out by the levels of the model.

| Level | Ozon indicators, 2021 vs 2020 |
|---|---|
| **North Star** | GMV including services: RUB 445 bn versus RUB 197 bn, ×2.26 |
| **Key** | buyers: more than 25 million versus 13.8 million, ×1.81; frequency: about 8.5 orders per buyer in Q4 2021, roughly +60% year on year; turnover per order: about RUB 2,020 versus RUB 2,660, −24% (calculated from GMV and orders: 445 bn / 220 m and 197 bn / 74 m) |
| **Traction** | buyers and frequency |
| **Pulse** | Ozon card holders: more than four times as many over the year |

Formula check: 25 million × 8.5 ≈ 212 million orders versus "more than 220 million" in the report — a discrepancy from rounding and from frequency being a Q4 figure. GMV including services also includes revenue from services, such as advertising, so the formula is approximate. Analysis of the shift: buyers gave about 70% of the growth, frequency about 60%, and the fall in turnover per order took away about 35%.

Decision: CEO Alexander Shulgin, naming GMV growth of more than 125% as the main result, also noted "incredible progress" in building the habit of frequent purchases. The report also shows investment in range (more than 80 million products, up from 11 million) and warehouses (close to 1 million m²); the link of these to frequency is our reading, not Ozon's statement.

Result for Q3 2022 versus the previous year: GMV +74%, orders +91%, frequency 11.7 versus 7.5 (+56%), buyers 32.7 million.

Sources of the case: Ozon press releases filed with the SEC — [2021 results](https://www.sec.gov/Archives/edgar/data/0001822829/000119312522025238/d663240dex991.htm) (2 February 2022) and [Q3 2022 results](https://www.sec.gov/Archives/edgar/data/1822829/000119312522285285/d406599dex991.htm) (15 November 2022).

## Common mistakes

- **The top is any convenient figure.** The team chose what is easy to count rather than the value for the customer.
- **A sum instead of a product.** The metrics of a level do not add up to the metric above, and the tree explains nothing.
- **Everything is Traction.** Ten metrics are marked, and the team again does not know what is the main one.
- **Ideas without a branch.** Features are built without specifying which metric they should move.

## Source

The model is described in Sergey Tikhomirov's [Product Architecture Framework](https://productframework.ru/activities/quantitative_analytics) (licence CC BY-SA 4.0) as a metric hierarchy (Metric Hierarchy) with the North Star, Traction and Pulse levels; the author and the date are not given on the page. The page does not describe Key metrics as a product of components, levers or the growth-share formula: these are this card's working elaboration. The concept of the North Star Metric, according to [Tikhomirov's words](https://productframework.ru/value_and_north_star) (February 2022), was first introduced by Sean Ellis.

## See also

- Enhanced by HEART Metrics: Use HEART categories to pick the Pulse metrics under each key metric of the pyramid.
- Enhanced by AARRR Metrics: Use AARRR stages as pyramid branches when the funnel is the main lever.
- Enhanced by Cohort Analysis: Check each key metric by cohort to trace a North Star shift to its branch.
- Followed by Impact Mapping: Make the North Star the impact map goal; map actors and features that move branches.
- Enhanced by YC Guide to Business Models: Start from YC guide top metrics for this business type, then split them into branches.
- Enhanced by Objectives and Key Results (OKR): Use the branches as candidate key results for the objective the main metric serves.
