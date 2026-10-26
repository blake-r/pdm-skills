---
name: five-whys
description: Run or review a 5 Whys root-cause analysis of an incident, a failed metric or a recurring complaint, and produce a filled 5 Whys slide. Use when the user wants to find why something happened or to check an existing why-chain.
---

# 5 Whys

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a problem, **review** when the user brings a finished chain.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the problem as a fact: what happened, where, when, how much (a number and a date);
- the timeline of events;
- where answers can be checked: logs, dashboards, people involved.

If the problem is phrased as an opinion ("checkout is bad"), propose a factual wording and get it confirmed.

### 2. Build the chain

1. Ask "why did this happen?" and record only answers the user backs with evidence. You may suggest candidate causes, but label each one "hypothesis, needs checking" and do not move past it until the user confirms it.
2. Repeat "why?" for each confirmed answer.
3. After each level, read the chain bottom-up with "therefore" and point out any link that does not follow.
4. Stop at a cause the team can change (a rule, a process, a working condition) whose removal would have prevented the problem. The chain may be shorter or longer than five.
5. If one level has several confirmed causes, follow each branch separately; each branch gets its own file (run the fill script once per branch).
6. If the answer drifts to a person ("the operator made a mistake"), ask why the process allowed it.

If the problem clearly has several independent causes, say that one linear chain will hide some of them and agree with the user which branch to follow first.

### 3. Close

Agree on the root cause, a countermeasure (what changes, owner, deadline) and a check (a metric or event that shows the problem did not recur). To test the countermeasure as a hypothesis, suggest the `hadi-canvas` skill.

### 4. Show, then write

Show the result in chat first:

| Level | Answer | Evidence |
|---|---|---|
| Problem | … | … |
| Why 1 | … | … |

followed by the root cause, the countermeasure and the check.

Write a file only after the user confirms. Ask for the output path (default `five-whys-<topic>.pptx` in the working directory). Save the data as JSON:

```json
{
  "text": {
    "title": "Checkout errors rose 3x in March",
    "problem": "Payment errors on checkout: 412 in March, 130 in February (12 March to 19 March)",
    "why_1": "The payment gateway timed out on card tokens older than 24 hours",
    "why_2": "Token refresh runs once a day and the job failed silently on 11 March",
    "why_3": "The job has no alert on failure, so nobody saw it for a week",
    "root_cause": "Failed background jobs do not raise alerts",
    "countermeasure": "Alert on any failed refresh job; owner: payments lead; deadline: 30 April",
    "check": "Errors per 1000 checkouts stay below the February level for 4 weeks"
  }
}
```

Keys are `title`, `problem`, `why_1` … `why_5`, `root_cause`, `countermeasure`, `check`. Omit `why_4` and `why_5` when the chain is shorter; their levels are removed from the slide. For a chain longer than five, join adjacent levels in one box with " → ". Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/five-whys.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's chain in any form (text, slide, document) and check it against the common mistakes in card.md:

1. The problem is a fact with a number and a date, not an opinion.
2. Every answer is backed by evidence; hypotheses are marked.
3. Read bottom-up with "therefore", every link follows.
4. The root cause is a process or condition, not a person.
5. The root cause is within the team's control.
6. Other causes on each level were considered; a single chain is justified.
7. The chain did not stop at a symptom or overshoot the team's leverage.
8. The countermeasure has an owner and a deadline.
9. There is a check that shows the problem did not recur.

Report findings as a numbered list: where (level or field), what is wrong, why it matters, the concrete fix. End with a verdict: "root cause found", "root cause not found yet" or "chain needs evidence", and the single most important fix.
