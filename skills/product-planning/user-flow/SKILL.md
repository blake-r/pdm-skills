---
name: user-flow
description: Build a user flow (a diagram of the steps a user takes in a product to reach one goal - entry, screens, conditions, end) and produce a one-slide PPTX, or review an existing user flow. Use when a team must agree how a user completes one task (checkout, payment, sign-up, order tracking), when a flow has dead ends or too many steps, or before a design handoff.
---

# User Flow

The theory, notation, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a goal or a product scenario to turn into a flow, **review** when the user brings a finished flow (text, list of steps, description of a diagram).

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and the user: who goes through the flow, in which product;
- the goal as a story "I as a user want X to get Y"; Y gives the end point;
- the entry: where the user comes from;
- the steps the user really takes now, if the flow exists, and where people get lost (usability test, analytics);
- conditions and alternatives that matter for the product logic (payment failure, retry, choice of method);
- who will read the diagram (self, team, development): this sets the detail level.

If the goal covers days or several channels, say that a flow describes minutes to hours in one product and propose to split it into flows with their own ends. Do not invent steps, numbers or findings: mark what the user did not give as unknown.

### 2. End point and entry

Fix the end point first, then the entry. If one path has several results, split it into several flows and name which one is drawn now; list the rest as other flows.

### 3. Steps, backwards

Go from the end to the start and keep only the steps without which the start and the end cannot be connected. A step is a screen or a change of state on the same screen. Write each step as "screen - user action"; a system reaction goes into the same step.

### 4. Conditions and branches

Mark each condition with two labelled exits. Draw only the branches that matter for the product logic. Show exits outside the interface (courier, call to an operator) as such.

### 5. Read the flow

Name dead ends, repeated steps, steps with no clear next move. Propose changes (merge, remove, move) and say how to check them: a repeat test with the same tasks and what is timed or counted. The diagram shows order, not whether an element is noticed: say that this is checked only on people.

### 6. Show, then write

Show the flow in chat first as a table by template blocks: title, goal, boundaries, entry, steps, condition, the "no" branch, end, other flows, problems, decision, check. Write a file only after the user confirms. Ask for the output path (default `user-flow-<product>.pptx` in the working directory). Save the data as JSON. The example is the Mama Mia case from card.md; the diagram in the source is not described in text, so the flow is rebuilt from the steps the article names and is drawn as a line, without a condition (the choice of delivery or pickup is a widget on the home screen and is repeated at checkout; the article shows no branch):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Mama Mia: ordering food in the app",
    "goal": "Order food and check the order status",
    "scope": ["Entry: app launch", "End: order status page", "Tracking flow drawn separately"],
    "start": "App launch",
    "s1": "Preloader and onboarding (2 steps)",
    "s2": "Home: pickup/delivery widget, menu",
    "s3": "Menu: dish card, cart",
    "s4": "Checkout: address, time, payment, points, status page",
    "end": "Order status page",
    "cond": null,
    "alt": null,
    "other": ["Order tracking: entry via the home widget or the personal account"],
    "issues": ["The pickup/delivery selection window on entering the menu got in the way", "The order widget went unnoticed", "The wording of the time choice was not understood"],
    "decision": ["Pickup/delivery choice kept, moved to the widget and onboarding", "Checkout split into 5 steps", "Widget highlighted with a background-dimming animation"],
    "check": ["Repeat test: task time -70%", "Number of participants and before/after times not given", "Diagram not described in the article text"]
  }
}
```

A list of strings becomes lines. Limits that fit the rendered slide: title under 60 characters; goal under 70; scope, other: up to three items under 50; start, end under 30; s1, s2, s3, s4 under 60; cond (optional diamond after s3) under 40; alt under 50; leave cond and alt null to drop the branch; issues, decision, check: up to three items under 55. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/user-flow.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint. The template has an optional condition after the third step; for more, split the flow or list the extra conditions in chat and in "other".

## Mode: review

Take the user's flow in any form (diagram description, list of steps, file) and check it against the common mistakes in card.md:

1. There is no end point, or it is vague, and the flow grows to the whole product.
2. Only the happy path is drawn: failures, empty states, retries are missing.
3. The flow is drawn from the intended design, not from observation of people.
4. Every screen is a step, and changes of state on the same screen are lost.
5. The detail level does not fit the reader (a development-level diagram for a discussion or a sketch for handoff).
6. All branches are drawn, including rare exceptions.
7. The symbols have no legend.

Items 2 and 3 usually cannot be judged from the diagram alone: ask what failures are possible and whether the flow was checked in a usability test or with analytics, instead of reporting a finding. Also check that every condition has two labelled exits, that entry is marked and that exits outside the interface are shown. Report findings as a numbered list: what is wrong, why it matters, the concrete change to the flow. End with a verdict: "flow is ready", "works after changes" or "needs an end point and steps first".

Example: a checkout flow "Cart - Address - Payment - Done" with no failure branch and no entry, built from the spec. Findings: item 2 - ask about payment failure and draw the "no" exit; item 3 - ask whether people tested it; entry is missing - mark where the user comes from. Verdict: "works after changes".
