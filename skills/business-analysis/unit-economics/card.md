# Unit Economics

## Essence

Unit Economics is a method of assessing the viability of a business model by the profitability of a single unit: a customer, an order, a unit of goods. According to the PAF (Product Architecture Framework) description, a model scales only when its unit pays back: the revenue from it minus the costs of producing, acquiring and delivering it. The cost of acquiring a customer (CAC, customer acquisition cost) is compared with the remainder after variable costs over a period and over the whole lifetime (LTV, lifetime value).

## When to use and when not to

Use it before scaling paid acquisition and when choosing a channel or a price. You need acquisition costs, new customers, revenue per customer, variable costs and churn (the share of customers who left in a period).

Do not use it on a small sample: CAC and churn swing wildly. Do not use it if fixed costs are not covered.

Limitations:

- **There is no single version of the formulas.** David Skok's (Matrix Partners) main LTV formula has no margin; the version with margin is separate. Wayfair defines contribution margin as gross profit minus customer support costs and payment-system fees. Fix the version.
- **Thresholds are tied to the industry.** Skok, for SaaS (subscription software): LTV/CAC above 3, CAC payback up to 12 months; later he wrote that healthy companies pay back in 20 months, and above 24 it is time to improve.

## Scheme

```
Revenue per customer per period
 − variable costs (goods, delivery, payments, support, returns)
 = contribution per period
 × customer lifetime        → LTV
 ÷ CAC                      → LTV/CAC
CAC ÷ contribution per period → CAC payback, periods
```

## How to apply

1. **Choose the unit and the period;** take the numbers for one period.
2. **CAC** = all sales and marketing spend for the period ÷ number of new customers (Skok).
3. **Contribution per period** = revenue per customer (ARPA, average revenue per account) × contribution margin.
4. **Lifetime** = 1 ÷ churn, in the same units: 3% per month is about 33 months (Skok), with constant churn. Without churn, take the window: this is an estimate for the window, not LTV.
5. **LTV** = ARPA × margin ÷ churn (Skok, version with margin).
6. **LTV/CAC** and **CAC payback in months** = CAC ÷ (ARPA × margin) (Skok).
7. **Set the thresholds before calculating** for your industry; calculate by channel.
8. **Decide.** Below 1: does not pay back, change channel, price or costs. Between 1 and the threshold: is there enough cash to reach payback? Above the threshold: scale while CAC does not grow. Set a review date.

## Example

Wayfair is an online store. In its S-1 registration statement for the IPO (S-1, 15.08.2014, pp. 58–59), the company compared customer acquisition in North America in Q3 2011 and Q3 2013. The share of repeat customers, that is, those who bought twice on the same site within the quarter and the next 180 days, rose from 12.5% to 24.0%. CAC here is calculated on advertising only, so it is understated relative to Skok's version:

| | Q3 2011 | Q3 2013 |
|---|---|---|
| Advertising, $ thousand | 8,797 | 20,966 |
| New customers | 244,778 | 451,750 |
| CAC, $ | 36 | 46 |
| Revenue per customer, $ | 265 | 311 |
| Contribution equaled advertising | 15.09.2011 | 30.10.2013 |

The contribution margin is taken as 20% of revenue. Our calculation, which is not in the S-1: contribution per customer $53 and $62.2; contribution/CAC 1.47 and 1.34; a remainder of about $17 and $16 per customer, totaling $4.2 and $7.1 million — if $265 and $311 are the revenue accumulated over the window.

Decision: in 2011 Wayfair redirected more than 240 niche sites to Wayfair.com. Previously it aimed for a short payback; now it acquires customers with higher lifetime value, accepting a longer payback. The ratio fell, the remainder grew.

What the case lacks: LTV, churn, a decision threshold, and the window for revenue per customer. The S-1 shows the result of a strategy, not the moment of calculation; the 20% is the company's assumption.

Source of the case: [Wayfair Inc., Form S-1](https://www.sec.gov/Archives/edgar/data/0001616707/000104746914007027/a2220999zs-1.htm), Growth in Customer Acquisition and Customer Retention.

## Common mistakes

- **LTV on revenue, not on contribution.** At a 20% margin, the value is overstated fivefold.
- **A threshold from another industry.** Skok's three is derived for SaaS with a margin of 80% and more, and LTV without margin.
- **The best ratio is not the best decision.** Wayfair's ratio fell while the remainder grew: look at the sum too.
- **Infinite lifetime.** With churn near zero, 1 ÷ churn grows without limit: set a horizon.
- **Mismatched periods.** Monthly revenue with annual churn distorts the lifetime.
- **Averaging channels.** An average CAC hides a loss-making channel.
- **The wrong unit.** With repeat purchases the unit is the customer, not the order.

## Source

The description in PAF (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, no date) gives only the definition. The formulas come from primary sources: David Skok (Matrix Partners), [«SaaS Metrics 2.0»](https://www.forentrepreneurs.com/saas-metrics-2/), a post from around 2011, and the appendix [«Detailed Definitions»](https://www.forentrepreneurs.com/saas-metrics-2-definitions/): CAC, lifetime, LTV with and without margin, LTV/CAC, CAC payback. The contribution margin and the example figures are from Wayfair's S-1 (2014).

## See also

- Preceded by Cohort Analysis: Use cohort retention curves to get the churn rate that the LTV formula needs.
- Enhanced by Financial Modeling: Use the per-customer unit economics as inputs to a financial model before launch.
- Enhanced by Cost / Benefit Analysis: Use it to compare feature cost and return by period; Unit Economics checks unit payback.
- Preceded by Product Lifecycle: Check contribution and CAC once the stage points to investment or exit.
- Preceded by YC Guide to Business Models: Calculate CAC and contribution per unit with the guide metrics to test the model.
- Enhanced by TAM / SAM / SOM Model: Use per-customer figures from unit economics in the bottom-up market check.
