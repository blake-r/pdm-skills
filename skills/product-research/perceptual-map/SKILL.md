---
name: perceptual-map
description: Build a perceptual map - brands or products placed on two dimensions the way buyers see them, with the circle size as market share - from buyer ratings or pairwise similarity judgments, read who is close, where the empty positions are and where the leaders stand, decide how to move the product, and produce a one-slide PPTX; or review an existing perceptual map. Use when the team must decide how the product should differ from alternatives in the buyer's eyes (before a launch, a price or message change, or when sales fall with no visible cause).
---

# Perceptual Map

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a market or survey data, **review** when the user brings a finished map.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product, the market, the buyer segment, and the decision the map feeds;
- the brands buyers actually choose between (four to eight);
- the data: ratings of each brand on each attribute, or pairwise similarity judgments, with the number of respondents and the date; market shares if known;
- if there is no data yet: what the team already knows about how buyers compare brands.

Do not invent ratings, coordinates or shares. A map drawn from the team's opinion is a hypothesis; label it so.

### 2. Survey (if no data yet)

Propose five to ten attributes taken from buyer interviews, a rating scale (for example 1-10), and the question per brand and attribute. Ask for dozens of answers per brand, better over a hundred. Stop here and let the user run it.

### 3. Compute the map

From attribute ratings: average each brand on each attribute and take the two dimensions that matter most for the decision, or reduce the attributes to two factors and name them by their strongest attributes. From similarity judgments: run multidimensional scaling and treat the axis names as guesses to check. Report the respondent count and, for scaling, the fit (stress).

### 4. Decide, show, then write

Read the map: who is closest to the product, which positions are empty and whether buyers want them, where the leaders stand. Propose a move and its lever: price, features or message. Show in chat first: the coordinates, the axis names, the reading, the decision, how it will be rechecked. Write a file only after the user confirms. Ask for the output path (default `perceptual-map-<product>.pptx` in the working directory). Save the data as JSON (the example is the Indonesian marketplace case from card.md; the decision is the authors' advice, not a company's):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Indonesian marketplaces: 385 buyers, January–February 2016",
    "x_axis": "Dimension 1: not named; on the right — leaders",
    "y_axis": "Dimension 2: not named",
    "scope": ["Online survey, 385 questionnaires", "Perceptual map, MDS calculation", "Circle size not set: no shares"],
    "gap": ["Only Tokopedia and Bukalapak on the right", "Left side of the field — three laggards"],
    "decision": ["Authors: improve sites to match buyer perception", "No company decisions based on the map"],
    "result": ["Rakuten left the market on 1 March 2016", "No link to the map: announced during the survey"]
  },
  "charts": {"map": {
    "points": [
      {"label": "Tokopedia", "x": 1.40, "y": -0.51},
      {"label": "Bukalapak", "x": 1.62, "y": 0.28},
      {"label": "Elevenia", "x": -0.34, "y": 0.82},
      {"label": "Qoo10", "x": -1.65, "y": 0.13},
      {"label": "Rakuten", "x": -1.03, "y": -0.72}
    ],
    "lines": {"Midpoint X": [[0, -1], [0, 1]], "Midpoint Y": [[-2, 0], [2, 0]]},
    "x_axis": {"minimum": -2, "maximum": 2, "major_unit": 1, "number_format": "0"},
    "value_axis": {"minimum": -1, "maximum": 1, "major_unit": 0.5, "number_format": "0.0"}
  }}
}
```

`points` holds one entry per brand, up to eight; add `"size"` (for example market share) to scale the circle area. `lines` moves the two guide lines to the middle of your scale; `x_axis` and `value_axis` set the ranges (the template's default is 1 to 10). The axis texts say what each end of the axis means. `scope`, `gap`, `decision` and `result` take up to four items of under 45 characters each; each item becomes its own paragraph. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/perceptual-map.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's map in any form and check it against the common mistakes in card.md:

1. The dimensions come from buyers (interviews, ratings), not from the team.
2. Positions rest on buyer data with a stated number of respondents and a date.
3. Axis names found by computation are marked as guesses and checked.
4. An empty position is backed by evidence that buyers want it.
5. The map is recent; it is rebuilt after major campaigns or new entrants.

Report findings as a numbered list: what is wrong, why it misleads the decision, the concrete fix. End with a verdict: "map supports the decision", "supports it after fixes" or "not enough data".
