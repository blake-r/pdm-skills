# Prototyping Process

## Essence

Prototyping is testing a solution on a cheap model before it is built. A prototype is a hypothesis in a form that can be shown to a user: a paper sketch, a static screen mock-up, a clickable sequence of screens, a service that a person performs behind the scenes. The team watches how people work with it and decides: build, rework or drop.

The process is a short cycle:

1. **Hypothesis and question:** what the prototype must show — will people understand it, find it, want it.
2. **Prototype:** the minimum level of detail that answers the question.
3. **Test:** several users perform tasks while the team observes.
4. **Decision:** the solution is changed according to the findings and, if needed, checked again.

The benefit lies in the cost of an error. Jakob Nielsen (2003) cites "the most common estimate": it is "100 times cheaper to make a change before any code has been written".

## When to use and when not to

Use when a solution is expensive to build and it is unclear whether users will understand it. When there are several interface variants and one must be chosen before development. When a new service requires complex back-end machinery and it must first be understood whether it is needed at all.

Do not use for small edits that are cheaper to release and measure. A prototype does not prove demand: "I like it" is not equal to a purchase. Not suitable if real speed or data matter — then a prototype on real data is needed.

Limitations:

- **Detail depends on the question.** A sketch checks structure and scenario, a screen mock-up checks the visibility of elements, a clickable mock-up checks the clarity of the path, a human simulation checks the value of a service without its machinery. An overly detailed prototype is expensive, and it is a pity to throw it away.
- **Few people — but many times.** According to Nielsen's model, five users find about 85% of usability problems; three tests of five people are better than one with fifteen.
- **Different groups — separately.** If audiences differ strongly, 3–4 people from each are taken for two groups and 3 each for three or more.

## Scheme

```
┌────────────┐  ┌──────────────────┐  ┌────────────┐  ┌──────────────────┐
│ HYPOTHESIS │→ │ PROTOTYPE        │→ │ TEST       │→ │ DECISION         │
│ question   │  │ □ sketch         │  │ users      │  │ what we found    │
│            │  │ □ screen mock-up │  │ tasks      │  │ □ go             │
│            │  │ □ clickable      │  │ observe    │  │ □ iterate        │
│            │  │ □ simulation     │  │            │  │ □ drop           │
│            │  │ □ live data      │  │            │  │                  │
└────────────┘  └──────────────────┘  └────────────┘  └──────────────────┘
        ↑___________________ next iteration ____________________│
```

## How to apply

1. **Formulate the hypothesis and the question:** which decision depends on the answer.
2. **Choose the fidelity:** the lowest that answers the question.
3. **Build the prototype:** only the screens and steps of the scenario; everything else can be drawn or simulated by hand. Go through it yourself before the test — a failure of the prototype will ruin the session.
4. **Select participants:** 5 people from the target audience per iteration, not colleagues.
5. **Give tasks without hints:** "order it and pick it up yourself", not "press the pickup button". Observe where people get stuck and ask what they expected.
6. **Record the findings and the decision:** what you change; after the fixes, a new iteration.

## Example

SberMarket (now Kuper), a grocery delivery service, tested on mock-ups a new entry point to ScanPay — paying for purchases in a store through the app.

| Stage | What was recorded |
|---|---|
| Question | is the new location of the entry point more noticeable than the current one |
| Prototype | mock-ups of the current and the new screens; first-click test on the Useberry platform |
| Test | users with different experience; 100 people per variant, each saw one |
| Found: current screen | only a third first clicked the tile "Scan Pay \| Scan"; 61% linked the entry to choosing a store |
| Found: new screen | 46% found the entry point correctly, wrong clicks were noticeably fewer; through the retailer's page — 31% |
| Decision | an additional entry point is needed on the retailer's main page |

In the same article — a moderated test of a pickup prototype in search: six 40-minute sessions with active shoppers. The outcome — recommendations: filters, distance to the store, choice of address and route.

What the case does not include: whether the new entry point was launched and how the use of the service changed; the pickup sessions are listed as 6 tests, but there were 8 participants — 6 women and 2 men.

Case source: S. Dergunov, [«How SberMarket tests simple and complex product hypotheses on real cases»](https://habr.com/ru/companies/kuper/articles/825034/), Habr, 28.06.2024.

## Common mistakes

- **An overly detailed prototype.** A week on pixels, while the question was about the scenario; it is a pity to throw it away.
- **Praise instead of behaviour.** Ten people liked it — this is not proof that they will use it.
- **A hint in the task.** The task words match the button label, and the test checks nothing.
- **Colleagues instead of users.** They know the product and do not get stuck where customers get stuck.
- **A broken prototype.** A transition does not work, and the participant looks for a fault in the prototype, not in the solution.
- **No decision.** A report is compiled, but the mock-up is not changed or checked again.

## Source

K. Pernice, [«UX Prototypes: Low Fidelity vs. High Fidelity»](https://www.nngroup.com/articles/ux-prototype-hi-lo-fidelity/), Nielsen Norman Group, 2016; J. Nielsen, [«Why You Only Need to Test with 5 Users»](https://www.nngroup.com/articles/why-you-only-need-to-test-with-5-users/), 2000; J. Nielsen, [«Paper Prototyping: Getting User Data Before You Code»](https://www.nngroup.com/articles/paper-prototyping/), 2003; M. Cagan, [«Flavors of Prototypes»](https://www.svpg.com/flavors-of-prototypes/), SVPG, 2014.

## See also

- Alternative to Physical Modeling: For solutions in space or in hand, test a physical model instead of screens.
- Preceded by User Flow: Diagram the steps to the goal first, then build only the screens of that flow.
- Enhanced by Single-feature Prototype (Concierge MVP, Wizard of Oz, Third-party product): Prototyping checks understanding of the solution; this one checks whether the need is solved.
