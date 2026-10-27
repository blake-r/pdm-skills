# GE–McKinsey Matrix

## Essence

The GE–McKinsey Matrix, also called the nine-box matrix or the GE business screen, is a way for a company with several businesses to decide where to put its money. Each business unit is placed on a 3x3 grid along two axes: how attractive its industry is, and how strong the unit is against its competitors. Each axis is not one number but a weighted score over several factors that the person using the matrix picks.

Placement gives one of three postures. Units with high attractiveness and high strength get investment and growth, and so do the two cells next to that corner. Units along the diagonal get selective investment and are run for earnings. Units with low attractiveness and low strength are harvested for cash, sold or closed.

It grew out of McKinsey's work for General Electric in the early 1970s, after the BCG growth-share matrix, which uses only one measure per axis. The grid does not decide for you: the factors and weights are your judgment, and the result is only as good as the evidence behind each rating.

## When to use and when not to

Use it when a company has several business units, product lines or markets, and has to choose where to invest, which to run for cash and which to sell. Use it to compare candidate markets before entry: the attractiveness axis scores the market, the strength axis scores your ability to win in it. That is an adaptation: the canonical use is portfolio investment.

Inputs: a list of units that could each be sold and survive alone, a horizon (usually 3 to 5 years), and evidence about each unit's industry and its position against rivals.

Do not use it for one product in one market, or for a unit whose market cannot be defined: the score depends on how the market is drawn.

Limitations:

- **Weights and ratings are subjective.** Two teams can produce different grids for the same unit.
- **No proven link between the axes and returns.** Critics note that no study shows attractive industries and strong units pay off.
- **Synergies are ignored.** A unit that feeds another can look weak alone.
- **It does not say how much to invest.** It sorts units, and the amount is a separate decision.
- **Portfolio matrices can mislead.** In an experiment with the BCG matrix, 64% of 1,015 subjects who saw it chose the clearly worse investment (Armstrong and Brodie, 1994).
- **No source gives numeric cut-offs** for high, medium and low.

## Scheme

```
 attractiveness
 of the industry
  high    │ Selective │  Invest   │  Invest   │
          │           │   grow    │   grow    │
  medium  │  Harvest  │ Selective │  Invest   │
          │           │           │   grow    │
  low     │  Harvest  │  Harvest  │ Selective │
          └───────────┴───────────┴───────────┘
              low        medium       high
                  strength of the unit
```

Both axes grow from the bottom left. (Some drawings put high strength on the left; the cells are the same, mirrored.) Each unit is a circle: its area shows revenue, an arrow shows where it is expected to move. Next to the grid, list the factors, weights and ratings behind every placement.

## How to apply

1. **Fix the units and the decision.** Each unit must be sellable on its own. Split dissimilar segments. Name the horizon and the money at stake.
2. **Pick factors for each axis.** Take no more than 10 per axis; 5 to 7 is usually enough. The full list of variants is in [factors.md](factors.md). Attractiveness factors describe the market and are the same for every player. Strength factors describe the unit against rivals. A factor sits on one axis only, and overlapping factors are merged.
3. **Set weights before scoring.** The decision maker sets them from their expertise; they sum to 100% on each axis. Write why the top factors weigh most.
4. **Write a scale.** Use 1 to 5 or 0 to 10, with a one-line meaning of the lowest, middle and highest score for every factor. A higher score is always better for the unit: "few competitors" or "low external risk" scores high.
5. **Rate each unit.** Hard market data is not required: weights and ratings are the method. Note the basis of each rating, a fact or a judgment.
6. **Add up.** Per axis, sum weight times rating.
7. **Fix the cut-offs before looking at results.** One choice is thirds of the scale (on 1 to 5: up to 2.33 low, up to 3.67 medium). Another is to round each total to a whole number and use bands on 0 to 10: 0 to 3 low, 4 to 7 medium, 8 to 10 high. Both are conventions; no source sets them.
8. **Place and read.** Plot the units, add arrows for expected movement, read the posture of each cell.
9. **Test the weights.** Shift each weight by a few points. If a unit changes zone, say that the placement is not stable.
10. **Decide.** Tie each posture to a budget and a date to revisit, quarterly or twice a year.

## Example

eBay at the end of 2019, with three reportable segments. In its 10-K for 2019, eBay announced "a strategic review of our asset portfolio" and the sale of StubHub. eBay did not use this matrix: the scoring below is ours, with five factors per axis, ratings of 1 to 5 and thirds as cut-offs.

