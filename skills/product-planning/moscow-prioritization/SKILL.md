---
name: moscow-prioritization
description: Sort requirements, user stories or tasks into Must Have, Should Have, Could Have and Won't Have this time (MoSCoW) for one release, increment or sprint, and produce a one-slide PPTX, or review an existing MoSCoW list. Use when the deadline or budget is fixed and scope must flex, when "everything is a must", or when the user says "MoSCoW", "must/should/could/won't", "what goes into the MVP", "what do we cut".
---

# MoSCoW Prioritization

The theory, the rules, the effort guideline and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a list of requirements, **review** when the user brings a finished MoSCoW list or table.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the timeframe (project, increment or timebox) and the fixed date or budget;
- the list of requirements, user stories or tasks, one item per line;
- a rough effort estimate for each item, if any;
- the business owner who explains why an item is a Must;
- the objective that each item serves.

If there is no fixed date or budget, say that MoSCoW has nothing to protect and ask what is fixed. If the user wants a value ranking, suggest `rice-scoring` or `impact-effort-matrix`. Do not invent estimates: mark them N/A.

### 2. Agree the Should / Could boundary

Before sorting, write down one objective rule that separates a Should from a Could (for example, the number of affected users). Keep it for the whole list.

### 3. Sort

Start every item as Won't Have and move it up only with a reason tied to an objective. For each proposed Must ask the two tests from the card: what happens if it is missing, and would we stop the deployment without it. Check that no Must depends on a Should or Could. Split items that look like a Must only in part.

### 4. Check the balance

Sum the effort per group. Musts should be at most about 60%, Coulds about 20%; Won't Haves are excluded. If effort is missing, say the check cannot be run and give counts only, marked as counts. If Musts exceed 60%, name which items to split or demote.

### 5. Show, then write

Show the result in chat first as a table: group, item, reason, effort; then the balance and the decision. Write a file only after the user confirms. Ask for the output path (default `moscow-<topic>.pptx` in the working directory). Save the data as JSON:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "MoreThan TALK (University of Southampton student project), site requirements, 2018",
    "timeframe": "Whole project: first version of the site; priorities per requirement",
    "effort": "N/A: the page gives no effort estimates. By count: 25 Must of 48 rows (52%)",
    "must": ["Login with username and password", "Profile page for every user", "Choose which data is public"],
    "should": ["Login via Google or Facebook", "Automatic translation of profiles"],
    "could": ["Link to city or country information", "Email alert on a new message"],
    "wont": ["Account lock after three failed logins", "User-created page layout"],
    "decision": "N/A: the page records no scope decision or cut line; 3 of 48 rows have no rating"
  }
}
```

Limits that fit the rendered slide: title under 80 characters; timeframe and effort under 100; each group up to six items under 45 characters (the rest stays in chat); decision under 200. A list of strings becomes lines. Run from the repo root:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run scripts/fill_pptx.py <this skill dir>/moscow-prioritization.pptx data.json <output>.pptx
```

`uv run scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's list in any form and check it against the common mistakes in card.md:

1. Everything, or almost everything, is a Must.
2. Balance is judged by item count, not by effort.
3. Musts were inflated by pressure, without the cancel and workaround tests.
4. There is no Won't Have list.
5. One priority is used for all timeframes.
6. A Must depends on a Should or Could.
7. Priorities were set once and not reviewed after each timebox.
8. Items are ranked inside a group, as if MoSCoW ordered them.

Items 3 and 7 usually cannot be judged from the list alone: ask the user instead of reporting a finding. Also check the timeframe and the Should / Could boundary. Report findings as a numbered list: item, what is wrong, why it changes the plan, the concrete fix. End with a verdict: "scope is protected", "works after changes" or "no flexibility left".

Example: 14 items, 11 Musts, no effort, no Won't list. Findings: item 1, 11 of 14 is too many, split large items and apply the cancel test; item 2, add effort and check the 60% limit; item 4, list what is out for this timeframe. Verdict: "no flexibility left".
