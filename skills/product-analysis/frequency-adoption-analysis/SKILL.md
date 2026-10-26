---
name: frequency-adoption-analysis
description: Place product features on a scatter of adoption (share of active customers who use a feature) against frequency (uses per adopter), sort them into key, special, utility and unneeded zones, decide what to develop, promote, automate or remove, and produce a one-slide PPTX, or review an existing feature audit. Use when a product has too many features and the team must decide what to keep.
---

# Frequency / Adoption Analysis

The theory, zones, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings usage data or a list of features to sort, **review** when the user brings a finished audit or a decision drawn from one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product, the period and the base: which customers count as active;
- the feature list at one level of detail;
- per feature: how many active customers used it at least once in the period, and the average number of uses per such customer;
- which features are rare by nature but critical (tax statements, account closing, disputes).

Do not invent usage figures. If a feature is not tracked, keep it out of the chart and list it as "not measured". If there are only words like "few" or "most", do not build the chart: sort in chat, say the figures are missing and what to measure. Leave out administrative actions (login, password reset, profile edits).

### 2. Check the data

- One base and one period for all features; adoption is a share of the same active base.
- Features at the same level of detail: split "payments" into the actions customers take.
- Mark rare-but-critical features before placing them; they are not judged by frequency.

### 3. Place and read

Compute adoption in percent and frequency per adopter. Draw the borders at the median of each axis or at thresholds the user states, and say which. Name every feature's zone. Features near a border are discussed, not read off the chart.

### 4. Decide

Per zone: key — develop; utility — automate and simplify; for both low-adoption zones (special and unneeded) choose one of four: remove, raise adoption, raise frequency or deliberately improve for current users; a special feature may also be accepted as a niche-segment feature and not grown. Many special features mean the product does more than it should. For every feature to remove, check first that customers can find it, and name what its remaining users lose and what replaces it. Do not promise effects.

### 5. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, how it was measured, the features with their coordinates and zones, the decisions and the checks. Write a file only after the user confirms. Ask for the output path (default `frequency-adoption-<topic>.pptx` in the working directory). Save the data as JSON:

```json
{
  "text": {
    "title": "…",
    "method": ["Base: active in the month", "Borders: medians — 4 times and 30%"],
    "decision": ["Develop: …", "Remove: …"],
    "checks": ["…"]
  },
  "charts": {
    "features": {
      "points": [{"label": "Transfer by phone number", "x": 71, "y": 6.2}],
      "x_axis": {"minimum": 0, "maximum": 100, "major_unit": 25},
      "value_axis": {"minimum": 0, "maximum": 8, "major_unit": 2},
      "lines": {
        "Adoption border": [[30, 0], [30, 8]],
        "Frequency border": [[0, 4], [100, 4]],
        "Special · decide": [[15, 7.7]],
        "Key · develop": [[65, 7.7]],
        "Unneeded · drop": [[15, 0.3]],
        "Utility · automate": [[65, 0.3]]
      }
    }
  }
}
```

`x` is adoption in percent (0–100), `y` is uses per adopter in the period, as in Traynor's original chart. Round both, and the borders, to one decimal. The template's axes run 0–100 on adoption and 0–20 on frequency, with borders at 50 and 10. When the frequency scale or the borders differ, set `value_axis` and pass `lines`: both borders, and the four zone labels at the middle of each zone on the adoption axis, at about 96% and 4% of the frequency axis maximum. Set the frequency `maximum` to four times `major_unit` and at least 1.2 times the largest frequency, so the label above the point stays inside the chart: some viewers, such as Keynote, always split an axis into four steps. If a feature sits under a zone label, move that label sideways within its zone. Keep labels under about 25 characters and at most 15 features; group the rest in chat. The keys in `lines` are the series names of the template's chart (they must match it exactly). Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/frequency-adoption-analysis.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's audit in any form and check it against the common mistakes in card.md:

1. Adoption uses one base and one period for all features.
2. Features are at one level of detail.
3. Frequency counts uses per adopter, not per all customers.
4. The borders are stated and features near them are discussed.
5. Rare-but-critical features are not sent to "unneeded".
6. Low adoption is checked for discoverability before removal.
7. Every removal names what the remaining users lose and what replaces it.

Items 5 and 6 often need the user's knowledge: ask instead of reporting a finding. Report findings as a numbered list: feature, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