| Segment | Revenue 2019 | Operating income 2019 | Attractiveness | Strength | Zone |
|---|---|---|---|---|---|
| Marketplace | $8,638 M (2018: $8,641 M) | $2,814 M | 3.15 medium | 3.80 high | Invest, grow |
| Classifieds | $1,061 M (2018: $1,022 M) | $420 M | 3.40 medium | 3.55 medium | Selective |
| StubHub | $1,121 M (2018: $1,083 M) | $139 M | 2.25 low | 2.65 medium | Harvest, divest |

Decisions: eBay sold StubHub to viagogo for $4.05 billion in cash (agreed 24 November 2019), which fits the grid. It also sold Classifieds to Adevinta for $2.5 billion plus about 540 million shares, valued at about $9.2 billion (agreed July 2020), which the grid does not predict: Classifieds had the highest margin, about 40%. The grid ignores the price and the buyer's synergies; Adevinta expected $150 to 185 million of run-rate EBITDA from the deal.

What the case lacks: the company never used the matrix, and public estimates of the ticket resale market differ several times over by report and scope, so the market ratings are judgments. Most ratings are our judgment; the full scoring is in `example.json`.

Sources: [eBay 10-K 2019](https://www.sec.gov/Archives/edgar/data/1065088/000106508820000006/ebay201910-k.htm), [segment table](https://www.sec.gov/Archives/edgar/data/1065088/000106508820000006/R12.htm), [eBay results Q4 2019](https://www.ebayinc.com/stories/news/ebay-inc-reports-fourth-quarter-and-full-year-2019-results/), [Adevinta announcement](https://adevinta.com/press-releases/adevinta-asa-ade-adevinta-signs-agreement-to-acquire-ebay-classifieds-group-creating-the-worlds-largest-online-classifieds-group-with-an-extensive-footprint-and-leading-marketplace-brand/).

## Common mistakes

- **Rating the whole company.** One cell for a group of unrelated businesses hides winners and losers.
- **Counting a factor on both axes.** The company's own market share is strength, not attractiveness.
- **Too many overlapping factors.** Fifteen factors that repeat one another turn weights into noise.
- **Setting weights after seeing the result.** The weights then defend a conclusion already chosen.
- **Equating attractiveness with growth.** Margins, capital needs and buyer power matter as much.
- **Scales that point different ways.** "Many competitors" rated high on one factor and "good brand" on another mixes good and bad in one sum.
- **Ratings with no stated basis.** Politics then decides the score.
- **Reading the cell as a verdict.** The grid ignores price, synergies and how much to invest.
- **Never revisiting.** Ratings go stale within a year or two.

## Source

McKinsey & Company, Kevin Coyne, ["Enduring Ideas: The GE–McKinsey nine-box matrix"](https://www.mckinsey.com/capabilities/strategy-and-corporate-finance/our-insights/enduring-ideas-the-ge-and-mckinsey-nine-box-matrix), McKinsey Quarterly, 1 September 2008: the matrix appeared in the early 1970s after the BCG matrix; two axes, industry attractiveness and competitive strength; three postures. The page lists no factors, weights or cut-offs.

Procedure and discussion: A. C. Hax and N. S. Majluf, "The Use of the Industry Attractiveness-Business Strength Matrix in Strategic Planning", Interfaces 13(2), 1983, pp. 54-71 (INFORMS; text not opened). Original GE planning: M. G. Allen, "Diagramming GE's Planning for What's Watt", Planning Review, 1977 (text not opened). Effect on decisions: J. S. Armstrong and R. J. Brodie, ["Effects of portfolio planning methods on decision making: experimental results"](https://repository.upenn.edu/marketing_papers/15), International Journal of Research in Marketing 11(1), 1994 (BCG matrix, not this one; abstract only).

## See also

- Alternative to BCG Matrix: Two axes with one measure each; this one uses weighted factors and a middle level.
- Alternative to ADL Matrix: Crosses industry stage with position; this one scores attractiveness and strength.
- Preceded by Porter's Five Forces: Rate the industry profitability and rivalry factors of the attractiveness axis.
- Preceded by PESTEL Analysis: Supplies the external risk and regulation factors.
- Followed by Ansoff Matrix: After choosing units to grow, pick the growth direction.
- Followed by Unit Economics: Check that a unit chosen for investment pays back.
