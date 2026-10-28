# RFM Analysis

## Essence

RFM analysis divides customers into segments by three features of purchasing behavior: recency of the last purchase (Recency), purchase frequency (Frequency) and purchase amount (Monetary). Each customer receives a score on each feature; the combination of scores defines the segment. For each segment a separate communication scenario is chosen: whom to retain, whom to wake up, whom to win back, and whom not to spend the budget on.

## When to use and when not to

Use it when there is purchase history for at least one or two purchase cycles and a channel through which segments can be addressed differently: newsletters, push notifications, a loyalty program, calls from a manager. Typical tasks are reactivating "sleeping" customers, retaining the most valuable ones, and limiting discounts to those who would have bought anyway.

Inputs: for each customer — the date of the last purchase, the number of orders and the purchase amount for the analysis period.

Limits:

- **It looks only at the past.** RFM describes behavior but does not explain its causes or predict the reaction to an offer.
- **Not suitable for rare purchases.** If a customer buys once every few years (an apartment, a car), recency and frequency barely distinguish customers.
- **Segments are not a result.** Value appears only when different actions are run for the segments and their effect is measured.

## Scheme

Each feature is divided into levels, usually 3 or 5; here level 3 is the best. In some sources, for example Mindbox, the best is level 1: check the direction of the scale before comparing codes. Combinations give a cube of 27 (3 × 3 × 3) or 125 cells. In practice the slice "recency × frequency" is looked at more often, and the amount is used inside the cell.

| | Frequent (F = 3) | Medium (F = 2) | One-time (F = 1) |
|---|---|---|---|
| **Recent (R = 3)** | retain, privileges | novelties, complementary products | second purchase |
| **Sleeping (R = 2)** | personal offer | reminder | selection |
| **Churning (R = 1)** | find the cause, win back | promo code | do not spend budget |

## How to apply

1. **Choose the analysis period** and the calculation date. The period should contain several purchase cycles.
2. **Compute R, F and M** for each customer: days since the last purchase, number of orders, amount.
3. **Set the level boundaries.** Either by business logic (for example, R = 3 — a purchase no older than 30 days), or by dividing customers into equal groups; for frequency this often does not work, since most customers have one order.
4. **Assign scores and segments.** Put the number of customers and revenue into a "recency × frequency" table.
5. **Interpret.** Where revenue is concentrated, what share of valuable customers is already "sleeping", how many one-time buyers never came back.
6. **Assign an action to each segment** and a goal for it: win back, raise frequency, retain.
7. **Check the effect on a control group:** part of the segment receives no messages; the difference in revenue shows the added effect.

## Example

Seedspost is an online store of seeds and seedlings with a mailing base of 397 thousand customers. The store divided customers into 9 segments by recency and frequency of purchases:

| | 4+ orders | 2–3 orders | 1 order |
|---|---|---|---|
| **Bought recently** | recent, frequent | recent, medium | recent, one-time |
| **"Sleeping"** | sleeping, frequent: promo code | sleeping, medium | sleeping, one-time |
| **Churning** | churning, frequent | churning, medium | churning, one-time |

The scenarios for the other eight segments are not disclosed in the sources.

Decision: Seedspost runs email and SMS scenarios (13 visual scenarios and 39 triggers in total) built on these segments. In the RFM review by Mindbox the segment "sleeping, used to buy often" gets an email or SMS with a promo code. To check the effect, 5% of customers who meet the mailing conditions are excluded from the recipients: the control group was connected in April 2021 and gave a statistically reliable result (99% confidence) from September 2021. It showed that about a fifth of the store's revenue is added by newsletters; after moving to the new platform the newsletters' share of revenue grew from 10% to 22.5%. These results apply to all newsletters, not only to RFM scenarios. The sources do not publish the other scenarios, the recency boundaries or the segment sizes; only the 4+ and 2–3 order boundaries are given, and the grid cell names are a reconstruction.

Sources of the case: [Mindbox, Seedspost story (2022)](https://mindbox.ru/journal/cases/seedspost/); example of a message for a segment — [Mindbox, "RFM analysis" (2026)](https://mindbox.ru/journal/education/chto-takoe-rfm-analiz/).

## Common mistakes

- **Boundaries unrelated to the purchase cycle.** "Recent" for food delivery and for furniture are different timeframes.
- **Discounts for all "sleeping" customers.** Some frequent buyers would have returned without a discount; without a control group this is not visible, and the discount eats the margin.
- **Amount instead of frequency.** One large purchase makes a one-time customer "valuable", although there may be no repeat purchase.
- **A one-off calculation.** Customers move between segments every week; scores are recalculated regularly and automatically.
- **No control group.** A growth in a segment's revenue after a newsletter may be seasonal.

## Source

The method has no single author: it came from direct-mail catalog retail practice. Arthur M. Hughes described it in the book [«Strategic Database Marketing»](https://openlibrary.org/books/OL1182563M) (1994); the usual form of the method has five levels per attribute and 125 cells. In Mindbox's description the scale runs the other way: 1 is the best on each attribute.

## See also

- Enhanced by Cohort Analysis: Pair the segments with retention curves by acquisition date.
- Alternative to ABCDX Segmentation: ABCDX segments paying customers by product need; RFM by purchase behaviour.
- Enhanced by A/B Testing: Hold out a control group in the segment and compare revenue of both groups.
- Enhanced by ABC Analysis: Rank customers by revenue with ABC, then check A-class recency and frequency with RFM.
