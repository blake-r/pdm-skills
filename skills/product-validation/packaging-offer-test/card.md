# Advertisement / Brochure / Packaging

## Essence

An offer test (offer — the wording of a value proposition: what the customer will get) through the "packaging" of a product that does not exist yet: an advertisement, a brochure or a box mock-up. People are shown the packaging and the number of those who show interest is counted. Within days and for little money it becomes visible whether the wording catches attention.

## When to use and when not to

Use when there is a value-proposition hypothesis and several wordings, and the choice must be made before development. Needed: an audience, a display channel (search, social networks, a stand, a meeting), a count of clicks or marks.

Do not use:

- **To check the solution or willingness to pay.** The test measures the attractiveness of the wording; a click is weaker than a purchase.
- **With a single variant.** PAF (Product Architecture Framework, see "Source") warns: a low conversion to one offer may reject a correct idea. PAF calls this a type I error; in common terminology it is a false negative: a good idea was rejected because of a weak wording (the card author's conclusion). Run a series of offers.
- **With a small number of views.** PAF requires statistical significance: the difference between variants must not be noise, and with dozens of clicks it may be.

## Scheme

```
Hypothesis → 2–4 offer variants → packaging (ad / brochure / box)
→ showing to the audience → non-binding action (click, tick, visit to a site)
→ conversion = showed interest / saw → comparison with the threshold → decision
```

## How to apply

1. **Formulate the hypothesis:** "customers [group] need [benefit], and the offer [text] will attract them". Measure: conversion to a click or to a mark of interest.
2. **Set the threshold and the number of views before launch.** Recommendation of the card author: compare the variants with each other, count clicks per variant, and compute conversion only for variants with a sufficient number of views; otherwise the result is explained after the fact.
3. **Make 2–4 variants of the offer** for one idea. Change one variable and keep the rest the same.
4. **Make the packaging.** Online — an advertisement. Offline — a brochure or a box; after the showing, a non-binding action is offered.
5. **Calculate conversion** by variant and by audience group: the overall total hides discrepancies.
6. **Decide:** above the threshold — check the solution itself; below it for all variants — change the wording or the group; if the groups diverge — choose the target group.

## Example

A book, not e-commerce and not fintech (see below). Hypothesis: the title "The Phoenix Project" will attract IT-professional readers more strongly than the working title "When IT Fails". On 23 October 2012 the cover had to be approved within a month.

Packaging: two Google AdWords ads — the title plus a placeholder subtitle. Keywords were collected for five reader groups (by characters of the novel: Erik, Patty and others); the click led to a thank-you page.

First day: ~150k views, 82 clicks, $170; CTR (click-through rate, the share of clicks among impressions) below 0.2%. "The Phoenix Project" led "When IT Fails" roughly 2:1, but information security specialists preferred "When IT Fails".

Subtitles (about eight variants): ~3 days, ~218k views, 86 clicks, $2.25 per click on average. For "Helping The Business Win" the security group gave less than 5% of the votes; for the Erik and ITIL-practitioner groups it was a clear winner.

Decision: the title "The Phoenix Project", subtitle "Helping Your Business Win". Kim's conclusion: at $2.25 per click and a book at $9.95, advertising as a sales channel is unlikely to pay off.

Discrepancy in the source: the introduction says "three days and about $500", while the step-by-step description gives one day and $170 plus about three days of subtitles without cost.

What is missing: a threshold set in advance; clicks per variant (only "roughly 2:1"); a public case from e-commerce or fintech with figures could not be found.

Case source: Gene Kim, [IT Revolution article](https://itrevolution.com/articles/phoenix-project-google-adwords-title-subtitle-testing/), 6.03.2013.

## Common mistakes

- **One offer and the conclusion "the idea is not needed".** The wording may be weak; run a series.
- **No threshold.** Any figure can be explained afterwards; in the case the choice was made by relative advantage.
- **Looking only at the overall total.** In the case the security group voted against the leader.
- **Taking a click for demand.** A CTR below 0.2% was considered expected for the general wording; compare the variants with each other.
- **Changing several elements at once.** The case authors tested titles first, then subtitles.
- **Not counting the cost of a click.** Here $2.25 against $9.95 for the book.

## Source

Description in PAF (Sergey Tikhomirov, [productframework.ru](https://productframework.ru/hypotheses/value_proposition), CC BY-SA 4.0, undated): the page on value-proposition hypotheses, section "Advertisement / Brochure / Packaging". PAF does not name the author of the method or the year.

Gene Kim, [article on the title test](https://itrevolution.com/articles/phoenix-project-google-adwords-title-subtitle-testing/), IT Revolution, 6.03.2013: the case. Eric Ries, [«Using AdWords to assess demand for your new online service, step-by-step»](https://www.startuplessonslearned.com/2008/11/using-adwords-to-assess-demand-for-your.html), Startup Lessons Learned blog, 7.11.2008: checking interest through an advertising campaign. Tim Ferriss, «The 4-Hour Workweek», 2007: according to Kim, he systematically tested ideas before investing, through eBay and AdWords; the title test is described in retellings ([Boing Boing, 2010](https://boingboing.net/2010/10/25/howto-use-google-adw.html): six titles; [InternetNews](https://internetnews.com/it-management/how-to-use-the-web-to-succeed-in-publishing-life): more than a dozen; the retellings diverge). The book was not checked.

## See also

- Alternative to Landing Page Test: Test the offer as an online page with a target action, not mock-ups.
- Followed by A/B Testing: Once the product exists, compare its live versions with a controlled split of users.
- Enhanced by Experiment Card: Record the hypothesis, the number of views and the threshold before running the offers.
