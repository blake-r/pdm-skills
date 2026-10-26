# HADI Canvas

## Essence

HADI Canvas is a canvas on which a team runs one cycle of hypothesis testing according to the HADI scheme: Hypothesis, Action, Data, Insights. The cycle is short, usually one or two weeks. The insights of one cycle give the hypotheses for the next.

The canvas splits the cycle into two parts:

- **lanes at the top, left to right:** problem → hypothesis → experiment → metrics. The problem is stated in numbers, the hypothesis links the change to a metric, the experiment says what we do and on whom, the metrics say what we measure and at what value the hypothesis is confirmed;
- **data and insights at the bottom:** metric values by experiment period and insights — interim along the way and final with a decision: roll out and scale, rework, or drop.

The method spread through the FRII accelerator: HADI cycles have a special role there in a methodology that was tried in more than 150 startups, and teams analyzed their cycles at a weekly traction meeting. The author of the method is not named in open sources.

## When to use and when not to

Use when a team has more ideas than resources and needs to understand quickly which of them move the required metric. Use when arguments of "it will work — it won't" are held at the level of opinions. Use when changes can be rolled out to part of the users, stores or traffic and measured within a week or two.

Do not use when the metric responds only after months: the cycle will stretch and the insights will be outdated. Not suitable when traffic is low and the difference drowns in the error. Not needed for mandatory tasks that are done in any case.

Limitations:

- **The canvas does not choose hypotheses.** Which one to test first is decided separately, by expected effect and effort.
- **One metric — one hypothesis at a time.** If the product description and the payment method are changed at the same time, it is impossible to tell what worked.
- **A negative outcome is also an outcome.** Most hypotheses are not confirmed; the value of the canvas is that this becomes visible quickly and cheaply.

## Scheme

```
┌───────────┐   ┌────────────┐   ┌────────────┐   ┌─────────────────────┐
│ PROBLEM   │ → │ HYPOTHESIS │ → │ EXPERIMENT │ → │ METRICS + THRESHOLD │
└───────────┘   └────────────┘   └────────────┘   └─────────────────────┘
┌─────────────────────────────────┬──────────────┬─────────────────┐
│ DATA   period 1 │ 2 │ 3         │ INSIGHTS     │ FINAL + DECISION│
│ metric … │ … │ …                │ interim      │                 │
└─────────────────────────────────┴──────────────┴─────────────────┘
```

## How to apply

1. **Name the problem in numbers:** which metric is bad, by how much, and how this is known.
2. **Formulate the hypothesis:** "if we do X, metric Y will change by Z, because…". One hypothesis — one metric.
3. **Plan the experiment:** what you change, on whom, for how long. Calculate in advance how many observations are needed to tell the effect from the error.
4. **Write down the threshold:** the metric value at which the hypothesis is confirmed. Record the value before the start.
5. **Collect data by period** and record interim insights.
6. **Sum up and make a decision:** scale, rework or drop. Turn the insights into the next hypotheses.

## Example

At the end of May 2015, Carrot quest, a service for communication between website users and site owners, together with FRII and its trainer Ilya Krasinsky ran a one-week HADI workshop for five startups. Each team wrote down ten hypotheses, estimated its confidence in the effect and the complexity, and in a week tested two or three of them.

The cycle of Carrot quest itself:

| Stage | What was recorded |
|---|---|
| Problem | main task — raise the sign-up conversion on the website |
| Hypothesis | not formulated as such; the change tested was to the headlines |
| Experiment | headline with the names of client companies (Ikea, Kaspersky, Intel), new block headings and button |
| Metric and threshold | not stated for this test; the article gives, for the workshop teams in general, about 3 thousand visitors per page and an error of about 1% |
| Conclusion | no growth in conversion was seen |
| Decision | move on to the next hypotheses |

What the case does not include: a formal hypothesis, a threshold applied to this test, whether the variant was kept, conversion figures before and after, data by period, and what the next hypotheses produced. Gap: it is a SaaS landing page, not e-commerce or fintech, and the company itself published it; no public e-commerce or fintech HADI board with figures was found.

A second example — from a column by the business development director of the video analytics company Facemetric (2020): the marketing department of VkusVill checked whether tablets at the checkout with information about promotions would increase sales of promotional goods. The check was run in five stores in Moscow. Sales barely grew, the tablets got in the way at the checkouts, and a survey showed that customers did not notice them. The marketing department was pleased that it tested the idea in several stores rather than across the whole chain. The column contains no figures or dates for the experiment.

Case sources: Carrot quest, [«How HADI cycles can improve a startup's metrics in 1 week»](https://www.carrotquest.io/blog/kejs-kak-uskorit-razvitie-proekta/), 18.06.2015; E. Dmitrieva, [«HADI cycles in retail»](https://new-retail.ru/business/hadi_tsikly_v_riteyle_kak_ispolzovat_metod_eksperimentov_chtoby_uvelichit_prodazhi_i_potok_v_magazin1858/), New Retail, 09.10.2020.

## Common mistakes

- **Obvious hypotheses.** "If we keep calling the database, sales will come" is current work, not a test.
- **No metric.** "We'll go to the forum, it will be useful" — it is unclear what measures success.
- **No threshold and no "before" data.** After the experiment, any result can be called a success.
- **Too few observations.** A difference smaller than the error is taken as an effect.
- **Stretching the cycle.** A check for a quarter instead of one or two weeks: while data are awaited, everything else changes.
- **No decision.** The cycle is closed with a report, but nothing is rolled out or cancelled.

## Source

P. Ryskov, [«HADI cycles: 5 life hacks for testing hypotheses»](https://iidf.ru/media/articles/lifehacks/hadi-tsikly-5-layfkhakov/), FRII, 2019; Carrot quest, a 2015 article about the workshop with FRII (link above). The layout of the canvas with lanes and period data is taken from the original set note; its public primary source was not found.

## See also

- Preceded by AARRR Metrics: Pick the bad metric, such as activation, before stating the problem in numbers.
- Enhanced by A/B Testing: Roll the change out to part of users and measure it against a control.
- Alternative to Experiment Card: Use it for a repeated hypothesis cycle with data and learning.
