---
name: stakeholders-matrix
description: Map the people and groups around a product, project or decision on a 2x2 grid - their influence on the product and the product's impact on them - assign a way of working to each quadrant (manage closely, keep satisfied, keep informed, monitor), and produce a one-slide PPTX; or review an existing stakeholder map. Use at the start of a product, project or large change when the outcome depends on many parties (regulator, partners, other teams, management), or when a launch could be blocked by someone nobody thought of.
---

# Stakeholders Matrix

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a product or project, **review** when the user brings a finished map.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product, project or decision, and its deadline;
- the parties the user knows: customers, users, management, adjacent teams, partners, suppliers, regulators;
- for each, what it can do to the product (approve, block, fund, withhold) and what the product changes for it;
- who is known to be for or against.

Do not invent parties or positions. Suggest parties that are often forgotten (regulator, support, legal, security, finance) as questions, not as facts.

### 2. Place the parties

Rate each party on both axes as high or low, with a one-line reason. Split a group whose members differ (supporters and opponents inside "banks" or "management"). Mark for or against separately from the quadrant. Say which placements are the user's estimate and which rest on evidence.

### 3. Way of working

For each quadrant write who engages each party, how often and in what format. Name the decision the map feeds and the date to revisit it.

### 4. Show, then write

Show in chat first: the parties by quadrant with reasons, for or against, the way of working, the decision. Write a file only after the user confirms. Ask for the output path (default `stakeholders-<project>.pptx` in the working directory). Save the data as JSON (the example is the M-Pesa case from card.md; the quadrants are ours, the central bank did not draw a grid):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "M-Pesa: Central Bank of Kenya approval to launch, 2006–2007",
    "manage_closely": ["Safaricom and the CBA bank (customers' money)", "Conditions: trust account, monthly reports to the CBK"],
    "keep_satisfied": ["International banks: \"a crisis is coming\" — against", "Deputy governor — against", "Ministry of Finance: minister for, staff aside", "Service demonstration and candid questions"],
    "keep_informed": ["Kenyan banks and microfinance: depositor outflow", "Explanation: integrate with M-Pesa"],
    "monitor": ["Ministry of Communications — for"],
    "decision": ["Demonstrate the service to all sides", "Conditions for CBA and Safaricom", "March 2007: CBK approved the launch"],
    "result": ["March 2007: 21,714 transactions", "April: 69,740", "December: 1.27 million"]
  }
}
```

Each quadrant is a list: parties first, one per item with for or against, then the way of working. Keep each quadrant to five items and `decision` and `result` to four; items under 50 characters, each becomes its own paragraph. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/stakeholders-matrix.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's map in any form and check it against the common mistakes in card.md:

1. Parties without a formal role (regulator, support, legal) are on the map.
2. Not everyone is in "manage closely".
3. Influence is judged by what a party can do, not by rank.
4. The map has a revisit date and is current.
5. Each quadrant has a way of working: who, how often, in what format.

Report findings as a numbered list: what is wrong, why it misleads the decision, the concrete fix. End with a verdict: "map supports the decision", "supports it after fixes" or "not enough data".
