---
name: sequence-diagrams
description: Build or review a sequence diagram of one user scenario — participants with lifelines, messages in order, synchronous vs asynchronous calls, alt blocks for failure branches — and produce a one-slide diagram, or check an existing one. Use when a scenario crosses several systems (payment, bank or payment-service integration, 3-D Secure, SBP, acquiring, notifications), before handing an integration to development, or when the team argues who calls whom and what happens on a timeout or refusal.
---

# Sequence Diagrams

The theory, the notation and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user has a scenario and needs a diagram, **review** when the user shows or describes a finished diagram and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the scenario: who starts it, what counts as the end, what the user wants to get;
- the participants: person, screen or app, internal services, external systems (bank, payment service, notification provider);
- the messages the user already knows, with what is passed and whether the sender waits for the answer;
- what can go wrong at each call to an external system: refusal, no answer, a late notification;
- the decision the diagram must support: a new integration, a change of order, a dispute about who owns a call.

Do not invent participants, messages or numbers: mark what the user did not give as unknown. If the user wants several scenarios in one picture, propose one diagram per scenario.

### 2. Participants and order

Name each participant separately (no single "System" block). Put the initiator on the left and external systems on the right. The template has four lifelines; if the scenario needs more, say which participants were merged and put it in the "gaps" block.

### 3. Messages

List messages top to bottom: from whom, to whom, what is passed. Mark each as a call that waits for an answer, a reply, or an asynchronous notification (webhook, polling). Number them.

### 4. Blocks and failure branches

For every call to an external system ask "what if it refuses or stays silent" and write the branch. The template has one `alt` block with a normal branch and an `else` branch: write the guard conditions in square brackets. If the source does not show the failure branch, say so in the guard and the message text and add it to the "gaps" block instead of making one up.

### 5. Read the result and decide

Say where the sender waits, who learns the outcome first, which branches are missing. Propose one change (remove a participant, make a step asynchronous, add a branch) and what to check after it.

### 6. Show, then write

Show the diagram in chat first as a table: number, from, to, message, kind (call, reply, notification), block. Then the scope, the decision and the gaps. Write a file only after the user confirms. Ask for the output path (default `sequence-diagram-<scenario>.pptx` in the working directory). Save the data as JSON. The example is the Dodo Pizza 2015 case from card.md, folded into the template's four lifelines; the source's steps 2–4 (redirect, card and 3DS, return) are folded, the webhook goes into the guard text, the polling reply is the result message; the source has no failure branch, so the else branch is marked as missing and the gaps block says so:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Dodo Pizza, 2015: online order payment via redirect",
    "p1": "Customer",
    "p2": "Website frontend",
    "p3": "Website backend",
    "p4": "Payment service",
    "m1": "1. Place order",
    "m2": "Place order",
    "m3": "Create payment",
    "m4": "Payment link (then customer redirect)",
    "g1": "[paid: webhook received, order created]",
    "m5": "Payment result (polling reply)",
    "g2": "[not paid: the branch author has none]",
    "m6": "“not paid” — branch needs to be added",
    "m7": "6. Show order page",
    "scope": [
      "Scenario: card payment for an order on the website",
      "Start: customer places an order",
      "End: order page is shown"
    ],
    "decision": [
      "2015: money goes straight from the payment services to franchisees",
      "Later: own forms, customer stays on the site",
      "Later: gateway — payment functions separately"
    ],
    "gaps": [
      "Steps 2–4 and Polling collapsed",
      "No failure branches in the article",
      "No conversion before and after"
    ]
  }
}
```

Limits that fit the rendered slide: title under 60 characters; participant names (p1..p4) under 24; messages (m1..m7) and guards (g1, g2) under 60; scope up to 3 items under 40; decision up to 3 items under 60; gaps up to 3 items under 40. A list of strings becomes lines, one thought per item. An unused message may be left empty or set to "—"; an empty value leaves an arrow without text, so for an arrow that stays say why (for example, that the source has no such branch). Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/sequence-diagrams.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint. Arrow directions follow the scheme in card.md (initiator → app → service → external system, reply, then in `alt` the service answers the app, then the app answers the initiator); if the scenario differs, say so and tell the user to move the arrow ends in PowerPoint.

## Mode: review

Take the user's diagram (image description, PlantUML or Mermaid text, or a list of messages) and check it against the common mistakes in card.md:

1. Only the happy path: no failure, timeout or refusal branches.
2. A single "System" participant hides the boundaries between screen, service and external system.
3. All arrows look the same: a synchronous reply and an asynchronous notification are not told apart, and it is unclear how the result becomes known (webhook or polling).
4. The time axis is read as duration, or durations are drawn by the distance between messages.
5. One picture holds several scenarios, with a dozen lifelines or deeply nested blocks.
6. Data instead of messages: fields and calculation rules are drawn on the diagram, not kept in the API contract.

Items 1 and 3 usually cannot be judged from a bare list of messages: ask what happens when the external system refuses or does not answer, and which messages are notifications, instead of reporting a finding. Also check that the start and the end of the scenario are clear and that each message has an owner. Report findings as a numbered list: what is wrong, why it matters for the integration, the concrete change to the diagram. End with a verdict: "ready for handoff", "works after changes" or "needs participants and failure branches first".

Example: a diagram of a card payment with participants "Client", "System", "Bank", every arrow solid, and no branch after "Request to bank". Findings: item 2 — split "System" into app and service; item 3 — mark the bank's result as a notification and say how it arrives; item 1 — add an `alt` block for refusal and no answer. Verdict: "needs participants and failure branches first".
