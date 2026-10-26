# BCG Matrix

## Essence

The BCG Matrix, the "growth — share" matrix, is a way to assess a company's portfolio of products or directions: how much money each one brings in or absorbs. Each direction is placed on a grid along two axes: the growth rate of its market and its relative market share — the direction's share divided by the share of the largest competitor. The size of the circle is the direction's revenue.

| | High relative share | Low relative share |
|---|---|---|
| **Fast market growth** | Stars: leaders of a growing market, they pay for themselves | Question marks: require more money than they bring in |
| **Slow market growth** | Cash cows: generate money beyond what is needed to hold share | Dogs: profit goes to holding share, no money is left |

Bruce Henderson's logic: the cash cows' money goes to the stars and to those question marks that can become leaders; the other question marks and the dogs are sold or closed. Over time, each direction becomes either a cash cow or a dog.

## When to use and when not to

There are two uses of the matrix.

- **Portfolio (the canon).** Use it when a company has several products, markets or directions and needs to decide where to put money and what to exit; when one direction feeds the others. The decision is about cash: fund, hold, take cash, exit.
- **Competitive comparison.** Put your products and the competitors' products of one market on the same grid to see who leads where, and where the market is growing. The decision is about where to attack and where to defend, not about cash, because a competitor's cash is not visible from outside. Use it when the market is defined and the same market can be measured for every player.

Do not use it for a single product in a single market, nor for a market where the players cannot be defined and measured: the position of a circle depends on how the market is drawn.

Limitations:

- **Two axes are not everything.** Synergy between directions, profitability and risks are not visible on the grid.
- **Competitor positions are estimates.** Companies rarely publish share and growth by product. In the comparison use, the relative share is the estimate most likely to be wrong, and it is the one the placement depends on.
- **The boundaries are conditional.** Henderson did not set them as numbers. Share is naturally divided at 1.0: above it, you are the market leader. The growth boundary is chosen by you, for example based on the average growth of the economy or the industry.
- **Phases have become shorter.** BCG's 2014 analysis: in the industries where businesses moved between quadrants faster, the later part of the life cycle (the cash cow phase) shortened by 55% on average.

## Scheme

```
  market growth
     ▲
     │  Stars          │  Question marks
     │  hold           │  invest
     │                 │  or exit
 10% ├─────────────────┼─────────────────
     │  Cash cows      │  Dogs
     │  take cash      │  exit
     │                 │
     └─────────────────┴─────────────────
    10×               1×             0.1×
       ◀ relative share (log scale)
```

As in BCG's original, high share is on the left.

## How to apply

1. **Split the business into directions:** product, country, segment.
2. **Define the market of each** and find its growth and shares: your own and the largest competitor's.
3. **Place the directions on the grid:** share on the horizontal axis in a logarithmic scale, growth on the vertical, circle size is revenue.
4. **Decide for each:** hold the stars, take cash from the cash cows, among the question marks choose whom to fund to leadership, sell or close the dogs.
5. **Check the balance:** whether the cows' money is enough for the chosen moves.

**In the competitive comparison** the steps change as follows. Take one market and list the players that sell there, your products and the competitors' main products. Compute each product's relative share against the market leader, and the market growth once for the whole market. Use one revenue measure for all circles (for example, the market's revenue per product, or the size of its user base if revenue is not published) and say which one in `scales`. Then read the grid as a map of attacks: a competitor's star is a threat to hold against, your question mark next to a competitor's cash cow is an attack candidate, and your dog next to a competitor's star is a line to give up on or to defend.

## Example

Sea Limited is a Singapore-based group: Garena games, Shopee e-commerce, SeaMoney fintech. In 2021 Garena earned $2.8 billion of adjusted EBITDA — profit before interest, taxes and amortization — with $4.6 billion in bookings, while Shopee lost $2.6 billion. Sea did not use the matrix or its terms and did not publish market shares by direction: the breakdown below is ours.

| Direction, end of 2021 | What is known | Quadrant per our assessment |
|---|---|---|
| Garena | the group's main profit; bookings are falling | cash cow |
| Shopee in Southeast Asia and Taiwan | according to Sea, the largest platform in the region | star |
| Shopee in France, Poland, Latin America | launched in 2021; Allegro is the leader in Poland | question marks |
| SeaMoney | revenue growing, loss-making | question mark |

Decision: in 2022 Shopee exited France (March) and scaled back Latin America, except Brazil (September) — "to concentrate resources on core markets" — and in January 2023 it closed in Poland. In November 2022 Forrest Li, Sea's head, announced: "we have entirely shifted our mindset and focus from growth to achieving self-sufficiency and profitability as soon as possible, without relying on any external funding."

Result: in Q4 2022 Shopee's adjusted EBITDA turned positive — $196.1 million against −$877.7 million a year earlier; Asia contributed +$320 million, the other markets −$123.9 million. For 2023 Sea posted its first annual net profit, $162.7 million, against a loss of $1.7 billion. Meanwhile the cash cow shrank: Garena's bookings were $4.6, $2.8 and $1.8 billion for 2021–2023.

Sources of the case: Sea press releases on results for [Q3 2022](https://www.sec.gov/Archives/edgar/data/1703399/000110465922119122/tm2230567d1_ex99-1.htm), [Q4 and full-year 2022](https://www.sec.gov/Archives/edgar/data/1703399/000110465923029545/tm238717d1_ex99-1.htm), [2023](https://www.sec.gov/Archives/edgar/data/1703399/000110465924030484/tm247857d1_ex99-1.htm); [2022 annual report on Form 20-F](https://www.sec.gov/Archives/edgar/data/1703399/000114036123017021/brhc10050860_20f.htm); Bloomberg on the exits from [France](https://www.businessoffashion.com/news/global-markets/seas-shopee-exits-france-just-months-after-europe-foray/) and [Latin America](https://www.bloomberglinea.com/english/shopee-says-adios-to-argentina-in-latin-america-retreat/); Trans.info on the [exit from Poland](https://trans.info/en/shopee-poland-departure-321341).

## Common mistakes

- **The market is drawn to fit the desired answer.** A narrow market makes any direction a leader.
- **Absolute share instead of relative.** 20% of a market is leadership in a fragmented market and lagging behind a leader with 60%.
- **Keeping a dog for accounting profit,** although all of it goes to holding share.
- **Funding all question marks a little.** None of them becomes a leader.
- **Treating a cash cow as permanent:** its money is built into the plan without checking how fast its market is declining.
- **Comparing products from different markets on one grid.** Each market has its own leader and growth; the same share means different things in each. Compare within one market.
- **Using a competitor's star as your own plan.** A competitor's leadership in its segment does not say what it will do next, and the matrix gives no reason to copy it.

## Source

Bruce D. Henderson, [«The Product Portfolio»](https://www.bcg.com/publications/1970/strategy-the-product-portfolio), BCG, 1970; Henderson called the dogs "pets". How BCG revisited the matrix 44 years later: M. Reeves, S. Moose, T. Venema, [«BCG Classics Revisited: The Growth Share Matrix»](https://www.bcg.com/publications/2014/growth-share-matrix-bcg-classics-revisited), 2014.

## See also

- Alternative to ADL Matrix: Use BCG when only market growth and relative share matter.
- Enhanced by Product Lifecycle: Mark each product stage first, so a maturing cash cow is not called permanent.
- Preceded by Competition Map: Use the competition map's shares to set each product's relative share.
