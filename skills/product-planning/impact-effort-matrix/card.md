# Impact / Effort Matrix

## Essence

The impact–effort matrix lays out ideas, features or tasks along two axes: what business effect the idea will bring (Impact) and how much effort its implementation will take (Effort). Four quadrants set the order: first quick wins, then major projects, then fill-ins; thankless tasks are not taken on.

## When to use and when not to

Use it when you need to agree on the order of 10–30 ideas in one meeting and show the decision visually: quarterly planning, reviewing a list of tasks after research, choosing improvements after a funnel audit. The method is cheap and understandable to people outside the product team: everyone sees where their idea landed and why.

Inputs: a list of ideas, one goal or metric, rough effort estimates from the team, and what is known about the possible effect of each idea.

Limitations:

- **Two axes are not the whole truth.** The matrix does not account for confidence in the estimate, risks, dependencies or urgency. An idea with a loud but unproven effect looks like a quick win.
- **The borders are conditional.** Points near the midlines fall into the neighboring quadrant after a shift of one point; a decision on them requires discussion, not just reading the quadrant.
- **Scores are subjective.** Without agreed scales, "effect 8" means different things to different people.

## Scheme

A 2×2 matrix: vertically — business effect, horizontally — implementation effort; both axes run from 0 to 10, with the quadrant borders at the middle of the scale.

| | Little effort | Much effort |
|---|---|---|
| **High effect** | Quick wins — 1st priority | Major projects — 2nd priority, plan separately |
| **Low effect** | Fill-ins — 3rd priority, when there is spare time | Thankless tasks — do not take on |

## How to apply

1. **Fix the goal.** One metric or task against which the effect is assessed.
2. **Collect the ideas.** Each one is a separate change, understandable without explanation. For example, "a pinned registration button on mobile", not "improve the mobile version".
3. **Agree on the scales.** What 0, 5 and 10 mean for effect and for effort. Count effort for the whole team: design, development, testing, launch.
4. **Score each idea** on the two axes from 0 to 10. It is better if participants first score silently and independently, and then discuss the discrepancies.
5. **Place the points** on the matrix and read the quadrants.
6. **Discuss the border points.** Ideas near the midlines are discussed separately: what would shift the score, whether the effort can be reduced by splitting the idea into parts.
7. **Make the decision.** Quick wins go into work now. Major projects go into the plan with a separate deadline, no more than one or two at a time: one major project displaces many quick wins. Fill-ins go into reserve or are delegated. Thankless tasks are struck out or reformulated.

## Example

Booking.com, Partner Hub — a platform for the site's partners: from registering a property to running a business on Booking.com. The experiment team with the main metric "clicks on the start of registration" selected ideas by impact on the business, supporting data and ease of implementation — two of the three criteria match the matrix axes. The source does not mention an impact–effort matrix, and neither scores nor placement of the ideas are published, so the matrix itself cannot be shown.

Among the tested ideas were changes to the "Join now" page:

- a sticky panel with a registration button on the mobile version — +36% clicks on the start of registration from mobile;
- moving the description of the registration steps higher on the page — no growth in conversion;
- button texts: "Start registration" worked best, while "Sign up today" reduced clicks by about 10%.

Decision: the sticky panel was rolled out to all users.

Source of the case: [Booking.com Partner Hub — Mobile Momentum (AB Tasty / Wingify, customer story)](https://wingify.com/success-stories/booking-com-partner-hub-mobile-growth/).

## Common mistakes

- **Everything is a quick win.** The team optimistically underestimates effort, and the right half of the matrix stays empty. Check the effort estimates with the people who will do the work.
- **Effect without a goal.** Ideas are scored by "importance in general", and the effects are incomparable.
- **Major projects are postponed forever.** The matrix favors the easy; without a separate place in the plan, strategic work never starts.
- **The matrix instead of verification.** A high effect is a hypothesis. A quick win with an unproven effect should be launched as a test with a metric.
- **A one-time layout.** After tests and new data the points shift; the matrix is revisited in every planning cycle.

## Source

The author of the method is unknown: MindTools states this directly in its description of the [Action Priority Matrix](https://www.mindtools.com/agst6d0/the-action-priority-matrix/), from which the quadrant names and the 0 to 10 scale are taken. A close variant from Lean Six Sigma is the [PICK chart](https://en.wikipedia.org/wiki/PICK_chart) (Possible, Implement, Challenge, Kill): according to Wikipedia, it was first developed at Lockheed Martin for prioritizing process improvements.

## See also

- Alternative to ICE Scoring: Score ideas with ICE when you need a single ranked number rather than quadrants.
- Preceded by RICE Scoring: Score reach first, then place ideas on the matrix.
- Preceded by Impact Mapping: Build the impact map first, so every matrix idea leads to a goal.
- Followed by Experiment Card: Test an unproven quick win on an experiment card with a preset metric.
- Alternative to Frequency / Adoption Analysis: Rank features by business effect and cost; adoption data shows actual use.
