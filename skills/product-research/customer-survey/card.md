# Customer Survey

## Essence

A survey is a way to study consumers: they fill in a questionnaire of a finite number of closed questions (with ready-made options) and open questions (free-form). According to the description in PAF (Product Architecture Framework, a product architecture framework), this is a key method for collecting statistics about consumers. It shows "how many" and "which people"; "why" remains a hypothesis (the author's conclusion).

## When to use and when not to

Use it when a hypothesis is formulated, there is someone to write to, and shares of answers are needed rather than stories. PAF: the method is universal, scalable, fast and not labour-intensive; it suits both a few questions and dozens.

Limitations (PAF): respondents need qualification, that is, selection of those who belong to the studied group, otherwise the data is irrelevant; questions are prepared in advance: the survey is usually automatic, and the answer cannot be clarified.

Less obvious points:

- **People's forecasts are unreliable.** NN/g (Nielsen Norman Group): questions like "how likely are you to use it" give poor data; ask about recent events.
- **The sample** (people whose answers you received) is not all consumers. If only interested people answered, the shares are accurate only for them (the author's conclusion).

## Scheme

```
Hypothesis → who we ask (selection) → channel and invitations
 → questions (closed + open) → trial run
 → collection → shares of answers by group + analysis of open answers
 → conclusion (marked as a conclusion) → decision and check
```

## How to apply

1. **Write down the hypothesis and the decision** that depends on the answer (NN/g: do not ask unnecessary questions).
2. **Define whom to ask,** and add a screening question about recent experience (PAF: qualification).
3. **Write the questions.** Pew Research Center: one idea per question, plain words without jargon, answer options do not overlap and cover everything. NN/g: neutral wording without a hint of a "correct" answer, balanced scales, a "don't know" or "not applicable" option. Questions are mostly closed, with one open question at the end.
4. **Test the questionnaire** on several people from the target group (Pew: "essential step").
5. **Send it out and keep count:** how many were invited, how many answered. The benchmark from Vohra (Rahul Vohra): the picture is roughly correct already at 40 respondents; advice from one practitioner, not a rule.
6. **Calculate shares** by group and read the open answers; if the groups differ, do not merge them into one figure.
7. **Write the conclusion separately from the data** (label "author's conclusion"), then the decision and a way to check it by behaviour.

## Example

Easyvest (a Belgian B2C fintech for passive investing), described by Matthieu Remy, 15 Mar 2024. With about 600 clients (the article places this towards the end of 2020), the team sent the four-question product-market fit survey (Sean Ellis's method, as popularised by Vohra) to its 591 active customers through an internally built tool. 120 answered within a week; the authors state a margin of error "in the 9% range" at 95% confidence.

| Question | Answers | Conclusion | Decision |
|---|---|---|---|
| 1. How would you feel if you could no longer use it? (very disappointed / somewhat / not) | "Very disappointed" 47% against the 40% benchmark; "not disappointed" 3%. By language: French 49%, Dutch 26%, English 70% | Fit is reached overall but not among Dutch speakers; "very disappointed" clients are likely to invest 2x more than "somewhat" ones | Hire a Dutch-speaking support person, rewrite Dutch content; the very-disappointed share becomes the top product metric, an OKR (objectives and key results) with it as the only key result |
| 2. Who benefits most? | A persona, "Thomas": worried about the long-term finances of his family, wary of traditional bankers and advisors | These are the people to build for | Roadmap is built around them |
| 3. What is the main benefit? | Simple, affordable passive investing; ease of use and access; responsive customer service | The product's strength | Half of the roadmap: more simplicity, more ease, more customer service |
| 4. How to improve? | Asks of the "somewhat" group: automation, better Dutch, brand refresh, ESG offer, more active investment plans | Barriers to remove | Other half: in-app direct debit, automatic investing without call confirmation, ESG tracking; active investing "respectfully ignored"; ESG answered with a blog, not funds |

Not in the source (as read): the exact share of "somewhat", the survey date, and the result of the decisions (no later score). The roadmap is rebuilt quarterly with the same process.

Source: M. Remy, [«How to build product/market fit for a B2C fintech?»](https://full.easyvest.be/articles/en_US/Post/how-to-build-product-market-fit-for-a-b2c-fintech), Easyvest, 15 Mar 2024.

## Common mistakes

- **No selection:** the shares mix different people.
- **A hint in the question.** The question suggests the answer (NN/g).
- **Two questions in one** ("simple and clear"): the answer cannot be interpreted.
- **Asking about the future** instead of recent behaviour.
- **Only closed questions:** you are limited by your own knowledge of the subject (PAF).
- **No trial run:** the answer cannot be clarified later.
- **Listening to everyone equally.** In the case, the request for active investing was declined as off-strategy.
- **Shares without the number of respondents:** 22% of 40 and of 400 are different things.

## Source

Don A. Dillman, Jolene D. Smyth, Leah Melani Christian, *Internet, Phone, Mail, and Mixed-Mode Surveys: The Tailored Design Method*, 4th ed., Wiley, 2014 ([publisher's page](https://www.wiley.com/en-us/Internet,+Phone,+Mail,+and+Mixed+Mode+Surveys:+The+Tailored+Design+Method,+4th+Edition-p-9781118456149)): a textbook on organising surveys. Rahul Vohra, [«How Superhuman Built an Engine to Find Product Market Fit»](https://review.firstround.com/how-superhuman-built-an-engine-to-find-product-market-fit/), First Round Review, November 2018: the four-question form and the 40% benchmark of Sean Ellis. Maddie Brown, [«Writing Good Survey Questions: 10 Best Practices»](https://www.nngroup.com/articles/survey-best-practices/), Nielsen Norman Group, 20.08.2023. Pew Research Center, [«Writing Survey Questions»](https://www.pewresearch.org/writing-survey-questions/), no date on the page. Description in PAF (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, no date; the section is titled "Focus group surveys").

## See also

- Preceded by In-Depth Interview: Use interviews first to learn what customers do, then turn it into survey questions.
- Enhanced by Kano Model: Run the Kano question pair per feature in a survey of about 100 users.
- Enhanced by HEART Metrics: Collect the Happiness metric through this survey, since logs cannot measure satisfaction.
- Preceded by Expert Interview: Test the expert hypotheses on consumers here, since experts give no shares.
- Followed by Perceptual Map: Use the 1–7 brand ratings from this survey as the map's input.
