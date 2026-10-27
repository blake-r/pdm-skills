# Sales Funnel

## Essence

The Sales Funnel is a model of a customer's movement toward a purchase as a sequence of stages: from first contact to payment. At each stage some people drop out, so the number of customers narrows from stage to stage. For each stage three numbers are calculated: how many customers reached it, what share moved on from the previous stage — the conversion — and how much time customers spend at it.

The funnel is needed to find the bottleneck — the transition where the most people or the most time is lost — and to change precisely that, rather than everything at once.

## When to use and when not to

Use it when the path to a purchase or to opening an account consists of several consecutive steps and there is data for each one: a loan application, sign-up in an app, checkout, a B2B deal. When overall conversion is low and it is unclear where customers are lost.

Do not use it if the path is nonlinear: customers return, skip steps, come from different channels — a single funnel then hides different scenarios. It does not fit if the stages are not recorded in the data: without events at each step, the numbers will be estimates.

Limitations:

- **The funnel shows where we lose people, but not why.** The reason is found in interviews, session recordings and analysis of rejections.
- **The person building the funnel sets the stages.** Stages that are too large hide the bottleneck inside themselves.
- **Compare customers of the same period.** If you add March applications to April payments, the conversion will be false.

## Scheme

```
 ┌──────────────────────────┐
 │ Stage 1: 5,000 customers │  entry        1 day
 └┐                        ┌┘
  │ Stage 2: 3,500         │  70%          3 days
  └┐                      ┌┘
   │ Stage 3: 1,500       │  43% ← bottle- 5 days
   └┐                    ┌┘       neck
    │ Stage 4: 800       │  53%          2 days
    └────────────────────┘
    customers at      conversion from    time at
    the stage         the previous       the stage
```

Numbers are illustrative.

## How to apply

1. **Describe the stages** from first contact to payment, so that each one is recorded by an event in the data.
2. **Choose a period** and take the customers who entered the funnel in that period.
3. **Calculate at each stage** the number of customers, the conversion from the previous stage, and the time at the stage.
4. **Find the bottleneck:** the transition with the largest loss of people or the longest wait, compared with past periods or similar products.
5. **Investigate the cause** and change that stage; leave the rest alone for now.
6. **Recalculate the funnel** after the change, on customers from the next period.

## Example

Monzo is a British neobank; in 2023 it was building a separate product for the US. In October 2023 only 9% of people who downloaded the app reached the end of sign-up and opened an account. Sign-up took 39 screens, an average of 210 taps and 17 minutes.

The team went through the sign-up funnel screen by screen and found two bottlenecks:

| Stage | What was found | Solution |
|---|---|---|
| Entering data and address | longest, with the most typos; address typos were noticed only later, when the address did not match the credit history | autofill from the phone, address hints while typing; four screens with terms replaced by a link |
| One of the customer checks | was responsible for 40% of the drop-off in the funnel; the check had been moved over from the UK and screened out reliable customers in the US | an external identity-risk provider (Alloy) sorts new customers into low, medium and high risk by rules; the check is skipped for low risk |

Result: after the first step, sign-up dropped to 17 screens and 74 taps, and 19% reached the end. Skipping the check was first enabled for 25% of sign-ups, then for all. The share completing sign-up rose to 40%, and the median time fell from 17 to 7 minutes.

What the case does not include: Monzo did not publish the funnel for all screens — the customer counts and conversion at each stage. Known are the overall conversion, the share of drop-off at one check, and the total time. The bank did not name the exact check that is skipped.

Source of the case: M. Aly, [«How we cut time to sign up for Monzo US from 17 minutes to 4 minutes»](https://monzo.com/blog/how-we-cut-time-to-sign-up-for-monzo-us-from-17-minutes-to-4-minutes), Monzo blog, September 4, 2024.

## Common mistakes

- **Looking only at overall conversion.** Growth at one stage and a drop at another cancel each other out.
- **Fixing everything at once.** It is unclear which change worked.
- **Expanding the entry instead of repairing the bottleneck.** More traffic into a leaky funnel means more money lost on acquisition.
- **Not measuring time at stages.** A customer who waits a week for approval leaves for a competitor, even though formally they are still in the funnel.
- **Blaming the product for a broken channel.** The average funnel looks weak, but the loss sits in one traffic source, partner or segment while the others convert normally. Split the funnel by channel before changing the product.
- **Sacrificing quality for conversion.** A removed check or a simplified step lets through those who should have been screened out: look also at what happens to customers after the purchase.

## Source

The image of the funnel was first applied to the steps of a sale — from the buyer's attention to interest and beyond — in the book William W. Townsend, [«Bond Salesmanship»](https://catalog.hathitrust.org/Record/006565786), Henry Holt, 1924. History and critique of the image: Tom Roach, [«Why the sales funnel is the cockroach of marketing concepts»](https://www.marketingweek.com/sales-funnel-100-years/), Marketing Week, 2021.

## See also

- Preceded by Customer Journey Map: Turn the journey map path into funnel stages, each with a recorded event.
- Enhanced by Cohort Analysis: Calculate funnel conversion only for customers who entered in the same period, grouped as cohorts.
- Enhanced by AARRR Metrics: Map each funnel stage to an AARRR group to see which group holds the bottleneck.
- Enhanced by TAM / SAM / SOM Model: Use funnel conversion rates to estimate the acquisition pace that limits SOM.
