# Feedback Matrix

## Essence

The feedback matrix (in the original, "feedback sorting matrix") sorts customer reviews by two questions: does the customer praise or criticize the product (the tone of the review), and does something need fixing. This gives four groups: advice, compliment, critique and suggestion. Each has its own order of action: sorting reviews turns into distribution of work — critique is fixed first, advice goes into improvements, suggestions are accumulated, compliments are protected as strengths.

## When to use and when not to

Use it when there are many reviews and they come from different channels: in-app ratings, support requests, app store reviews, survey answers. The matrix separates what requires a response from noise.

Inputs: reviews for the period with text and channel; for each — the topic (which part of the product), the tone and the rating, and whether the problem gets in the customer's way of using the product.

Limits:

- **One review is not a problem.** The matrix sorts individual statements; the frequency of a topic and the number of affected customers are counted separately.
- **Severity is not decided by tone.** A calm "payment did not go through" matters more than an angry review about the color of a button; the "must fix" axis is assessed by the consequences for the customer, not by emotions.
- **Silent customers are not visible.** Reviews are left by the most satisfied and the most dissatisfied; those who quietly left do not appear in the matrix.

## Scheme

A 2×2 matrix: vertically — the tone of the review (positive or negative), horizontally — whether something must be fixed.

| | Must be fixed | Can be left as is |
|---|---|---|
| **Positive** | **Advice** — "good, but worth improving": goes into improvements | **Compliment** — a strength: keep it and use it in communication |
| **Negative** | **Critique** — "bad, gets in the way": fix first | **Suggestion** — "bad, but livable": accumulate, watch the frequency |

## How to apply

1. **Collect the reviews** for one period from all channels into one table.
2. **Split them into statements:** one review may contain both praise for delivery and a complaint about payment.
3. **Assign a topic** to each statement: payment, delivery, search, support.
4. **Assess the tone and the need for a fix.** Agree on the "must fix" criterion in advance: for example, the customer could not complete an action, lost money or time, or is about to leave.
5. **Place them in quadrants** and count how many statements and customers each topic has. Neutral statements with no request and no rating are not placed in the matrix, but they are counted.
6. **Distribute the work:** critique goes to the owners of the topics with a reply to the customer, advice goes to the improvement list, suggestions go to a pool reviewed by frequency, compliments go into the description of strengths.
7. **Close the feedback loop:** tell the customer what was done about their review.

## Example

Magnit is a Russian grocery chain; its OMNI app combines grocery ordering, a marketplace and a bonus program. From early 2024, in a year and a half, the company grew review collection from about 2 to 150 thousand per day; reading them by hand became impossible. A language model classifies each review by 80 parameters, from product availability to parking, and determines the tone: positive, negative or neutral.

The tone alone was not enough. The team distinguishes severity: "parking is inconvenient, but tolerable" and "because of your parking I will never set foot here again" — both reviews are negative and about parking, but in the matrix the first is a suggestion and the second is critique. The decision made on the basis of this tagging:

- simple and positive reviews go straight into analytics, to managers' dashboards;
- problematic and critical reviews become tasks for the store: the store fixes the issue and reports on it, and the call center tells the customer what was done.

The company saw the need to respond in the reviews themselves: customers wrote that "nobody reads these reviews". In A/B tests, customers who received a reply about the measures taken returned to that store more often and had a higher average check (the article gives no figures).

Caveat: the article shows only the tone axis, severity of a topic and the split into problematic cases and the rest; it does not use the four quadrants, so they are reconstructed from the parking pair, and the advice quadrant is not singled out. The reviews concern the chain's offline stores.

Source of the case: [Magnit Tech, "How we taught AI to turn reviews into money" (Habr, 2025)](https://habr.com/ru/companies/magnit/articles/950262/).

## Common mistakes

- **Sorting by tone instead of consequences.** Loud complaints get priority, while quiet breakdowns remain.
- **A whole review in one cell.** Praise and complaint from one text cancel each other out.
- **Suggestions without review.** "Livable" for one customer, but a hundred identical suggestions are already critique.
- **No reply to customers.** Customers stop writing, and the flow of reviews dries up.

## Source

The primary source is a blog article by the online school Zillion, [«Feedback in a team: 5 models, the feedback sorting matrix, criticism and compliments»](https://web.archive.org/web/20140304210844/http://zillion.net/ru/blog/565/obratnaia-sviaz-v-komandie-5-modieliei-matritsa-sortirovki-os-kritika-i-komplimienty) (February 17, 2014, author not stated). There the matrix serves for feedback within a team: a person sorts feedback about themselves by evaluation ("+" or "−") and by whether they should keep doing it that way or change something. The quadrant formulas are: "good, it can stay this way in the future", "bad, but I can live with it", "good, but it needs refinement and improvement", "bad, and it must be fixed". Applying it to customer reviews and the criterion "by consequences for the customer" are adaptations made by this card.

## See also

- Followed by 5 Whys: Run 5 Whys on a recurring critique to find its root cause before fixing it.
- Followed by Product Backlog: Add advice items to the product backlog as improvements, and review suggestions there by frequency.
- Enhanced by ABCDX Segmentation: Tag reviews by ABCDX segment; rank critique from paying A and B customers first.
- Enhanced by Customer Journey Map: Place each sorted review on its journey stage to show where customers get stuck.
