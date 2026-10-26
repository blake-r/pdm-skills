---
name: opportunity-solution-tree
description: Build or review an Opportunity Solution Tree (Teresa Torres, Product Talk) on one slide - one outcome, customer opportunities, a target opportunity, three solutions and the assumption tests for them. Use for continuous discovery, "what should we build next", "map the customer needs behind this outcome", "opportunity tree", "OST", "compare solutions before building", "choose which customer problem to solve first", or to check whether a tree has solutions disguised as opportunities.
---

# Opportunity Solution Tree

The theory, steps, limits and the Grailed case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings an outcome and interview material, **review** when the user brings a finished tree.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product, the team and the one outcome (a product outcome is preferred);
- the target customer and the value proposition;
- interview material: notes or stories from at least three or four story-based interviews;
- opportunities, solutions and tests already on the table, if any.

Do not invent opportunities, numbers or results. A missing value is "N/A"; say how to get it (for example: "interview three more customers about the last time they ...", or "no test has run yet"). The values in the JSON below are the Grailed case, not data for the user's tree. If no interviews exist, say the tree would hold guesses and offer a first interview plan (In-Depth Interview) before continuing. If this skill runs inside pdm-brief, the questions above are answered by pdm-brief's fallback.

### 2. Build the tree step by step

1. Confirm the single outcome; if the user gives several, ask which one this tree serves.
2. Turn interview notes into opportunities in the customer's words; group similar ones under a parent. Test each: if only one way addresses it, it is a solution in disguise, rewrite it. Keep effort out of the judgement.
3. Propose the target opportunity with the reason and let the user pick. Work on one.
4. Brainstorm solutions for the target only; shortlist three.
5. For each solution name the riskiest assumption and a quick test, with the result if one has run, else "N/A".
6. State the decision: drop, refine for delivery, or choose a new target opportunity.

### 3. Show, then write

Show in chat first, block by block as they will appear on the slide: title, outcome, three opportunities (the middle one is the target), three solutions, three assumption tests, decision. The template has exactly three opportunities; list the rest in chat. Write the file only after the user confirms. Ask for the output path (default `opportunity-solution-tree-<product>.pptx` in the working directory). Save the data as JSON. Limits: title under 80 characters; outcome under 100; each opportunity under 90; each solution under 80; each test under 110; decision under 140. Each list item becomes its own paragraph.

```json
{
  "text": {
    "title": "Grailed Discovery team: a feed for users who browse without a specific item",
    "outcome": "N/A: the article does not state the outcome; reported result is about 20% higher LTV for feed users",
    "opp1": "Show me things I interact with",
    "target": "Show me stuff that's popular",
    "opp3": "There should always be new stuff when I come",
    "sol1": "Add popular items to the feed for users who want them",
    "sol2": "Interleave content and recommendations with different parameters",
    "sol3": "Track previously seen items to keep the feed fresh",
    "test1": "Quick low-lift test; the result of this test is N/A",
    "test2": "N/A: no individual experiment results in the source",
    "test3": "N/A: no individual experiment results in the source",
    "decision": "Feed developed over about 6 months; feed users: ~30% more app opens, ~40% more discoveries, ~20% higher LTV"
  }
}
```

The Grailed article shows the tree only as images, so the outcome, target and tests are N/A or our reading; say this in chat if the example is shown. Run from the repo root:

```bash
uv run scripts/fill_pptx.py skills/product-planning/opportunity-solution-tree/opportunity-solution-tree.pptx data.json <output>.pptx
```

`uv run scripts/fill_pptx.py <template> --list` prints every placeholder and its hint. `example.json` next to the template is a sample of the finished result; use it only when the user explicitly asks to see an example, otherwise fill in the user's own data.

## Mode: review

Take the user's tree in any form and check it against the common mistakes in card.md:

1. Every opportunity is an unmet need in the customer's words, not a solution (a one-way opportunity is a solution in disguise).
2. Opportunities come from interviews, not from the team's ideas.
3. No branch was reshaped on a single interview.
4. Solutions are brainstormed for the one target opportunity only, and at least three are compared.
5. Tests target the riskiest assumptions, not the whole idea or a built feature.
6. The tree has one outcome, one team and a stable top, with the work in the lower branches.

Report findings as a numbered list: node or branch, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "tree holds", "tree changes after fixes" or "not enough interview evidence to judge".
