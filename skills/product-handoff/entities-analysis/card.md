# Entities Analysis

## Essence

Entities analysis is a description of a product's domain through its main objects, their attributes and the relations between them. An entity is something that can be told apart from others and that changes over time while remaining itself: an order, a shop, a payment. An attribute is a property: an amount, a date, a status. A relation is how objects relate to each other.

Peter Chen proposed the entity-relationship model in 1976; it can also be drawn as a UML class diagram, where UML is the Unified Modeling Language. Eric Evans ("Domain-Driven Design", 2003) separated entities, which are distinguished by identity, from value objects, which are distinguished only by their attributes: an address, an amount.

Types of relations in UML:

1. **Association:** the objects are linked: a buyer places an order.
2. **Generalization:** one entity is a kind of another: card payment is a kind of payment.
3. **Composition:** a part lives and is deleted together with the whole: an order line and an order.
4. **Aggregation:** a "whole–part" link without a strict meaning.

Each end of a relation has a multiplicity, the number of objects on that side: `1`, `0..1`, `0..*`, `1..*`.

## When to use and when not to

Use it when the product has complex business logic — money, orders, refunds, roles — when the team gets confused by terms, or when a decision depends on what is linked to what.

Do not use it if there are only a couple of objects: the model will restate the obvious.

Limits:

- **The boundary is conditional.** Chen noted that some would consider a marriage an entity, others a relation. The modeler decides, based on their own tasks.
- **It is not a database schema.** The model describes business concepts, not tables and fields. The schema is derived from it later.
- **Completeness hurts clarity.** Martin Fowler: a sketch is valuable for its selectivity. Show what the conversation needs, not everything.

## Scheme

```
┌──────────────┐ 1      0..* ┌──────────────┐
│   Entity A   │─────────────│   Entity B   │
│  attributes  │ association │  attributes  │
└──────◆───────┘             └──────△───────┘
       │ composition                │ generalization
┌──────┴───────┐             ┌──────┴───────┐
│   Entity C   │             │   Entity D   │
└──────────────┘             └──────────────┘
Rules behind multiplicities · what was decided about the model
```

## How to apply

1. **List the nouns** from the requirements, scenarios and conversations with the business — these are the candidate entities.
2. **Filter out the excess:** merge synonyms under one name, move properties into attributes, separate value objects.
3. **Draw the relations** the business needs to remember between events, and name each with a verb.
4. **Set the multiplicity** at both ends of each relation and write down the rule behind it.
5. **Add attributes** needed for the requirements — no more.
6. **Check against the scenarios:** does the model answer their questions? An end marked "?" is a question for the business, not a guess.
7. **Decide based on the model:** an agreed model sets the terms of the requirements and what to store and change together. Update it as new knowledge arrives.

## Example

Etsy, a marketplace for handmade and vintage goods, at the end of 2020 hit the ceiling of its payment databases: two of them ran on the most powerful Google Cloud tier.

| Stage | What was recorded |
|---|---|
| Seller ledger | root entity Ledger; rule "one ledger per shop" — the database was split into parts (sharded) by shop_id |
| Payment model | Payments at the centre; ShopPayments, PaymentFee, PaymentAdjustment reference it by payment_id; card and PayPal transactions — by reference_id to the payment and to the adjustment |
| Problem | a payment is linked to many ShopPayments with different shop_id: a shop key would spread one payment across many shards |
| Option 1 | rebuild the model: the old Payment, in essence a purchase, becomes Purchase; the new Payment groups everything about the payment |
| Option 2 | shard small hierarchies by the keys that already exist |

The team drew the current and possible models and checked them against the queries. Decision: option 2 — the rebuild would have required rewriting the core. Project result from December 2020 to May 2022: 23 tables, more than 40 billion rows, load on the main payment database down by 60%.

What the case lacks: this is a data-level model — attributes are reduced to keys, and multiplicity is spelled out in words only in places. The contribution of the model choice to the 60% has not been measured separately.

Case source: R. Rainne, A. Ciavolino, [“Scaling Etsy Payments with Vitess: Part 1 – The Data Model”](https://www.etsy.com/codeascraft/scaling-etsy-payments-with-vitess-part-1--the-data-model), Etsy Code as Craft, 22.02.2023 ([archived copy](https://web.archive.org/web/2025/https://www.etsy.com/codeascraft/scaling-etsy-payments-with-vitess-part-1--the-data-model)).

## Common mistakes

- **Database schema instead of a model.** Tables and service fields instead of business concepts.
- **One name — different concepts.** At Etsy the old name Payment actually meant a purchase; rebuilding the model would start with a renaming.
- **No multiplicities.** It is unclear whether an order may have no payment or several.
- **Aggregation without explanation.** Fowler, following Rumbaugh, calls it a "placebo": it has no standard meaning.
- **Mechanical model.** A set of classes per concept according to a template, without understanding the domain.
- **A model for developers only.** The business speaks in other words, and the translation loses meaning.

## Source

P. Chen, [“The Entity-Relationship Model — Toward a Unified View of Data”](https://www.csc.lsu.edu/~chen/pdf/erd-5-pages.pdf), ACM TODS, 1976; E. Evans, "Domain-Driven Design", 2003, and [DDD Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf), 2015; M. Fowler, [“Aggregation And Composition”](https://martinfowler.com/bliki/AggregationAndComposition.html) and [“Uml As Sketch”](https://martinfowler.com/bliki/UmlAsSketch.html), 2003; G. Dechamps, [“Model anti-patterns”](https://www.tripled.io/07/11/2017/model-anti-patterns/), 2017; V. Khorikov, [“Mechanical approach to domain modeling”](https://enterprisecraftsmanship.com/posts/mechanical-approach-to-domain-modeling/), 2016; OMG, [UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF), 2017, ch. 9 and 11.

## See also

- Followed by State Modelling: Once entities are defined, describe the states and transitions of one.
- Enhanced by Use Case: Use cases show how actors act, and the steps change these entities and relations.
