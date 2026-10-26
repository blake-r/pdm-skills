---
name: product-requirements-document
description: Draft or review a Product Requirements Document (PRD) for handing a chosen solution to development and testing — purpose and goals, customer and value, solution and scope, release criteria, launch plan, non-goals, open questions — and produce a one-slide PRD map in the PAF structure (ten sections), or check an existing PRD. Use when a decision is made and requirements must be written down, when a PRD is vague or has no boundaries, or before handing a feature to engineers.
---

# Product Requirements Document

The theory, the section list, the sources and a worked case (Queenswood, PRD "Payments") are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user must write a PRD, **review** when the user gives an existing PRD or its outline and wants it checked. If discovery (customer research, checking value and feasibility of the solution) has not been done, say so first: card.md warns that a PRD written instead of discovery only documents a guess.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product or feature, the release it belongs to, and who reads the PRD (engineers, testers, designers, stakeholders);
- what pushed the work: research, customer requests, expert opinions, with links;
- goals with numbers or clear qualitative targets, and what is explicitly not a goal;
- the customer segment, its needs and how it solves the task today;
- economics and market size, industry or company constraints, if the readers need them;
- the chosen solution at top level, links to mock-ups, the main scenarios;
- the riskiest assumptions, the plan, resources, launch criteria;
- launch: early adopters, channels, onboarding, changes for sales and support; what to do if goals are met or missed.

Do not invent anything. Mark what the user did not give as null and list it as a gap.

### 2. Fill the ten sections

Go through the PAF structure from card.md: Purpose (Background, Goals), Customer & Value (Segment, Market & Business Analysis, Value Propositions, Risk Assumptions), Solution (Solution, Project Plan), Execution (Launch Strategy, Post-Launch Plan). State needs, not implementations. Make goals measurable. Tie each requirement to a goal. Rank requirements: must-have, high-want, nice-to-have, then number inside each class. Give release criteria for performance, scalability, reliability, usability, supportability, localizability, with real minimums. Write the boundaries and open questions with assumptions.

### 3. Completeness test and decision

Answer two questions: can an engineer build from this, can a tester write a check plan from this. List empty sections and why they are empty (not needed, or a gap). Decision: hand over, or return for the missing items.

### 4. Show, then write

Show the PRD map in chat first as a table by template blocks: title, ten sections, decision. Write a file only after the user confirms. Ask for the output path (default `prd-<product>.pptx` in the working directory). The example is the Queenswood case from card.md; the source has no market, economics or launch sections, so they stay null:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Queenswood: PRD “Payments” (docs/prd/payments.md)",
    "background": "The Queenswood open banking core moves money in three ways: internal transfers, outgoing and incoming payments via UK Faster Payments (Objective section).",
    "goals": ["Three payment types in one interface; internal transfer is executed immediately, external ones in two stages", "Non-goals: cross-border, FX, cancellation after sending, direct debit, bulk, scheduled and recurring payments"],
    "segment": "Client's engineering team, end customer, platform operator, payment provider",
    "market": null,
    "proposal": null,
    "risks": "Assumption: providers are simulated; test with the provider's real sandbox has not been run",
    "solution": "Scope: internal transfer, outgoing and incoming payments, recipient check (Confirmation of Payee), idempotency; 8 user scenarios",
    "plan": null,
    "launch": null,
    "postlaunch": null,
    "decision": "An engineer and a tester can work only on payments; empty: market, economics, launch criteria, launch plan. Decision: hand over for the payment core, return the rest"
  }
}
```

The slide is a map: Cagan's release criteria (performance, scalability, reliability, usability, supportability, localizability) do not have their own block. Keep them in the full PRD and put only the launch criteria in the Project Plan block. Limits that fit the rendered slide: title under 60 characters; the blocks Background, Goals, Solution, Project Plan, Launch Strategy and Post-Launch Plan up to 240 characters (Goals: up to two items); the four blocks of part 2 up to 150 characters each; decision up to 220 characters. A list of strings becomes lines. Put the rest in chat or in the full document: the slide is a map, not the PRD. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/product-requirements-document.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's PRD or outline and check it against the common mistakes in card.md:

1. The PRD is written instead of discovery: no evidence that value, usability, feasibility and viability were checked.
2. Requirements state a solution, not a need.
3. Everything is must-have, or requirements are not ranked inside classes.
4. Release criteria are generic or missing.
5. There is no "what we are not doing" section.
6. The document is signed off and not updated; changes live in chats.
7. The product owner wrote it alone, without the team.

Items 1, 6 and 7 usually cannot be judged from the text alone: ask how the solution was checked, when the PRD was last changed and who took part, instead of reporting a finding. Also check that goals are measurable, every requirement ties to a goal, and the two completeness questions (engineer, tester) get a yes. Report findings as a numbered list: what is wrong, why it matters for the team, the concrete fix. End with a verdict: "ready to hand over", "works after changes" or "return to discovery".

Example: a PRD with a feature list, "all P0", no goals and no boundaries. Findings: item 3, everything is must-have, rank and cut the class; item 2, features describe screens, restate the needs; item 5, add non-goals; item 4, no release criteria. Ask about item 1. Verdict: "return to discovery".
