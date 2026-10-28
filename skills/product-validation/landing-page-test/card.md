# Landing Page Test

## Essence

A landing page (landing page, lead page) is a page or presentation with a full description of the value proposition: what the customer will get and why they need it. The visitor is asked for a target action: leave contacts, enter card details, place a pre-order. No product is needed: you can see what share of those who saw the page took this action. That share is called the conversion.

## When to use and when not to

Use when there is a hypothesis about the value proposition, and the product has not yet been built. Needed: a description of the offer, a target action, a source of visitors, a success criterion.

Do not use:

- **To check that a solution works.** The page measures interest in the description, not usefulness.
- **Without a check of clarity.** PAF (Product Architecture Framework, see "Source") requires a little experience in designing a landing page and advises talking to consumers before and after: is the text clear. Otherwise a low conversion cannot be told apart from poor text (the author's conclusion).
- **With a small number of visitors.** PAF requires statistical significance: the probability of a random result must be small.
- **To collect addresses.** Joel Gascoigne, founder of Buffer: the actions of people and conversations with them are valuable, not the number of addresses.

The signal depends on the price of the action: an e-mail address costs nothing, a card costs more. Eric Ries, author of the Startup Lessons Learned blog: zero after a request for payment does not mean there is no business, but it is a reason to think seriously.

## Scheme

```
Hypothesis → page (problem · offer · terms · button)
→ visitors of the right group → target action
→ conversion = did the action / saw the page
→ comparison with the threshold → decision
```

## How to apply

1. **Hypothesis in the PAF form:** "We believe that [offer] will interest [group], which will be confirmed by [criterion], because [reasoning]". Examples of PAF: conversion to an application of at least 10%; a pre-order for a book of 20%.
2. **Target action by steps:** e-mail address → choice of a plan → card or pre-order. The more expensive the step, the stronger the signal and the fewer people there are.
3. **Page layout:** headline with the benefit, the problem, the offer, the terms, one button.
4. **Set the threshold and the volume before launch.** Recommendation of the card author: hundreds of visitors. The 95% confidence interval for the true conversion at an observed 10%: about 5–17% with 100 visitors, 7–13% with 400 (the card author's calculation, Wilson method). Ries (2008): up to 100 clicks a day, for one to two weeks.
5. **Bring visitors from the target group,** not only acquaintances.
6. **Count by steps.**
7. **Talk to those who left contacts** and, if possible, to those who left: why.
8. **Decide:** above the threshold — check the solution itself; below it, with clear text — change the offer or the group; zero on a paid step — a reason to seriously reconsider the group and the offer (Ries: this does not yet mean there is no business).

## Example

Buffer (an app for a tweet queue, paid subscriptions; not e-commerce and not fintech). Author: Gascoigne, 2010.

Hypotheses: people will want to use the app; then — pay for it. Page: a description, a page with plans, a form "we'll let you know at launch". He wrote personally to those who left an address.

Reaction. An article from 2011: people went further, "a small number" clicked on the paid plans. An article from 2013: 120 sign-ups over seven weeks, 50 started using it at launch, one paid after 3 days.

Decision: start development "without hesitation"; launch on 30 November 2010. Two and a half months later — over 500 users, about 4% pay.

Discrepancies. "Seven weeks": in 2011 it was the development time, in 2013 — the collection of 120 sign-ups. First payment: "within 4 days" (2011) and "after 3 days" (2013).

What is missing: visitor numbers, clicks on plans, the threshold. I did not find a public case from e-commerce or fintech with figures.

Sources: J. Gascoigne, [«Idea to Paying Customers in 7 Weeks»](https://buffer.com/resources/idea-to-paying-customers-in-7-weeks-how-we-did-it/), Buffer blog, 16.02.2011; [Medium article](https://web.archive.org/web/20141219021419/https://medium.com/@joelgascoigne/how-to-successfully-validate-your-idea-with-a-landing-page-mvp-ef3c2d02dc51), 30.11.2013, archive snapshot from 2014.

## Common mistakes

- **A page for addresses.** Without a price step and conversations, there is nothing to learn.
- **An e-mail address as demand.** Look at the paid steps.
- **Threshold and volume not set in advance.** Any figure can be explained in one's favor.
- **A small sample.** 120 sign-ups gave conversations, not an exact conversion.
- **Low conversion = "the idea is not needed".** The cause may be unclear text or distrust of a request for a card (the author's conclusion).
- **Only acquaintances** inflate the result (the author's recommendation).
- **Forgetting those who responded.** If the offer cannot be fulfilled, Ries advises apologising personally.

## Source

Description in PAF (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, undated): the section "Landing page / Presentation / Contact collection" of the page on value proposition hypotheses. PAF does not name the author of the method or the year.

Eric Ries, [«Using AdWords to assess demand for your new online service, step-by-step»](https://www.startuplessonslearned.com/2008/11/using-adwords-to-assess-demand-for-your.html), Startup Lessons Learned blog, 7.11.2008: a "fake landing page" test. Gascoigne: articles of 2011 and 2013 (links in "Example").

## See also

- Alternative to Advertisement / Brochure / Packaging: Compare offer wordings on ads or a brochure before building the page.
- Alternative to Fake Door Test: Test the same benefit as an element in a running product, leading to a stub.
- Followed by Minimum Viable Product: If conversion clears the threshold, build the cheapest version to test the main assumption.
- Preceded by USP 4U Formula: Check the phrase with 4U first, then see whether visitors respond to it.
- Preceded by USP "Familiar without familiar": Test the phrase on this page before building the replacement.
- Preceded by Maxwell USP Formula: Put the phrase with its time frame and guarantee on this page.
