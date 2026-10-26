# ICE Scoring

## Essence

ICE is a fast method for prioritizing hypotheses, experiments and features. Each idea is rated on three parameters from 1 to 10: its impact on the target metric (Impact), confidence in the estimates (Confidence), and ease of implementation (Ease). The three scores produce one number; the list is sorted by it and the top ideas are taken into work.

## When to use and when not to

Use it when there are many ideas, they must be sorted in one meeting, and there is little data for precise estimates: an early product, a growth experiment backlog, a weekly choice of tests. The method is cheap: scoring an idea takes minutes, so it can be repeated every week.

Inputs: the list of ideas, one target metric, rough effort estimates from the team, and what is known about each idea (data, research, results of past tests).

Limitations:

- **Scores are subjective.** "Impact 7" means different things to different people. Without agreed scales, the rating reflects the tastes of the scorers, not the ideas.
- **Reach is not considered separately.** A small improvement on the home page and a large one on a rarely visited screen can easily get the same impact. If the audience sizes differ greatly, factor them into impact explicitly.
- **A strong bias toward easy work.** Big bets with low ease and confidence systematically end up at the bottom. Strategic work is planned separately.
- **Ideas with different metrics are not comparable.** Impact on conversion and impact on retention are different quantities.

## Scheme

| Idea / hypothesis | Impact, 1–10 | Confidence, 1–10 | Ease, 1–10 | ICE | Place |
|---|---|---|---|---|---|
| Idea X | 7 | 6 | 5 | 6.0 | 1 |
| Idea Y | 4 | 3 | 8 | 5.0 | 2 |
| Idea Z | 5 | 4 | 4 | 4.3 | 3 |

**ICE = (I + C + E) ÷ 3**, the average variant (in the table above), or **ICE = I × C × E**, the product, which is how Gilad defines it: then X, Y, Z get 210, 96 and 80. For one list, choose one method.

## How to apply

1. **Fix the goal.** One metric the ideas should affect, and the period.
2. **Agree on the scales** before scoring: what 1, 5 and 10 mean for impact and ease. Ease is convenient to tie to effort: for example, 10 — less than a day, 5 — about a week, 1 — more than a quarter.
3. **Estimate the impact:** how much the idea will shift the metric if it works.
4. **Estimate the confidence** by the strength of the evidence, not by liking the idea. Teams often agree on a simplified scale, for example: the author's opinion — 1–2, feedback from several customers — 3–4, analytics data — 5–7, a test result — 8–10. Gilad's Confidence Meter is stricter: each kind of evidence has a weight, and the confidence is the sum of the weights of the evidence you have, capped at 10. The weights in the spreadsheet are: self conviction 0.01, thematic support 0.05, internal reviews 0.1, estimates and plans 0.3, anecdotal evidence 0.5, market data 1.0, customer evidence 2.0, test results 5.0, launch data 7.0. So opinions alone stay near zero, and a few customer comments give 0.5, while live usage alone gives 7.
5. **Estimate the ease:** the time and resources of the whole team, including design, testing and launch.
6. **Calculate ICE.** The average of the three scores, or their product. The product punishes an idea more for one low score and widens the gap between the top and bottom of the list.
7. **Interpret.** Sort in descending order. A difference of one or two points in the average is within the margin of error; decide such ideas on additional considerations. Check an idea with high impact and low confidence first with a cheap test, then re-estimate the confidence.

## Example

Booking.com, Partner Hub — a platform for the site's partners: from registering a property to running a business on Booking.com. The experiment team, with the main metric "clicks on the start of registration", scored each idea on business impact, supporting data and ease of implementation. The source does not call this ICE, and no scores are published: the three criteria match ICE, but the filled table is not available.

Among the tested ideas:

- a sticky panel with a registration button on the mobile version of the "Join now" page — +36% clicks on the start of registration from mobile;
- moving the description of the registration steps higher on the page — no growth in conversion;
- button texts: "Start registration" worked best, while "Sign up today" reduced clicks by about 10%.

Decision: the sticky panel was rolled out to all users.

Source of the case: [Booking.com Partner Hub — Mobile Momentum (AB Tasty / Wingify, customer story)](https://wingify.com/success-stories/booking-com-partner-hub-mobile-growth/).

## Common mistakes

- **Confidence as enthusiasm.** An idea that management likes gets an 8 without a single fact. Confidence should rise only with new data.
- **Mixed calculation methods.** Some rows are calculated as an average, others as a product, or the method changes between meetings: the ratings become incomparable.
- **Ease of development only.** Without design, launch and support, ideas with a heavy tail look "easy".
- **One score for everyone.** If one person gives all the scores, the method legitimizes their opinion. Score together, or average the independent scores of several people.
- **One-time sorting.** Scores become outdated: after a test, a new study or a change in the metric, the ideas need to be re-scored.
- **A ranking instead of a decision.** Close scores do not mean the top idea is better. The number shows trade-offs but does not cancel dependencies and strategy.

## Source

The method was devised by Sean Ellis, founder of GrowthHackers and author of the term "growth hacking", for choosing growth experiments. Ellis and Morgan Brown described it in the book [«Hacking Growth»](https://www.penguinrandomhouse.com/books/545936/hacking-growth-by-sean-ellis-founder-of-growthhackerscom-and-morgan-brown/) (2017); how the book combines the three scores (average or product) is not verified. The attribution to Ellis, the product formula (ICE = Impact × Confidence × Ease) and the confidence scale based on the strength of evidence (Confidence Meter) come from Itamar Gilad's article [Product Discovery With ICE and The Confidence Meter](https://itamargilad.com/the-tool-that-will-help-you-choose-better-product-ideas/) (April 2018). The evidence weights come from his Confidence Meter spreadsheet (CC BY-SA 4.0), downloaded on 22 October 2026 from the author's [downloads page](https://itamargilad.com/resources/downloads/) (the Excel link there, [direct file](https://drive.google.com/uc?export=download&id=1J7HYkvY_91wvyt5WCXf0PgMvJglbQ7fX)), sheet "Ideas", row "Weight". The article's round-by-round numbers do not match the spreadsheet (for example, the article gives 0.1 for self conviction, thematic support and other's opinion together; the spreadsheet has no "other's opinion" column, and its nearest columns, self conviction, thematic support and internal reviews, sum to 0.16), so the card quotes the spreadsheet weights.

## See also

- Alternative to RICE Scoring: Use RICE when audience size differs greatly between ideas, since RICE adds reach.
- Alternative to Impact / Effort Matrix: Use the matrix to show ideas visually when a picture beats a single score.
- Followed by Experiment Card: Test a high-impact, low-confidence idea on an experiment card, then re-score it.
- Followed by Cost / Benefit Analysis: Take the ICE shortlist and calculate the payback of these options in cost-benefit analysis.
