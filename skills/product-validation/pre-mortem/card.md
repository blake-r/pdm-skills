# Pre-mortem

## Essence

A pre-mortem is a short team session held before a project starts. The leader tells the team to imagine that the plan has already been carried out and has failed badly, and everyone writes down the reasons why. The reasons are collected into one list, and the plan is changed against them. Gary Klein proposed it as a way to let people voice doubts about a plan that they would not raise in an ordinary review, and to find weak points while they are still cheap to fix.

## When to use and when not to

Use it after the plan exists and before the team commits: at the kickoff of a launch, a migration, a pricing change or a large feature. Inputs: a written plan that every participant has read, and the people who know the work (engineering, support, sales, operations), not only the plan's author.

Limitations:

- **It checks a plan, it does not produce one.** Without a concrete plan the reasons turn into a generic risk list.
- **Imagined failure is not evidence.** The list is a set of hypotheses. A reason that sounds plausible may never happen, and the real cause may be missing from the list.
- **Seniority distorts it.** If the sponsor speaks first or comments on the reasons, juniors stop writing candidly.
- **The 30% figure is about quantity.** The 1989 study behind "prospective hindsight" (imagining the event as already happened) found that people produced about 30% more reasons; it did not measure how correct the reasons were.
- **Do not use it** when the decision is already made and cannot change, or as a ritual after which nothing in the plan moves.

## Scheme

```
Plan briefing → "It has failed" → Silent writing → Round-robin list → Changes to the plan
   (leader)       (leader)        (each, 2 min)   (one reason each)   (owner, then revisit)

| # | Reason it failed | Change to the plan |
```

## How to apply

1. **Prepare.** Invite 6-12 people who know the plan and the work. The leader presents the plan briefly. Plan 20-30 minutes.
2. **Announce the failure.** The leader says: the plan has been carried out and the outcome is a disaster. This is stated as a fact, not as "what might go wrong"; Klein's point is that the certainty of failure makes people produce more reasons.
3. **Write silently.** Each person writes down every reason for the failure for about two minutes, including ones that are politically awkward.
4. **Collect the list.** Go round the room; each person reads one reason, the leader or project manager goes first to set the tone of candour, and each reason goes on a board. Repeat until all are recorded. Do not discuss or defend reasons in this step.
5. **Choose what matters.** Group duplicates. Klein's later variant has the team rate each reason by likelihood, impact and ease of prevention; use any scale agreed in advance.
6. **Change the plan.** For each reason you take up, write a change: a prevention, a check, a trigger to stop, an owner. Reasons you cannot prevent get a response plan.
7. **Decide and revisit.** Record whether the plan goes ahead, changes or stops. Return to the list at milestones.

Interpretation: the result is the revised plan and a decision, not the list itself. A list with no changes means the session failed.

## Example

A subscription-app consultancy (RevenueCat blog, May 2026) describes a quick pre-mortem it ran for a client before launching a new subscription tier, in 2025. The client is not named.

Reason named: existing customers might feel cheated if new customers get a better deal. The team could not remove the risk, because the new tier had to offer more value to reach customers who were priced out.

Changes: position the existing tier, not only the new one; add a relevant feature to the higher tier to limit cannibalization; tell existing customers about the tier in advance; prepare answers for support.

Decision and result: the tier was launched with these changes. The author reports fewer complaints than expected, a small rise in support tickets from customers who missed the updates, and a significant rise in monthly recurring revenue (MRR).

What the case lacks: the article shows only this one reason, not the full list, who took part, or the session format, and it gives no figures. The form is reconstructed from the described reason, changes and decision; the other rows of the template are N/A.

Case source: D. Tideman, [«How to run a pre-mortem for your subscription app»](https://www.revenuecat.com/blog/growth/subscription-app-pre-mortem), RevenueCat blog, 8.05.2026.

## Common mistakes

- **Asking "what could go wrong".** Klein contrasts this with assuming the project has already died; the plain question yields fewer and more cautious reasons.
- **Discussing while collecting.** Debating each reason makes people hold back the next one.
- **The sponsor speaks first or last.** Seniority silences the dissenters the method is meant to hear.
- **Running it too late.** After the budget and promises are fixed, no reason can change the plan.
- **A list without owners.** Reasons that do not become a change, an owner and a date are forgotten.
- **Treating the list as complete.** It holds only what the room could imagine; revisit it as facts arrive.

## Source

G. Klein, [«Performing a Project Premortem»](https://hbr.org/2007/09/performing-a-project-premortem), Harvard Business Review, September 2007 (vol. 85, no. 9, pp. 18-19). The HBR page shows only the summary; the session steps above follow Klein's own later description: G. Klein, [«The pre-mortem method»](https://www.psychologytoday.com/ie/blog/seeing-what-others-dont/202101/the-pre-mortem-method), Psychology Today, 2021. The 30% figure is from D. Mitchell, J. E. Russo, N. Pennington, «Back to the future: temporal perspective in the explanation of events», Journal of Behavioral Decision Making, 1989, as cited by Klein. Experimental test: Veinott, Klein, Wiggins, 2010 (178 students, a hypothetical plan). There is no description in PAF (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, undated); the card is built from the author's sources.

## See also

- Preceded by Project Canvas: the canvas gives the written plan that the team then imagines as failed.
- Followed by Experiment Card: turn the most dangerous reasons into hypotheses with a test.
- Enhanced by Retrospective Meeting: compare the predicted reasons with what actually went wrong.
- Alternative to SWOT Analysis: SWOT lists threats in general; the pre-mortem finds them for one specific plan.
