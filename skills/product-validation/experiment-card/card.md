# Experiment Card

## Essence

The Experiment Card is one page on which a team records the test of a single hypothesis, from the question to the conclusion. The fields follow the order of a scientific experiment:

1. **Our question** — what we want to learn in order to make a decision.
2. **Our hypothesis** — what we believe is true.
3. **We are right if** — the metric and threshold, set in advance.
4. **People and materials** — who takes part, whom we test on, what is needed.
5. **How we test** — steps, duration, volume.
6. **What we observed** — facts and numbers.
7. **The hypothesis turned out** — confirmed, refuted or unclear.

The first five fields are filled in before the start, the last two after. The key field is the third: a threshold written in advance prevents fitting the conclusion to the result.

## When to use and when not to

Use when a team is about to test a hypothesis and needs to agree in advance what will count as success. Use when experiments are numerous and their outcomes get lost in correspondence. Use when a feature decision depends on the test and will be made by people who did not take part in the experiment.

Do not use for changes that will be made anyway: the card turns into a report for its own sake. Not suitable for long research without a clear question — first you need to understand what to ask.

Limitations:

- **One card — one hypothesis.** If several are tested at once, the field "The hypothesis turned out" cannot be filled honestly.
- **The card does not choose hypotheses.** What to test first is decided separately.
- **"Unclear" is a legitimate outcome.** If data are scarce or metrics diverge, that is what gets written, rather than forcing a conclusion.

## Scheme

```
┌─────────────────────────────┬──────────────────────────────┐
│ 1 OUR QUESTION              │ 5 HOW WE TEST                │
├─────────────────────────────┤                              │
│ 2 OUR HYPOTHESIS            ├──────────────────────────────┤
├─────────────────────────────┤ 6 WHAT WE OBSERVED           │
│ 3 WE ARE RIGHT IF           ├──────────────────────────────┤
├──────────────┬──────────────┤ 7 HYPOTHESIS VERDICT         │
│ 4 PEOPLE     │ MATERIALS    │ confirmed │ refuted          │
│              │              │ unclear                      │
└──────────────┴──────────────┴──────────────────────────────┘
```

## How to apply

1. **Write down the question** whose answer is needed for the decision. If the answer changes nothing, the experiment is not needed.
2. **Formulate the hypothesis** in one sentence that can be refuted.
3. **Set the success condition:** which metric and by how much it should change. Decide in advance which metric is the main one if they diverge.
4. **List the people and materials:** who does the work, who takes part, which page variants, texts, budget.
5. **Describe the procedure:** steps, duration, how many observations are needed.
6. **Run the experiment** and record the observations — numbers and whatever surprised you.
7. **Mark the outcome** and record the decision: roll out, rework, drop, test further.

## Example

The analytics agency AIC trained the product team of a large Russian bank to test hypotheses and ran several pilot experiments at the bank on its product list page. One of them, broken down by the card's fields:

| Field | What was recorded |
|---|---|
| Question | do users have other reasons to choose a product besides its characteristics |
| Hypothesis | the number of views on the product preview will push the choice — by analogy with booking.com |
| People and materials | the agency's analysts together with the bank's product team; two versions of the page: the current one and one with view counts |
| How we test | show the versions to different visitors and collect the required volume of data; the order of metric priority is set in advance |
| What we observed | time to click on the card, share of clicks on the preview, number of attempts to submit an application, time on page: users got to the popular product faster and more often moved from the list to the product |
| The hypothesis turned out | confirmed: product popularity also affects the choice |

Next steps proposed: use the conclusion more broadly — add visual hints and notifications that raise interest in the product. After the pilot, the bank launched a full project to train the team.

What the case does not include: the bank's name, figures for the metrics, the experiment dates and the success threshold; the card was not published in this form — the fields were reconstructed from the text. The agency itself told the case.

Case source: A. Klimenko, interview with V. Cheremisinov (AIC), [«AIC case: building hypothesis testing processes on the example of a large bank»](https://vc.ru/flood/57376-keis-aic-postroenie-processov-testirovaniya-gipotez-na-primere-krupnogo-banka), vc.ru, 05.02.2019.

## Common mistakes

- **No question.** The experiment is run to "see what happens", and any outcome decides nothing.
- **The threshold is set afterwards.** A result of +0.5% is declared a success, although no one would have called it that before the start.
- **Stopping on the first days' data.** Regular users are initially confused by the new thing: the indicators are low in the first days and rise day by day, while the experiment is already closed.
- **Several changes at once.** A new design, other texts and bug fixes in one version — it is unclear what worked.
- **"Refuted" is not recorded.** Unsuccessful experiments get lost, and six months later they are run again.

## Source

No public primary source of the card with these fields has been found; the author is not identified. The closest published relative is the Test Card: A. Osterwalder, [«Validate your ideas with The Test Card»](https://www.strategyzer.com/library/validate-your-ideas-with-the-test-card), Strategyzer, 2015. It also requires the hypothesis, the way of testing, the metric and the success threshold to be written down in advance.

## See also

- Enhanced by A/B Testing: Fill the question and hypothesis, then run a controlled comparison on live users.
- Preceded by Validation Board: Take the riskiest assumption and its minimum success criterion as hypothesis and threshold.
- Alternative to HADI Canvas: Use it for a single hypothesis test with a written verdict.
- Preceded by ICE Scoring: Test high-impact, low-confidence ideas first.
- Preceded by Morphological Analysis: Test the chosen combination against preset criteria.
- Preceded by SCAMPER Method: Record each selected idea as one hypothesis.
- Preceded by Lean Canvas: Test its riskiest assumption as this card's hypothesis.
- Preceded by Feature Canvas: Test each unverified block on its own card.
- Preceded by Impact / Effort Matrix: Test quick wins with unproven effects first.
- Preceded by Lean UX Canvas: Record its minimal experiment from box 8.
- Preceded by Six Thinking Hats: Settle the disputed option under the six hats first, then test the chosen one here.
- Enhanced by A/A Testing: Check the test noise on this card before reading the real experiment result.
- Enhanced by Fake Door Test: Write the hypothesis and the click threshold on this card before the door is shown.
- Enhanced by Advertisement / Brochure / Packaging: Set the hypothesis and decision threshold here before showing the offers.
