---
name: screen-map
description: Build or review a screen map - the screens of a product for one user scenario as nodes (existing, new, screens of other teams), the transitions between them with who triggers each one, the states of each screen (loading, data, empty, error), and the decision taken on the structure - and produce a one-slide PPTX; or review an existing screen map. Use when a scenario must be turned into concrete interface decisions, when screens are merged, split or moved, or when requirements for development are written.
---

# Screen Map

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language. If the user has only a goal and no scenario yet, ask for the scenario first: the map implements a scenario and does not invent one.

Pick the mode from the request: **do** when the user wants a map built, **review** when the user gives an existing map or screen list.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and the user scenario: who, what they want, where they enter and where it ends;
- the list of current screens and how they are reached;
- what changes: new screens, removed, merged, moved;
- screens of other teams or shared libraries that the change may touch;
- states known for each screen (loading, data, empty, error);
- the design system or components used;
- what was tested and measured, if anything.

Do not invent screens, transitions or numbers: mark what the user did not give as unknown.

### 2. Nodes and levels

Put the entry screen first, then screens of the second and third level in hierarchy order. The template holds five screens; if there are more, keep the ones on the main path and list the rest in "affected". Mark each screen as new or existing.

### 3. Transitions and states

For each transition write from where, to where and who triggers it: user action or system event. For each screen write the states that need a separate decision.

### 4. Reading the map

Look for a long chain before the target action, a screen without an exit, a transition without a reason, a pair of screens that could be one. Name the decision on the structure and how it was or will be checked on people.

### 5. Show, then write

Show the map in chat first as a table by template blocks: title, scenario, change, five screens, transitions, states, affected, decision, check. Write a file only after the user confirms. Ask for the output path (default `screen-map-<product>.pptx` in the working directory). Save the data as JSON. The example is the OTP Bank case from card.md; the article has no map, so the chain is restored from its text and unknown fields say so:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "OTP Bank, card screen, 2025: 4 screens for the card",
    "scenario": "Customer goes from the main screen to card actions: payment, details, top-up",
    "change": ["Option 2: account and card on one screen", "Option 1 with two screens was not accepted"],
    "s1": "Main screen: accounts with cards (already updated)",
    "s2": "Account screen (option 1, not accepted)",
    "s3": "Account and card screen together (option 2, accepted)",
    "s4": "Card screen (option 1, not accepted)",
    "s5": null,
    "transitions": ["Main → account: tap", "Account → card: tap (opt. 1)", "Main → account and card: tap (opt. 2)"],
    "states": ["Loading skeleton added", "Other states are not described in the article"],
    "affected": ["No other screens in the article", "The card screen itself is not in the article"],
    "decision": ["One screen instead of two", "Fixes: removed coloured header background, block order", "Gradual rollout after fixes"],
    "check": ["Customers: two screens are unclear", "iOS test, 2 weeks: CSI 8.3 debit, 8.1 credit", "Final CSI not stated"]
  }
}
```

Unused fields: null. Limits that fit the rendered slide: title under 60 characters; scenario under 110; change: up to three items under 55; each screen s1..s5 under 80; transitions: up to four items under 45; states: up to three items under 45; affected: up to three items under 40; decision: up to three items under 55; check: up to three items under 55. A list of strings becomes lines, one thought per item. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/screen-map.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's map, screen list or description and check it against the common mistakes in card.md:

1. The map has no states: loading, empty and error are left to the developer.
2. Only the happy path is drawn: no transitions on error and on system events.
3. Only new screens are drawn: screens of other teams that the change touches are missing, so the volume of work is understated.
4. Screens are blocks, not components of the design system, so the volume cannot be estimated.
5. Looks were taken for clarity: the structure was not checked on people.
6. A test result is carried to everything: one platform, a small share of traffic, one product type.
7. The map is not updated after changes and is no longer documentation.

Items 5 and 6 usually cannot be judged from the map alone: ask what was tested, on whom and on which platform instead of reporting a finding. Also check that the entry and the end are marked, every transition has a trigger and every screen is marked new or existing. Report findings as a numbered list: what is wrong, why it matters for development, the concrete change to the map. End with a verdict: "ready for requirements", "works after changes" or "needs scenario and states first".

Example: a map of five boxes with arrows, no trigger on arrows, no states, only new screens drawn. Findings: item 1 — add states per screen; item 2 — mark triggers and add error transitions; item 3 — ask which existing screens change and add them; item 5 — ask how the structure was checked. Verdict: "works after changes".
