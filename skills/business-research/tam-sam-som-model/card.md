# TAM / SAM / SOM Model

## Essence

TAM / SAM / SOM is a way to estimate a market's size in three steps, from all demand down to the part the company can really capture. On the diagram these are three nested circles:

- **TAM (Total Addressable Market)** — the whole market: everyone who has the problem the product solves, and how much they spend on it or how many times they solve it.
- **SAM (Serviceable Available Market)** — the available market: the part the product can serve with its model — geography, segments, channels.
- **SOM (Serviceable Obtainable Market)** — the obtainable share: how much of the available market the company can take within a given period, given its resources and competitors.

The size is counted in money or in units — purchases, trips, payments. The main thing is one unit across all three levels.

## When to use and when not to

Use it when you need to decide whether to enter a market; when you prepare an investment or budget request and must show where the revenue will come from; when you choose which segment or country to start with.

Do not use it as a sales forecast: SOM is a benchmark, not a plan. In a market that the product is only creating, TAM cannot be confirmed by anything except indirect data, and its error is large.

Limitations:

- **The circles are easy to inflate.** TAM counted as "all people with a wallet" says nothing about demand.
- **The two counting methods give different answers.** Top-down, from industry statistics; bottom-up, from the number of customers and the average check. If the results differ several times over, the error is in the assumptions.
- **SOM depends on the period.** Without a date, the market share cannot be checked.

## Scheme

```
┌───────────────── TAM: whole market ─────────────────┐
│   ┌───────── SAM: serviceable market ─────────┐     │
│   │     ┌──── SOM: obtainable share ────┐     │     │
│   │     │  how much we take in the term │     │     │
│   │     └───────────────────────────────┘     │     │
│   └───────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

Next to the circles, write who falls into each level, how it is calculated and where the data comes from.

## How to apply

1. **Define the unit:** money per year, or the number of purchases, trips, payments.
2. **Calculate TAM:** everyone who has the problem, from industry statistics or from the number of potential customers multiplied by their spending.
3. **Narrow down to SAM:** remove the countries, segments and channels the product does not serve.
4. **Estimate SOM:** what share of SAM can realistically be obtained within the period — based on the pace of customer acquisition, the budget and competitors' shares.
5. **Check bottom-up:** customers × frequency × average check should converge with SOM.
6. **Compare SOM with the goal** — the revenue plan or the amount you are asking for. If SOM over the period is below the goal, look for another segment, channel or period, or drop the market. If it is above but not backed by a pace of customer acquisition, do not promise it as a plan.
7. **Record the sources and assumptions** and recalculate when actual sales appear.

## Example

Airbnb, then AirBed&Breakfast, put together its first investor presentation in 2008–2009. The "Market Size" slide — three circles in trips:

| Level | How it was labeled on the slide | Size |
|---|---|---|
| TAM | all trips booked worldwide (Total Available Market) | more than 1.9 billion |
| SAM | budget and online trips (Serviceable Available Market) | 532 million |
| SOM | trips via AirBed&Breakfast (Share of Market) | 10.6 million |

The next slide translated SOM into money: a 10% commission, on average $20 per trip ($70 per night, three nights), a total of $200 million in revenue for 2008–2011.

Decision: with this presentation the founders looked for their first round. In April 2009 Sequoia Capital invested $585 thousand, when the site had 2,500 listings and 10 thousand registered users.

Result: by February 2011, 1 million nights had been booked through Airbnb in total. By the presentation's own assumption (three nights per trip), that is about 330 thousand trips — more than thirty times less than the SOM for that period. The obtainable share, calculated without a pace of customer acquisition, turned out to be overstated for this period.

Case sources: Business Insider, [photos of the presentation slides](https://www.businessinsider.com/airbnb-a-13-billion-dollar-startups-first-ever-pitch-deck-2011-9) (2011, updated 2019); Sequoia, [«Airbnb IPO: Embracing the Adventure»](https://sequoiacap.com/article/airbnb-ipo-embracing-the-adventure/) (2020); Airbnb, [press release on one million nights](http://assets.airbnb.com/press/press-releases/Airbnb_1M_Nights_Booked_Press_Release.pdf) (24 February 2011).

## Common mistakes

- **TAM without boundaries.** The market includes everyone who could theoretically buy, not only those who have the problem.
- **Different units across levels.** TAM in money, SAM in customers — the circles cannot be compared.
- **SOM as a percentage of a ceiling.** "We will take 1% of the market" with no calculation of customer acquisition.
- **No period and no sources.** The estimate cannot be checked or updated.

## Source

The model has no single author. The division into total and available market is described, for example, by Steve Blank and Bob Dorf in «The Startup Owner's Manual», K & S Ranch, 2012. The third level, SOM, reflects competition: the company will get only part of the available market. The definitions of the three levels are summarized in the Wikipedia article [«Total addressable market»](https://en.wikipedia.org/wiki/Total_addressable_market).

## See also

- Preceded by Segment Scoring: the chosen segment sets the boundaries of SAM.
- Enhanced by Unit Economics: the bottom-up check (customers × average check) can use per-customer figures from unit economics.
- Enhanced by Sales Funnel: funnel conversion rates set the acquisition pace that limits SOM.
- Followed by Financial Modeling: compare SOM with the revenue goal inside a financial model with scenarios.
