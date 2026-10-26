# Use Case

## Essence

A use case is a step-by-step description of how a person or an external system (an actor) interacts with a system to achieve their goal. Ivar Jacobson devised it at Ericsson in the 1960s, presented it in 1987 and described it in a 1992 book; later it entered the UML modeling language. The practical template was proposed by Alistair Cockburn in the book "Writing Effective Use Cases", 2001.

Cockburn's full template:

1. **Name:** the actor's goal as a short verb with an object.
2. **Scope and level:** which system is described and the goal level.
3. **Primary actor:** the role that triggers the scenario.
4. **Preconditions and trigger:** what is already true and what starts the scenario.
5. **Main success scenario:** numbered steps from the trigger to the goal; each names who acts.
6. **Extensions:** deviations and failures tied to a step: "3a. card declined: …".
7. **Guarantees:** what is true after success and what is true whatever the outcome.

The UML diagram shows actors, use cases and the relations between them. "include" is a common step that is always performed inside the use case. "extend" is behaviour that is added to a use case under a condition.

## When to use and when not to

Use it when a feature has many steps and participants, including external systems, and failures matter: payment, checkout, refunds; and when requirements are handed to a team that will build and test the system.

Do not use it for a simple feature of one or two actions. A scenario does not establish whether the feature is needed: it records a decision already taken.

Limits:

- **The goal level.** Cockburn calls the user-goal level the main one — "sea level": one task in one sitting. Below it are small subfunctions, above it strategic goals. Once he was sent over a hundred pages of use cases at the subfunction level; they were replaced with six use cases at the user level, and the work became simpler.
- **Precision in layers.** First a list of actors and goals, then the main scenarios, then the list of failures, and only then their handling. Those who write the handling right away often fail to list all the failures.
- **Less is better than more.** Cockburn's advice: of two mistakes — writing too little or writing too much — choose the first.

## Scheme

```
              ┌──────────── system boundary ────────────┐
   actor      │  (UC 1) ◄- -«extend»- - (UC 4)          │
    O ────────┤  (UC 2) - -«include»- -► (UC 5)          ├──── external
   /|\        │  (UC 3)                                 │     system
   / \        └──────────────────────────────────────────┘
Description: name · goal · boundary and level · actor · preconditions ·
trigger · main scenario 1..n · extensions "step+letter" · guarantees
```

## How to apply

1. **List the actors and their goals** at the user level; set priorities.
2. **For each use case, define** the boundary, the level, the actor, the preconditions and the trigger.
3. **Write the main scenario** in 3–9 steps: each step has an acting party, with no buttons or screen fields.
4. **List all failures and deviations** by step, then describe the reaction to each.
5. **Write the guarantees** of success and the minimal guarantee.
6. **Draw the diagram:** common steps go into "include", conditional ones into "extend".

## Example

Russell Walters and Dave Scott of FirePond Corporation gave Cockburn a use case "Research a solution" for an e-commerce site.

| Field | What was recorded |
|---|---|
| "Before" | 8 pages, of which 6 are the scenario and alternatives; two columns "actor — system", 45 numbered steps |
| Actor | Shopper — any arbitrary web surfer |
| Boundary, level | web system; level "Task" |
| Trigger | the customer decides to research a solution |
| Main scenario "after" | 7 steps: the system helps choose the line, model and options, asks questions, records transitions; the customer puts the choice in the cart |
| Extensions | 1a — a request from a partner site carries customer data; 2a — skips the questions; 2d — reaches the point where a sales lead is created; 7d — wants to arrange financing |
| Success guarantee | the customer has zero or more products to buy; the system recorded the choices, transitions and specs |

Decision: remove the interface from the scenario — screens, input order — and describe intentions. Result: the "after" version is four times shorter with the same information. According to Russell Walters of FirePond, all requirements were kept, the text became easier to read, and the design became freer.

What the case lacks: Cockburn rewrote it, not the team; what was built from the scenario and how it affected the product is not stated; the minimal guarantee is not filled in.

Case source: A. Cockburn, [“Writing Effective Use Cases”, draft 1999, pp. 143–152](https://people.inf.elte.hu/molnarba/Informaciorendszerek_ELTE/Writing_effective_Use_cases_Cockburn.pdf).

## Common mistakes

- **Interface in the steps.** "Clicks the button", "types into the field" — the scenario ties the designers' hands and grows.
- **Too low a level.** A separate step for every field: name, address, phone.
- **The actor disappears.** "Accepts the card, checks the balance" — it is unclear who acts.
- **No extensions.** Only success is described; failures surface during development.
- **A forest of small use cases.** Hundreds of pages of subfunctions instead of a few user goals.

## Source

I. Jacobson, "Object-Oriented Development in an Industrial Environment", OOPSLA 1987; I. Jacobson et al., "Object-Oriented Software Engineering: A Use Case Driven Approach", 1992; A. Cockburn, "Writing Effective Use Cases", Addison-Wesley, 2001; OMG, [UML 2.5.1](https://www.omg.org/spec/UML/2.5.1/PDF), 2017, ch. 18; I. Jacobson, I. Spence, K. Bittner, [“Use-Case 2.0”](https://www.ivarjacobson.com/files/use-case_2_0_e-book_2023_0.pdf), 2011.

## See also

- Alternative to User Story: Use a user story for small needs, a use case for multi-step scenarios.
- Followed by Sequence Diagrams: Once the main steps are fixed, draw messages between the system and actors.
- Enhanced by State Modelling: Model the life cycle of the changed entity, so each step has a valid state.
- Enhanced by Entities Analysis: Check that the steps change only entities and relations the analysis defines.
- Enhanced by Product Requirements Document: Write each PRD function as a scenario with actor steps and failure extensions.
- Alternative to Story Mapping: Choose this over a story map when one complex path needs full failure cases.
- Followed by Screen Map: Place the screens.
