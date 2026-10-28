---
name: pugh-matrix
description: Choose among alternatives with a Pugh matrix (Stuart Pugh concept selection) - criteria as rows, alternatives as columns, one datum alternative, marks better/same/worse (+/S/-) against the datum, counts by formula, optional importance grades - and produce an XLSX with live formulas; or review an existing Pugh or decision matrix. Use when a team must pick among a few alternatives (designs, vendors, solution approaches) with only directional data, or says "Pugh matrix", "concept selection", "decision matrix", "compare options against a baseline", "datum".
---

# Pugh Matrix

The theory, scheme and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user is choosing among alternatives, **review** when the user brings a filled matrix.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the decision and what it should achieve;
- the alternatives (up to 8), each described at a similar level of detail;
- the datum: the current solution, the status quo or the strongest known alternative;
- the criteria (up to 30), each defined so two people mark it alike; where they come from (customer needs, risks, constraints);
- the requirements the alternatives must meet (the criteria come from them), and whether to grade criteria High, Medium or Low (Pugh's grading; numeric weights are not Pugh's, only a later-practice extra, to be agreed before marking).

Do not invent alternatives, criteria or marks. If a mark cannot be justified, leave it blank and say so; blanks are counted in "Criteria not marked".

### 2. Mark and count

Mark each alternative against the datum, one criterion at a time: + better, S same, - worse, with a short reason for contested marks. The spreadsheet counts +, S and - per alternative; that pattern is the result (Pugh: the marks must not be summed as scores). The net, weighted net and ranks are labelled later practice; use them only as a hint. Read the pattern: strong and weak alternatives, criteria that do not discriminate, minuses on the criterion that matters most. Then improve the negatives of strong alternatives (add the improved one as a new column), drop truly weak ones, and rerun with the strongest as the new datum.

### 3. Decision

Write which alternatives are dropped, which go to the next round, what is combined, and which alternative becomes the new datum. If the matrix decides nothing, say so.

### 4. Show, then write

Show the matrix in chat first (a table of criteria by alternatives with the counts), then the decision. Write a file only after the user confirms. Ask for the output path (default `pugh-matrix-<topic>.xlsx` in the working directory).

The JSON below shows the format only. Its values come from the example case in card.md (Corning conveyor, first chart), not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill the fields with the user's facts.

```json
{
  "text": {
    "title": "Corning conveyor: stabilizing short ceramic parts, concept selection, first Pugh chart",
    "datum": "Current T system (plexiglass T supports)",
    "decision": "Sensor Gate and Swedish Wheels dropped; Magnetic Swivel became the datum of the next chart; the final three (Magnetic Swivel, Pincer, Self-nesting T) went to an AHP step, which chose Self-nesting T",
    "alt1": "Magnetic Swivel",
    "alt2": "Pincer",
    "alt3": "4 Bar",
    "alt4": "Sand Bag",
    "alt5": "Sensor Gate",
    "alt6": "2 Long Poles",
    "alt7": "Swedish Wheels",
    "alt8": "Self-nesting T"
  },
  "rows": [
    [
      "Protects Ceramics",
      null,
      "S",
      "S",
      "S",
      "S",
      "S",
      "S",
      "S",
      "S",
      "S"
    ],
    [
      "Scaleable for Ceramics",
      null,
      "S",
      "+",
      "+",
      "S",
      "+",
      "S",
      "+",
      "+",
      "S"
    ],
    [
      "Limit Human Interaction",
      null,
      "S",
      "+",
      "+",
      "+",
      "+",
      "+",
      "+",
      "+",
      "+"
    ],
    [
      "Works with Given Space",
      null,
      "S",
      "+",
      "S",
      "+",
      "S",
      "S",
      "-",
      "+",
      "+"
    ],
    [
      "Works with Conveyor Conditions",
      null,
      "S",
      "+",
      "S",
      "+",
      "+",
      "S",
      "+",
      "+",
      "+"
    ],
    [
      "Material Choice",
      null,
      "S",
      "-",
      "-",
      "-",
      "S",
      "-",
      "S",
      "-",
      "-"
    ],
    [
      "Improves Current Method",
      null,
      "S",
      "+",
      "+",
      "+",
      "S",
      "S",
      "S",
      "S",
      "+"
    ]
  ]
}
```

Row format: criterion, importance ("High", "Medium", "Low" or null for none; a number is accepted for the weighted net only), datum mark (always "S"), then one mark per alternative in column order ("+", "S" or "-"; null for not marked). Do not pass counts, net, ranks or the "Weight used" column: the spreadsheet computes them. Limits: title under 100 characters; datum under 40; alternative names under 20 each; criterion under 45; decision under 250. Run from the repo root:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run scripts/fill_xlsx.py <this skill dir>/pugh-matrix.xlsx data.json <output>.xlsx
```

`uv run scripts/fill_xlsx.py <template> --list` prints the columns with their hints. Keep the number of alternatives to the 8 prepared columns; if fewer than 8 alternatives are used, set the unused alt fields to "" so that their columns stay blank.

## Mode: review

Take the user's matrix in any form and check it against the common mistakes in card.md:

1. Marks summed as absolute scores: the winner is picked by the count without looking at where its minuses are.
2. The datum is weak or never changed; no rerun with the strongest alternative as datum.
3. Alternatives differ in level of detail or kind.
4. Criteria overlap or are vague.
5. Numeric weights added late or after the first result.
6. Only one run: no dropped losers, no improved or combined alternatives, no new datum.
7. The matrix is treated as the decision: nothing written about who decided and what goes on.

Items 2 and 5 usually cannot be judged from the table: ask which datum was tried and when the weights were fixed, instead of reporting a finding. Also check that every alternative has a mark on every criterion and that the datum column is all S. Report findings as a numbered list: what is wrong, why it matters, the concrete change. End with a verdict: "pattern holds", "pattern changes after fixes" or "not enough to choose".

Example: eight alternatives, the winner has the most pluses and a minus on "Protects Ceramics", the only requirement that cannot be missed, one run only, no decision written. Findings: item 1 - the minus is on the decisive criterion; item 6 - run another round with the winner as datum; item 7 - no decision. Verdict: "pattern changes after fixes".
