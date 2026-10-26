# Acceptance tests for pdm-brief

The model's output cannot be compared byte by byte, so the checks are split.

- **Deterministic, no model:** `uv run scripts/smoke_test.py` (fill, merge, layout check, catalog checks). Run it after every change to scripts, templates or the catalog.
- **Scenario checks:** each scenario in [scenarios.md](scenarios.md) is run in a clean folder with `pdm-brief`, and the result is checked against the run checklist and the scenario's rubric. Compare structure only: the set of tools, the slides present, `N/A` marks, source tiers and dates. Do not compare wording.

## Run checklist (every run)

1. The deck has a title slide, the tool slides, a sources slide and an assumptions slide; a conclusions slide if the artifact is analytical.
2. `uv run scripts/check_pptx.py <deck>.pptx` reports no problems, and no `{{` is left in the deck.
3. Every missing value is `N/A`; nothing is made up.
4. Every fact in `brief.md` has a source tier (official, corporate, other) and a date; a regulatory fact is "confirmed" only with an official source.
5. Every question the user did not settle appears on the assumptions slide with the assumption used and who confirms it.
6. Every tool picked has the run's data mode in its row of the Selection table (`product_notes.md`); every tool skipped for lack of data is named with the reason "not picked: needs data".
7. All questions to the user went through AskUserQuestion, at most 4 per call, and no data was asked twice.
8. Time from the first message to the first finished artifact is written down.

## Rubric scores per scenario

For each rubric line in the scenario: 2 = met, 1 = partly, 0 = not met. A scenario passes with no 0 and a total of at least 80%.

Run the scenarios again after a change to `skills/pdm-brief/SKILL.md`, the Selection table or the chains, and record the scores and the time in the pull request.

## Results of the first run (26 October 2026)

Conditions: each scenario was run by a Sonnet agent that played both `pdm-brief` (fallback mode, no AskUserQuestion, no independent grilling) and the PM from the sheets in [answers/](answers/). The mechanical part is `uv run tests/check_run.py <run folder>`. This does not replace a run with a real PM in a real session: the agent never saw the questions as a user would. Regulatory facts in scenarios 4 and 5 were rechecked by the maintainer against the cited pages.

| # | Result | Reason |
|---|---|---|
| 1 | passed | `validation-board` picked; four tools named "not picked: needs data"; no number invented; the data-mode question was asked once. |
| 2 | partially passed | Segments and the sample-size warning are correct, files are named. The two picked tools are XLSX, so the full deck has no tool slides; the rule "XLSX next to the deck, result on the conclusions slide" was added after this run. Only synthetic fixtures were used. |
| 3 | passed | Each fact has a tier and a date; the act text on the regulator's site could not be read, so the status stays unconfirmed. |
| 4 | passed after one fix | First run: the layout check failed on a label of the PRD template; the template was fixed and the run repeated (second run clean). The regulator's requirement stays unconfirmed; the ticket's claim contradicts the press. Quick depth: tool results sit in `brief.md`, not on slides. |
| 5 | passed | The second run read the context file and did not ask the card-count question again. |
| 6 | partially passed | The tool sets are identical (PESTEL, Porter's Five Forces) and the briefs differ (189 vs 501 words). The web research was done once and shared, so the two runs are not independent. |

Defects found and fixed by these runs: PRD and storytelling template labels overflowed (now checked by the smoke test for every template); the skill said nothing about XLSX tools in a deck, a run without local data, the shape of the JSON for title/sources/assumptions slides, the context file name and the slide count; segment tools were in no chain; no check that `plugin.json` lists a new skill.

Not covered yet: a run with a real PM; scenario 2 with real (not synthetic) files; independent grilling in a real session.
