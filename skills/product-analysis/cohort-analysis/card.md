# Cohort Analysis

## Essence

Cohort analysis groups customers by the period in which they did a first action: installed the app, opened an account, placed a first order. That group is the cohort. For each cohort, one metric is traced over the following periods: the share of customers remaining (retention), revenue, number of orders. Comparing cohorts shows whether the product is getting better for new customers.

## When to use and when not to

Use it when a total metric mixes old and new customers: revenue grows, but each new cohort leaves faster than the previous one. The method is especially useful for subscriptions, marketplaces, cards and loans. It is also used to check whether a change worked: cohorts from before and after the launch are compared over the same periods of life.

Inputs: the date of each customer's first action and the events or amounts per period after it. You need at least 4–6 cohorts and as many periods.

Limits:

- **Correlation, not cause.** A difference between cohorts may be caused by season, acquisition channel or price, not by a change in the product.
- **Small cohorts are noisy.** A cohort of a few dozen customers produces jumps in percentages that mean nothing.
- **Recent periods are incomplete.** The right edge of the table sees few cohorts; conclusions drawn from it are unreliable.

## Scheme

A triangular table: rows are cohorts, columns are periods from the start of the cohort. Values are normalized: share of the cohort size (retention) or index to the entry period (spend, orders). Cell colour highlights strong and weak spots.

| Cohort | Size | Period 0 | Period 1 | Period 2 | Period 3 |
|---|---|---|---|---|---|
| January | 1,000 | 100% | 42% | 35% | 31% |
| February | 1,200 | 100% | 45% | 37% | |
| March | 900 | 100% | 51% | | |

The table is read in three directions: along a row — how a single cohort lives; down a column — whether newer cohorts are better at the same age; along a diagonal — what happened in one calendar period to all cohorts at once.

## How to apply

1. **Formulate the question.** For example: do customers retain better after the new onboarding than before it.
2. **Choose the cohort attribute and the period step** matching the usage cycle: for food delivery — a week, for a loan — a month.
3. **Choose one metric** and a definition of activity. For example, "the customer made at least one purchase in the period".
4. **Build the table** and normalize the values: share of the cohort size for retention, index to period 0 for spend.
5. **Read the columns.** If the values in one column grow from top to bottom, newer cohorts are better than older ones.
6. **Read the diagonals.** A simultaneous drop across all cohorts points to an external event or a failure, not to the quality of acquisition.
7. **Draw the conclusion and the decision,** checking alternative explanations: channels, season, cohort size.

## Example

The American fintech lender Oportun, in its quarterly report (10-Q, Q3 2023), publishes a cohort analysis of losses. A cohort is the loans issued over a year (a generation, vintage); the metric is cumulative net charge-offs as a percentage of the amount issued, by month of the loan's life. The report contains a chart of the curves for all generations since 2007 and a table of losses as of September 30, 2023:

| Generation | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 |
|---|---|---|---|---|---|---|
| Losses as share of amount issued | 8.2% | 9.8% | 10.7% | 8.6%* | 14.3%* | 6.3%* |
| Average loan term, months | 26.3 | 29.0 | 30.0 | 32.0 | 33.3 | 37.8 |

\* The generation has not yet matured: losses will continue to grow.

On the chart, the 2021 curve after its first year rises above all earlier generations, including the crisis year 2008, and reaches 14.3% by the 22nd month. The company explains this by a larger share of loans to new customers.

Decision: since July 2022, Oportun has significantly tightened requirements for borrowers, especially those from risky digital channels, reduced loan amounts and terms, cut the volume of issuance, and focused on existing and returning customers, whose losses have historically been lower. The company tracks loans from before and after the tightening separately (back book and front book); according to the report, generations after July 2022 are tracking close to the 2019 generation. This is not visible on the chart: the annual 2022 generation mixes loans from before and after the tightening.

Source of the case: [Oportun Financial Corp — Form 10-Q for Q3 2023 (SEC), sections "Key Performance Metrics" and "Historical Credit Performance"](https://www.sec.gov/Archives/edgar/data/1538716/000153871623000178/oprt-20230930.htm).

## Common mistakes

- **Comparing cohorts of different ages.** Comparing the one-month retention of the March cohort with the three-month retention of the January cohort.
- **Changing the definition of activity.** "Opened the app" and "made a purchase" produce incomparable tables.
- **Confusing columns and diagonals.** A seasonal drop is taken for a deterioration of new cohorts.
- **Mixing channels.** A cohort from a cheap advertising promotion drags the average down; split cohorts by channel if channels changed.

## Source

The method came from epidemiology; in lending, cohorts are called generations (vintages). Attention to the method was drawn by the work of Wade Hampton Frost on tuberculosis mortality among people born in different years: [«The Age Selection of Mortality from Tuberculosis in Successive Decades»](https://pubmed.ncbi.nlm.nih.gov/7801964/), published posthumously in 1939 (the link is to the 1995 reprint).

## See also

- Enhanced by AARRR Metrics: Use the Retention stage of AARRR as the metric traced across cohorts.
- Enhanced by A/B Testing: Cohorts show correlation only; a controlled A/B test shows what caused the gap.
- Enhanced by RFM Analysis: Read retention curves next to RFM segments.
- Enhanced by Sales Funnel: Compute conversion per cohort, so customers from different periods are never mixed.
- Followed by Unit Economics: Take churn from cohort retention curves for the LTV formula.
- Enhanced by HEART Metrics: Trace adoption and retention by cohort, so new arrivals are not counted as growth.
- Enhanced by Metric Pyramid: Check each key metric by cohort to trace North Star shifts to a branch.
- Enhanced by Soft Launch: Group users by install date to read retention on days 1, 3 and 7.
