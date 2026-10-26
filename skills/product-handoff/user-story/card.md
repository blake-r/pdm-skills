# User Story

## Essence

A user story is a short description of what a specific person needs and why, written in their language rather than the language of implementation. The classic template:

> **As a** <role>, **I want** <action or capability>, **so that** <benefit>.

The template is attributed to Rachel Davies of the British company Connextra, early 2000s; it spread widely through Mike Cohn's book "User Stories Applied", 2004. The original Connextra text is not preserved in open access.

Ron Jeffries described three aspects of a story:

1. **Card:** a couple of lines so that everyone remembers what it is about. It is not the whole requirement, but a reminder of it.
2. **Conversation:** the details are discussed together by the customer and the team.
3. **Confirmation:** acceptance criteria — checks that show the story is done.

Criteria are conveniently written as examples in the form "Given — When — Then": state, action, observable result.

## When to use and when not to

Use it when the team needs to understand the need and agree on the boundaries of the work before development starts, and when a requirement could easily be understood in different ways.

Do not use it for purely technical work without a user — a library upgrade, a server move: a forced role only masks the task. A story is not written to carry a full specification: the card remains a short prompt for discussion.

Limits:

- **A story is not a contract.** The details arise in the conversation; without it the card leaves too much room for interpretation.
- **Size.** According to Bill Wake, a good story takes no more than a few person-weeks; for many teams, a few person-days.
- **"I want" can be inaccurate.** Cohn gives an example: nobody wants to enter a complex password — this is a requirement on the role, not its desire.

## Scheme

```
FRONT                               BACK
┌──────────────────────────┐      ┌────────────┬───────────────────────────┐
│ AS A    role             │      │ Notes from │ Acceptance criteria       │
│ I WANT  action           │      │ the talk   │ # │ Given │ When │ Then   │
│ SO THAT benefit          │      │            │ 1 │ …     │ …    │ …      │
├──────────────────────────┤      │            ├───────────────────────────┤
│ Team estimate            │      │            │ INVEST: I N V E S T  ✓   │
└──────────────────────────┘      └────────────┴───────────────────────────┘
```

INVEST is Wake's checklist: independent, negotiable, valuable, estimable, small, testable.

## How to apply

1. **Name the role:** a concrete segment, not "user".
2. **Write the goal and the benefit** in the words of this role, without a ready solution. Cohn calls the "so that" part the most important, though not mandatory: knowing why helps the team decide how best to build the feature.
3. **Discuss with the team:** what is included, what is not, which questions are open; the answers go into the notes.
4. **Write the acceptance criteria** in the form "Given — When — Then", including errors and default cases.
5. **Check against INVEST.** If "small" or "estimable" fails, split the story together with the team: according to Cohn, a product owner who splits a story alone usually splits it badly.
6. **Estimate** and record the team's estimate.

## Example

GOV.UK Pay is the UK government service through which public bodies accept online payments. At a quarterly retrospective the team found that stories were incomprehensible without context, work was being redone, and delivery was slower than wanted. The cause was seen in stories that left too much room for interpretation.

| Stage | What was recorded |
|---|---|
| Feature | a connected service creates a payment in Welsh |
| Criterion "before" | the service can pass a language property with a supported code (English or Welsh) — the payment is created in that language |
| Open questions | which codes are supported, in what format, what error is returned for an unsupported code, what if no code is passed |
| Criterion 1 "after" | Given: the service sends a request to create a payment. When: "language": "cy" in the request. Then: the payment is created with Welsh language |
| Criterion 2 | When: no language property. Then: the payment is created in English |
| Criterion 3 | When: "language": "cym". Then: the payment is not created; a 422 response and an error text about the allowed values |

Decision: write stories and criteria with the whole team before work starts, go through them in meetings, make stories smaller. Result, in the authors' words: estimates became more reliable, stories no longer had to be rewritten, and the same questions stopped being discussed again.

What the case lacks: the wording "As…, I want…" itself and any numbers — neither deadlines nor the share of rework. The service is governmental, although by function it is a payment service.

Case source: K. Bates, A. Bishop, [“How GOV.UK Pay used Behaviour Driven Development to improve delivery times”](https://technology.blog.gov.uk/2019/07/29/how-gov-uk-pay-used-behaviour-driven-development-to-improve-delivery-times/), GDS, 29.07.2019.

## Common mistakes

- **"As a user".** The role is not named, and it is unclear whose need is being addressed.
- **No "so that".** Without a benefit the team builds what is literally written, not what is needed.
- **Solution instead of need.** "Add a button" instead of what the person wants to achieve.
- **Vague criteria.** Errors and default cases are not described — as in the "before" criterion at GOV.UK Pay.
- **A story that is too large.** It cannot be estimated or finished in a short time.
- **A card without a conversation.** The story is handed over as a finished task, and details surface in the middle of development.

## Source

R. Jeffries, [“Essential XP: Card, Conversation, Confirmation”](https://ronjeffries.com/xprog/articles/expcardconversationconfirmation/), 2001; B. Wake, [“INVEST in Good Stories, and SMART Tasks”](https://xp123.com/invest-in-good-stories-and-smart-tasks/), 2003; M. Cohn, "User Stories Applied", Addison-Wesley, 2004; M. Cohn, [“User Story Template: What It Is and Why It Works So Well”](https://www.mountaingoatsoftware.com/agile/why-the-three-part-user-story-template-works-so-well); D. North, [“What's in a Story?”](https://dannorth.net/blog/whats-in-a-story/).

## See also

- Alternative to Use Case: Choose a use case when the path has many steps, failures and external systems.
- Followed by Story Mapping: Place the written stories on a two-dimensional map to cut them into releases.
- Enhanced by Definition of Done: Keep acceptance criteria for this story's behaviour; Definition of Done covers shared conditions.
- Enhanced by Product Backlog: Write ordered backlog items as stories, so the top items are detailed first.
- Enhanced by State Modelling: Write the acceptance criteria for each state transition as Given, When, Then.
