---
name: physical-modeling
description: Plan or review Physical Modeling - checking a solution hypothesis on a life-size physical model or mock-up of a product or environment (cardboard, 3D print, marked-out room, props) by running prepared scenarios against success criteria, fixing the model at once and re-running - and produce a one-slide card. Use when the user wants to test a branch, pick-up point, warehouse, POS, terminal, packaging or device layout before building it.
---

# Physical Modeling

The definition, steps, limits and the worked case (Intesa Sanpaolo and frog, 2014-2015) are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language. The card avoids the word "prototype" and other tools' names; keep to that wording ("physical model", "mock-up") when quoting it.

Pick the mode from the request: **do** when the user plans a model test, **review** when the user brings a plan or results and wants them checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the solution and the hypothesis: what is physical in it (size, placement, shape, a person's path) and for whom;
- the model: dimensions, materials, props, where it will stand, budget;
- participants: future users and staff, how many;
- scenarios, including rare and problem situations, and a measurable success criterion for each;
- term, number of fix-and-rerun cycles, decision owner.

If the product is complex, say that cost and feedback time grow with complexity (card.md) and propose a smaller part to model. Do not invent numbers: mark unknown values "not in source" or "unknown".

### 2. Scenarios and criteria

Check that scenarios cover the domain fully (PAF) and that every criterion is written before the first run. Criteria examples (card author's suggestion): operation time, number of errors, share who managed without a hint.

### 3. Run and fix

Run each scenario with future users and staff (card author's suggestion), measure, change the model at once and run the scenarios again. Record run 1, the change and run 2 per scenario.

### 4. Decision

Criteria met in all scenarios: move to development. Not met after fixes: rethink the solution. Warn that the model shows usability in the given scenarios, not demand, willingness to pay or behavior over months (card author's conclusion).

### 5. Show, then write

Show the card in chat first as a table by template blocks: title, hypothesis, model, participants, term, three scenario rows (scenario, criterion, run 1, change, run 2), decision. Write a file only after the user confirms. Ask for the output path (default `physical-modeling-<product>.pptx` in the working directory). Save the data as JSON. The example is the Intesa Sanpaolo case from card.md; what the source does not give says "not in source":

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Intesa Sanpaolo and frog: new branch model, 2015",
    "hypothesis": "Not in source. Card author's conclusion: the new model is understandable to customers and staff",
    "model": "Full-size branch model; material and location not in source",
    "people": "600+ customers and 300+ staff",
    "term": "5 weeks of trials, from March 2015; launch in June 2015",
    "sc1": "Not in source", "sc2": "—", "sc3": "—",
    "cr1": "Not in source", "cr2": "—", "cr3": "—",
    "ra1": "No figures", "ra2": "—", "ra3": "—",
    "ch1": "Design was refined along the way; which edits, not in source", "ch2": "—", "ch3": "—",
    "rb1": "Not in source", "rb2": "—", "rb3": "—",
    "decision": ["June 2015: the new design launched for the public", "frog: 50 branches in 2015, another 1,000 planned for 2016", "Bank (27.10.2015): full update of 50 medium and large branches by year end, goal about 1,000", "The bank's release does not mention frog; a link to the trials is not in the source"]
  }
}
```

Limits that fit the rendered slide: title under 60 characters; hypothesis under 130; model, people and term under 110 each; each table cell (sc, cr, ra, ch, rb) under 60; decision up to four items under 70 each. Unused table cells say "—", unused text fields "not in source". A list of strings becomes lines. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/physical-modeling.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's plan, notes or results and check them against the common mistakes in card.md:

1. Criteria are set after the run.
2. The model is far from reality (wrong dimensions, heights, distances, no props); the card says as close to reality as possible.
3. Scenarios do not cover the domain: only typical cases, no queue, error or atypical user.
4. Fixes are not re-run, so nobody knows whether they helped.
5. Participants are the wrong people, for example the own team that knows the idea (card author's conclusion).
6. Usability is taken for demand: a successful run does not prove that customers will pay (card author's conclusion).
7. Everything is modeled at once, so a complex product makes the model costly and the cycle long.

Items 1, 4 and 5 usually cannot be judged from a description alone: ask when criteria were written, whether scenarios were re-run after each change and who took part. Report findings as a numbered list: what is wrong, why it misleads, the concrete change. End with a verdict: "model test is sound", "works after changes" or "needs scenarios and criteria first".

Example: a cardboard pick-up point tested once with colleagues, criteria written afterwards. Findings: item 1 - criteria after the run, set thresholds before the next one; item 5 - colleagues know the idea, invite future users; item 4 - no re-run after fixes. Verdict: "works after changes".
