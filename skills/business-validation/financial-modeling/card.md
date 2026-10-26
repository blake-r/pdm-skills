# Financial Modeling

## Essence

Financial Modeling (financial, or mathematical, modeling) checks a business-model hypothesis by calculation before launch. Business and product metrics are linked into a system of formulas, and a combination of initial metrics is sought at which the target metrics are reached. In the Product Architecture Framework (PAF) this is a fast and cheap way to filter out weak options, but the proof remains "a priori" (before experimental data).

## When to use and when not to

Apply when there is no experimental data and there are many options: calculation sorts through dozens and selects those worth testing in the market. Needed: metrics of the chain "costs → profit": product creation, acquisition, sales, logistics, retention, upsell, support.

Limitations:

- **Low trust.** PAF: the model is a priori and must be checked in the real world. Initial metrics are hypotheses, and the model returns what was put into it.
- **Skills are needed.** PAF: knowledge of financial modeling is required.
- **Facts are more reliable.** If the initial metrics are factual, the hypothesis is a posteriori (after experience) and trust is higher.

## Scheme

```
Initial metrics ──► system of formulas ──► Target metrics
(assumptions)       (costs into profit)    (profit, payback)
Forward problem:  from initial metrics compute target
Inverse problem:  from target find initial metrics
Criterion set before calculation; is a combination found?
  yes: go and check; no: change the sets
```

## How to apply

1. **Formulate the hypothesis:** "conditions (initial metrics) will ensure the goal (target metrics)". Choose the unit (customer, store) and the period.
2. **List the metrics** across the seven groups and assemble them into a chain from costs to profit.
3. **Choose the problem.** Forward or inverse. The inverse has many solutions: add a boundary condition (PAF: cost of a lead no higher than 1200 ₽) or an optimization function.
4. **Fill in the assumptions and mark the basis:** fact, estimate, target or hypothesis. Give three scenarios: pessimistic, base, optimistic.
5. **Set the criterion before calculation:** target profit, allowed payback period.
6. **Calculate** (formulas are the card author's calculation): unit contribution = revenue per unit × (1 − share of variable costs); payback period = launch costs ÷ unit contribution; period profit = volume × contribution − fixed costs; net profit over the term = allowed term × period profit − volume × launch costs; break-even = fixed costs ÷ unit contribution; launch cost limit = allowed term × contribution.
7. **Check sensitivity** (the card author's conclusion): shift each assumption by ±10% and see how net profit changes. Check the most influential assumptions first.
8. **Decide.** Criteria met: the hypothesis is not rejected, time to check it with facts. Not met: change the metric sets and repeat (PAF), or drop the option.

## Example

Warby Parker, an American eyewear brand with online sales and stores (in S-1: multichannel); a prospectus for a stock exchange, Form S-1 of the US Securities and Exchange Commission, 24.08.2021. The case is incomplete: the model is given as targets, not as a calculation.

Company targets: mature stores (open 12+ months) have sales of $2,900 per sq. ft and a four-wall margin of 35%; a new store must pay back in less than 20 months. Four-wall margin is the share of store sales left after the store's own costs: cost of goods, rent, staff.

Hypothesis of the card author: a new store reaches the level of a mature one and pays back on time, so the network can be expanded. Assumption of the author: the figures for a mature store are valid for a new one.

Calculation by the card author: the period is taken as a year (not stated in S-1), and store costs are entirely variable: contribution $2,900 × 35% = $1,015 per year per sq. ft. Inverse problem: investment per sq. ft no higher than $1,015 × 20 ÷ 12 ≈ $1,692, otherwise the term is not met.

Decision: S-1 names a plan to open 30–35 stores in 2021 (126 at the end of 2020, 145 on 30.06.2021); the source does not say the plan follows from a model. Potential in the US per the analysis of a third-party firm: 900+ stores.

What is missing: investment per store, area, fixed costs, scenarios, sensitivity, and the actual margin in the sections reviewed.

Case source: Warby Parker Inc., [Form S-1](https://www.sec.gov/Archives/edgar/data/1504776/000162828021017546/warbyparkerincs-1.htm), 24.08.2021, pp. 125 and 127.

## Common mistakes

- **Assumptions without basis.** Numbers pulled from thin air are presented as a calculation. Mark them: fact, estimate, target, hypothesis.
- **One scenario.** Without a pessimistic one the option looks more reliable.
- **Criterion after the calculation.** The threshold is fitted to the result, so it always "adds up".
- **The solution of the inverse problem is taken as the only one.** PAF: there are many solutions; boundary conditions are needed.
- **Not all cost items.** Advertising is included, but logistics, returns and fees are not.
- **Different periods and units.** Monthly revenue against annual costs distorts the payback period (card author's conclusion).
- **"Adds up" is read as "proven".** The calculation does not replace checking in the real world.

## Source

PAF description (Sergey Tikhomirov, [productframework.ru](https://productframework.ru/hypotheses/business_model), CC BY-SA 4.0, undated): section on business-model hypotheses. No single author of the method is named in the sources. Additions by the card author, not in PAF: three scenarios, criterion before calculation, break-even point, payback period, net profit over the term and sensitivity.

Warby Parker Inc., [Form S-1](https://www.sec.gov/Archives/edgar/data/1504776/000162828021017546/warbyparkerincs-1.htm), SEC, 24.08.2021.

## See also

- Enhanced by Unit Economics: unit economics gives the per-unit contribution that the model's payback formula needs.
- Enhanced by Cost / Benefit Analysis: cost-benefit compares costs and returns by period; the model adds scenarios and sensitivity.
- Preceded by Business Model Canvas: the canvas's revenue and cost blocks become the metrics of the model.
- Followed by Minimum Viable Product: once the model passes, test the main assumption on real users with an MVP.
- Preceded by TAM / SAM / SOM Model: Take the SOM estimate and compare it with the revenue goal inside the model.
