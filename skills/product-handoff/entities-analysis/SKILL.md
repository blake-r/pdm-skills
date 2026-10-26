---
name: entities-analysis
description: Build or review an entity model of a product domain - the main business objects (entities) with their attributes, the relations between them (association, generalization, composition, aggregation) with multiplicity on both ends, and the business rules behind the multiplicities - drawn as a UML-style class diagram, and produce a one-slide PPTX; or review an existing domain model, ER diagram or class diagram. Use when a product has complex business logic (money, orders, refunds, roles), when the team mixes up terms, or when a decision depends on what is linked to what.
---

# Entities Analysis

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings requirements, scenarios or a description of the domain to model, **review** when the user brings a finished model or diagram.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- what the product does and what decision or conversation the model is for;
- the requirements, scenarios or a description of how the business works, in the business's own words;
- the rules that limit the objects ("one ledger per shop", "an order has at least one line");
- any existing database schema or API objects, as a cross-check only.

Do not invent entities, attributes, multiplicities or rules. If the product has only a couple of objects, say a model would restate the obvious.

### 2. Find entities

- Take the nouns from the requirements and conversations as candidates. Merge synonyms under one name, move properties into attributes, and separate value objects (an address, an amount of money) from entities that keep their identity over time.
- Use the business's names. Flag any name that means different things to different people, and any concept called by two names.
- Where the boundary between an entity and a relation is unclear, say so and choose by the task at hand.

### 3. Relations, multiplicity, attributes

- Draw only the relations the business must remember between events; name each with a verb or the key it goes through.
- Put multiplicity on both ends and write the rule behind it. If the rule is unknown, mark the end "?" and list it as a question; do not guess.
- Use composition only when the part lives and dies with the whole; use generalization only for a true "is a kind of". Avoid aggregation, or explain what it means.
- Add only the attributes the requirements need. Table names, technical columns and indexes belong to a schema, not to the model.
- Check the model against each scenario: can it answer the scenario's questions? Every "?" end is a question for the business, not a guess.
- Say what the model decides: the terms the requirements must use, and what is stored and changed together. Say the model is a sketch for a conversation with the business and is updated as the team learns.

### 4. Show, then write

Show in chat first: the entities and attributes, the relations with multiplicities and rules, the open questions. Write a file only after the user confirms. Ask for the output path (default `entities-<topic>.pptx` in the working directory). Save the data as JSON (the example is the Etsy case from card.md; the source diagram shows keys as attributes and gives multiplicity in words only for "a payment has many ShopPayments" (written `0..*`), so the "1" ends follow from a single foreign key and every other end is "?"; the links from the two transaction types to PaymentAdjustment are not drawn, and are noted in the rules instead):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Etsy: payment model before sharding, 2020–2022",
    "e1": "Payments", "a1": ["payment_id"],
    "e2": "ShopPayments", "a2": ["shop_payment_id", "payment_id", "shop_id"],
    "e3": "PaymentFee", "a3": ["payment_fee_id", "payment_id"],
    "e4": "PaymentAdjustment", "a4": ["payment_adjustment_id", "payment_id"],
    "e5": "PaymentAdjustmentItem", "a5": ["payment_adjustment_item_id", "payment_adjustment_id"],
    "e6": "CreditCardTransaction", "a6": ["reference_id", "transaction_type"],
    "e7": "PayPalTransaction", "a7": ["reference_id", "transaction_type"],
    "r1": "by payment_id", "m1a": "0..*", "m1b": "1",
    "r2": "by payment_id", "m2a": "?", "m2b": "1",
    "r3": "by payment_id", "m3a": "1", "m3b": "?",
    "r4": "by reference_id", "m4a": "?", "m4b": "?",
    "r5": "by reference_id", "m5a": "?", "m5b": "?",
    "r6": "by adjustment_id", "m6a": "?", "m6b": "1",
    "rules": ["Payment has many ShopPayments per shop_id", "Transactions also reference adjustments", "Decision: shard by existing keys", "Project result: main DB load −60%", "? — not in source; 1 — from foreign key"]
  }
}
```

The slide has seven entity slots: `e1` is the central one; `e2` sits above it, `e4` below, `e3` to the left, `e7` to the right, `e6` top right and `e5` bottom left. The six relations are fixed: `r1` e2–e1, `r2` e3–e1, `r3` e1–e4, `r4` e6–e1, `r5` e1–e7, `r6` e5–e4; `m<n>a` is the multiplicity at the first named end and `m<n>b` at the second. Every line is drawn as a plain association; write any other type in the relation label ("composition: …"). Leave unused slots and relations as empty strings and say which; with more than seven entities, split the model by area into several slides. The title takes under 60 characters; each `e` under 26; each `a` up to four items of under 32; each `r` under 24; each `m` under 6; `rules` up to five items of under 45; each list item becomes its own paragraph. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/entities-analysis.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's model in any form and check it against the common mistakes in card.md:

1. It describes business concepts, not database tables and technical fields.
2. Every name means one thing, and each concept has one name.
3. Every relation has multiplicity on both ends, with the rule behind it.
4. Aggregation, if used, is explained; composition and generalization are used only where they hold.
5. Entities were found from the domain, not stamped out by a fixed template of classes.
6. The model uses the business's language and was discussed with the business, not drawn only for developers.

Report findings as a numbered list: what is wrong, why it misleads the team, the concrete fix. End with a verdict: "model supports the decisions", "supports them after fixes" or "not enough data".
