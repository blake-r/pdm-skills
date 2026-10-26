---
name: six-thinking-hats
description: Run a decision or discussion through de Bono's Six Thinking Hats (white facts, red feelings, black risks, yellow benefits, green new options, blue process), record the conclusions under each hat and the decision, and produce a one-slide PPTX, or review an existing hats session. Use when a choice between options goes in circles, one voice dominates the discussion, or emotions mix with facts.
---

# Six Thinking Hats

The theory, hats, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a question or a choice to think through, **review** when the user brings notes from a finished session or a decision drawn from one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the question in one sentence and the options, if there are any;
- the known facts with their sources and dates;
- who takes part and who decides;
- the deadline for the decision.

If the decision is obvious, cheap to undo or purely a calculation, say that the hats add little and stop unless the user insists.

### 2. Set the order

Propose an order that opens and closes with the blue hat. For a choice between options de Bono's sequence is blue, white, (green), yellow, black, red, blue. If the user runs it as a meeting, plan about two minutes per hat, a longer white hat at the start and about 30 seconds for red.

### 3. Go hat by hat

Under each hat write 3–5 short points in that mode only; move points of another mode to their hat. Under white, separate facts with sources from missing data. Do not invent facts, feelings or numbers: red comes from the user and the participants, not from you; if they have not said it, ask. Under black and yellow, go through every option so each has both risks and benefits. Under green, add combined and intermediate options.

### 4. Decide

Under the blue hat write how the session went: the question, the order, who led it. Put the decision itself in the decision block: what was decided, who owns it, the date and the metric that shows it worked. If the facts under white are too thin to decide, say so and name what to find out first.

### 5. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, six hats, the order and participants, and the decision. Write a file only after the user confirms. Ask for the output path (default `six-thinking-hats-<topic>.pptx` in the working directory). Save the data as JSON:

```json
{
  "text": {
    "title": "What to do after the ad account was blocked?",
    "white": ["The product is tailored to Google search", "An appeal — weeks with no guarantees"],
    "red": ["Anger at the block", "Fear of losing everything in grey schemes"],
    "black": ["Grey schemes: a chain ban"],
    "yellow": ["Agency account: quickly get back to testing"],
    "green": ["Appeal and agency account in parallel"],
    "blue": ["Question: how to get traffic back", "Led by the author"],
    "order": ["White → red → black → yellow → green → blue", "Participant: the product's author"],
    "decision": ["Appeal and an agency account", "Metrics: install cost, account stability", "Check: first weeks of the account's operation"]
  }
}
```

Keep the title to one line of under 90 characters, each hat to four list items of under 40 characters, and the order and the decision to four items of under 60 characters each; list the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/six-thinking-hats.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's session notes in any form and check them against the common mistakes in card.md:

1. The question is one sentence and the session opens and closes with the blue hat.
2. Hats were worn by the whole group in turn, not assigned to people.
3. Each hat holds only its own mode: no risks under white, no flaws under yellow.
4. White separates facts with sources from missing data.
5. Red is present and not argued.
6. Every option has both black and yellow points.
7. The session ends with a decision, an owner, a date and a metric.

Item 2 usually cannot be judged from the notes: ask the user instead of reporting a finding. Report findings as a numbered list: hat, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
