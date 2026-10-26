---
name: now-next-later-roadmap
description: Build or review a Now-Next-Later roadmap, a product plan of three columns (Now, Next, Later) with business objectives instead of dates, and produce a one-slide roadmap. Use when a timeline roadmap keeps slipping, stakeholders ask for dates, a team wants a roadmap built around problems and OKRs, or the user says "now next later", "roadmap without dates", "дорожная карта now-next-later", "роадмап без дат".
---

# Now-Next-Later Roadmap

The theory, the column meanings and the case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language. Examples are format only: never reuse the example's values for the user's product; a missing value is "N/A".

Pick the mode from the request: **do** when the user is building or converting a roadmap, **review** when the user shows an existing one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product or team and the planning period;
- the business objectives or OKRs the work serves;
- the problems to solve (customers, business, technical), not only ideas and features;
- current candidate ideas, experiments and features, and any existing timeline roadmap to convert;
- how certain each item is, and which items have a real deadline (law, contract) and who set it;
- who reads the roadmap and what they expect (dates?).

If the user gives only features, ask for the problem behind each one. If there are no objectives, say the roadmap will be unlabelled and mark it N/A rather than inventing them.

### 2. Horizons and sorting

Write one sentence for what Now, Next and Later mean for this team, without calendar dates. Sort items by urgency and certainty: Now is specified work being built; Next follows Now and is less detailed; Later is large problems without solutions. Items should be problems, each with its idea or experiment. Tie every item to an objective; flag items with none.

### 3. Deadlines and the decision

Put a real deadline on the item with its source. Name the decision the roadmap supports (what enters Now, what leaves, what stakeholders hear) and how dates are explained to them.

### 4. Show, then write

Show the roadmap in chat first as a table by template blocks: title, objectives, Now, Next, Later, decision. Write the file only after the user confirms. Ask for the output path (default `now-next-later-roadmap-<product>.pptx` in the working directory). Save the data as JSON. The JSON below shows the format only, with values from the WooCommerce case of card.md; use it only when the user asks for an example. Otherwise fill each field with the user's facts and write "N/A" where there is none.

```json
{
  "text": {
    "title": "WooCommerce public roadmap, announced 30 May 2023",
    "objectives": "Give the developer community visibility into current work, future plans and the overall direction of WooCommerce. Items by objective: N/A (the announcement lists no items)",
    "now": ["Projects the team is currently working on", "Item names: N/A (not in the announcement)"],
    "next": ["Projects the team is committed to executing but has not started", "Item names: N/A (not in the announcement)"],
    "later": ["Projects being scoped and likely to happen, not yet scheduled", "Item names: N/A (not in the announcement)"],
    "decision": ["Roadmap published as a living document, kept updated", "Fourth stage Ideation: planned, no work begun", "Office hours and community events to discuss items"]
  }
}
```

Limits that fit the slide: title under 70 characters; objectives under 220 characters; now, next, later: up to six items under 70 characters each, each item "problem: idea (objective)"; decision: up to four items under 80 characters. A list of strings becomes lines. Run from the repository root:

```bash
uv run scripts/fill_pptx.py <this skill dir>/now-next-later-roadmap.pptx data.json <output>.pptx
```

`uv run scripts/fill_pptx.py <template> --list` prints every placeholder and its hint. `example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

## Mode: review

Check the user's roadmap against the common mistakes in card.md:

1. Dates or quarters sit under the columns, so it is a timeline in disguise.
2. The horizons are not defined: nobody can say what Next means.
3. Items are ideas or features, not problems.
4. Now is full of output with no objective labels (feature factory).
5. Stakeholders were not told why dates were replaced by horizons; Next is read as a promise.
6. Accountability was dropped: no OKRs or other commitments back the roadmap.
7. Later is detailed as much as Now, or the columns are forced equal.

Items 5 and 6 usually cannot be judged from the roadmap alone: ask what stakeholders were told and where commitments live, instead of reporting a finding. Report findings as a numbered list: what is wrong, why it matters, the concrete change. End with a verdict: "works as a roadmap", "works after changes" or "is a timeline in disguise".

Example: columns "Q1, Q2, Q3" renamed Now, Next, Later, with feature names and no objectives. Findings: item 1, the quarters stay as hidden dates; item 3, features without problems; item 4, no objective labels. Verdict: "is a timeline in disguise".
