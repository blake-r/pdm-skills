# Frequency / Adoption Analysis

## Essence

Frequency and adoption analysis lays out a product's features along two axes: what share of customers uses a feature (adoption) and how often those who have adopted it use it (frequency). Four zones suggest what to do with each feature: develop the key ones, decide the fate of the special ones, automate the utility ones and remove the unneeded ones. The method shows what the product actually rests on, and what merely takes up space in the interface and in support.

## When to use and when not to

Use it when the product has grown features and the team needs to decide what to develop, what to simplify and what to close: before planning the roadmap, when redesigning navigation, when preparing for a redesign, or when the support cost of old code is rising.

Administrative actions — login, password reset, profile edits — are not included in the analysis: they are done out of necessity, not for value.

Inputs: the list of features and their usage events from product analytics for one period — how many active customers used each feature at least once, and how many times on average.

Limits:

- **The value of a one-off action is not visible.** A feature used once a year, for example downloading a tax certificate, the method will send to "unneeded", although without it the customer will leave.
- **Event tagging is needed.** If feature usage is not logged, a point cannot be placed; eyeballed estimates replace the analysis.
- **It shows what, not why.** Low adoption can happen because the feature cannot be found, not because it is not needed.

## Scheme

A scatter diagram: horizontally — adoption, the share of active customers who used the feature; vertically — frequency of use among those who adopted it. Each feature is a point; the zone borders are the medians across features or thresholds the team has agreed on.

| | Low adoption | High adoption |
|---|---|---|
| **High frequency** | Special — engage more customers, or recognize the feature as niche and do not grow it | Key — develop |
| **Low frequency** | Unneeded — drop or rework | Utility — automate and simplify |

## How to apply

1. **Choose the period and the base:** active customers for a month or a quarter, the same for all features.
2. **Compile the list of features** at one level of detail: "transfer by phone number", not "transfers".
3. **Compute adoption:** the share of active customers who used the feature at least once.
4. **Compute frequency:** the average number of uses per adopter of the feature over the period.
5. **Draw the borders** and place the points on the diagram.
6. **Work through each zone.** For features with low adoption — unneeded and special — choose one of four: remove, raise adoption, raise frequency or deliberately improve for those who use it. Many special features are a sign that the product does more than it should.
7. **Record the decision** and repeat the measurement after the changes.

## Example

Monzo is a British digital bank. The app had two tools for tracking spending: the old "Summary" with a budget for a period, and the new "Trends". In November 2025 the current accounts team announced it was closing Summary from December 21, 2025. The rationale was adoption: since March 2023 Summary has not been shown to new customers, "very few" use it, and "the vast majority" has moved to Trends. On the diagram Summary would sit on the left, in the low-adoption zone, and Trends on the right. Monzo did not name frequency: the decision was made on adoption and on the fact that the feature has a replacement. Caveat: the low adoption was partly created by the company itself by hiding Summary from new customers — the two features have different denominators.

The decision did not stop at removal. The team listed what Trends still lacks for the remaining Summary users: weekly and four-weekly spending periods and the exclusion of individual transactions (categories can be excluded), and promised to improve Trends.

Gap: Monzo published no figures or diagram, and no public e-commerce or fintech case with a filled adoption/frequency chart was found, so the placement above is a reading of the announcement, not Monzo's own chart.

Source of the case: [Monzo Community, "Retiring the Summary feature" (November 2025)](https://community.monzo.com/t/retiring-the-summary-feature/186087).

## Common mistakes

- **Different denominators.** One feature's adoption is counted from all customers, another's from active ones; the points become incomparable.
- **Removal without checking the cause.** A feature with low adoption is closed, although customers simply cannot find it.
- **Rare but critical features in "unneeded".** One-off actions such as closing an account or getting a tax certificate are judged by frequency.
- **Closure without a plan for the remaining users.** The few users of a feature lose what is missing in the replacement and go to support or to a competitor.

## Source

The diagram "how many customers use a feature × how often" was proposed by Des Traynor, co-founder of Intercom, in the post [«Prioritising Features: Who'll Use It & How Often?»](https://www.intercom.com/blog/prioritising-features-wholl-use-it-how-often/) (2012): horizontally the share of people ("few", "some", "most", "all"), vertically the share of time ("very little", "some", "most", "all"), a 4×4 grid. The name "feature audit" and the four outcomes for features with low adoption appeared in his article [«Before you plan your product roadmap»](https://www.intercom.com/blog/before-you-plan-your-product-roadmap/) (2014). The Russian names of the four zones and the borders at the medians are a later adaptation; Traynor does not have them.

## See also

- Enhanced by Kano Model: Kano sorts features by effect on satisfaction; adoption and frequency show actual use.
- Alternative to Impact / Effort Matrix: Use the impact-effort matrix to rank features by business effect and cost, not usage.
- Followed by Product Backlog: Put the remove and rework decisions into the product backlog as ordered items.
