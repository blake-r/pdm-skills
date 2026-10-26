# Product Requirements Document

## Essence

A PRD (Product Requirements Document) is a written description of what the team builds: the goal, functions and behaviour of the product. According to Marty Cagan (Silicon Valley Product Group, SVPG), its purpose is to "clearly and unambiguously articulate the product's purpose, features, functionality, and behavior", so that the team can build the product from it and check it.

## When to use and when not to

Use it when the decision is made and needs to be handed to development and testing. Cagan: a PRD describes one release, not a strategy.

Do not use it instead of discovery. Cagan (2021): PRDs are almost always written instead of checking the value, usability, feasibility and viability of the solution.

- **The contents depend on the readers.** Cagan has four areas about the product; the PAF (Product Architecture Framework) template is broader and includes market, economics and launch. Do not fill in extra sections just for form's sake.
- **The document is alive.** Cagan: questions about requirements are answered by linking to the PRD, and what is missing from it gets added.

## Scheme

The PAF template: four parts, ten sections:

1. **Purpose:** Background (premises), Business & Product Goals (goals and boundaries).
2. **Customer & Value:** Customer Segment, Market & Business Analysis, Proposal & Value Propositions, Risk Assumptions (risky hypotheses).
3. **Solution:** Solution (product properties, scope), Project Plan (steps, risks, resources, launch criteria).
4. **Execution:** Launch Strategy (early adopters, channels, onboarding), Post-Launch Plan (actions on success and on failure).

Cagan has four areas: goal, functions, release criteria, timing.

## How to apply

1. **Gather the inputs:** customer research, economics, the chosen solution.
2. **Describe the goal through the need, not the solution.** Cagan: "Make sure you don't specify a candle in the PRD and prevent yourself from getting a light bulb". Goals are measurable and ordered.
3. **Describe the functions** at the level of usage scenarios, without imposing an implementation. For each requirement, state which goal it supports.
4. **Set priorities** per Cagan: must-have (we do not release without it), high-want (desirable before release, but the deadline does not move), nice-to-have (useful to know, can come later); number each class from 1 to n.
5. **Set the release criteria:** performance, scalability, reliability, usability, supportability, localizability.
6. **Fix the boundaries:** what we are not doing, and open questions with assumptions.
7. **Check completeness.** Cagan: is there enough information for an engineer to build, and for testers to write a test plan?
8. **Decision:** if the answer is "no" for at least one reader, the document goes back for revision; if "yes", hand it over and keep it updated.

## Example

Queenswood is an open banking core, repository [repldriven/queenswood](https://github.com/repldriven/queenswood), MIT. The file [docs/prd/payments.md](https://github.com/repldriven/queenswood/blob/main/docs/prd/payments.md) is the PRD for payments. Sections: Objective, Users and stakeholders, Goals, Non-goals, Functional scope, User journeys, Open questions.

What it shows: three payment types (internal transfers, outgoing and incoming via UK Faster Payments, the British fast-payment system); four groups of readers; eight numbered scenarios; boundaries in Non-goals: cross-border and currency payments, cancellation, bulk payments. Open questions are given with assumptions, e.g. "An installation uses one payment provider."

What was done with the PRD: in PR #785 (merged 1 October 2026) eight scenarios were turned into end-to-end API (application programming interface) tests; the test checks the catalogue against the PRD scenarios in both directions; the PR description reports 21 068 checks, 0 failures. This is an engineering step, not a decision to "hand over or return the PRD". The PR was opened and merged by one author (kjothen) without review; the repository has 3 stars; the PR also edits the PRD itself (scenarios 7 and 8, names in the diagrams).

What is missing: market, economics, value, release criteria and launch plan, success metrics; the providers are simulators, as the PRD states. The case shows the form and the boundaries, not a commercial decision.

## Common mistakes

- **PRD instead of discovery.** The document is written without checking value and feasibility (Cagan, 2021).
- **Solution instead of need.** The requirement dictates the implementation and rules out better options.
- **Everything is must-have.** Must-have means "we do not release without it"; without numbering, when time runs short, the wrong things get cut.
- **Release criteria "for the record".** Cagan: they are often brushed off with generic words, while real minimums are needed.
- **A document without boundaries.** Atlassian: the "what we are not doing" section keeps the team on the current work; without it the boundaries are not named.
- **Sign-off as the end of the work.** Atlassian calls it an anti-pattern: a detailed PRD with rigid approval before the start, which is never updated.
- **The author writes alone.** Atlassian: never write a PRD alone, a developer must be alongside; an anti-pattern is the product owner writing requirements without the team's involvement.

## Source

M. Cagan, [“How To Write a Good PRD”](https://www.svpg.com/wp-content/uploads/2024/07/How-To-Write-a-Good-PRD.pdf), Silicon Valley Product Group, 2005; M. Cagan, [“Discovery vs. Documentation”](https://www.svpg.com/discovery-vs-documentation/), SVPG, 25.08.2021; D. Radigan, [“How to create a product requirements document (PRD)”](https://www.atlassian.com/agile/product-management/requirements), Atlassian Agile Coach, undated.

The scheme and the ten sections are based on the PAF description (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, undated): [document template](https://docs.google.com/document/d/1I61-3IfI6qqsDQM5Cnvw0aFztQNbRU9CCq9St8Z3vCE/edit?usp=sharing) and [Requirements Design](https://productframework.ru/activities/requirements_design). PAF gives no definition of PRD as a term, only the template; the definition is taken from Cagan.

## See also

- Preceded by Minimum Viable Product: Test the main assumption with an MVP first; a PRD should not replace discovery.
- Preceded by Customer Profile: Fill the Customer Segment section from the profile of the target segment.
- Enhanced by Use Case: Describe PRD functions as usage scenarios, the level at which use cases describe them.
- Followed by Product Backlog: Turn the PRD's functions into ordered backlog items for the team.
- Followed by Test Case: Derive each expected test result from the requirement written here, not the code.
