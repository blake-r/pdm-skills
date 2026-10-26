---
name: ansoff-matrix
description: Sort a company's or product's growth ideas on the Ansoff Matrix (product-market grid) - market penetration, market development, product development, diversification - decide which growth direction to pursue and produce a one-slide PPTX, or review an existing Ansoff matrix. Use when a team asks where growth will come from, whether to enter a new market or launch a new product, how risky a growth idea is, or says "Ansoff", "growth strategy options", "product-market grid", "expand to new segments or new products".
---

# Ansoff Matrix

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a company or product and growth ideas, **review** when the user brings a filled matrix.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the unit (company or product line) and the planning horizon;
- current products and current markets (segments, regions, channels), with the definition of "existing";
- the growth ideas already on the table, and the evidence behind each (customer data, research, competitor moves);
- what the company lacks for each idea: skills, channels, partners, regulation, budget;
- the constraints: the share left to win, the budget, the deadline.

Do not invent figures. Mark what the user did not give as N/A. If there are no growth ideas, offer to brainstorm at least one per cell, and say that the ideas are hypotheses until checked.

### 2. Define "new"

Write in one line each: what counts as an existing product and an existing market for this unit. Keep these definitions for the whole exercise.

### 3. Place the ideas

Put each idea in one cell by two questions: is the product new to the company, are the customers new to it. Split an idea that needs both a new product and a new segment. If the user's classification looks off, say so and explain.

### 4. Compare and choose

Show what is new in each cell and what evidence is still missing. Use the risk order (penetration lowest, diversification highest) as a prior, not a verdict. Propose one direction, at most two, with an owner, a date, a metric and a stop condition, and say why the other cells were rejected. If the user gave no basis for a choice, say that the grid only sorts and ask for the evidence.

### 5. Show, then write

Show the result in chat first as a table by template blocks: title, four cells, chosen direction, decision. Write a file only after the user confirms. Ask for the output path (default `ansoff-matrix-<company>.pptx` in the working directory). Save the data as JSON. The example is the Amazon case from card.md; a field with no fact says N/A.

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Amazon, grocery: Whole Foods Market deal, June 2017",
    "pen": "N/A: the press release gives no figures on Amazon's existing grocery sales",
    "dev_p": "N/A: not described in the press release",
    "dev_m": "N/A: not described in the press release",
    "div": "Buy Whole Foods Market, a natural and organic grocery chain: about $16 billion sales in fiscal 2016, 460+ stores in the US, Canada and the UK. $42 per share in cash, about $13.7 billion with net debt",
    "choice": "Diversification: the release does not name the matrix, the quadrant is our reading",
    "decision": "16 June 2017: agreement to acquire. Whole Foods keeps its brand, John Mackey stays CEO, headquarters stay in Austin. Closing expected in the second half of 2017 after shareholder and regulatory approval"
  }
}
```

Field limits that fit the rendered slide: title under 70 characters; each of pen, dev_p, dev_m, div under 230 characters (up to four short lines); choice under 160; decision under 330. A list of strings becomes lines, one thought per item. Put the rest in chat. Run from the repository root:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run scripts/fill_pptx.py <this skill dir>/ansoff-matrix.pptx data.json <output>.pptx
```

`uv run scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's matrix and check it against the common mistakes in card.md:

1. The risk order is treated as a law: a cell is rejected or chosen by its position alone.
2. A renamed or modified product counts as new.
3. "New" is loose: products and markets are not defined, so ideas sit in the wrong cells.
4. Penetration is skipped although share in the current market is still open.
5. The grid is used as a plan: no owner, metric, date or stop condition.
6. Competitors' reaction and the effect on the core business are not considered.
7. The unit is mixed: company-wide and product-line ideas share one grid.

Items 4 and 6 usually cannot be judged from the matrix alone: ask for market share and the competitors' likely response instead of reporting a finding. Report findings as a numbered list: what is wrong, why it matters for the choice, the concrete change. End with a verdict: "direction is justified", "works after changes" or "define the cells and evidence first".

Example: the matrix puts "a loyalty program for existing customers" into diversification, and the decision is "go into the bottom right cell". Findings: item 2 and 3 - the idea sells to current customers, so it is product development at most; define what is new. Item 5 - no owner, metric or date. Verdict: "works after changes".
