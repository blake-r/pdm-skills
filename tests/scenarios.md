# Scenarios

Each scenario is run in an empty folder. The task text is what the tester types; the tester answers the questions as described. "Expected tools" are checked against the Selection table in `product_notes.md`.

## 1. No data

- **Task:** "We think of a weekly food box subscription for families. Nothing is measured yet. What should we decide first?"
- **Data mode:** none. The tester answers "Continue without the data" to every data question.
- **Expected tools:** only tools with `none` in their row, for example `impact-mapping`, `stakeholders-matrix`.
- **Rubric:** tools that need numbers (`metric-pyramid`, `unit-economics`, `cost-benefit-analysis`) are not picked and appear as "not picked: needs data"; the plugin asked once whether to add a data mode; no number appears that the tester did not give; the assumptions slide lists the unmeasured quantities.

## 2. Local files

- **Task:** "From the interview notes and the order export in this folder, show which customer groups to focus on."
- **Data mode:** local files. The folder holds a markdown file of interview notes and a small CSV of orders (test fixtures, marked as synthetic, not real data).
- **Expected tools:** tools with `local` in their row that fit the question, for example a segmentation tool.
- **Rubric:** the folder was scanned and files listed by type; the user was asked once how to use local data; every figure in the deck comes from a file and names the file; small samples are flagged.

## 3. Web

- **Task:** "We consider entering the consumer lending market in a new country. What does the environment look like?"
- **Data mode:** web only.
- **Expected tools:** tools with `web` in their row, for example `pestel-analysis`, `porters-five-forces`.
- **Rubric:** each fact has a tier and a date; regulatory facts rest on an official source or stay unconfirmed; an edition date later than today is recorded as an anomaly; one country per analysis.

## 4. Numbers entered by hand (reference case: removing a per-client card limit)

- **Task:** "Remove the limit on the number of cards a client can hold, in all issue flows. The regulator reportedly requires it. Prepare the decision for management and the hand-off to development." Security policy forbids sharing real metrics.
- **Data mode:** none and entered by hand. The tester enters only rounded aggregates (indicator, value, period, unit) or declines.
- **Expected tools:** `impact-mapping`; further tools only if they change a decision. With the quick depth the tool results are checked in `brief.md` (a quick deck has no tool slides).
- **Rubric:** the plugin says before the input that raw rows, personal data and source code are not needed; entered values are marked "internal data, not verified"; the regulator's requirement stays unconfirmed until an official act is found, with the reason; the metric of the goal is a measurable target (for example "cases of issue refused because of the limit: 0 after release"), not N/A; the assumptions slide lists what replaces the count limit and who confirms it.

## 5. A missing fact, "Continue without the data"

- **Task:** any task from scenarios 1-4 with one fact the tools need and nobody gave.
- **Data mode:** as in the base scenario. At the data question the tester picks "Continue without the data".
- **Rubric:** the field is `N/A`; the fact is in "not confirmed" on the sources slide; the assumption used instead is on the assumptions slide; the question is not asked again in the same run or in the next run in the same folder (it is read from the context file).

## 6. Quick conclusion and full analysis

- **Task:** the same task as scenario 3, run twice in two folders. First answer "quick conclusion", then "full analysis".
- **Rubric:** the set of picked tools is identical in both runs; the quick run has a shorter brief and puts the decision, the conditions under which it holds and the assumptions in front; the full run has every tool slide and a full brief.
