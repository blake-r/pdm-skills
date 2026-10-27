---
name: ask-pdm
description: Navigator for the pdm-skills set. Takes a product-management task described in plain words and picks the right PAF tool for it, then hands the work to that tool's skill. Use when the user describes a product task and does not know which tool fits, asks "which tool should I use", "what framework for this", "where do I start", or invokes /ask-pdm.
disable-model-invocation: true
---

# Ask PDM

A navigator over every tool of the pdm-skills set. It does not do the tool's work itself: it chooses the tool and hands over.

## Procedure

1. Take the user's task description as it is. If it is empty, ask the user to describe the task, the product and what they need as the result.
2. Match the task to the table below on three axes:
   - **Function** (the first word of the folder): `business` (company, market, model), `product` (a product, its customers and features), `development` (the team and the delivery process).
   - **Stage** (the second word of the folder): `research`, `analysis`, `planning`, `validation`, `execution`, `handoff`.
   - **Situation**: what the user has now and what they want to get, as the purpose column says.
3. Pick one main tool. Read its row in the Selection table of `product_notes.md` (`Data modes` and `Input needed`). If the user has said what data they have and it does not match the tool's modes (for example the tool needs numbers and the user has none), say so and offer the nearest tool whose modes match, or the same tool with the missing input marked N/A. State in one or two sentences why the tool fits, then invoke that tool's skill by its name from the first column.
4. If two tools fit equally or the task spans several, ask one clarifying question (through AskUserQuestion) that separates them, for example what the user has now or what the result is for. Do not guess.
5. Name neighbouring tools only as alternatives after the main answer, one line each, saying when they fit better.
6. If nothing in the table fits, say so plainly and suggest `pdm-brief` when the task is a research or strategy question that needs several tools; otherwise do not invent a tool.

Reply in the user's language.

## Tools

The folder column is the category and stage folder under `skills/`.

