---
name: buyer-persona
description: Build or review a buyer persona - a description of the person who chooses and buys a product, built from interviews with recent buyers and focused on decision criteria, barriers, the approval process, budget and alternatives - and produce a one-slide persona, or check an existing one. Use when the team argues about what buyers want, messaging or sales pitches are built on guesses, deals stall in approval, or a persona is made of age and hobbies.
---

# Buyer Persona

The method, the eight blocks, the interview procedure and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language. Do not compare the persona with other tools and do not call it a "customer profile".

Pick the mode from the request: **do** when the user wants to build a persona, **review** when the user shows an existing persona or interview notes and wants them checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and the buyer: who buys, in what segment, which role starts the search or decides;
- interview material: notes or recordings of talks with people who decided in the last months, how many, and whether there are buyers who chose a competitor or bought nothing;
- direct quotes from buyers;
- what the team wants to decide with the persona: messaging, sales pitch, barriers to remove.

If there are no interviews, say that the card builds the persona from conversations with buyers, not from the team's guesses or sales reps' retellings. Offer a plan instead: whom to find (6-10 recent buyers, including those who left or did not buy), the open questions from card.md, 30 minutes each. Do not write the persona from imagination. Do not invent numbers, roles or quotes: mark what the user did not give as unknown.

### 2. Fill the blocks from the interviews

Go through the eight blocks of card.md: company goals, personal motivation, management motivation, decision criteria, barriers, approval process, budget, alternatives. Write each in the buyer's words and from the buyer's view, not as a reverse of the product's features. Take three to five decision criteria and say what the buyer means by each. For the approval process name who starts, who evaluates and who approves, and what they really influence. Mark a block as unknown when the interviews do not cover it, and list the questions for the next interviews.

### 3. Check repeatability and decide

State how many interviews support the persona; if roles differ, propose separate personas. Then write the decision: which messages go first, which barriers to remove, what to give sales, and when to check.

### 4. Show, then write

Show the persona in chat first as a table by template blocks: title, persona, quote, eight blocks, decision. Write a file only after the user confirms. Ask for the output path (default `buyer-persona-<product>.pptx` in the working directory). Save the data as JSON. The example is the Deloitte Private case from card.md; blocks the source does not give are null:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Deloitte Private, family and small business, Aamplify research",
    "persona": "Recently chose solutions like Deloitte Private; the number of interviews is not stated",
    "quote": null,
    "goals": "Global business growth opportunities; solving specific tasks; improving processes with technology",
    "personal": null,
    "management": null,
    "criteria": "The comparison source with competitors does not disclose criteria item by item",
    "barriers": null,
    "approval": null,
    "budget": null,
    "alternatives": "Competitors are mentioned, their composition is not disclosed",
    "decision": ["Three reasons to come are placed at the center of the home page", "Sales were shown how to tell clients the same stories", "The source has no result figures"]
  }
}
```

Limits that fit the rendered slide: title under 70 characters; persona under 90; quote under 100; each of the eight blocks under 150 characters; decision up to three items under 100 each. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/buyer-persona.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's persona and the interview notes and check them against the common mistakes in card.md:

1. The persona is a portrait (age, city, hobbies) and does not explain the choice.
2. The answers come from sales reps, not from interviews with buyers.
3. Pains and benefits are derived from the product's features, not from the buyer's circumstances.
4. The person at the top is assumed to decide everything; real influence at each step is not asked.
5. Only the company's own customers were interviewed; those who left or bought nothing are missing.
6. Blocks are generalities: "quality and price" without what the buyer means by them.
7. The research is one-off and has no date or plan to repeat it.

Items 2, 4 and 5 usually cannot be judged from the persona alone: ask who was interviewed, how many and when, instead of reporting a finding. Also check that the persona is not about the user of the product when the buyer is another person, and that the decision names concrete messages or barriers. Report findings as a numbered list: what is wrong, why it misleads, the concrete change. End with a verdict: "persona explains the choice", "works after changes" or "needs interviews first". If several blocks are empty or marked unknown, the verdict is "needs interviews first" unless the empty blocks are explained by the data, and say which blocks the next interviews must fill.

Example: a persona "Anna, 35, Moscow, likes yoga" with the pain "wants a convenient service", filled in by the sales team. Findings: item 1 - a portrait with no decision; item 2 - sales reps' retelling, not interviews; item 6 - "convenient" is not defined; item 5 - ask who was interviewed. Verdict: "needs interviews first".
