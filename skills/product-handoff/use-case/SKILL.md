---
name: use-case
description: Write or review a use case - the goal of a primary actor as a short verb phrase, the system scope and goal level, preconditions and trigger, a numbered main success scenario where every step names who acts, extensions tied to steps ("3a. card declined: ..."), success and minimal guarantees, plus a UML use case diagram with actors, the system boundary and include/extend relations - and produce a two-slide PPTX (the diagram and the description); or review existing use cases. Use when a feature has many steps and participants, including external systems, when failures matter (payment, checkout, refunds), or when requirements are handed to a team that will build and test the behaviour.
---

# Use Case

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a feature, a flow or requirements to describe, **review** when the user brings finished use cases or a diagram.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- which system is described and where its boundary lies; which people and external systems interact with it;
- what each of them wants to achieve with the system;
- what is already true before the flow starts and what starts it;
- the known failures, rejections and alternative paths; what must hold whatever happens (data kept, money not charged twice).

Do not invent actors, steps, failures or guarantees. If the feature is one or two actions, say that a use case is overkill and a short description or acceptance criteria will do. A use case records a decision already taken; if the user is still deciding whether the feature is needed, say so.

### 2. Actors and goals

- List actors with their goals at user-goal level ("sea level": one task in one sitting) and rank them. Merge subfunction-level goals into the user goals they serve; lift summary goals into a separate overview.
- Pick the use case to write first. Precision grows in layers: actors and goals, then main scenarios, then the list of failures, and only then their handling.

### 3. Write the use case

- **Name:** the actor's goal as a short verb phrase. **Scope and level:** the system and the goal level. **Primary actor**, **preconditions**, **trigger**.
- **Main success scenario:** 3 to 9 numbered steps from the trigger to the goal. Every step names who acts; no buttons, fields or screens, only intentions.
- **Extensions:** first list every failure and alternative by step number with a letter ("3a", "3b"), then write the handling of each. A step with no extensions is worth a second look.
- **Guarantees:** what is true after success; the minimal guarantee, true whatever the outcome. If the source gives none, mark it as missing.
- Say that less is better than more: prefer writing too little to writing too much.

### 4. Diagram

- The system boundary with the use cases inside, the primary actor on the left, supporting actors and external systems on the right.
- "include": a common step always performed inside the use case; the dashed arrow points to the included one. "extend": behaviour added on a condition; the dashed arrow points to the extended one. Use them only where the text supports them.

### 5. Show, then write

Show in chat first: the actors and goals, the use case text and the gaps. The file has two slides: the diagram and the description. Write a file only after the user confirms. Ask for the output path (default `use-case-<topic>.pptx` in the working directory). Save the data as JSON (the example is the FirePond case from card.md; the source gives only the text, so the diagram is reconstructed from it: the extend comes from extension 2d, the link to financing from extension 7d, and the include of the credit rating from step 26d2 of the "before" version; the minimal guarantee is marked as missing):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "FirePond: product selection on an e-commerce site, 1999",
    "system": "E-commerce site (web system)", "actor": "Customer", "actor2": "Financial system",
    "uc1": "Research a solution (EC5)", "uc2": "Arrange financing", "uc3": "Request contact with the seller", "uc4": "Create a sales lead", "uc5": "Get credit rating",
    "name": "EC5 Research possible solutions", "goal": "Select a product matching own specs and put it in the cart",
    "scope": "Web system", "level": "User task", "primary": "Customer — any visitor to the site",
    "pre": "None", "trigger": "Customer decides to research a solution",
    "success": "Customer has zero or more products to buy; the system recorded the choices, transitions and specs",
    "minimal": "Not filled in the source",
    "main": ["1. Customer starts researching a new solution", "2. System helps choose the line, model and options: shows information and asks questions depending on the answers", "3. System records transitions", "4. Customer selects the final configuration", "5. Customer adds it to the cart", "6. System adds the product and transition information to the cart", "7. System shows the cart with all products"],
    "ext": ["1a. Request from a partner site carries customer data: system records it and starts from the deeper question point", "1b. Customer continues a saved solution: gives their name, system returns them to where they stopped", "2a. Customer skips the questions: chooses from recommendations based on incomplete data", "2d. Customer reached the set point: system creates a sales lead", "5a. Customer does not put the product in the cart: system saves transitions", "7d. Customer wants to arrange financing: option “Arrange financing”"]
  }
}
```

The diagram keys are `system`, `actor` (left), `actor2` (right, linked to `uc5`) and `uc1`–`uc5`; `uc4` extends `uc1`, `uc2` includes `uc5`, and `actor` is linked to `uc1`–`uc3`. If a relation does not apply, leave both of its ovals empty and say so. The title takes under 60 characters; `system` under 50; `actor` and `actor2` under 30; each `uc` under 40; `name` under 60; `goal` under 80; `scope` and `level` under 30; `primary` under 50; `pre` under 80; `trigger` under 60; `success` under 110; `minimal` under 60; `main` up to nine items of under 110; `ext` up to eight items of under 120; each list item becomes its own paragraph. With more steps or extensions, move the extension handling to a second file or shorten the wording. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/use-case.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's use cases or diagram in any form and check them against the common mistakes in card.md:

1. Steps describe intentions, not the interface: no buttons, fields or screens.
2. The level is the user goal, not one step per field.
3. Every step names who acts.
4. There are extensions for failures and alternatives, tied to step numbers, with handling.
5. The set is a few user-goal use cases, not a forest of small subfunctions.

Also check that the scope, primary actor, trigger and both guarantees are filled in, and that include/extend arrows point the right way. Report findings as a numbered list: what is wrong, why it misleads the team, the concrete fix (rewrite the step or the use case). End with a verdict: "ready for development", "ready after fixes" or "needs rework".