| Skill | Folder | Purpose |
|---|---|---|
| `abc-analysis` | business-analysis | Rank products, customers or features by contribution; set a rule per class |
| `adl-matrix` | business-analysis | Pick a business unit's strategy from industry life-cycle stage and competitive position |
| `ansoff-matrix` | business-analysis | Choose a growth direction: existing or new products in existing or new markets |
| `bcg-matrix` | business-analysis | Sort products by market growth and share; decide fund, hold, harvest or exit |
| `ge-mckinsey-matrix` | business-analysis | Score units on weighted industry attractiveness and unit strength; decide invest, selective or harvest |
| `moscow-prioritization` | product-planning | Split requirements into Must, Should, Could and Won't within a fixed time or budget box |
| `now-next-later-roadmap` | product-planning | Show a roadmap by certainty (now, next, later) tied to business objectives, without dates |
| `opportunity-solution-tree` | product-planning | Link a desired outcome to customer opportunities, solutions and the tests of their assumptions |
| `pre-mortem` | product-validation | Imagine the plan has failed, list why, and change the plan before it starts |
| `product-lifecycle` | business-analysis | Find a product's lifecycle stage from sales history and choose invest, extend or harvest |
| `rapid-decision-rights` | business-planning | Assign who recommends, agrees, performs, gives input and decides in one decision |
| `sales-funnel` | business-analysis | Measure conversion and time per stage from contact to deal; find the bottleneck |
| `segment-scoring` | business-analysis | Score customer segments on size, ability to pay, pain and access; pick the focus |
| `swot-analysis` | business-analysis | List strengths, weaknesses, opportunities, threats and cross them into strategies (TOWS) |
| `technology-adoption-lifecycle` | business-analysis | Find which adopter group buys now and why growth stalls between groups |
| `unit-economics` | business-analysis | Calculate CAC, LTV, margin and payback per channel; check if growth pays off |
| `value-chain-and-nets` | business-analysis | Map a value chain or network; see cost, time and client value per link |
| `working-backwards-pr-faq` | product-planning | Write a product's future press release and FAQ to test the idea before building |
| `yc-guide-to-business-models` | business-analysis | Pick key metrics for your business type among nine Y Combinator models |
| `business-model-canvas` | business-planning | Describe a whole business model in nine blocks (Osterwalder), for an existing company |
| `business-model-patterns` | business-planning | Improve a business model by applying one of 55 known patterns, e.g. Freemium |
| `lean-canvas` | business-planning | Sketch a new startup idea: problems, solution, segments, metrics; faster than the full canvas |
| `objectives-and-key-results` | business-planning | Set OKRs: a few objectives with measurable key results for a team or company |
| `product-ecosystem-map` | business-planning | Map an ecosystem's products by role (lead, profit, retention) and the flows between them |
| `smart-goals` | business-planning | Make a vague goal specific, measurable and time-bound using SMART |
| `usp-4u` | business-planning | Check a headline or offer against four tests: useful, unique, specific, urgent |
| `usp-aida` | business-planning | Write offer or ad text in the Attention, Interest, Desire, Action order |
| `usp-habitual-without-habitual` | business-planning | Phrase a USP as a familiar thing minus a familiar element |
| `usp-maxwell-formula` | business-planning | Phrase a USP as result, time to get it, answer to objection |
| `competition-map` | business-research | Map direct, indirect and substitute competitors along the customer's scenario steps |
| `competitor-analysis-template` | business-research | Profile one competitor: model, pricing, users, product, reviews; compare with yours |
| `gartners-hype-cycle` | business-research | Place a technology on the hype cycle and decide when to adopt it |
| `pestel-analysis` | business-research | Scan the external environment (politics, economy, society, tech, ecology, law) for threats and chances |
| `porters-five-forces` | business-research | Judge how attractive and profitable an industry is by five competitive forces |
| `strategy-canvas` | business-research | Compare value curves against competitors; decide what to eliminate, reduce, raise, create |
| `tam-sam-som-model` | business-research | Size a market in three levels, top-down and bottom-up, with sources |
| `financial-modeling` | business-validation | Test a business-model hypothesis by calculation before launch, forward or inverse |
| `kanban-board` | development-execution | Design or fix a team's board: columns, WIP limits, exit rules, flow metrics |
| `retrospective-meeting` | development-execution | Run a team retrospective on an iteration and agree improvement actions |
| `sprint` | development-execution | Plan a Scrum sprint around one goal with capacity and limit; track results |
| `stand-up-meeting` | development-execution | Set up or fix a team's daily stand-up: format, order, what goes offline |
| `team-canvas` | development-execution | Align a team in one session on goals, roles, values and working rules |
| `definition-of-done` | development-handoff | Write a team checklist that says when work counts as finished |
| `gantt-chart` | development-planning | Build a dated project plan with dependencies, milestones and critical path |
| `test-case` | development-validation | Write test cases for a requirement or user story: steps, expected results, priority |
| `pdm-brief` | - | Start from a product task: pick 3-5 tools and assemble a short deck |
| `aarrr-metrics` | product-analysis | Lay out metrics across acquisition to revenue stages; find the funnel's weakest stage |
| `abcdx-segmentation` | product-analysis | Split paying customers by need for the product; compare revenue and support load |
| `buyer-persona` | product-analysis | Describe the person who chooses and buys: criteria, barriers, approval, budget |
| `cohort-analysis` | product-analysis | Read retention or spend by cohort and period; see if behaviour improves over time |
| `customer-journey-map` | product-analysis | Map a customer's path to a goal across stages: touchpoints, problems, opportunities |
| `customer-profile` | product-analysis | Describe a typical customer of one segment on one page around a named persona |
| `feedback-matrix` | product-analysis | Sort customer feedback by tone and need to fix; turn it into actions |
| `five-whys` | product-analysis | Find the root cause of an incident, failed metric or recurring complaint |
| `forces-of-progress` | product-analysis | Explain why customers switch or do not: push, pull, habit, anxiety |
| `frequency-adoption-analysis` | product-analysis | Sort features by adoption and use frequency; decide what to develop, promote or cut |
| `rfm-analysis` | product-analysis | Segment customers by recency, frequency and spend; assign an action per segment |
| `entities-analysis` | product-handoff | Model a domain's business objects, attributes and relations before design |
| `product-backlog` | product-handoff | Build or tidy one ordered list of work under a product goal |
| `product-requirements-document` | product-handoff | Write a PRD to hand a chosen solution to development and testing |
| `screen-map` | product-handoff | Map a scenario's screens, transitions and states for design and development |
| `sequence-diagrams` | product-handoff | Show how participants exchange messages in time, including failure branches |
| `service-blueprint` | product-handoff | Map a service scenario with frontstage, backstage and support processes |
| `state-modelling` | product-handoff | Model an entity's states and allowed transitions (order, payment, loan) |
| `story-mapping` | product-handoff | Lay out the user's path as a story map and slice it into releases |
| `use-case` | product-handoff | Describe an actor's goal as a step-by-step scenario with exceptions |
| `user-story` | product-handoff | Write a story (role, want, benefit) with acceptance criteria in Given/When/Then |
| `cost-benefit-analysis` | product-planning | Compare costs and benefits of options over time; find break-even |
| `elevator-pitch` | product-planning | Phrase a product positioning in one pitch: for whom, need, benefit, difference |
| `feature-canvas` | product-planning | Describe a new feature before design: problem, customers, value, risks |
| `heart-metrics` | product-planning | Choose UX metrics (happiness, engagement, adoption, retention, task success) for a product or redesign |
| `ice-scoring` | product-planning | Quickly rank hypotheses or features by impact, confidence and ease |
| `impact-effort-matrix` | product-planning | Sort ideas on a 2x2 of impact against effort to find quick wins |
| `impact-mapping` | product-planning | Link a business goal to actors, behaviour changes and deliverables; choose what to build |
| `lean-ux-canvas` | product-planning | Turn a feature request into a business problem, hypotheses and smallest experiment |
| `metric-pyramid` | product-planning | Break the main metric into a tree from North Star down to levers |
| `morphological-analysis` | product-planning | Generate variants by splitting an object into properties and combining their values |
| `project-canvas` | product-planning | Define a project on one page: goals, participants, deliverables, risks, milestones |
| `rice-scoring` | product-planning | Rank initiatives by reach, impact, confidence and effort; more rigorous than ICE |
| `scamper-method` | product-planning | Generate ideas to change an existing product with seven prompting questions |
| `six-thinking-hats` | product-planning | Discuss a decision from six viewpoints in turn: facts, feelings, risks, benefits, ideas, process |
| `storytelling` | product-planning | Structure a pitch or launch talk as a story with a call to action |
| `theory-of-inventive-problem-solving` | product-planning | Resolve a hard problem with conflicting requirements using TRIZ |
| `user-flow` | product-planning | Draw the steps a user takes to reach one goal, with conditions |
| `value-proposition-canvas` | product-planning | Match one segment's jobs, pains and gains to what the product offers |
| `customer-survey` | product-research | Plan a questionnaire to measure shares and frequencies in a customer hypothesis |
| `diary-study` | product-research | Study behaviour over days or weeks through participants' own diaries |
| `empathy-map` | product-research | Capture what one person sees, says, does, thinks and feels |
| `expert-interview` | product-research | Check hypotheses with market experts instead of end consumers |
| `field-research` | product-research | Observe people in their natural environment to test behaviour hypotheses |
| `in-depth-interview` | product-research | Run a CustDev interview about past experience to test a hypothesis |
| `jobs-to-be-done` | product-research | Find the jobs customers hire a product for and write job stories |
| `jtbd-interview` | product-research | Interview about a recent purchase or switch and rebuild its timeline and forces |
| `kano-model` | product-research | Classify features as must-be, one-dimensional or attractive with a Kano survey |
| `perceptual-map` | product-research | Place brands on two dimensions as buyers see them; find empty niches |
| `problem-interview-script` | product-research | Build a script to test a problem hypothesis and record answers |
| `stakeholders-matrix` | product-research | Rank people around a product by influence and impact; set engagement |
| `aa-testing` | product-validation | Check the experimentation system itself: both groups see the same version |
| `ab-testing` | product-validation | Plan or read a controlled experiment between two versions with one primary metric |
| `experiment-card` | product-validation | Record any experiment in one card: hypothesis, success condition, result, verdict |
| `fake-door-test` | product-validation | Measure demand with a button or banner for a feature that does not exist |
| `hadi-canvas` | product-validation | Run one hypothesis-action-data-insights cycle on a single metric |
| `landing-page-test` | product-validation | Test demand with a page describing the offer and asking for a target action |
| `minimum-viable-product` | product-validation | Test the riskiest assumption with the smallest real or manual version |
| `packaging-offer-test` | product-validation | Test demand with an ad, brochure or box mock-up of a nonexistent product |
| `physical-modeling` | product-validation | Test a solution on a life-size model or mock-up by running scenarios |
| `pilot-project` | product-validation | Give real users a trial solution with minimum features; decide scale, rework or stop |
| `prototyping-process` | product-validation | Choose prototype fidelity and test it against one question |
| `single-feature-prototype` | product-validation | Test one function for one need as Concierge or Wizard of Oz |
| `soft-launch` | product-validation | Release the real solution to a limited audience or region without loud advertising |
| `validation-board` | product-validation | Track customer and problem hypotheses across pivots; test the riskiest cheaply |

## Routing examples

Five fixed tasks and the tool each one routes to by the table above.

- "How big is the market for our B2B payments app, and how much of it can we realistically win?" -> `tam-sam-som-model`
- "We have thirty feature ideas and little data; rank them fast by impact, confidence and ease." -> `ice-scoring`
- "Check demand for a feature we have not built by showing a button and counting clicks." -> `fake-door-test`
- "Our daily stand-up runs forty minutes and turns into a status report; fix the format." -> `stand-up-meeting`
- "Checkout conversion fell last week; find the root cause by asking why step by step." -> `five-whys`

## Keeping this list current

When a skill is added, renamed or moved between folders, update this table in the same change. `build/quality_gate.py` checks that every skill appears here.
