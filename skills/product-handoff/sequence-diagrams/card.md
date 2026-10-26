# Sequence Diagrams

## Essence

A sequence diagram shows which messages the participants of a system pass to each other when one user scenario runs, and in what order. Participants stand in a row, each with a vertical lifeline, and time runs from top to bottom. Teams use the diagram to agree on the boundaries between the screen, the services and the external systems.

## When to use and when not to

Use it when a scenario has three or more participants and the result depends on the order of calls: payment, integration with a bank, confirmation of an operation. Inputs: the scenario, the list of systems, the documentation of external APIs (application programming interfaces).

Do not use it:

- **For logic with many branches.** In nested condition blocks the order cannot be read.
- **For data.** The UML (Unified Modeling Language) 2.5.1 standard, Interactions section: interactions are not focused on data processing; data only labels the messages.

Limits:

- **Time is not measured.** The distance between messages does not equal duration: it is only known that a message was sent first and received later.
- **Not the whole history.** The standard: permissible chains of messages usually exist outside the diagram. One diagram — one scenario.

## Scheme

```
Client      Screen       Service      Bank
  │ 1 request │            │            │
  │──────────>│ 2 call     │            │
  │           │───────────>│ 3 request  │
  │           │            │───────────>│
  │           │            │<┄┄┄┄┄┄┄┄┄┄┄│ 4 reply
┌─alt [success]────────────────────────────┐
│ │           │<───────────│ 5a result    │
├─[else: refusal or no answer]─────────────┤
│ │           │<───────────│ 5b reason    │
└──────────────────────────────────────────┘
  │<──────────│ 6 outcome  │            │
```

UML 2.5.1 notation: a filled arrow is a synchronous message (the sender waits), an open arrow is asynchronous, a dashed line is a reply. The `alt` block is a choice: no more than one branch is executed depending on the condition, `else` covers all other cases. `opt` — a step may not be executed, `loop` — repetition, `par` — parallel branches.

## How to apply

1. **Choose one scenario** and fix its start and end.
2. **Name the participants:** person, screen, internal services, external systems. The initiator on the left, external systems on the right.
3. **List the messages top to bottom.** For each: from whom, to whom, what is passed. Mark whether the sender waits for a reply (synchronous) or not (asynchronous, for example a notification from the bank).
4. **Add the blocks.** For every call to an external system ask "what if it refuses or stays silent?" and draw the branch in `alt`. Optional steps go in `opt`, repetitions in `loop`.
5. **Number the messages** and walk through the diagram aloud with a developer: each has an owner and a contract.
6. **Read the result:** where the sender waits, who learns the outcome first, which branches are missing. Decision: remove a participant, make a step asynchronous or add a branch; record the "before" and "after".

Also drawable as text: [PlantUML](https://plantuml.com/sequence-diagram), [Mermaid](https://mermaid.js.org/syntax/sequenceDiagram.html).

## Example

Dodo Pizza, online ordering. Dmitry Kochnev presents two payment diagrams.

**2015, payment via redirect (transfer to the service's page).** Participants: Client, the website's Frontend and Backend, Payment service. Messages: "Create payment", "Payment link", redirect to the service, entering the card and 3DS (3-D Secure, payment confirmation by the issuing bank), redirect back, a webhook (notification from the service) with the result, order creation. The "Polling" block (periodic querying): the frontend asks the backend about the result. Decision: money does not accumulate in the company's accounts; franchisees receive it directly from the payment services.

**Global website, payment by a new card.** Decisions: own card-entry forms, so that the client does not leave the app (the author expected conversion to grow), and a payment gateway (requirements: do not store card data, put the payment functions in a separate service). Two participants were added, the gateway's Frontend and Backend, and blocks: "If CST" (tokenization on the client side: the card is sent to the payment service, which returns a token) or "If CSE" (encryption on the client side), "Optional" twice (creating a payment at the payment service; redirect to 3DS), "Polling".

What the case lacks: branches for payment refusal in both diagrams, conversion before and after. The reasons for the decisions are given from the author's words. For 3DS the client still leaves the site.

Case: D. Kochnev, [“How internet payments work at Dodo”](https://habr.com/ru/companies/dododev/articles/709598/), Dodo Engineering blog on Habr, 09.01.2023.

## Common mistakes

- **Only the happy path.** No refusal and timeout branches. In the case, the design document covered only the old redirect payment and did not account for the new methods.
- **A participant "System".** The boundaries are not visible, and the owner of a call cannot be disputed.
- **All arrows identical.** A synchronous reply and an asynchronous notification must be told apart: for the latter, decide how the outcome is learned (webhook or polling).
- **The time axis read as duration.** The standard does not set a scale: waiting time has to be measured separately.
- **One picture for all scenarios.** A dozen lifelines are unreadable: split by scenario.
- **Data instead of messages.** Fields are described in the API contract.

## Source

PAF description (Product Architecture Framework; Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, undated): sequence diagrams display the information that the objects or processes of a system pass to each other when a user scenario runs; the order of message passing is set by a timeline.

Primary source of the notation: the OMG (Object Management Group) consortium, [UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/About-UML), December 2017, document formal/17-12-05, section 17 "Interactions", subsection 17.8 "Sequence Diagrams" ([PDF](https://www.omg.org/spec/UML/2.5.1/PDF)). M. Fowler, [“UML Distilled”](https://martinfowler.com/books/uml.html), 3rd edition, Addison-Wesley, 2003: a short guide to the main UML diagrams.

## See also

- Preceded by Screen Map: Take screen transitions from the map as user messages, then add services and bank.
- Preceded by Use Case: Build from the main scenario, drawing each extension as an alt branch.
- Enhanced by State Modelling: Draw messages that fire state transitions, so call order matches allowed states.
- Enhanced by Service Blueprint: Detail the blueprint's system layer as the messages between services.
- Preceded by User Flow: Show the messages behind each step once the flow fixes the user's steps.
