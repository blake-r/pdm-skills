# Segment Scoring

## Essence

Segment Scoring is the evaluation of customer segments by several criteria in order to choose which one to focus on. Each segment gets a score on each criterion, an overall score is calculated from the scores, and the segments are sorted by it.

The overall score is calculated in one of two ways:

- **Product:** X × Y × Z. One low score drags the whole score down: a segment without money or without access will not win on size alone.
- **Weighted sum:** X·Kx + Y·Ky + Z·Kz. A strong criterion can compensate for a weak one, and the weights set what matters more.

A quick version for a startup uses four criteria: segment size, ability to pay, sharpness of the pain, and accessibility. Each is rated from 1 to 3, the scores are multiplied, and the focus goes to the segment with the highest score.

## When to use and when not to

Use it when you need to choose the first segment for a new product or a market entry; when you need to split sales and marketing effort between segments; when a team argues about which segment is the main one and needs a common language for the debate.

Do not use it while the segments are not described or overlap: the score would compare something unclear. It does not replace conversations with customers: without facts behind the scores, the score is an opinion written down as a number.

Limitations:

- **The scale is coarse.** With scores of 1–3, close scores are a tie, not a win.
- **Weights and the meaning of scores are subjective.** They are agreed before scoring; otherwise they are tuned to the desired answer.
- **Criteria do not describe everything.** The score chooses where to start, but does not say what to do next.

## Scheme

| Segment | Criterion X | Criterion Y | Criterion Z | Score |
|---|---|---|---|---|
| Segment A | 3 | 3 | 2 | **18 — focus** |
| Segment B | 2 | 1 | 2 | 4 |
| Segment C | 1 | 2 | 3 | 6 |

## How to apply

1. **Describe three to seven segments:** who the customer is and in what situation, without overlaps.
2. **Choose the criteria** and agree what 1, 2 and 3 mean for each.
3. **Choose the calculation method.** Product — when a weak criterion must knock a segment out; weighted sum — when the criteria are unequal. Set the weights before scoring.
4. **Score the segments,** recording a fact behind each score: data, interviews, reports.
5. **Check the leader:** does it have a low score on a critical criterion; for close scores, decide by checking with customers.
6. **Choose the segment to focus on** and re-score when new data appears.

## Example

Amazon, 1994. Jeff Bezos compiled a list of 20 products that could be sold online and narrowed it down to five: music CDs, computers, software, video and books. Bezos compared market segments by product rather than by customer group, and did not publish scores: the table below was compiled by us from his criteria.

| Category | Number of items | Mail catalog | Suppliers |
|---|---|---|---|
| Books | more than 3 million in print | too large to mail out | wholesalers already have electronic warehouse lists |
| Music CDs | about 200 thousand | not in the sources | not in the sources |
| Computers | not in the sources | not in the sources | not in the sources |
| Software | not in the sources | not in the sources | not in the sources |
| Video | not in the sources | not in the sources | not in the sources |

In a 1997 interview, Bezos explained: books have more titles than any other category; "with such a number of products, one can build a store that could not otherwise exist".

Decision: start with books only. The site opened in July 1995.

Result: within 30 days, without press advertising, Amazon had sold books in all 50 states and 45 countries; by September it was selling $20 thousand a week. In 1997 revenue grew 838%, to $147.8 million; customer accounts reached 1.51 million.

Sources of the case: CNBC, [Bezos interview, 1997](https://www.cnbc.com/2024/01/13/in-1997-jeff-bezos-said-why-he-chose-books-to-sell-on-amazon.html); Academy of Achievement, [Bezos biography](https://achievement.org/achiever/jeffrey-p-bezos/); Amazon, [shareholder letter for 1997](https://s2.q4cdn.com/299287126/files/doc_financials/annual/Shareholderletter97.pdf); the list of 20 products — Wikipedia, [«History of Amazon»](https://en.wikipedia.org/wiki/History_of_Amazon).

## Common mistakes

- **Scores without facts.** The score looks precise, but behind it are opinions.
- **A "everyone" segment or overlapping segments.** The same customers get scored twice.
- **Weights set after scoring.** The weights are chosen to fit a winner picked in advance.
- **Sum instead of product.** A large segment without money wins on size.
- **A tie treated as a win.** A one-point difference on a coarse scale decides the choice.

## Source

The method in this form is described in the glossary of [Product Framework](https://productframework.ru/activities/segment_scoring); the author of the formula is not named. Similar criteria for choosing a first market are in Bill Aulet: «Disciplined Entrepreneurship», Wiley, 2013, and in the [MIT 15.390 course slides](https://ocw.mit.edu/courses/15-390-new-enterprises-spring-2013/5e1d0f18b12ccbd4e05f3fd05295c56a_MIT15_390S13_lec07.pdf): does the customer have money, is the customer reachable by sales, is there a compelling reason to buy. A weighted sum of scores by attractiveness factors appears in the McKinsey matrix for General Electric in the early 1970s: [GE multifactorial analysis](https://en.wikipedia.org/wiki/GE_multifactorial_analysis).

## See also

- Preceded by ABCDX Segmentation: Split paying customers into ABCDX groups first, then score those groups as the segments.
- Followed by Buyer Persona: Describe the top segment's typical buyer: who decides and what holds them back.
- Enhanced by ABC Analysis: Use ABC to find key objects, then score segments to decide where to focus.
- Preceded by Technology Adoption Lifecycle: Pick the beachhead niche from the lifecycle, then score it against other segments.
- Followed by TAM / SAM / SOM Model: Use the chosen segment as SAM, then size TAM and SOM around it.
