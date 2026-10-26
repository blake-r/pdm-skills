# Kano Model

## Essence

The Kano Model is a way to find out from users how the presence and absence of each feature affects their satisfaction, and to sort features into categories:

- **must-be (M)** — their presence goes unnoticed, while their absence strongly frustrates: payment security, a working login;
- **one-dimensional (O)** — the better it is done, the more satisfied people are, and vice versa: speed, commission;
- **attractive (A)** — they are not expected; their presence delights, and their absence does not frustrate;
- **indifferent (I)** — no difference whether they are there or not;
- **reverse (R)** — their presence irritates.

Kano's main point: satisfaction is asymmetric. A must-be feature will not bring joy no matter how much is invested in it, while an attractive feature does not cause dissatisfaction when it is absent.

## When to use and when not to

Use it when there is a list of candidate features and you need to understand which of them users consider a given, which they value, and which they are indifferent to. When the team argues whether to build the "basics" or a "wow feature".

Do not apply it to features that a user cannot imagine from a single phrase: the answers will be random. It is not suitable for choosing between two or three variants of one feature — that is a question for an experiment, not a survey.

Limitations:

- **A survey shows attitude, not behaviour.** It is easier to say "I like it" than to pay.
- **The counting rule changes the conclusion.** By Berger, the category is the most frequent answer; many studies take the largest of A, O, M, if their sum is greater than the sum of I, R, Q. For the same feature, the results diverge.
- **Categories become outdated.** An attractive feature becomes expected over time, so the survey is repeated.

## Scheme

```
 satisfaction
     ▲             attractive ╱ one-dimensional
     │                  ___.-'  ╱
     │            _.--''      ╱
 ────┼──────────────────────╱────────────▶ how well
     │                    ╱  ___.--''''    the feature is done
     │                  ╱.-''  must-be
     │                ╱ /
```

Evaluation table: the answer to "if the feature is present" × the answer to "if the feature is absent".

| Present ↓ / absent → | I like it | I expect it | I am neutral | I can live with it | I dislike it |
|---|---|---|---|---|---|
| I like it | Q | A | A | A | O |
| I expect it | R | I | I | I | M |
| I am neutral | R | I | I | I | M |
| I can live with it | R | I | I | I | M |
| I dislike it | R | R | R | R | Q |

Q — questionable answer.

## How to apply

1. **Select the features** and formulate each one as a benefit for the user, understandable without explanation.
2. **Ask two questions** for each feature: how would you feel if it is present, and if it is absent; five answer options.
3. **Survey** users of the needed segment, from several dozen people.
4. **Classify** each answer pair using the table and count the answers by category.
5. **Assign a category** to the feature. A tie or many Q is a reason to ask again. Calculate Berger's coefficients: Better = (A + O) / (A + O + M + I), Worse = −(O + M) / (A + O + M + I).
6. **Decide:** first close the must-be features, then invest in the one-dimensional ones, add one or two attractive ones, and defer the indifferent ones.

## Example

Researchers from Gadjah Mada University surveyed, in March to May 2020, users of the Indonesian wallets OVO and ShopeePay who paid for online purchases with them. Part of the results for ShopeePay, based on 145 responses per feature:

| Feature | A | O | M | I | Category in the article |
|---|---|---|---|---|---|
| Navigation | 49 | 53 | 12 | 31 | one-dimensional |
| Ad frequency | 26 | 51 | 31 | 37 | one-dimensional |
| Screen quality | 29 | 32 | 28 | 56 | one-dimensional |
| Transaction security | 11 | 25 | 39 | 69 | must-be |
| Brand image on screen | 33 | 21 | 25 | 66 | attractive |

The authors counted the categories by the rule "A + O + M against I + R + Q". By the most frequent answer, the bottom three features would have been indifferent.

The decision the authors propose, from their satisfaction map (built on Better and Worse coefficients, so its quadrants differ from the table categories): improve the features in the one-dimensional, must-be and indifferent quadrants, starting with the indifferent ones; ad frequency and reviews — to reduce dissatisfaction. They place all ease-of-use items, such as navigation, in the attractive quadrant.

What the case does not have: this is an independent study, not the company's own work. Whether ShopeePay followed the recommendations and what changed has not been published.

Source of the case: V. H. Budiarani et al., [«The Kano Model: How the Pandemic Influences Customer Satisfaction with Digital Wallet Services in Indonesia»](https://journal.ugm.ac.id/jieb/article/download/59879/30458), Journal of Indonesian Economy and Business, 2021.

## Common mistakes

- **Asking only about the presence of a feature.** Without the second question, categories cannot be determined.
- **Mixing segments.** For newcomers a feature is attractive, for experienced users it is must-be; in total it comes out as a tie.
- **Trusting a category with nearly equal answers.** A gap of a couple of votes is not a result.
- **Investing in attractive features without closing must-be gaps.** The joy of a novelty will not cover a failure in the basics.
- **Not repeating the survey.** Last year's attractive feature is today's expected one.

## Source

N. Kano, N. Seraku, F. Takahashi, S. Tsuji, [«Attractive Quality and Must-Be Quality»](https://www.jstage.jst.go.jp/article/quality/14/2/14_KJ00002952366/_article/-char/en), Journal of the Japanese Society for Quality Control, 1984. The evaluation table and coefficients: C. Berger et al., [«Kano's Methods for Understanding Customer-defined Quality»](https://www.walden-family.com/public/cqm-journal/2-4-Whole-Issue.pdf), Center for Quality of Management Journal, 1993.

## See also

- Enhanced by Customer Survey: Ask the two Kano questions per feature in a survey of about 100 users.
- Followed by RICE Scoring: Rank features kept in the plan by RICE to set the work order.
- Enhanced by Strategy Canvas: Use Kano categories to decide which canvas factors to keep, raise or create.
- Enhanced by Frequency / Adoption Analysis: Compare Kano categories with usage data to see which satisfiers are used.
- Preceded by Value Proposition Canvas: Match features to pains and gains first, then classify them by Kano category.
