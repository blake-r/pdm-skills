---
name: forces-of-progress
description: Lay out the four forces behind a customer's switch from a current solution to a new one (push of the current situation, pull of the new solution, habit of the present, anxiety about the new), judge which side wins, choose which force to move and how to check it, and produce a one-slide PPTX, or review an existing forces breakdown. Use when customers do not switch to a better offer, a new feature does not replace the old way, or the team wants to know why customers leave or stay.
---

# Forces of Progress

The theory, forces, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings interviews, surveys or observations about a switch, **review** when the user brings a finished forces breakdown or a decision drawn from one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the switch: from what current solution to what new one, and for which customers;
- the evidence: interviews, survey results, support tickets, switching data; who was asked — customers who switched, nearly switched and stayed;
- shares of customers per factor, if known;
- the switching rate now, and the goal, if there is one.

Do not invent factors or shares. If the user has only the team's guesses, say so, mark them "hypothesis" and name who to ask.

### 2. Sort factors

Put each factor under one force: push (what is wrong with the current way), pull (what the new one promises), habit (what the customer would give up or is used to), anxiety (what could go wrong with the new one). Keep the customer's words where possible and add the share and the source in brackets. A factor that fits two forces goes where it acts on the decision: "fees are high" is push, "the new bank is cheaper" is pull. A force counts only if the customer feels it: an overpayment the customer does not notice is an analyst's fact, not push. Write such facts in the balance, next to what customers perceive.

### 3. Weigh

State which side wins now, using switching data if there is any. Name the weakest force for the switch and the strongest against it. Do not turn the forces into a score: the model gives direction, not size.

### 4. Decide

Choose the force or forces to move and the measures for each. Consider reducing anxiety and habit before adding more pull. Name the expected switching rate or share and the date of the check. Do not promise effects.

### 5. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, the current and new solutions, the four forces, the balance and the decision. Write a file only after the user confirms. Ask for the output path (default `forces-of-progress-<topic>.pptx` in the working directory). Save the data as JSON:

```json
{
  "text": {
    "title": "UK current accounts: why customers do not switch banks (CMA, 2016)",
    "current": ["Current account at the same bank for years"],
    "new": ["Current account at another bank"],
    "push": ["Over half very satisfied with their bank"],
    "pull": ["Little gain seen, though ~90% would gain £92 a year"],
    "habit": ["No end date; over half with bank 10+ years"],
    "anxiety": ["Over half see a hassle; over 40% fear a failure"],
    "balance": ["3% switched in a year, 8% in three years", "Habit and anxiety outweigh weak push and pull"],
    "decision": ["Anxiety: oversee CASS, extend payment redirection", "Habit: reminders to review the account", "Pull: service quality information, open banking"]
  }
}
```

The JSON above is the CMA case from card.md. Keep up to about four factors of under 45 characters per force and up to four lines in the balance and the decision; list the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/forces-of-progress.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's breakdown in any form and check it against the common mistakes in card.md:

1. All four forces are filled, not only push and pull.
2. Factors come from customers, with sources, and are what customers perceive, not the team's guesses or analysts' facts.
3. The evidence includes customers who stayed or nearly switched, not only those who switched.
4. Each factor sits under the right force.
5. The balance is stated, and switching data is used if it exists.
6. The decision names which force to move and why that one.
7. The decision targets the strongest force against the switch, not only more pull.
8. The decision has an expected result and a date to check.

Items 2 and 3 often need the user's knowledge: ask instead of reporting a finding. Report findings as a numbered list: force or factor, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
