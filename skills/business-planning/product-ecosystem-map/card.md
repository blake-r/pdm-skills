# Product Ecosystem Map

## Essence

Product Ecosystem Map is a map of an ecosystem's products: each product is assigned a role, and each role has a key metric. An ecosystem in the Product Architecture Framework (PAF) is a portfolio of products on one platform with a unified consumer profile, between which there is "transfer value": a product becomes more useful because of data that another product has provided. The map makes it possible to treat the ecosystem as one business model.

## When to use and when not to

Use it when a company has several products for one consumer and must decide which to launch, which to close, and which to keep even though they are loss-making. Inputs: the products, their metrics, customer transitions, the platform.

Do not use it:

- for a set of products grouped by industry, without a common profile and data transfer: by the PAF definition these are separate products or a platform; showcase super apps are the same;
- for a single product: roles describe products relative to one another.

Limits:

- **A role is a position in the portfolio, not a property of the product.** A paid product is often both Value and Profit; allow two roles.
- **The method is the author's model.** PAF itself notes that there is little data on the bundle subscription (a set of products for one price).

## Scheme

| Role | Task | Key metric (PAF) |
|---|---|---|
| Lead Generators | attract and activate | conversion to activation |
| Value Generators | cover the core need of the audience | North Star Metric (value metric) |
| Profit Generators | earn on the core | average revenue per paying customer |
| Engagement Generators | engage through other needs | number of conversions per consumer per period |
| Upsale Generators | additional profit; customers do not come for them | average check |
| Retention Generators | retain customers | retention rate |
| Operational Efficiency Generators | automation | cost of operations |
| Platform | unified profile, transfer value | — |

Above the table: touchpoints (apps, entry points to the products).

## How to apply

1. **Describe the platform and the level of transfer value:** authorization data (a common login), transactional data (points between products), contextual data (one product's data saves steps in another).
2. **List the products and the needs they meet.**
3. **Assign roles by asking "why does the company need this product":** customers come for it — Value; it earns money for us — Profit; it brings new customers — Lead. A product without a role is a candidate for closure.
4. **Record the role's metric and its current value;** if there is no data, leave a gap.
5. **Draw the transfer value arrows:** which data goes from which product to which. No arrows means it is just a set of products.
6. **Check the balance:** no Lead — customers are brought only by advertising; no Profit — the core is not monetized; no Retention — customers leave.
7. **Decide product by product:** launch, close, or change the role. Keep a loss-making product if it raises an ecosystem metric.
8. **Judge by the customer:** share of wallet instead of market share, and the ecosystem's LTV (customer revenue over the whole relationship) instead of the product's LTV.

## Example

Tinkoff, Strategy Day, June 2018. Slide 13 "On-line customer-centric ecosystem": products around Retail and SME (small business) customers: loans, investments, payments; "Proprietary platform" and "Brokerage platform" are two labels for the delivery method of SME products. Slide 15, subtitle "How Tinkoff Black is involved into this story": by our reading, the column "gives % of share of new customers inflow" shows the share of new customer inflow to a product through Tinkoff Black, the debit card (selected): investments 80%, All Airlines 32%, cash loans 32%, insurance 31%, SME 30%. Tinkoff Journal — 3+ million MAU (monthly active users, slide 27); the app — 2.5+ million (slide 28); telesales in the cloud — 77% of activities (slide 33). Adopted (slide 12): from 2018, the Lifestyle Banking stage — a bank plus solutions for life (slide 11); examples are on slides 13 and 27.

Roles: Tinkoff Journal is Lead (stated directly in PAF; slide 27 shows it under its own name); the rest is our reconstruction from the general PAF examples: Black — Value, loans — Value and Profit, insurance — Upsale (assumption). What the case lacks: a role and metric map, a unified profile, data transfer between products (slide 15 shows cross-sales), and a decision to launch or close a product.

Case source: [Tinkoff Strategy Day, June 2018](http://finside.ru/wp-content/uploads/tinkoff-strategy-day-2018.pdf), slides 11, 12, 13, 15, 27, 28, 33.

## Common mistakes

- **An ecosystem in name only.** Industry showcases and super apps without a common profile do not generate transfer value.
- **A shared login taken as transfer value.** Authorization (Sber ID) only shortens registration; the benefit comes from transactions and context.
- **One role per product.** A debit card is Value; a credit card is Value and Profit.
- **Closing a "loss-maker" by default.** In an ecosystem one looks at the product's contribution to engagement and retention.
- **Roles without metrics.** A role without a metric and a value is a label, not management.
- **Hypotheses presented as facts.** PAF calls the answer about the bundle subscription a hypothesis, and gives the ecosystem's effects (CAC — customer acquisition cost, adoption — the share of those who adopted the product) without measurements.

## Source

Sergey Tikhomirov's model: [description in PAF](https://productframework.ru/product_ecosystem_map) (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, undated). According to PAF, the structure rests on the value chain: M. Porter, ["Competitive Advantage"](https://openlibrary.org/works/OL1827734W), Free Press, 1985. Note by the card's author, not from PAF: the term "business ecosystem" was introduced by J. F. Moore, ["Predators and Prey"](https://hbr.org/1993/05/predators-and-prey-a-new-ecology-of-competition), Harvard Business Review, May–June 1993.

## See also

- Enhanced by Value Chain & Nets: Show how the products link along the path to value for customers.
- Enhanced by YC Guide to Business Models: Take each product's key metric from its business model when assigning roles.
