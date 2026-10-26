# Pilot Project / Sample

## Essence

A way to test a value proposition (what the customer gets and why they need it): build a trial solution with the minimum set of features sufficient to test the demand hypothesis, and hand it to real users or clients. People see the result (or part of it) of a full product on a live example. PAF (Product Architecture Framework) considers this method the most valid, that is the most reliable, but also the most expensive in resources.

## When to use and when not to

Use when the value cannot be shown in words (a service, an integration) and a working trial solution can be assembled. Inputs: a hypothesis, a group of participants, success indicators with a threshold, a term, a person who makes the decision.

PAF points to a limitation: far more resources are needed than for other ways of testing a value proposition. Card author's recommendation: if the question can be closed more cheaply, start with the cheap option.

Do not use it, and read its result carefully:

- **Success among the first participants does not equal market demand.** Steve Blank writes that the first version is sold to "visionaries, not to everyone"; most customers do not need such a minimum.
- **Two things are tested at once.** PAF notes that both the value and the specific solution are tested this way. Failure is then ambiguous: either the proposition itself is not needed or the solution was poorly made.
- **A pilot does not promise continuation.** According to Natalia Degtyareva (VTB, 2019), a pilot checks how useful the solution is to the bank and how well it fits it; it opens opportunities but does not guarantee the continuation of cooperation.

## Scheme

```
Hypothesis → trial solution (minimum) → participants → criteria and term (before start)
→ launch → numbers + feedback → comparison with the threshold
→ decision: scale / rework and repeat / stop
```

## How to apply

1. **Hypothesis:** "[group] will get [benefit] from [result of the solution]".
2. **Minimum:** one key benefit; everything else by hand.
3. **Participants:** from the target group, not only the most loyal ones; record how they were selected.
4. **Criteria before the start.** Card author's recommendation: 2–3 indicators, a threshold, a term, the person responsible for the decision. Benchmarks from banks: Alfa-Bank names 2–3 key performance indicators (KPIs) for a pilot (RB.RU, 2025); the VTB accelerator — about 14 weeks (2019).
5. **Launch and collect.** Count conversion (the share of participants who reached the target action out of all who received the sample) and collect feedback: numbers show what happened, feedback shows why.
6. **Decision.** Above the threshold — scale, having assessed integration and load separately (among other things these are the conditions for scaling at Alfa-Bank). Near the threshold or without a clear reason — rework and repeat. Below — stop.

## Example

Fintech, mortgages, United Kingdom; no criteria in the source.

- **Hypothesis** is not formulated in the sources. In meaning: brokers find it more convenient to submit applications to Virgin Money directly from their working platform (card author's conclusion).
- **Pilot.** On 1 December 2020 Virgin Money (a lender among the "top ten" mortgage lenders) and Twenty7Tec (the CloudTwenty7 platform for brokers) announced the APPLY integration: first for two intermediaries, Connells and Mortgage Advice Bureau, then for the market in early 2021. The word "pilot" is not in this release. Brokers requested a decision in principle on a mortgage (Decision in Principle) and submitted a full application.
- **Result.** More than 1,000 applications to Virgin Money via APPLY. Simon Wallace (Virgin Money) noted how quickly brokers submit applications.
- **Decision.** The integration was opened to all CloudTwenty7 users (messages of 15 and 16 March 2021). Only in them do Twenty7Tec and Virgin Money call it a successful pilot. The term is not given; from announcement to decision no more than 3.5 months (card author's calculation).

There is no threshold, term, share of applications from possible ones, conversion or feedback. The decision is visible, the criterion is not.

Sources: [Virgin Money, 2020](https://virginmoneyukplc.com/newsroom/article/partnership-with-twenty7tec), [Financial Reporter, 2021](https://www.financialreporter.co.uk/mortgages/virgin-money-apply-integration-rolled-out-to-all-cloudtwenty7-users.html), [Mortgage Introducer, 2021](https://mpamag.com/uk/mortgage-types/residential/apply-integration-accessible-to-all-cloudtwenty7-users/388616).

## Common mistakes

- **No criteria and term before the start.** Any result is explained after the fact, and the pilot drags on as a free trial. In the case the threshold was not published.
- **Participants unlike the market.** Two agreeing partners show success with them, not with everyone.
- **Volume instead of share.** "More than 1,000 applications" without a denominator does not show reach.
- **A sample without the key benefit or with extras.** In the first case the value is not visible; in the second, cost and term grow.
- **Mixing hypotheses.** On failure it is unclear whether the value or the execution is to blame; decide in advance what exactly is being tested.
- **No decision after the pilot.** Scaling requires checks of integration and load; decide: scale, rework, stop.

## Source

Description in PAF (Sergey Tikhomirov, [productframework.ru](https://productframework.ru/hypotheses/value_proposition), CC BY-SA 4.0, undated): the page on value-proposition hypotheses, section "Pilot project / Sample". PAF does not name the author of the method or the year; "a solution with the minimum set of features" is rendered as "trial solution".

Steve Blank, [«Perfection By Subtraction»](https://steveblank.com/2010/03/04/perfection-by-subtraction-the-minimum-feature-set/), blog, 4.03.2010: the first version for "earlyvangelists" (early enthusiastic customers). Natalia Degtyareva, [«Pilot with a bank: how a startup does not crash on the runway»](https://habr.com/ru/companies/vtb/articles/462069/), Habr (VTB blog), 1.08.2019. Alina Aleshchenko, [«Effective piloting»](https://rb.ru/stories/effektivnoe-pilotirovanie/), RB.RU, 14.03.2025. HBR, McKinsey, Gartner were not used: full text is unavailable.

## See also

- Preceded by Single-feature Prototype (Concierge MVP, Wizard of Oz, Third-party product): The cheap by-hand test comes first; the pilot follows it.
- Followed by Soft Launch: After value is shown, release to a limited audience in a similar market.
- Preceded by Business Model Patterns: Take the chosen pattern idea as the hypothesis the pilot tests.
- Preceded by Gartner's Hype Cycle: Run the pilot once the technology reaches phase 3 or 4 and passes fit check.
- Preceded by Physical Modeling: Give real users the trial solution only after the model meets its criteria.
