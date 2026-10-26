---
name: porters-five-forces
description: Analyse an industry with Porter's Five Forces — buyers, suppliers, threat of new entrants, substitutes and rivalry — judge whether the industry is profitable and attractive, and produce a one-slide analysis, or review an existing five-forces analysis. Use when the user is deciding whether to enter a market or niche, asks why an industry has thin margins, or wants a strategy position where competitive pressure is weaker.
---

# Porter's Five Forces

The theory, factors per force, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language. If the user needs a comparison of products with rivals on criteria rather than a verdict on industry profit, say that other tools of the set (strategy canvas, competition map) fit better.

Pick the mode from the request: **do** when the user wants an industry analysed, **review** when the user brings a finished analysis to check.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the industry and its boundaries: product, geography, customer segments;
- the decision behind the analysis: enter a market, choose a niche, change position, explain low margins;
- the players: who they are, shares, number, size;
- the buyers, split by segment; the suppliers of key inputs; possible entrants and what stops them; what else meets the same need in a different way;
- known facts: prices, switching costs, regulation, growth, fixed costs, exit barriers;
- the date and the sources of facts.

Do not invent numbers: mark what the user did not give as unknown and suggest where to look.

### 2. Boundaries

Fix the industry in one line. Warn that too narrow boundaries hide substitutes and too wide ones average different segments.

### 3. Forces

For each force go through its factors listed in card.md, give a level (weak, medium, strong; the scale is the analyst's, not Porter's) and support it with a fact. When the levels are your reading of a source, say so in the title ("estimate from the article"). Split buyers by segment if their power differs. Separate a substitute (same need, different way) from a direct rival.

### 4. Verdict, dynamics, decision

State whether the industry is attractive: few strong forces means high profit potential. Name the strongest force. Add what will change the forces in the coming years. Propose a decision: enter or not, which position to take, which force to weaken and how. If the user has no decision to make, say that a table without a decision changes nothing.

### 5. Show, then write

Show the analysis in chat first as a table by template blocks: title, five forces with level and facts, verdict, dynamics, sources, decision. Write a file only after the user confirms. Ask for the output path (default `porters-five-forces-<industry>.pptx` in the working directory). Save the data as JSON. The example is the PYMNTS payments case from card.md; what the source does not give says so:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "US payments industry (PYMNTS, March 2014), levels — estimate from the article",
    "entrants_level": "medium, barriers fell",
    "entrants": ["Around 2005: internet, mobile, cloud, regulation, 2008 crisis", "clearXchange (banks) — possible new supplier"],
    "suppliers_level": "strong",
    "suppliers": ["Four networks: American Express, MasterCard, Visa, Discover", "Universal card acceptance is long and costly to replicate"],
    "rivalry_level": "medium, growing",
    "rivalry": ["Issuers (banks that issue cards) compete for customers", "New players: Square, ChaseNet"],
    "buyers_level": "medium, growing",
    "buyers": ["Large merchants negotiate terms", "Durbin Amendment cut banks' debit fees", "Chase created ChaseNet"],
    "substitutes_level": "weak",
    "substitutes": ["Wallets run on network rails", "Threat: MCX on ACH, bitcoin"],
    "verdict": ["Supplier power has barely changed", "Unlikely to weaken over the decade (article author)"],
    "dynamics": ["Change will come from buyers and new rails", "MCX on ACH: if successful, networks lose volume"],
    "sources": "PYMNTS article of 17.03.2014; levels — our estimate",
    "decision": ["The article has no company decision", "Visible moves: Discover licensed the PayPal network (2012), Chase created ChaseNet"]
  }
}
```

Limits that fit the rendered slide: title under 90 characters; levels (`*_level`) under 24; facts for suppliers, rivalry and buyers: up to three items under 60; for entrants and substitutes: up to two items under 65; verdict and decision: up to three items under 50; dynamics and sources: up to two items under 55. A list of strings becomes lines, one thought per item. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/porters-five-forces.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's analysis and check it against the common mistakes in card.md:

1. Only direct rivals are examined; buyers, suppliers, entrants and substitutes are missing.
2. A substitute is confused with a competitor (a product meeting the same need in the same way).
3. The industry boundaries are wrong, or one assessment is given for all buyers: the forces are counted for the market in general, without segments.
4. Industry structure is taken for the fate of one company: the company's own position is ignored.
5. The analysis is a snapshot: what will change the forces (law, technology, a player's move) is missing.
6. Levels are given without facts such as the number of players, shares or switching costs.
7. There is no decision: entry, position or weakening of a force.

Items 3 and 6 often cannot be judged from the text alone: ask for the boundaries and the facts instead of reporting a finding. Also check that the verdict follows from the levels. Report findings as a numbered list: what is wrong, why it distorts the profit estimate, the concrete fix. End with a verdict: "supports a decision", "works after changes" or "needs boundaries and facts first".

Example: an analysis of a marketplace lists only three rival marketplaces, gives "high rivalry" and no facts. Findings: item 1 — buyers, sellers as suppliers, entrants and substitutes are missing; item 6 — no shares or switching costs behind "high"; item 7 — no decision. Verdict: "needs boundaries and facts first".
