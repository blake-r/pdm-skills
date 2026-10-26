# State Modelling

## Essence

State modelling describes the life cycle of one entity (an order, a payment, a loan application): the states it can be in, how it moves from one to another, and what happens on entry. The result is a state diagram (a finite-state machine model: a finite set of states and the transitions between them) with the rules that determine when a transition is allowed.

## When to use and when not to

Use it when the entity's status determines what can be done: showing a "Cancel" button, refunding money, calling a courier. You need: the events that change the entity, and an owner for each state.

Do not use it for reference data or for algorithms made of steps.

Limits:

- **One status — one entity.** An order, a payment and a delivery each live by their own scheme; a shared status such as "order paid and on its way" produces a combinatorial explosion. Move parallel parts into separate machines.
- **A forbidden transition is not drawn.** Under the UML (Unified Modeling Language) specification, if there is no suitable transition for an event in the current state, the event is simply discarded. Forbidden transitions are therefore written down separately, together with the system's reaction.

## Scheme

```
(●) ──event [condition] / action──▶ [State A] ──event──▶ [State B] ──▶ ((End))
                                          │
                                          └──event [condition]──▶ [State C] ──▶ ((End))
● start · [ ] state · (( )) final · arrow — transition
Template slide: entity and scope at the top, diagram in the centre, below: blocks "Forbidden transitions" (rows "from → to → reaction"), "Assumptions", "Decision"
```

## How to apply

1. **Name the entity**, the moment of its creation and the moment of its completion.
2. **List the states** as stable positions in which the entity waits for an event: "paid", not "payment". For each — what it means for the customer.
3. **Collect the events**: customer actions, system responses, expiry of time.
4. **Draw the transitions** in the format "event [condition] / action". The condition (guard) is a check; if it is false, the transition does not fire. The action is what the system does.
5. **Mark the initial** (black circle) and the **final** (circle within a circle) states. There are no transitions out of a final state.
6. **List the forbidden transitions** and the reaction: rejection with a code, a log entry, manual review.
7. **Check completeness:** for every pair "state, event" the answer is "transition" or "forbidden".
8. **Fix the scheme** in code or in a transition table: the status changes only through it.

## Example

Domclick, a blog post on Habr, 2021: tech lead Mikhail Gulyaev walks through the order status model of an online store. There are nine statuses: New, Ordered, Reserved, Paid, Shipped, Delivered, Completed, Returned, Cancelled (translations of the status names are ours). The main path runs from New to Completed along the NEXT chain. In total there are 12 transitions in three directions: forward (NEXT), return (RETURN), cancellation (CANCEL). From Ordered, Returned and cancellation are possible; from Reserved and Delivered, cancellation; from Returned, back to Ordered or to cancellation. Completed and Cancelled are final. Some states have an owner; notifications to the manager (Paid, Completed, Cancelled) and to the client (Shipped) fire on entering the state.

The author calls the worst option a solution where status changes are "smeared" across the code, with no overall picture. The decision taken: describe the process as a text scheme in JSON format in the code and change the status only through a single Workflow class. An event with no transition in the scheme is rejected, and no step is possible from a final state. A new status is added by editing the scheme.

What the case lacks: conditions on transitions, a list of forbidden transitions, and the results of the implementation; the example illustrates the approach, not an analysis of a product change.

Case source: M. Gulyaev, [“Implementing a finite-state machine to automate processes”](https://habr.com/ru/articles/545540/), Domclick blog on Habr, 25.03.2021.

## Common mistakes

- **Status as a set of flags.** "Paid", "shipped", "returned" are stored in separate fields: impossible combinations become possible.
- **Catch-all state.** "In processing" merges different positions with different allowed actions.
- **Action-states.** "Payment" instead of "awaiting payment" and "paid".
- **No final states,** or arrows leave them: the entity "comes back to life" and breaks reporting.
- **Cancellation and return forgotten:** only the happy path is drawn.
- **Forbidden transitions not described:** the event is lost silently.
- **The scheme exists only as a picture:** the code behaves differently.

## Source

D. Harel, [“Statecharts: A Visual Formalism for Complex Systems”](https://doi.org/10.1016/0167-6423(87)90035-9), Science of Computer Programming, vol. 8, no. 3, June 1987, pp. 231–274: state diagrams with hierarchy, concurrency and communication; Object Management Group, [“Unified Modeling Language 2.5.1”](https://www.omg.org/spec/UML/2.5.1/), December 2017, section State Machines: notation of initial and final states, the transition format "event [condition] / action"; M. Fowler, "UML Distilled: A Brief Guide to the Standard Object Modeling Language", 3rd ed., Addison-Wesley, 2003 (copyright 2004), ch. 10 "State Machine Diagrams" ([table of contents](https://www.informit.com/store/uml-distilled-a-brief-guide-to-the-standard-object-9780321193681)); PAF description ([page](https://productframework.ru/activities/business_logic_design), Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, undated): possible states of entities, transitions between them, and what happens on entering a state. The advice in "Limits" and "Common mistakes" (one status per entity, flags, catch-all state, action-states, recording forbidden transitions separately) is the card author's practice; it is not in the sources. In the Order class of the article there is a paid field next to status.

## See also

- Enhanced by Use Case: Take the failures listed in the use case extensions as candidate events and forbidden transitions.
- Enhanced by Sequence Diagrams: Use messages between participants to show which events change the state, and in what order.
- Enhanced by User Story: Write the acceptance criteria for each transition as Given, When, Then.
- Enhanced by Screen Map: Check screens showing this entity against its states, covering loading, empty and error views.
- Preceded by Entities Analysis: Describe the states and transitions of one entity from the model.
