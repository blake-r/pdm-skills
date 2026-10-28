---
name: balanced-scorecard
description: Build or check a Balanced Scorecard (Kaplan and Norton, 1992) - goals, measures and targets in four perspectives (financial, customer, internal business process, innovation and learning) - and produce a one-slide PPTX; or review an existing scorecard. Use when a unit steers only by financial results, results arrive too late to correct anything, teams optimize their own number at the expense of others, or the user says "balanced scorecard", "BSC", "scorecard", "KPI by perspectives".
---

# Balanced Scorecard

The theory, scheme and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user is building a scorecard, **review** when the user brings an existing one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the unit and the period the scorecard covers;
- the strategy or vision in one or two sentences;
- what customers expect and how the unit knows today;
- the processes and skills that decide whether customers get it;
- what the owners watch now (financial and other measures), with values and dates;
- what the scorecard should help decide.

Do not invent numbers or goals. Mark what the user did not give as N/A. Say that the card has no fixed list of measures: they follow the strategy.

### 2. Fill the four perspectives

For each perspective write goals, measures and targets (value and date). Work in the card's order: customer, internal process, innovation and learning, finance. Keep each scorecard short and give every goal one or two measures. Check the balance: does one measure improve at the expense of another?

### 3. Decision

Write what the scorecard changed or should change: a goal, a process or a measure. If it changes nothing, say so.

### 4. Show, then write

Show the scorecard in chat first as a table by template blocks: title, strategy, then a row per perspective with goals, measures, targets, and the decision. Write a file only after the user confirms. Ask for the output path (default `balanced-scorecard-<unit>.pptx` in the working directory). Save the data as JSON. The example is the Analog Devices case from card.md; fields the slides do not show say so.

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Analog Devices IC operations: QIP goals to 1992",
    "strategy": "Business objectives: market leadership, revenue growth, profitability. Driver: be rated number 1 by customers in total value delivered",
    "g1": "Market leadership, revenue growth, profitability",
    "m1": "N/A: no financial measure on the slides read",
    "t1": "N/A: no financial target on the slides read",
    "g2": "Be rated number 1 by customers in total value delivered",
    "m2": "On-time delivery; outgoing defect level; lead time; share of customer requested dates (CRDs) matched; excess lead time",
    "t2": "1987 / 1990 / 1992 goal: delivery 85% / 96% / >99.8%; defects 500 / 230 / <10 PPM; lead time 10 / 5.4 / <3 weeks; CRDs matched 31% / 50% / n/a",
    "g3": "Eliminate all forms of waste at all entities, functions and levels",
    "m3": "Manufacturing cycle time; process defect level; yield",
    "t3": "1987 / 1990 / 1992 goal: cycle time 15 / 8 / 4-5 weeks; process defects 5000 / 1100 / <10 PPM; yield 20% / 38% / >50%",
    "g4": "Shorter time to market; reduced turnover",
    "m4": "Time to market; labor turnover as a proxy for employee satisfaction; from FY1990 bookings of products introduced after 1985",
    "t4": "Time to market 1987 / 1990 / 1992 goal: 36 months / not read / 6 months; turnover target not read",
    "decision": "FY1990: delivery is measured against the customer's requested date; the old new-product measures, poor predictors, are replaced by a product tracking system and two innovation measures. FY1991-92: scorecard unchanged"
  }
}
```

Fields: g1..g4 are goals, m1..m4 measures, t1..t4 targets, one per perspective in the order financial, customer, internal process, innovation and learning. Limits that fit the slide: title under 60 characters; strategy under 140; each goal under 90; each measure under 150; each target under 150; decision under 230. Put the rest in chat. Run from the repo root:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run scripts/fill_pptx.py <this skill dir>/balanced-scorecard.pptx data.json <output>.pptx
```

`uv run scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's scorecard and check it against the common mistakes in card.md:

1. Financial measures only, relabeled: every perspective holds revenue ratios.
2. Too many measures to act on.
3. Targets or measures not tied to the strategy (copied from other companies).
4. Measures that never change, though the strategy did.
5. Measures are defined on the unit's own terms, not the customer's (for example delivery against a window the unit sets itself).
6. Used as a pay formula while measures are still being defined.
7. Units that differ are combined into one number.

Items 3, 4 and 6 usually cannot be judged from the table alone: ask for the strategy, when the measures were last reviewed and whether pay depends on them, instead of reporting a finding. Also check that every goal has a measure and a target with a date, and that the decision is stated. Report findings as a numbered list: what is wrong, why it matters, the concrete change. End with a verdict: "steers the strategy", "works after changes" or "needs a strategy first".

Example: four perspectives, each with revenue, margin and cost lines, no targets, and the user says it is reviewed once a year. Findings: item 1 - the non-financial perspectives hold financial ratios, replace them with customer, process and innovation measures; item 4 - ask when the measures were last changed. Verdict: "needs a strategy first".
