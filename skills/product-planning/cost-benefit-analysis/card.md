# Cost / Benefit Analysis

## Essence

Cost-benefit analysis compares how much a feature or change costs and how much it brings in, period by period. For each option it counts the money it will bring or save, and the money it will consume: development, support, marketing, operating expenses. The ratio of cumulative benefits to cumulative costs shows whether the option has paid back and when: a value of 1.0 is the break-even point. Different options pay back in different ways: one grows fast and then fades, another grows slowly, a third is loss-making for a long time but then overtakes the others.

## When to use and when not to

Use it when you need to decide whether to launch a feature, which of several options to choose, whether to keep investing in a function that already works, or whether to shut it down. It is especially useful when costs and benefits are spread over time.

Inputs: for each option and period, estimates of benefits (extra revenue, saved costs, reduced losses) and costs (one-off and recurring), the analysis horizon, and the discount rate (by how many percent a year future money is worth less than money today).

Limitations:

- **Estimates, not facts.** A feature's benefits are almost always a forecast; estimates can vary several-fold, so calculate a range.
- **Not everything converts to money.** Convenience, trust and reputational risks have to be described in words next to the numbers.
- **The horizon changes the answer.** Over a short horizon, fast options win; over a long one, slow but stable options win.

## Scheme

Chart: time on the horizontal axis, the ratio of cumulative benefits to cumulative costs on the vertical axis. The dashed line at 1.0 is the break-even point; an option above the line has paid back.

| Period | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Cumulative costs | 100 | 130 | 160 | 190 |
| Cumulative benefits | 20 | 90 | 180 | 290 |
| Ratio | 0.2 | 0.7 | 1.1 | 1.5 |

Here the option pays back in the third period. Totals for the option: the payback period, the final ratio, and the net benefit — benefits minus costs, brought to today's money when discounted (NPV, net present value).

## How to apply

1. **Formulate the decision and the options**, including the "change nothing" option — the others are compared against it.
2. **Choose the horizon and the step:** month, quarter or year, according to the product cycle.
3. **List the costs:** development, infrastructure, support, marketing, operating expenses.
4. **List the benefits:** extra revenue, saved costs, reduced losses — only above the "change nothing" option.
5. **Estimate each line by period** as a range "cautious — optimistic" and state the source of the estimate.
6. **Calculate cumulative sums, the ratio and the net benefit**; if the horizon is longer than a year, discount.
7. **Decide** and record the actual figures under which the decision would be revisited.

## Example

In 2017 the Payments Strategy Forum of the UK (a forum created by the regulator, made up of banks, fintech companies and payment users) chose how to upgrade the interbank payment systems Bacs and Faster Payments. The "change nothing" option was ruled out: the regulator already required moving them to the ISO 20022 message standard. The new NPA architecture with three services on top of payments (a request-to-pay service, a payee and payment verification service, and account reconciliation data) was therefore compared with a minimal upgrade of the old systems. The horizon was 2019–2031, and the discount rate was 3.5% per year:

| | NPA | Minimal upgrade |
|---|---|---|
| Benefits | £11.0–13.5 bn | £4.0–4.9 bn |
| Costs | £5.4–6.6 bn | £4.3–5.2 bn |
| Net benefit | +£5.6–6.8 bn | −£0.2–0.3 bn |
| Benefit-to-cost ratio | about 2.0 | about 0.94 |

The whole difference in benefits comes from the new services: £6.9–8.5 bn, assuming that up to 18–30% of payments would use them over ten years. The benefit of the existing systems was taken as equal to their current expenses in both options. Growing competition and financial inclusion were not converted into money; they were described in words.

Gap: the source gives discounted totals for the whole horizon, not a period-by-period profile, so the payback curve from the Scheme cannot be reconstructed from it.

Decision: the Forum chose NPA and included the calculation in its November 2017 blueprint; the blueprint was meant to be handed to the New Payment System Operator for delivery.

Source of the case: [Payments Strategy Forum, "Cost Benefit Analysis of the NPA" (November 2017)](https://www.psr.org.uk/media/pdbcnfmy/cost-benefit-analysis-blueprint.pdf); on the handover of the project — [Osborne Clarke (on the 2017 consultation)](https://www.osborneclarke.com/insights/payments-strategy-forums-blueprint-for-a-new-uk-payment-system).

## Common mistakes

- **Benefits without comparison to "change nothing".** Revenue that would have come in without the feature gets recorded as a benefit.
- **Double counting.** A transfer of money between parties is counted as both a cost and a benefit.
- **Only one-off costs.** The feature's support and infrastructure eat up the benefit within a year or two.
- **A precise figure instead of a range.** The decision looks more reliable than it is.
- **No condition for revisiting.** The feature has not paid back, but it keeps being supported.
- **Choosing by ratio alone.** A small option with a ratio of 3.0 may bring less net benefit than a large one with 1.5; check both indicators.

## Source

The idea of comparing the public benefits and costs of a project in money terms was formulated by the French engineer Jules Dupuit in the article "De la mesure de l'utilité des travaux publics" (1844), about evaluating bridges and roads ([about Dupuit on Wikipedia](https://en.wikipedia.org/wiki/Jules_Dupuit)). In the 20th century the method became mandatory for public projects, and then moved into the evaluation of investments and product decisions.

## See also

- Preceded by ICE Scoring: Rank ideas with ICE first, then run the cost-benefit analysis on the shortlist.
- Enhanced by Financial Modeling: Use a financial model to calculate cash flows and net benefit per period.
- Enhanced by Unit Economics: Check that one customer or order is profitable before counting total feature benefit.
