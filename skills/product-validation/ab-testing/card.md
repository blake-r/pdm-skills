# A/B Testing

## Essence

An A/B test, a controlled experiment, is a comparison of two or more product versions on live users. Users are randomly split into groups: the control sees the current version A, the others see the new versions B, C… Everything except the change under test is the same for the groups, so a difference in the metric can be attributed to the change rather than to the season or advertising.

The answer of a test is not "B is better", but "the difference is of this size, and the probability of getting it by chance is such-and-such". A decision is made when the significance (p-value) is below a level set in advance, usually 5%, and the confidence interval of the difference does not include zero.

## When to use and when not to

Use when the change can be shown to part of the users and the metric responds within days or weeks: button text, the order of results, a checkout step. Use when people argue about opinions and are ready to accept an unpleasant result.

Do not use when there are too few users: the required volume will not be reached in a reasonable time. Not suitable for decisions that cannot be shown to part of the audience (price for everyone, legal changes), and for effects that will appear only after months.

Limitations:

- **Most ideas do not work.** At Microsoft, only a third of the tested ideas improved the target metric; at Google, out of roughly 12 thousand experiments in 2009, about 10% led to changes in the business.
- **One change — one conclusion.** If many things are changed at once in version B, it is unclear what worked.
- **The sample size is calculated before the start.** It depends on the baseline conversion and on the difference we want to detect.

## Scheme

```
        random split by users
        ┌───────────────┴───────────────┐
   A: current version              B: change
   users, conversions              users, conversions
        └───────────────┬───────────────┘
   difference, p-value, confidence interval
   → decision by the rule written before the start
```

## How to apply

1. **Write down the hypothesis:** "if we change X, metric Y will change, because…".
2. **Choose one primary metric before the start** and guardrail metrics that must not get worse.
3. **Choose the splitting unit** — usually the user, so that each person sees one version for the whole test.
4. **Calculate the size and duration:** from the baseline conversion, the minimum detectable effect, the significance level and power. Kohavi's rule for 5% and 80%: n ≈ 16·p(1−p)/Δ² users per group, where p is the baseline conversion and Δ is the difference in proportions. Round the duration up to whole weeks, better two: behavior on weekdays and weekends differs.
5. **Check the split:** the group shares must match the planned ones. A skew is a sign of a configuration error, not of an effect.
6. **Do not stop the test as soon as the p-value drops below 5%.** Frequent peeking with a stop at the first significance multiplies false positives.
7. **Make the decision by the rule written in advance:** roll out, reject, or test further.

## Example

Etsy, a marketplace for handmade and vintage goods, added infinite scroll to search results. The premise on the team's slide: seeing more items faster is a better experience. The feature was designed and built entirely, and the test was supposed to only "measure the obvious large improvement".

| Metric | Control (pages) | Infinite scroll | Difference |
|---|---|---|---|
| Median item impressions | 80 | 40 | half as many |
| Clicks on results | 0.6520 | 0.5811 | −10.87% |
| Additions to favorites | 0.0752 | 0.0689 | −8.38% |
| Purchases from search | 0.0164 | 0.0127 | −22.5% |

Overall purchases did not decrease — people stopped finding items through search. For a month the team looked for bugs across browsers and countries; the findings did not change the outcome, and there were so many changes that it was impossible to identify the culprit. Then the premises were checked with separate tests: more items per page gave only a barely noticeable increase in clicks, purchases did not change; an artificial delay in search made no difference. Decision: the feature was removed.

The author, an Etsy search engineer, acknowledges: the premises should have been checked with small tests before development.

What the case does not include: a primary metric chosen in advance, the sample size, the duration and the p-value; the slides have the dates 6–9 February without a year (the talk was published in December 2012).

Case source: D. McKinley, [«Design for Continuous Experimentation»](https://mcfunley.com/design-for-continuous-experimentation), talk first given at Warmgun 2012, San Francisco; post of 22.12.2012, and [slides](https://mcfunley.com/continuous-experimentation/out.pdf).

## Common mistakes

- **The metric is chosen after the test.** Out of twenty metrics at the 5% level, on average one will be "significant" by chance.
- **Stopping at the first significance.** Peeking every day turns a 5% false positive rate into a noticeably larger share.
- **Too few users.** The sample size is not calculated, and a difference smaller than the error is declared an effect or the absence of one.
- **Incomplete weeks.** A test from Monday to Wednesday does not account for weekends.
- **Not checking the split.** It was set to 50/50, but across hundreds of thousands of users it came out 52/48 — this is a configuration error, and the result cannot be trusted.
- **Many changes in one version.** There is a result, but no cause.

## Source

R. Kohavi, R. Longbotham, D. Sommerfield, R. Henne, [«Controlled experiments on the web: survey and practical guide»](https://ai.stanford.edu/~ronnyk/2009controlledExperimentsOnTheWebSurvey.pdf), Data Mining and Knowledge Discovery, 2009; R. Kohavi et al., [«Online Controlled Experiments at Large Scale»](https://www.exp-platform.com/Documents/2013%20controlledExperimentsAtScale.pdf), KDD 2013; R. Kohavi et al., [«Trustworthy Online Controlled Experiments: Five Puzzling Outcomes Explained»](https://exp-platform.com/Documents/puzzlingOutcomesInControlledExperiments.pdf), KDD 2012; C. McRee, [«How Etsy Handles Peeking in A/B Testing»](https://www.etsy.com/codeascraft/how-etsy-handles-peeking-in-a-b-testing), Etsy, 2018.

## See also

- Preceded by A/A Testing: Run an A/A test first to check group split and false positive rate.
- Enhanced by Experiment Card: Write the hypothesis, primary metric and threshold on the card before the test.
- Alternative to Fake Door Test: Use it to compare two live variants of an existing element.
- Preceded by USP AIDA(s) Formula: Compare its text variants on live users.
- Enhanced by Cohort Analysis: Pick the test from cohort trends, then confirm the cause.
- Enhanced by RFM Analysis: Split the RFM segment into test and control groups.
- Preceded by Theory of Inventive Problem Solving (TRIZ): Check it against the current version on real users.
- Enhanced by HADI Canvas: Run the test as the experiment step of HADI.
- Preceded by Advertisement / Brochure / Packaging: Compare live versions after the packaging test.
