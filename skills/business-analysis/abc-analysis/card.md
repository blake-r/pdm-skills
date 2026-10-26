# ABC Analysis

## Essence

ABC Analysis is a way to split homogeneous objects into three classes by their contribution to a total result. The objects can be products, customers, sellers or features. The result is revenue, profit or units sold. Objects are ranked by contribution in descending order and the cumulative share is calculated. Class A is the few objects that deliver the main part of the result. Class B is the middle. Class C is the long tail of many objects with a small contribution.

The point is not the table itself but managing the classes differently. A gets more attention and money: an accurate forecast, frequent control, the best service. C is run by simple rules and is rarely checked or removed.

## When to use and when not to

Use it when there are many objects, from dozens upward, and the contribution is distributed unevenly. When the resource — team time, money for stock, system capacity — is not enough to deal with everything equally. When you need to decide what to cut and what to protect.

Do not use it if there are only a few objects: they are easier to analyze one by one. It does not fit if the contribution is distributed almost evenly: the classes will be arbitrary.

Limitations:

- **One criterion.** A class C product by revenue may be needed as a reason for an order or as part of a set. This is visible only from other data.
- **The boundaries are conditional.** The APICS dictionary gives a guideline for inventory: class A — 10–20% of items and 50–70% of value in money, B — about 20% and 20%, C — 60–70% of items and 10–30% of value. The rule "20% of items give 80%" is a rounding, not a law.
- **A snapshot of the past.** New items and seasonal items fall into C until they accumulate sales.

## Scheme

```
 cumulative share
 of result
 100% ┤                    .........
      │           ....'''
  95% ┤ - - - - -'  - - - - - - - - - -
  80% ┤ - - - .'
      │     .'
      │   .'
      │  /
      │ /
   0% └───┬─────────┬──────────────────▶
       A  │    B    │        C        share of objects,
                                      in descending order of contribution
```

Class boundaries are drawn by the cumulative share of the result: for example, up to 80% — A, up to 95% — B, the rest — C.

## How to apply

1. **Choose the objects and the criterion:** what we rank, by which result, for which period.
2. **Collect the values** for each object from one source.
3. **Sort in descending order** and calculate the share of each object and the cumulative share.
4. **Split into classes** by the boundaries chosen in advance and look at how many objects and what share of the result is in each.
5. **Set rules for each class:** control frequency, service level, budget, removal.
6. **Recalculate regularly,** for example once a quarter: objects move between classes.

## Example

Instacart is an American grocery delivery service. For each product in each store, the service estimates the probability that the product is on the shelf and hides from the results what is most likely not there. There are hundreds of millions of products and more than 80 thousand stores.

Updating the estimates for all products at once, with full synchronization, was expensive and not necessary. The team noticed that the estimate changes more often for products that are searched or bought frequently, while for the others it almost stays still. Solution: different updating for the head and the tail.

| | Which products | How the estimate is updated |
|---|---|---|
| Head | often searched or bought | on demand: as soon as the product appears in search results and the estimate is stale |
| Tail | rarely searched, out of stock | full synchronization several times a day |

Result, according to the team: estimates for popular products began to update more often, and the ingestion load on the database dropped by two thirds.

What the case does not include: Instacart did not build a table with classes A, B and C and did not publish the shares of products and demand. The boundary between the head and the tail is set by the search itself: a product's estimate is updated when it appears in the results. This is the same logic as ABC Analysis — managing classes differently — but in a simplified form with two classes.

Source of the case: M. Prescott, [«Instacart's Item Availability Architecture: Solving for scale and consistency»](https://company.instacart.com/tech-innovation/instacarts-item-availability-architecture-solving-for-scale-and-consistency), Instacart tech blog, September 6, 2023.

## Common mistakes

- **A table without decisions.** The classes are calculated, but no rules are set for them: the work has not changed.
- **Cutting the tail wholesale.** Without checking which class C products are bought together with class A products.
- **Mixing different objects.** Products and services, different currencies or periods in one list.
- **Revenue instead of profit where margin matters.** A class A product by revenue may be unprofitable.
- **Not recalculating the classes.** A table a year old governs the current assortment.

## Source

H. Ford Dickie, «ABC Inventory Analysis Shoots for Dollars Not Pennies», Factory Management and Maintenance, 1951, — the first description of the method; reference via [an overview of inventory classification methods](https://www.ijraset.com/fileserve.php?FID=5680), IJRASET, 2016. The principle of "the few important and the many others" — Joseph Juran, [Juran Institute](https://www.juran.com/blog/a-guide-to-the-pareto-principle-80-20-rule-pareto-analysis/). Class boundaries — per the APICS dictionary definition, [quoted by Arkieva](https://blog.arkieva.com/abc-segmentation/).

## See also

- Enhanced by RFM Analysis: Rank customers by revenue with ABC, then check A-class recency and frequency with RFM.
- Enhanced by Segment Scoring: Use ABC to find objects that bring results, then score segments to pick a focus.
