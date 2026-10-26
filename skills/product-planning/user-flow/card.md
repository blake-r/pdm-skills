# User Flow

## Essence

A user flow is a diagram of the steps a user takes in a product's interface to reach one goal: from entry to result. In PAF (Product Architecture Framework, an open catalogue of product management tools) it is defined as a "model of the sequence of user interaction with the product's interface to achieve their goal". Nielsen Norman Group (NN/g, a user-experience consultancy) defines a flow as a "typical or ideal set of steps" for a typical task; it shows the user's steps and the system's reactions.

## When to use and when not to

Use it when a team needs to agree how a user reaches one goal in one product: places an order, pays, registers. Inputs: the goal and the result that counts as the end; observations of people (usability tests) or analytics.

Do not use it:

- **For a path lasting days or weeks across several channels.** NN/g: a flow covers goals of "minutes or hours, at the most" in one product; a journey unfolds over days, weeks or months.
- **As the only picture of reality.** A flow shows the typical path; failures and empty states get onto the diagram only if they are drawn.

A nuance: the reader sets the level of detail: a sketch for oneself, medium detail for the team, technical states for development (E. Pliner). A flow does not convey emotions.

## Scheme

```
(Start) → [Screen: action] → <Condition?> —yes→ [Screen: action] → (End)
                                  └—no→ [Screen: other action] ──┘
```

Flowchart conventions (ISO 5807, 1985): an oval — start and end, a rectangle — a step, a diamond — a condition with two exits. An arrow — a transition; a label — the user's action or the system's reaction. There is no single standard for symbols of user flows: give a legend on the diagram.

## How to apply

1. **Name the goal and the end.** Write the story "I as a user want X to get Y"; Y sets the end point. If the path is longer, split it into several flows with their own ends.
2. **Fix the entry.**
3. **Go from the end to the start** and keep only the steps without which the start and the end cannot be connected (Pliner).
4. **Count a screen or a change of state** on the same screen as a step.
5. **Mark conditions** with diamonds and label both exits. Draw the branches that matter for the product logic (payment refusal, a retry).
6. **Show exits outside the interface** (courier, offline pickup).
7. **Check on people.** NN/g: the best way to collect a flow is a usability test; analytics is the second source.
8. **Read the diagram:** merge superfluous steps, close dead ends and gaps. The result is a list of changes to the flow and a repeat test.

## Example

The Focus studio analysed the food-ordering app of the Mama Mia restaurant chain: it designed the order and order-tracking flows and tested new mock-ups on respondents. The tests showed that the "delivery or pickup" selection window on entering the menu got in people's way. On examination, the authors saw that pickup carried a 30% discount, and a survey showed that some of the audience chose pickup and knew about the discount. The step was kept, but moved to a widget at the top of the home screen, explained in onboarding (two introductory screens), and repeated at checkout. Checkout was split into five steps: address, time, payment, points, status page. Some respondents did not understand the time choice; the cause was the wording, which was changed, and the repeat test raised no questions. Tracking got two entries: the widget on the home screen and the personal account. The widget went unnoticed; a background-dimming animation helped. In the repeat test, the time to complete the tasks fell by 70% (measured per task).

What the case lacks: the diagram itself (the flow was reconstructed from the description of the steps, without branches: the article shows no conditions), the number of participants, and the "before" and "after" times. The −70% refers to the whole new interface, not to a single diagram. The rollout by the chain is not described; this is food delivery, neither a marketplace nor fintech.

Source of the case: Focus studio, ["How a UX refinement helped cut the time to complete the food-ordering scenario by 70%. Part 3"](https://habr.com/ru/articles/708222/), Habr, 28.12.2022.

## Common mistakes

- **No end point.** People argue about where the flow ends; the diagram grows.
- **Only the happy path.** A payment refusal, an empty cart, a loss of connection appear only if they are drawn.
- **A diagram from the design, not from observation.** A diagram drawn at a desk does not show where the user gets lost. In the case, the order widget went unnoticed: its visibility showed up only in the test.
- **Every screen is a step.** A change of state on the same screen is a step too; otherwise conditions are lost.
- **Detail not matched to the reader.** A development version is unreadable in a discussion, and a sketch for oneself is no good for development.
- **All branches in a row.** Rare exceptions turn the diagram into a maze.
- **Symbols without a legend.**

## Source

K. Kaplan (NN/g), [«User Journeys vs. User Flows»](https://www.nngroup.com/articles/user-journeys-vs-user-flows/), 16 April 2023: the definition of a flow, its boundaries, the role of the usability test. P. Laubheimer (NN/g), [«Wireflows: A UX Deliverable for Workflows and Apps»](https://www.nngroup.com/articles/wireflows/), 4 December 2016: a flowchart in which screens replace abstract blocks. Flowcharts and notation: [Flowchart](https://en.wikipedia.org/wiki/Flowchart) (F. and L. Gilbreth, 1921; ASME (American Society of Mechanical Engineers), 1947; ISO 5807, 1985). E. Pliner, ["User flow. How to design it and why"](https://habr.com/ru/articles/1081360/), Habr, 11 September (the page shows no year): the order of building from the end. Description in PAF (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, no date).

## See also

- Preceded by Customer Journey Map: Map the path across channels first, then draw the flow for one goal.
- Enhanced by Screen Map: Draw screens and transitions as nodes and arrows, then trace the steps across them.
- Followed by Sequence Diagrams: Once the flow fixes the steps, show the messages exchanged behind each step.
- Followed by Prototyping Process: Build only the screens of this flow for the prototype.
- Followed by Physical Modeling: Turn the mapped steps into the scenarios run on the physical model.
