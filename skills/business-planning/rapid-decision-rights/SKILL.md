---
name: rapid-decision-rights
description: Assign decision rights with RAPID (Recommend, Agree, Perform, Input, Decide) and produce a one-slide role table for one decision, or review an existing one. Use when a decision stalls between teams, nobody knows who decides, a veto appears late, or the user asks "who decides", "who approves", "decision owner", "RAPID", "кто принимает решение", "распределить роли в решении".
---

# RAPID Decision Rights

The theory, role definitions, limits and the Wyeth case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode: **do** when the user must assign roles for a decision, **review** when the user shows a finished role table or describes who decides now. To find out who is affected first, use Stakeholders Matrix.

## Mode: do

### 1. Collect inputs

Ask in one message for what is missing:

- the decision in one sentence and its deadline;
- who and which units are touched by it, and who will carry it out;
- mandatory requirements (legal, regulatory, security) and who guards them;
- who decides today, and where the decision stalls.

Do not invent names. Mark an unknown holder as "N/A" and say so.

### 2. Assign the roles

In this order: Decide (one person; if a group, the tie rule), Recommend (one person), Agree (few, only for mandatory requirements; a veto comes with an alternative or goes to the decider), Perform (add them to Input too), Input (facts, affected people). Write the conflict rule for Recommend versus Agree and the outcome (decision, who, when). Mention that the letters are not a sequence.

### 3. Show, then write

Show the table in chat first, by template blocks: title, decision, five roles with holder and scope, conflict rule, outcome. Write the file only after the user confirms. Ask for the output path (default `rapid-<decision>.pptx` in the working directory). Save the data as JSON. The values below come from the Wyeth case in card.md and show the format only; use them only if the user asks for an example. Otherwise fill each field with the user's facts and "N/A" where there is no fact.

```json
{
  "text": {
    "title": "Wyeth: expanding Enbrel production capacity (Ireland plant), 2006 article",
    "decision": "How to expand Enbrel production capacity quickly, including a new plant in Ireland",
    "r_who": "People closest to the knowledge; some responsibilities pushed down to the business units",
    "r_note": "Make a proposal or offer alternatives; individual names are not given",
    "a_who": "Wyeth top executives",
    "a_note": "Kept veto power over many important proposals; a veto comes with an alternative or goes to the Decide role",
    "p_who": "The business unit",
    "p_note": "Carries out the plan; responsibility for execution rested firmly with it",
    "i_who": "Other managers",
    "i_note": "Gave input to the Enbrel team before the decisions; the recommender weighs it but need not follow it",
    "d_who": "Cavan Redmond, executive vice president and general manager of the biotech division",
    "d_note": "Took many Enbrel decisions after he and his team gathered input from other managers",
    "conflict": "Veto holder offers an alternative or escalates to the person with the D",
    "outcome": "Roles assigned for Enbrel decisions; the article gives no date, result or confirmation that the Irish plant was approved"
  }
}
```

Length limits: title under 70 characters; decision under 110; each "who" under 90; each note under 120; conflict under 100; outcome under 140. Put the rest in chat. Run from the repo root:

`uv run scripts/fill_pptx.py <this skill dir>/rapid-decision-rights.pptx data.json <output>.pptx`

`uv run scripts/fill_pptx.py <template> --list` prints every placeholder and its hint. `example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

## Mode: review

Check the user's role table against the common mistakes in card.md:

1. More than one decider, or a group with no tie rule.
2. Agree given to many people, so it works as consensus.
3. The letters read as steps, with Perform and Input started only after the decision.
4. Dropped Perform and Input.
5. A recommender the decider does not trust, or several recommenders.
6. The table is not shared with the people named in it.
7. RAPID applied to a minor decision where the effort does not pay off.

Items 5 and 6 cannot be judged from the table alone: ask. Report a numbered list: what is wrong, why it stalls the decision, the concrete change. End with a verdict: "rights are clear", "works after changes" or "name the D first".

Example: a table where Product, Legal and Finance all hold "D" for a pricing change. Findings: item 1, three deciders, so pick one and write the tie rule; item 2, if Legal and Finance only guard mandatory limits, move them to Agree. Verdict: "name the D first".
