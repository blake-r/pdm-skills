# ABCDX Segmentation

## Essence

ABCDX segmentation divides already paying customers into five groups by how much they need your product specifically. A — the product is very much needed: they buy quickly, a lot or often. B — needed and well paid for, but there are objections. C — there is a need, but the product helps little: a long sales cycle (time from first contact to payment), a small check, customers leave easily. D — they ask many questions, take a lot of effort and do not buy. X — could become segment A, but they need a changed product. The goal is to direct the product, sales and support to A and B, and to make serving C and D cheaper.

## When to use and when not to

Use it when the product already has paying customers and the team does not understand whose requests matter more: support is drowning in tickets, the task list grows, but revenue does not. The method helps choose whose problems to solve first and whom to acquire.

Inputs: for each customer — revenue or margin for the period, number of purchases, if needed the sales cycle and the number of support requests; plus conversations with sales and support about what distinguishes the best customers.

Limits:

- **A base is needed.** According to the authors, the method works roughly from 10,000 paying customers in B2C (selling to people) and from 100 in B2B (selling to companies).
- **There are no ready-made thresholds.** The traits of the segments are specific to each product; they are found in the data and interviews, not taken from a textbook.
- **Only paying customers are visible.** Those who left and those who never reached payment are not in the picture, and before there are any paying customers there is nothing to divide.

## Scheme

| Segment | Who they are | What we do |
|---|---|---|
| **A** | the product is very much needed, they buy quickly, a lot or often | best salespeople, features for their requests, attract similar customers |
| **B** | needed, but there are objections; check above average | remove objections |
| **C** | helps little, long cycle, small check | automate servicing |
| **D** | many questions, much effort, do not buy | do not acquire, minimal service |
| **X** | ready to pay a lot, but need a changed product | assess whether it is worth building a changed product for them |

According to FRII's study of its portfolio companies, A and B bring about 80% of revenue, yet teams spend only about 20% of their time on features for them; C and D draw the attention.

## How to apply

1. **Export customers** with revenue or margin and purchase frequency for the period.
2. **Find candidates:** who pays a lot and often — candidates for A and B; who pays little and rarely — candidates for C and D.
3. **Describe the traits.** What do the best customers have in common: need, situation, channel, geography? Ask sales and support.
4. **Tag customers** by traits, not just by amount: a new customer with the right traits is also A.
5. **Compare the shares** of customers, revenue and tickets by segment.
6. **Tag requests and tickets** by the segments they came from.
7. **Decide:** features and acquisition go to A and B, servicing C and D is automated, X is a separate decision.

## Example

Kidkin is a mobile app in which parents choose a club for their child (swimming, drawing, modeling) and pay for it online right away. In the autumn of 2018 the service attracted many customers who only went to free trial classes — these are segments C and D. The three most frequent support topics for the month, after tagging by segment:

| Support topic | Total | From A and B | From C and D |
|---|---|---|---|
| Few offers in my district | 60 | 2 | 58 |
| The class search filter does not work well | 39 | 12 | 27 |
| Outdated studio contacts | 14 | 3 | 11 |

Decision: first solve the search filter problem and rely on the details of tickets from A and B customers. The most frequent topic — "few offers in the district" — is almost entirely created by C and D, and working on it would spend resources without revenue. The example shows the step of tagging requests; the traits of segments A and B and the outcome of the decision are not published in the source.

Source of the case: [Ivan Zamesin, "How to Make a Product", chapter "ABCDX segmentation"](https://zamesin.ru/books/product-howto/abcdx-segmentation/).

## Common mistakes

- **Segments by revenue alone.** Without traits it is unclear whom to acquire, and a new customer with the right traits does not fall into A.
- **Working by request frequency.** The loudest requests often come from C and D.
- **Dropping X without a decision.** X are the highest-paying potential customers; was that postponed deliberately or forgotten?
- **One-off tagging.** Customers move between segments; traits and shares are reviewed regularly.

## Source

The method was developed by Ilya Krasinsky at the Foundation for the Development of Internet Initiatives (FRII) and tested on startups of its accelerator. One of the first public descriptions is [a presentation by Artyom Azevich (FRII accelerator)](https://www.slideshare.net/profyclub_ru/abcd-77396478); in it, segment X is a reason to direct product managers and development to a product for these customers. A detailed description with cases is in [the chapter by Ivan Zamesin](https://zamesin.ru/books/product-howto/abcdx-segmentation/).

## See also

- Alternative to RFM Analysis: RFM segments customers by purchase behaviour; ABCDX segments paying customers by need for the product.
- Followed by Customer Profile: Once customers are split into segments, write one customer profile per segment.
- Enhanced by Feedback Matrix: Tag reviews by ABCDX segment, so paying A and B customer critique comes first.
- Followed by Segment Scoring: Score ABCDX groups as segments; the top one gets the first product and sales focus.
