# Awesome Problem Interview Script

## Essence

A problem interview script is a plan of a conversation with a potential customer, built from a problem hypothesis. The hypothesis is written by the formula Person + Problem + Cause + Motivation: who has the problem, what it is, why it arises and why the person cares. Each question is tied to a part of the hypothesis.

## When to use and when not to

Use it when a problem has been assumed and needs to be confirmed or rejected. Inputs: a hypothesis, respondents.

Do not use it (the limits of the PAF handbook, Product Architecture Framework): when the problem is still unknown and is being searched for; when you are checking whether your solution closes the problem.

Nuances:

- **A problem exists only in the context of a goal.** The handbook: the absence of a hand is not a problem until one needs to type quickly.
- **One hypothesis is not enough.** The handbook: an interview spent on a single one is too expensive; add additional ones.
- **The handbook gives no number of interviews and no confirmation threshold.** Set them before starting (recommendation of the card's author).

## Scheme

```
Hypothesis = Person + Problem + Cause + Motivation
  Problem    = behaviour + blocker metric ┐ the same
  Motivation = desired result + goal metric ┘ metric
Script (left to right, top to bottom):
  questions about behaviour and the problem ← Problem
  questions about the goal ← Motivation; about the solution ← Cause; closing
  each question: check → new knowledge
Outcome: persona description (characteristics, context, values, pains)
```

## How to apply

1. **Formulate the hypothesis.** Person — the name of the segment. Problem — the behaviour plus the metric it worsens. Cause — possible causes (the hypothesis of the solution is usually hidden in them). Motivation — the desired result plus the goal metric. The blocker metric and the goal metric are the same one.
2. **Build the verification flow.** About the behaviour: "Walk me through step by step how you ___?", "When was the last time? Show me an example", "How often?". About the problem: "What takes up most of your ___?", "When did this really make you furious?", "What prevents you from cutting it in half?". About the goal: "How much does this get in the way of your goals?". About the solution: "How do you solve it now?". Closing: "If you could do anything at all…", "What else should I ask you?".
3. **Add the new-knowledge flow:** "Why is ___ important to you?", "Who else runs into this?", "Do you decide this way every time?". If an answer contradicts the hypothesis, clarify with these questions. For a categorical judgement: "How did you come to that conclusion?"; for words about price: "Who owns the budget?".
4. **Conduct the interview.** In pairs: one leads, the other records. Do not put the answer into the question (anchor effect). Do not interrupt. Write notes, not a recorder. Take breaks.
5. **Record additional hypotheses** (of behaviours, problems, motivations, blockers, solutions) using the handbook's templates, for example "When <role>, <situation>, then <problem>, and this gets in the way of <result>".
6. **Collect the persona description** from four parts: general characteristics, contextual behaviour, values and goals, pains and difficulties. The outcome: the hypothesis is confirmed, rejected or a new one is needed (conclusion of the card's author).

## Example

No public analysis with a script and a hypothesis in formula form could be found. The best real case is the fintech team Karat (a service for content creators) from the Stripe guide.

The team wanted to build tax software for creators; the product was received coolly. Creators asked for a loan of 5,000 or 10,000 dollars in advance to cover upcoming invoices. A merchant cash advance (an advance against future revenue) did not work. The team realised a card was needed and made a business card that finances creators against revenue from digital platforms. According to Stripe, transactions through it reached "over eight figures" (the currency is not given).

Person (creators) and Problem (money for invoices) are visible. There is no Cause, Motivation, metrics, questions, or number of conversations; the conversations are not called interviews.

Source of the case: Stripe, [«Best practices for building a fintech company, from four startups»](https://stripe.com/guides/building-a-fintech-company), section 6, no date (footer: 2026).

## Common mistakes

- **Behaviour passed off as a problem.** Without a goal there is no blocker.
- **Different metrics for the blocker and the goal.** The hypothesis cannot be measured.
- **Questions not derived from the hypothesis.** The parts Cause and Motivation remain unchecked.
- **Closed questions and "ideally".** Open questions and cases are needed.
- **The answer inside the question.** The anchor effect suggests an option.
- **Interrupting and rushing.** The person is not given time to recall.
- **One hypothesis and a series without breaks.** It is expensive, and perception drops.
- **A script in place of searching for the problem.** If the problem is unknown, the method does not fit (a limit of the handbook).

## Source

Description in PAF (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, no date): the handbook «How to create Awesome Problem Interview Script», 14 pages, [page with the PDF](https://productframework.ru/problem_backlog). It draws on Steve Blank («The Four Steps to the Epiphany», 2005; «The Startup Owner's Manual», 2012), Rob Fitzpatrick («The Mom Test», 2013, [momtestbook.com](https://www.momtestbook.com/)), as well as Cindy Alvarez, Eric Ries and Ivan Zamesin.

Chapter 7 «The Problem Interview» of Ash Maurya's book «Running Lean» (1st edition 2010, 2nd 2012): [O'Reilly](https://www.oreilly.com/library/view/running-lean-2nd/9781449321529/ch07.html). Maurya's handbook is not named.

"Conclusion" and "recommendation of the card's author" are things that are not in the handbook.

## See also

- Followed by In-Depth Interview: Use the script's questions to run each in-depth interview.
- Alternative to JTBD Interview: Use the JTBD interview instead after a recent purchase, to get its decision timeline.
- Followed by Buyer Persona: Write the persona description from the notes the script collected: characteristics, context, values and pains.
- Preceded by Feature Canvas: Use missing problem and customer blocks of the canvas as the interview question list.
- Preceded by Validation Board: Take the riskiest assumption from the Validation Board as the main question to answer.
