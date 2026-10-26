# A/A Testing

## Essence

An A/A test is an experiment in which both groups see the same thing. The experimentation system splits users as usual, counts metrics and significance, but the product version is identical for both groups. So any "difference" is noise, and how the system shows that noise tells you whether it can be trusted.

What an A/A test checks:

- **Splitting.** The group shares match the planned ones: at 50/50 you do not get 52/48 across hundreds of thousands of users.
- **False positive rate.** At a 5% significance level, a difference is "significant" in about 5% of runs or metrics. If it is noticeably more, there is an error in the calculation; if noticeably less, that is also a problem.
- **Data collection.** The numbers in the experimentation system match the main accounting system.
- **Metric variance.** Data from an A/A test is used to estimate how many users future experiments will need.

Ronny Kohavi and co-authors from Microsoft call the A/A test the most useful tool for finding errors in experimentation systems and advise running it continuously.

## When to use and when not to

Use before the first experiment on a new system, after changes to user splitting, and when moving to a new metric or significance formula. Also use when experiment results seem "too good" and there is a suspicion of an error in the system.

Do not use it as a substitute for checking changes: an A/A test says nothing about the product. A single run proves little; one "significant" difference out of twenty is expected.

Limitations:

- **A series is needed.** The false positive rate is visible only over dozens of runs; they are cheap to get by re-splitting historical data.
- **A live run takes traffic and time.** Re-splitting history is faster but does not catch splitting errors in real time.
- **It finds a symptom, not a cause.** The cause is looked for separately: splitting, data collection or formulas.

## Scheme

```
    users ──random split──┬── group A: current version
                          └── group A': the same version
    runs 1..N: share of A, conversions, p-value
    ├─ shares match the planned ones?          no → splitting error
    ├─ significant results around 5%?          more → calculation error
    └─ p-values uniformly distributed?         no → formula does not fit the metric
```

## How to apply

1. **Write down what you are checking:** the splitting system, a new metric or a significance formula.
2. **Choose the metric and the splitting unit** — the same as in future experiments.
3. **Set the number of runs:** live tests on real traffic or repeated re-splits of history; ideally a hundred.
4. **Check the split** in each run: a deviation of the share from the planned one with p below 0.001 is a system error.
5. **Calculate the share of significant results** and compare it with the significance level; build a histogram of p-values — the bars should be roughly equal.
6. **Make a decision:** all good — run experiments; not good — look for the cause, fix it and repeat the A/A test.

## Example

Airbnb, a short-term rental marketplace, checked its own experimentation system and ran many A/A tests with different splits. The team wanted to know what the system would return when there was clearly no difference.

| Runs | Split | What the system showed |
|---|---|---|
| several | 50/50 | neutral result, as expected |
| several | 75/25 | strong imbalance against the smaller group |

Decision: find the cause of the imbalance. The investigation found a serious error in how the system distributed visitors who were not logged in between the groups. The author also warns about noise: if an A/A test is split across 100 countries, about five of them will show a "significant" result.

What the case does not include: the number of runs, users and the size of the imbalance — only a chart; there is also no direct statement that the error was fixed.

A second example — Microsoft's experimentation team, not e-commerce: in the first offline A/A tests, run on already collected data, 30% of metrics turned out significant instead of the expected 5%. The cause was that standard formulas underestimated the variance of many metrics.

Case source: J. Overgoor, [«Experiments at Airbnb»](https://web.archive.org/web/20170624103833/https://medium.com/airbnb-engineering/experiments-at-airbnb-e2db3abf39e7), Airbnb Engineering, 27.05.2014.

## Common mistakes

- **One run instead of a series.** One "significant" difference is declared a breakdown, or one clean run is taken as proof the system works.
- **Checking only significance, not group shares.** An imbalance in the split goes unnoticed.
- **Only equal splits.** The error may appear only with unequal shares.
- **A different metric or splitting unit** from the one used in future experiments.
- **A problem is found — and experiments are launched anyway.** Without a fix and a repeated A/A test, the results are still unreliable.

## Source

T. Crook, B. Frasca, R. Kohavi, R. Longbotham, [«Seven Pitfalls to Avoid when Running Controlled Experiments on the Web»](https://www.exp-platform.com/Documents/2009-ExPpitfalls.pdf), KDD 2009; R. Kohavi et al., [«Trustworthy Online Controlled Experiments: Five Puzzling Outcomes Explained»](https://exp-platform.com/Documents/puzzlingOutcomesInControlledExperiments.pdf), KDD 2012. The other name, Null Test, the authors take from E. T. Peterson's book «Web Analytics Demystified», 2004.

## See also

- Followed by A/B Testing: After the A/A test confirms the split, run A/B tests.
- Enhanced by Experiment Card: Record the question and conclusion of the A/A check on one card.
