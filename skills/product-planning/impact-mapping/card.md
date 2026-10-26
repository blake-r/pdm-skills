# Impact Mapping

## Essence

An impact map is a tree that links a business goal with what the team will do. Four levels are read from left to right: **Why?** — the goal with a metric; **Who?** — the people and organizations on whom the goal depends; **How?** — how their behaviour should change; **What?** — the features and actions that will cause this change. Each feature on the map is explained by a chain leading to the goal, and a feature without such a chain becomes visible as superfluous. The results on the right edge are options, not commitments: the team chooses a branch, does the minimum, measures the shift in the metric, and decides whether to continue.

## When to use and when not to

Use it at the start of a product or a major initiative, when there are many wishes and you need to choose what to do first; when stakeholders bring ready-made features and you need to understand which goal they serve; when the goal changes — to see which branches are no longer needed.

Do not use it if the goal is already narrow and clear and the work is a single feature: the tree degenerates into a line. The map does not estimate effort and does not replace a work plan.

Limitations:

- **The map is no better than the goal.** A goal without a metric ("improve the experience") does not let you cut off any branch.
- **Behaviour changes are assumptions.** The link "feature → behaviour → metric" is checked after release, otherwise the map merely justifies a list of features.
- **It is easy to miss actors** who hinder the goal: competitors, regulators, the company's own departments.

## Scheme

```
Why?              Who?            How?                         What?
goal and metric ─┬─ actor 1 ─┬─ behaviour change 1.1 ── features, actions
                 │           └─ behaviour change 1.2 ── …
                 ├─ actor 2 ─┬─ behaviour change 2.1 ── …
                 │           └─ …
                 └─ actor 3 ──── …
```

## How to apply

1. **Formulate the goal** as a change in a business metric with a number and a deadline, not as a feature.
2. **List the actors:** who can help achieve the goal, who can hinder it, and who will be affected by it.
3. **For each actor, write the behaviour changes:** what they should start, stop or do differently.
4. **For each change, list the possible deliverables:** features, work, campaigns. Not every branch has to be taken down to this level.
5. **Choose one or two branches** that will shift the metric fastest, do the minimum, and measure.
6. **Revisit the map** based on the results: develop the branches that were confirmed, cut the ones that do not work.

## Example

UPI is an Indian instant payment system run by NPCI. In January 2022 the head of NPCI, Dilip Asbe, set the goal: a billion transactions a day within 3–5 years. In 2021 UPI had processed more than 38 billion transactions, about 100 million a day; without effort, in his words, the goal would be reached in about ten years. NPCI did not publish an impact map; below, the goal and the features launched after it are laid out by level, and the user groups are taken from the feature descriptions.

| Who? | How? | What? |
|---|---|---|
| Owners of feature phones without internet (over 400 million people) | start paying via UPI | UPI 123PAY, March 2022: payment by a call to a voice menu, by a missed call, from the phone's built-in app, or by an audio signal |
| Those who find it hard to use a screen | pay by voice | Hello! UPI, September 2023: voice payments in Hindi and English |
| Smartphone users | pay small amounts via UPI instead of cash | UPI Lite, September 2022: payments up to 200 rupees without a PIN |
| Credit card holders | pay with a credit card via a UPI QR code | RuPay cards in UPI, September 2022 |
| Merchants | accept UPI instead of cash | zero fee for accepting payments |

Result: by June 2026 UPI was processing over 750 million transactions a day; the goal has not been reached, and five years from January 2022 end in January 2027. RuPay credit card payments through UPI grew from 363 million transactions in fiscal 2023/24 to over 750 million in April–October 2024. Voice payments, according to Asbe, have not caught on so far.

Decision: in September 2026 NPCI announced that from 15 October merchants will pay 0.4% on UPI payments above 2,000 rupees, capped at 300 rupees. Payments up to 2,000 rupees (over 95% of merchant payment volume), consumer payments and person-to-person transfers stay free. NPCI said the revenue would support infrastructure and cybersecurity; industry estimates put the annual cost of running the system near 20,000 crore rupees.

Sources of the case: Business Standard — [goal](https://www.business-standard.com/article/finance/1-bn-transactions-a-day-on-upi-quite-possible-in-3-5-years-time-npci-ceo-122011200537_1.html) (12 January 2022) and [RuPay cards](https://www.business-standard.com/finance/news/rupay-credit-card-upi-transactions-double-in-first-seven-months-of-fy25-124120301103_1.html) (3 December 2024); The Tribune on [123PAY](https://www.tribuneindia.com/news/business/rbi-governor-shaktikanta-das-launches-upi-service-for-40-crore-feature-phone-users-376094/amp) (8 March 2022); Business Today on [UPI Lite](https://www.businesstoday.in/personal-finance/banking/story/rbi-introduces-upi-lite-for-faster-real-time-low-value-transactions-check-more-details-here-348070-2022-09-23) (23 September 2022) and [Hello! UPI](https://www.businesstoday.in/amp/technology/news/story/hello-upi-npci-rolls-out-new-voice-enabled-payment-methods-and-more-features-check-details-397313-2023-09-07) (7 September 2023); [TNW](https://thenextweb.com/news/india-upi-npci-ai-billion-daily-transactions) (28 June 2026); Swarajya on the [merchant fee](https://swarajyamag.com/news-brief/upi-mdr-from-october-15-npci-sets-04-per-cent-merchant-fee-on-payments-above-rs-2000-caps-charge-at-rs-300) (15 September 2026).

## Common mistakes

- **A feature instead of a goal.** "Launch the app" at the root — there is nothing to cut the branches with.
- **Features at the "How?" level.** Instead of a behaviour change, a feature is written, and the link to the goal is lost.
- **Only one's own users.** Those who hinder the result or on whom it depends are forgotten.
- **The map as a plan.** All branches are taken into work, and nobody measures which one shifted the metric.

## Source

Gojko Adzic, [«Impact Mapping: Making a Big Impact with Software Products and Projects»](https://www.impactmapping.org/book.html), Provoking Thoughts, 2012. The method develops effect maps from the book "Effect Managing IT" by Mijo Balic and Ingrid Ottersten (2007).

## See also

- Preceded by Metric Pyramid: Take the root goal from the North Star metric, so it has a number.
- Preceded by Stakeholders Matrix: Find goal helpers and blockers in the matrix before listing the Who? level.
- Followed by Story Mapping: Lay out the chosen branch features as a story map by user path.
- Followed by SMART Goals: Word each map goal with SMART, giving it an executor and date.
- Followed by Feature Canvas: Fill business goals from the map's behaviour changes.
- Followed by Impact / Effort Matrix: Place only ideas that lead to a goal.
- Followed by Lean UX Canvas: Fill the problem and user boxes from the map's goal and actors.
- Followed by RICE Scoring: Score the map's initiatives with RICE once each is linked to a goal.
