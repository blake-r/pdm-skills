---
name: single-feature-prototype
description: Plan or review a single-feature prototype - checking a solution hypothesis by building a prototype of one function for one customer need, delivered as Concierge (manual work), Wizard of Oz (manual work hidden, customer thinks it is software) or Third-party product (existing services, APIs, platforms) - and produce a one-slide test card. Use when the user wants to know whether a solution solves a need before automating it.
---

# Single-feature prototype

The definition, the three approaches, conditions for choosing, steps, limits, the worked case (Food on the Table) and the common mistakes are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants to design the prototype, **review** when the user brings a finished plan or results and wants them checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product, the single customer need and the single function that should solve it;
- the role of the customer and what result they should reach;
- who can do the manual work, how many customers can take part, how long the run lasts;
- whether the customer may know that a person does the work (law, trust, sensitive data);
- which ready services or APIs could replace own code;
- the success criterion and the threshold for the decision.

If the user wants to test the look or usability of the interface, say that this method checks whether the need is solved (card.md) and ask what exactly should be learned. Do not invent numbers: mark unknown values as "not in the source" or "unknown".

### 2. Hypothesis and threshold

Write the hypothesis by the PAF template: "If I, as <role>, am given <solution>, then <result>, which will confirm <criterion>, because <reason>". Set the threshold before launch. Say that three zones (automate, change the solution, stop) are the card author's advice, not a rule of the sources.

### 3. Approach

Choose Concierge, Wizard of Oz or Third-party product by the PAF conditions listed in card.md. For Wizard of Oz agree on disclosure to the customer after the session, a protocol, a set of answers and a rehearsal of the "wizard" and a trial run with a colleague or a real user (NN/g steps). For a third-party product list the services and check their terms and data handling. In all three, agree on a log of manual actions: minutes per customer, errors, what was repeated.

### 4. Reading the result

Compare facts with the threshold. If met, name what to automate first (the most time-consuming manual task); if not, change the solution, not the interface. Warn that a small group shows whether the need is solved, not that automation will give the same quality.

### 5. Show, then write

Show the card in chat first as a table by template blocks: title, hypothesis, need and function, approach, behind the scenes, up to four criteria rows (indicator, threshold, fact, conclusion), group and period, result, decision. Write a file only after the user confirms. Ask for the output path (default `single-feature-prototype-<idea>.pptx` in the working directory). Save the data as JSON. The example is the Food on the Table case from card.md; what the source does not give says "not in the source"; unused table cells get "—" (null would leave an empty bordered row):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Food on the Table: menus and shopping lists, 2010",
    "hypothesis": "Not in source (slide 11: \"No defined hypothesis\", 150+ conversations, 20 group discussions)",
    "need": "The family needs menu selection and a shopping list",
    "approach": "Concierge: full service by hand (openness — the card author's conclusion); in-person meeting, then a call",
    "behind": "Recipes and shopping lists were sent by mail; dynamic pages were replaced with Google Apps",
    "m1": "not in the source",
    "t1": "not in the source",
    "f1": "not in the source",
    "c1": "Move on when the reaction is predictable",
    "m2": "—",
    "t2": "—",
    "f2": "—",
    "c2": "—",
    "m3": "—",
    "t3": "—",
    "f3": "—",
    "c3": "—",
    "m4": "—",
    "t4": "—",
    "f4": "—",
    "c4": "—",
    "group": "First 20 users, added one at a time; term not given in the source",
    "result": "No result figures in the source; a case from product retail, not e-commerce or fintech",
    "decision": "Code only the tasks that became too long to do by hand"
  }
}
```

Limits that fit the rendered slide: title under 60 characters; hypothesis under 130; need, approach and behind under 105 each; indicator (m) under 55; threshold and fact (t, f) under 22; conclusion (c) under 45; group, result and decision under 110. A list of strings becomes lines. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/single-feature-prototype.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's plan, description or results and check them against the common mistakes in card.md:

1. The interface is tested, not whether the need is solved.
2. The approach does not fit the conditions: for example Wizard of Oz where the customer has the right to know about the person.
3. The threshold was set after the result.
4. The "wizard" improvises, so sessions cannot be compared.
5. Manual actions are not logged, so it is unknown what to automate.
6. A small group is taken for scale: the result does not promise the same quality from automation.
7. The terms, limits and data handling of the ready service are not checked.

Items 3, 5 and 7 usually cannot be judged from the description alone: ask when the threshold was written, whether a log exists and who read the service terms, instead of reporting a finding. Report findings as a numbered list: what is wrong, why it distorts the result, the concrete change. End with a verdict: "result can be trusted", "trusted after changes" or "repeat the run".

Example: the user says "we ran a manual service for 15 customers and they liked the screens, so we build the app", with no threshold and no log. Findings: item 1 — liking screens is not a solved need, ask what the customers achieved; item 3 — ask when the threshold was set; item 5 — no log, so the first thing to automate is unknown; item 6 — 15 customers do not promise the same quality from the app. Verdict: "repeat the run".
