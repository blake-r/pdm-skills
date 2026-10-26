---
name: minimum-viable-product
description: Plan or review a Minimum Viable Product (MVP) test — hypothesis, riskiest assumption, the form of the MVP (what is real for the user, what is done by hand, what is not built), success metric and threshold set in advance, sample, result and a continue / change / stop decision — and produce a one-slide MVP card. Use when the user wants to check demand cheaply before building, asks what the smallest version to test should be, or wants an MVP plan or result checked.
---

# Minimum Viable Product

The theory, the sources and a worked case (Zappos) are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode: **do** when the user needs an MVP test designed or its result recorded, **review** when the user shows an MVP plan or result and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for what is missing:

- the product idea, who it is for and what problem it solves;
- what the user already knows and what is only a guess;
- how people could do a real action (buy, pay, order, sign up) and what the team can do by hand;
- budget, time, the audience that can be reached;
- if the test has already run: what was measured and the numbers.

Do not invent numbers, dates or names. Mark what the user did not give as unknown, and write "not in source" or "unknown" in the template block instead of leaving it empty.

### 2. Hypothesis and riskiest assumption

Write the hypothesis in one sentence. Pick the one assumption that, if wrong, makes everything else pointless. If the user names several, ask which is the weakest.

### 3. Form of the MVP

Fill three lists: what is real for the user (the action being tested), what is done by hand instead of automation, what is deliberately not built. The MVP is the cheapest version that tests the assumption with behaviour, not the version with the fewest features.

### 4. Metric, threshold, sample, cost

Set the metric and the success threshold before launch, name who the people are (real users, not friends), how many, how many weeks, the cost. If the user cannot set a threshold, say that the result will then be read any way you like and propose one to confirm.

### 5. Result and decision

If the test has run, record facts and what was not measured. Offer one of three decisions: continue, change the hypothesis, stop; with the next step and a date. If the test has not run, write "not yet run" in result and decision.

### 6. Show, then write

Show the card in chat first as a table by template blocks: title, hypothesis, assumption, real, manual, skip, metric, sample, cost, result, decision. Write a file only after the user confirms; ask for the output path (default `mvp-<name>.pptx` in the working directory). Example data is the Zappos case from card.md; what the source lacks says "not in source" (the template blocks must not stay empty):

```json
{
  "text": {
    "title": "Zappos (late 1990s): will people buy shoes online",
    "hypothesis": "People will buy shoes online",
    "assumption": "A customer will order shoes from a photo on the internet",
    "real": "Ordering shoes online (reconstructed from the source)",
    "manual": "Buying a pair from the store at full price after the order (reconstructed from the source)",
    "skip": "not in source",
    "metric": "not in source",
    "sample": "not in source",
    "cost": "not in source",
    "result": "The store agreed, \"a few orders\"; no numbers; test year not given",
    "decision": "Decision per Fortune: put the whole collection online; $150,000 raised. The card author's conclusion: there was no threshold, so the decision was made without a formal criterion"
  }
}
```

Length limits that fit the slide: title under 70 characters; no empty blocks, use "not in source"; hypothesis and assumption under 110; real, manual, skip, metric, sample, cost under 90; result under 130; decision under 170. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/minimum-viable-product.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's MVP plan or result and check it against the common mistakes in card.md:

1. The MVP is a "first version with fewer features", not a test of an assumption.
2. There is no success threshold set before launch.
3. The wrong assumption is tested: something is built well while the risk lies elsewhere, such as willingness to pay.
4. A survey stands in for behaviour: words about intent instead of a purchase or sign-up.
5. The sample is friends and acquaintances.
6. Too much is real: months of development before the first signal.
7. There is no decision: the test ended without "continue, change or stop".
8. A weak result is ignored or read as "not enough features".

Items 2, 4 and 5 usually need questions to the user rather than a verdict: ask when the threshold was fixed, what exactly people did, who they were. Report findings as a numbered list: what is wrong, why it matters, the concrete change. End with a verdict: "tests the assumption", "works after changes" or "needs a hypothesis and a threshold first".

Example: plan "build an app with five features and see if people like it", no threshold, a survey of colleagues. Findings: 1 — a bundle of features, not a test; 2 — no threshold; 4 — survey instead of behaviour; 5 — colleagues. Verdict: "needs a hypothesis and a threshold first".
