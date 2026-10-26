---
name: validation-board
description: Run a Validation Board for a new product idea - customer and problem hypotheses tracked across pivots, the core assumptions, the riskiest one, the cheapest method to test it and the minimum success criterion set before getting out of the building, then the result (validated or invalidated) and the pivot - and produce a one-slide PPTX; or review an existing board. Use at the start of a new product or direction when the team is sure of the idea but has not checked that customers have the problem, when the team keeps switching segments and loses track of what it rejected, or when an idea must be tested cheaply before development.
---

# Validation Board

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings an idea or test results, **review** when the user brings a finished board.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the idea and who the team thinks the customer is;
- the problem the customer supposedly has;
- what the team already did: conversations, sign-up pages, sales, with numbers and dates;
- the time and money available for testing.

Do not invent customer answers, counts or results. If nothing has been tested yet, the board is a plan: fill the top-left column and the experiment, leave the results empty.

### 2. Hypotheses and the riskiest assumption

Write the customer and the problem as specifically as possible. List the core assumptions that must be true. Pick the riskiest one and phrase it so it can be proved wrong, without subjective words. Do not write a solution hypothesis until the customer and problem are validated.

### 3. Method and criterion

Pick the cheapest method that answers the question: conversations first, then an offer to sign up or pay, then delivering the service by hand. Set the minimum success criterion as a number before going out (for example "5 of 10 confirm the problem"); count customers, not friends.

### 4. Result and pivot

Compare the result with the criterion. Validated: keep going and pick the next riskiest assumption, moving to the solution once customer and problem hold. Invalidated: propose a pivot of the customer or the problem into the next column, based on what customers said.

### 5. Show, then write

Show in chat first: the pivot table, the experiment, the result and the next step. Write a file only after the user confirms. Ask for the output path (default `validation-board-<product>.pptx` in the working directory). Save the data as JSON (the example is the Fashion Metric case from card.md; the board shows the thresholds, not the counts):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Fashion Metric: Lean Startup Machine board, 2012",
    "customer_0": "Shop for clothes alone",
    "problem_0": "Can't decide what to buy",
    "solution_0": "",
    "customer_1": "Fashionable men aged 20–40 from big cities",
    "problem_1": "Hard to find clothes that fit well",
    "solution_1": "",
    "customer_2": "", "problem_2": "", "solution_2": "",
    "customer_3": "", "problem_3": "", "solution_3": "",
    "customer_4": "", "problem_4": "", "solution_4": "",
    "assumptions": ["Need real-time advice", "Need help finding clothes by fit", "Will sign up for such a service"],
    "riskiest": "Will sign up for a service that helps find clothes by fit",
    "method": "An offer to sign up (after conversations)",
    "criterion": "80% sign-ups (conversations: 5 of 10)",
    "results": ["The number interviewed and agreed is not given on the board", "Dates and further results not published"],
    "invalidated": "Need real-time advice → pivot of the customer and problem",
    "validated": ["Need help finding fitting clothes", "Will sign up"]
  }
}
```

Leave unused cells as empty strings. Table cells take under 45 characters. `assumptions` takes up to five items, `results` and `invalidated` up to three items, all under 60 characters; `validated` up to two items under 35 characters; `riskiest`, `method` and `criterion` one sentence under 60 characters. Each list item becomes its own paragraph. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/validation-board.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's board in any form and check it against the common mistakes in card.md:

1. The customer is a specific group that can be found and asked, not "everyone".
2. Customer and problem are validated before any solution is tested.
3. The riskiest assumption can be proved wrong and has no subjective words.
4. The minimum success criterion is a number set before going out, counted on customers.
5. After an invalidation the customer or the problem changes, not just the wording.
6. The method is the cheapest one that answers the question.

Report findings as a numbered list: what is wrong, why it misleads the decision, the concrete fix. End with a verdict: "board supports the decision", "supports it after fixes" or "not enough data".
