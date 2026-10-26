---
name: expert-interview
description: Plan an expert interview (checking hypotheses with market experts instead of end consumers; interview, workshop or survey form) and produce a one-slide plan with results, or review an existing expert-interview plan or readout. Use when consumers are hard to reach, when a hypothesis is about the market, rules, partners or channels, when roles of experts must be chosen, or when expert answers are turned into a decision.
---

# Expert Interview

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user is planning expert interviews or reading their results, **review** when the user shows a plan or a readout and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the hypothesis and the decision that depends on it;
- which roles of experts know the answer and how each knows consumers (work, not opinion);
- how many people are reachable and in which form (interview, workshop, written questions);
- whether answers already exist (then ask for them per role, in the experts' words);
- what is already known and what must be measured on consumers.

If the user needs shares or counts, say that expert interviews do not measure behaviour quantitatively (PAF) and ask what they want to decide. Never invent names, numbers or quotes: write "not in the source" for what the user did not give.

### 2. Hypothesis, decision and roles

Write the hypothesis and the decision it feeds. List roles of experts; more than one role (author's advice). Note for each role its own position and interest.

### 3. Questions

Draft three to six open questions about the experts' real experience and barriers, not about the user's idea and not hypothetical situations. Follow the general PAF interview tips: hypotheses fixed beforehand, no answer hidden in the question, agreed goal and time, two people (one talks, one records). PAF gives no number or duration of expert sessions; do not invent them. State for each question what decision it serves.

### 4. Answers and conclusion

If answers exist, record what each role said separately from the conclusion; label the conclusion as the author's. Compare roles and keep disagreements. Name what the data does not show (participants, exact words, missing roles).

### 5. Decision and check

Propose a decision and a way to check it on consumers or in data (author's advice).

### 6. Show, then write

Show the plan in chat first as a table by template blocks: title, hypothesis, experts, format, question rows (question, expert answer or author's summary with role, conclusion), gaps, decision, check. Write a file only after the user confirms. Ask for the output path (default `expert-interview-<topic>.pptx` in the working directory). Save the data as JSON. The example is the M-PESA case from card.md; what the source does not give says so:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "M-PESA: workshops with market players, Kenya",
    "hypothesis": "What hinders the growth of financial services and access to them? Decision: which service to pilot",
    "experts": "Banks, MFIs, technology providers, NGOs, regulators; the source gives no number",
    "format": "Open workshops in Nairobi and Dar es Salaam after the grant contracts were signed; the source gives no dates",
    "q1": "Suppose technology can do anything: what are the main difficulties in growing and accessing finance?",
        "a1": "Authors' summary: (1) processes will be faster; (2) it must be very simple for the client to get finance",
    "c1": "Authors: took the second conclusion (simplicity for the client)",
    "gaps": ["Participants and their number are not named", "No verbatim answers", "No workshop dates"],
    "decision": ["Pilot: operator, MFI, bank", "Loan and repayment from the phone via top-up agents"],
    "check": ["Pilot with Faulu Kenya from 11.10.2005", "Clients started sending money: the launch was already built on this"]
  }
}
```

Limits that fit the rendered slide: title under 60 characters; hypothesis, experts and format under 120 each; questions (q1..q4) under 90; answers (a1..a4) under 90; conclusions (c1..c4) under 70; gaps, decision and check: up to three items under 60 each. A list of strings becomes lines, one thought per item. Unused rows (q3, q4, a3, a4, c3, c4) stay empty and the script prints a harmless warning. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/expert-interview.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's plan or readout and check it against the common mistakes in card.md, one by one:

1. An expert replaces the consumer: the expert's words about a "typical customer" are taken as data about the user's customer.
2. Numbers from an expert: "70% of clients" is presented as a measurement.
3. One role only: all experts are banks, or all are regulators.
4. Belief without allowance for the expert's position and psychological distortions.
5. A question about the user's idea instead of the expert's work, so the answer is a polite "yes".
6. Words and conclusion merged: it is not visible what the expert actually said.
7. Available experts instead of the needed ones.
8. No check of the decision on consumers.

Items 3, 4, 7 and 8 cannot be judged from the questions alone. First ask which roles were interviewed, how they were found, and how the decision will be checked; if the user does not know, mark the item "not checked" instead of reporting a finding. Also check that a conclusion is labelled as the author's, that disagreements between roles are kept, and that a decision exists. Report findings as a numbered list: what is wrong, why it distorts the answer, the concrete rewrite. End with a verdict: "plan answers the question", "works after changes" or "needs a hypothesis and expert roles first".

Example: the readout says "Three bankers confirmed: 70% of small shops will use the card", the question was "Would our card be useful?", all three came from one bank. Findings: item 2 — a share from experts, replace with "bankers expect interest" and check on shops; item 5 — ask about their work and barriers; item 3 and item 7 — add other roles and say how the bankers were found. Verdict: "works after changes".
