# AARRR Metrics

## Essence

AARRR, or "pirate metrics" (the abbreviation is read as a pirate's "Arrr!"), is five groups of metrics that describe the customer's path from first contact to money: Acquisition, Activation, Retention, Referral and Revenue. At each stage one or two metrics are chosen and compared with a benchmark. The stage where the product loses the most is the bottleneck: that is where the team works first.

## When to use and when not to

Use it when the product already works and the team needs to understand where to direct its effort: acquisition, first experience, returning users or monetization. The method is good for a regular product review and for talking to management in a shared language.

Inputs: product analytics data for the period — the number of new customers and their acquisition cost, the share who reached first value, the share who came back, the share who came through referral, revenue per customer; plus benchmarks for comparison.

Limits:

- **Numbers without a benchmark say nothing.** 73% active is a lot or a little only when seen next to the previous period, a target or the market.
- **Stages do not always come in order.** A referral can happen before payment, and revenue can start on day one; the funnel is a model, not a law.
- **It shows where, not why.** The cause of losses at a stage is found through interviews, breakdowns of data by customer groups and tests.

## Scheme

| Stage | Question | Example metric |
|---|---|---|
| **Acquisition** | Where do new customers come from and what do they cost? | new customers, CAC (cost of acquiring one customer) |
| **Activation** | Did the customer get first value? | share who did the key action |
| **Retention** | Does the customer come back? | share still active after a month, churn |
| **Referral** | Does the product get recommended to others? | share who came through referral, NPS (net promoter score) |
| **Revenue** | How much does a customer bring? | revenue per active customer |

Next to each metric is a benchmark; the stage with the largest lag is marked as the bottleneck.

## How to apply

1. **Describe the customer's path** in the product and attach the five stages to it.
2. **Choose one or two metrics per stage** with an exact definition: what counts as "active" or "returned".
3. **Collect the values** for the same period.
4. **Pick the benchmarks:** previous period, target, competitors or market — with a source.
5. **Find the bottleneck** — the stage with the largest lag behind its benchmark. Metrics have different units, so the lag is compared as shares: what part of the benchmark the value makes up, or how many times worse it is.
6. **Decide what you change at this stage,** which metric will show the result and by when you will check it.
7. **Repeat** the review regularly: once the bottleneck is fixed, another stage becomes the bottleneck.

## Example

Nubank is a digital bank operating in Brazil, Mexico and Colombia. Below are the metrics from its IPO prospectus (Form F-1, 2021), laid out across the five stages; the periods differ and are given in the rows:

| Stage | Value | What it was compared with |
|---|---|---|
| Acquisition | 48.1 million customers as of 30.09.2021, net growth of over 2 million per month in Q3; CAC $5.0 for the 9 months of 2021 | CAC $3.4 for the 9 months of 2020 |
| Activation | 73% of customers were active in the last 30 days (30.09.2021) | 63% as of 30.09.2020 |
| Retention | voluntary churn of 0.06% of customers per month, another 0.07% closed by the bank due to risk (9 months of 2021) | no direct benchmark; the company calls the churn low |
| Referral | 80–90% of customers came without paid advertising — on their own or by referral (average over the year since founding); NPS 90 in Brazil | NPS 94 in Mexico |
| Revenue | about $4.9 of revenue per month per active customer (Q3 2021) | $23 to over $34 per month for customers active across the core products (Sept 2021) |

The bottleneck is revenue: acquisition is getting more expensive but remains cheap, activity is growing, churn is small, and an average customer brings several times less than one using the core products. The solution stated in the prospectus: grow revenue per customer by increasing the share of their money held in current products and by selling additional products.

Source of the case: [Nu Holdings Ltd., Form F-1 (SEC, 2021)](https://www.sec.gov/Archives/edgar/data/1691493/000119312521314359/d213207df1.htm).

## Common mistakes

- **Vanity metrics.** The number of downloads or sign-ups instead of the share who reached value.
- **Different periods and definitions.** Stages are counted for different months, or the definition of "active" changes between reviews.
- **Working on all stages at once.** Effort gets spread thin; the bottleneck remains.
- **Scaling acquisition while retention leaks.** New customers leave as fast as they arrive, and their acquisition cost keeps rising.

## Source

The scheme was proposed by Dave McClure, later founder of the 500 Startups fund, in the talk [«Startup Metrics for Pirates: AARRR!»](https://www.youtube.com/watch?v=irjgfW0BIrw) at Ignite Seattle in August 2007; later he published an [extended version of the slides](https://www.slideshare.net/dmc500hats/startup-metrics-for-pirates-long-version).

## See also

- Enhanced by Cohort Analysis: Trace the Retention metric by cohort to see whether customers return over time.
- Enhanced by Customer Journey Map: AARRR shows where customers are lost, not why; a journey map finds the cause.
- Alternative to HEART Metrics: Use HEART for user experience rather than the path from first contact to revenue.
- Enhanced by Sales Funnel: Read funnel conversions as AARRR groups to find the bottleneck stage.
- Enhanced by YC Guide to Business Models: Check each funnel stage against the business model's key metrics.
- Enhanced by Metric Pyramid: Map the pyramid's branches onto AARRR stages to check each key metric.
- Followed by HADI Canvas: Turn the bottleneck stage into a HADI hypothesis.
- Enhanced by Soft Launch: Use retention and revenue numbers as launch thresholds.
