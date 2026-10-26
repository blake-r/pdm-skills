# YC Guide to Business Models

## Essence

The YC Guide to Business Models is Y Combinator's cheat sheet: nine business models of tech companies and, for each, three to four key metrics. First determine how the product makes money, then take the metrics of that model and do not substitute other people's: a marketplace's GMV is not revenue, usage-based revenue is not recurring, and registered users of an advertising model are an empty number.

## When to use and when not to

Use it when you need to choose success metrics for a product or business line; when a company changes its model, for example moving from its own retail to a marketplace, and the old metrics stop describing the business; when you need to agree with investors or the team on which numbers to judge the direction by.

Do not use it as a complete set of metrics: the guide gives the top level, not the metrics of features and experiments. Do not use it until you have decided how to make money.

Limitations:

- **Nine models do not cover everything.** Lending, insurance and data sales are not on the list.
- **A company often lives in several models at once.** Metrics are then chosen for each direction separately.
- **The metrics are for a startup.** A mature company also needs profit, cash flow and risk measures.

## Scheme

| Model | How it earns | Key metrics |
|---|---|---|
| SaaS | cloud software on subscription, usually for businesses | MRR or ARR, growth rate, revenue retention, CAC |
| Transactional | takes a share of transactions, usually fintech and payments | GTV, net revenue from fees, user retention, CAC |
| Marketplaces | connects buyers and sellers | GMV, net revenue (take rate), growth rate, retention |
| Subscription | regular payments from consumers | MRR or ARR, growth rate, retention, CAC |
| Enterprise | large contracts with big companies | bookings (signed contract value), revenue, ACV, pipeline |
| Usage Based | payment per usage | monthly revenue, growth rate, revenue retention, gross margin |
| E-commerce | sells its own goods online | monthly revenue, growth rate, gross margin and unit economics, CAC |
| Advertising | sells advertising, users are free | DAU, MAU, retention by day, CPM or CPC |
| Hardtech / Bio / Moonshots | long technical risk | milestones, signed contracts, letters of intent |

MRR and ARR are recurring revenue per month and per year; GMV and GTV are the volume of sales and payments through the platform; take rate is the share of that volume the platform keeps; CAC is the cost of acquiring a customer; ACV is the annual contract value; bookings are the total signed contract value; pipeline is the deals at each funnel stage.

## How to apply

1. **Split the business into directions** that earn money in different ways.
2. **Choose a model for each** from the nine; if none fits, name your own and explain it.
3. **Take the key metrics of the model** and write down their exact definitions: what is included and what is not.
4. **Check for substitutions:** platform volume is not passed off as revenue, one-off revenue is not passed off as recurring.
5. **Revisit the metrics when the model changes,** and notify those who track the numbers.

## Example

Kaspi.kz is a Kazakhstan-based company with three platforms. In its 2023 20-F annual report, each platform has its own metrics, and they match the guide's models. The guide does not mention Kaspi: this is the same logic, not borrowing.

| Platform | Model per guide | Metric | 2022 | 2023 |
|---|---|---|---|---|
| Payments | Transactional | payment volume (TPV), KZT bn | 19,913 | 28,406 |
| Marketplace | Marketplaces | GMV, KZT bn | 2,872 | 4,161 |
| Marketplace | Marketplaces | take rate on third-party sellers' GMV | 8.2% | 9.2% |
| Fintech | not in the guide | loans issued, KZT bn | 5,411 | 7,930 |

Decision: in February 2023, after acquiring 90.01% of Magnum E-commerce Kazakhstan, Kaspi moved its e-Grocery grocery delivery from the marketplace model (third-party sellers) to its own sales — "due to the more complex operational and logistical requirements of the grocery business". The metrics changed along with the model: the report added retail revenue, GMV of own sales is shown separately, and the take rate is calculated only on third-party sellers' GMV. The risk section warns that the grocery business has low profit margins.

Result: e-Grocery GMV grew 254%, from KZT 19.4 bn to 68.7 bn; purchases reached 5.2 million against 1.6 million. e-Grocery retail revenue was KZT 58.4 bn. Marketplace net income grew 63%, but by our calculation its share of segment revenue fell from 64% to 55%: delivery costs grew faster than revenue.

Source of the case: Kaspi.kz, [2023 annual report on Form 20-F](https://www.sec.gov/Archives/edgar/data/1985487/000095017024049512/kspi-20231231.htm).

## Common mistakes

- **GMV instead of revenue.** A platform reports sales volume, but earns only its commission.
- **One-off revenue presented as MRR.** Usage-based payments or one-time services are presented as recurring.
- **One model for the whole company.** A platform, payments and own retail are measured with the same numbers.
- **Empty metrics.** Registered users instead of active ones.
- **The model changed, the metrics did not.** A switch to own sales, while the margin is not tracked.

## Source

Aaron Epstein, Y Combinator, [«YC guide to business models»](https://www.ycombinator.com/library/Gh-yc-guide-to-business-models), YC library, and the Startup School video [«Business Models and Pricing»](https://www.youtube.com/watch?v=oWZbWzAyHAE). An earlier lecture on the same nine models: Anu Hariharan, «Nine Business Models and the Metrics Investors Want», Startup School, 2019 ([recap](https://blog.ycombinator.com/startup-school-week-3-recap-anu-hariharan-and-adora-cheung)).

## See also

- Enhanced by Metric Pyramid: Take the top-level metrics from the YC guide as the pyramid root.
- Enhanced by AARRR Metrics: Read the funnel stages against each business model's key metrics.
- Followed by Unit Economics: After choosing metrics, calculate CAC and unit contribution to test the model.
- Enhanced by Product Ecosystem Map: Use this guide's model metrics as the key metrics when assigning product roles.
