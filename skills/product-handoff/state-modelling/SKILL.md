---
name: state-modelling
description: Model the states of one entity (order, payment, loan application, KYC check, return) as a state diagram — states, transitions with event, condition and action, start and final states, and a list of forbidden transitions — and produce a one-slide state model, or review an existing status model. Use when statuses are unclear or scattered across code, a status change breaks something, or a team must agree on what statuses an order, payment or application can have.
---

# State Modelling

The theory, the notation and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user needs a state model built or changed, **review** when the user shows an existing status list, table or diagram and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the entity and the system it lives in (order in a shop, payment, loan application, KYC check);
- when it is created and when it counts as finished;
- the statuses that exist today, if any, and what each means;
- the events that change it: user actions, answers of external systems, timeouts;
- who or what moves it on from each state;
- what goes wrong now: wrong statuses, impossible combinations, status changed from many places.

If the user describes a sequence of steps with branches and no status of an object, say that the card applies to the life cycle of one entity and ask which entity it is. Do not invent states, events or numbers: mark what the user did not give as unknown.

### 2. States

List states as stable positions where the entity waits for an event ("paid", not "payment"). Write one phrase per state about what it means for the customer. Split a state that hides different allowed actions. Mark the start and the final states.

### 3. Transitions

For every transition write `event [condition] / action`. Say who sends the event. Cancellation and return are usually possible from several working states: check them.

### 4. Forbidden transitions

Write pairs "from → to" that must never happen and the reaction of the system (reject with a code, log, manual review). Write them as rows "from → to → reaction". Remind that a UML diagram does not draw them: an event with no transition is discarded.

### 5. Completeness and the decision

For every pair state and event the answer is "transition" or "forbidden". Name states without an exit, except final ones. State where the model is fixed (code, table of transitions) so that a status changes only through it, and what was decided.

### 6. Show, then write

Show the model in chat first as a table by template blocks: title, entity, scope, states (up to six on the main chain plus final, one alternative state and one final failure), transitions, forbidden, gaps, decision. Write a file only after the user confirms. Ask for the output path (default `state-model-<entity>.pptx` in the working directory). Save the data as JSON. The example is the Domclick case from card.md. State meanings ("Ordered" and the like) are our reading of the status names: the article defines none, say so in chat. Notifications fire on entering the target state (notify_manager on Paid, Completed, Cancelled; notify_client on Shipped), so they sit on the incoming transition. Fields the source does not give say so:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Online store order: status model (Domclick, 2021)",
    "entity": "Order: created as New, ends as Completed or Cancelled",
    "scope": "9 statuses, 12 transitions in three directions (NEXT, RETURN, CANCEL)",
    "start": "order creation",
    "s1": "New: order created",
    "s2": "Ordered: placed; responsible manager",
    "s3": "Reserved: goods reserved",
    "s4": "Paid: paid; responsible warehouse keeper",
    "s5": "Shipped: dispatched; responsible driver",
    "s6": "Delivered: delivered to the customer",
    "e1": "Completed: processing finished",
    "s7": "Returned: order returned",
    "e2": "Cancelled: order cancelled",
    "t1": "DIR_NEXT",
    "t2": "DIR_NEXT",
    "t3": "DIR_NEXT, notify manager",
    "t4": "DIR_NEXT, notify client",
    "t5": "DIR_NEXT",
    "t6": "DIR_NEXT, notify manager",
    "t7": "DIR_RETURN",
    "t8": "return to Ordered: DIR_NEXT",
    "t9": "DIR_CANCEL, notify manager",
    "tc": "DIR_CANCEL from Ordered, Reserved, Delivered; notify manager",
    "forbidden": ["No explicit list in the article", "Not in the scheme → reject “Transition was not performed”", "From Completed, Cancelled → reject “Request processing is complete”"],
    "gaps": ["No conditions (guards) on transitions", "Actions shown only as notifications and responsibility", "No DIR_FAIL transition in the scheme"],
    "decision": ["The process scheme is set up as a JSON schema and stored in code", "Status changes are made by a single Workflow class, not scattered code", "A new status is added by editing the schema"]
  }
}
```

The template fits a main chain of six states (s1..s6) and a final success state (e1), one alternative state (s7) with a return arrow to s2 (t7 down, t8 back) and a final failure state (e2) fed by s7 (t9) and by a cancellation from several states (tc: label the arrows with the event and the source states). Leave unused slots empty (null or omit the key). Limits that fit the rendered slide: title under 70 characters; entity and scope under 80; state text (s1..s7, e1, e2) under 50; transition labels t1..t6 under 30, t7 under 30, t9 under 35, t8 under 55, tc under 70 (two lines above the cancellation arrows), start under 25; forbidden, gaps and decision: up to three items under 70 each. A list of strings becomes lines, one thought per item. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/state-modelling.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's status list, table of transitions or diagram and check it against the common mistakes in card.md:

1. Status is a set of flags: "paid", "shipped", "returned" are separate fields, so impossible combinations exist.
2. A catch-all state ("in progress") hides positions with different allowed actions.
3. States are named as actions ("payment") instead of positions ("awaiting payment", "paid").
4. There are no final states, or arrows leave a final state.
5. Cancellation and return are missing: only the happy path is drawn.
6. Forbidden transitions are not described: the event is silently lost.
7. The scheme exists only as a picture: the code behaves differently and the diagram is out of date.

Items 1, 2, 3 and 6 are the card author's practice, not claims of the sources: phrase them as advice. Items 1, 6 and 7 usually cannot be judged from the description alone: ask how the status is stored, what happens on an event with no transition, and where the scheme lives, instead of reporting a finding. Also check that the start state, the entity and the event with condition on each transition are given. Report findings as a numbered list: what is wrong, why it matters for the entity's life cycle, the concrete change to the model. End with a verdict: "model is complete", "works after changes" or "needs states and events first".

Example: statuses "new, in progress, paid, shipped, done" with no cancellation, no list of events and stored as a free text field. Findings: item 2 — "in progress" hides picking and waiting for payment, split it; item 5 — no cancellation or return, add them with the states they are possible from; item 6 — ask what the system does when "shipped" is set on a new order; item 7 — ask where the allowed changes are enforced. Verdict: "works after changes".
