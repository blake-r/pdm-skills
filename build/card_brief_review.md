# Brief for the reviewer: one tool card

Run commands from the repo root; all paths below are relative to it. You are an independent reviewer of ONE card. Do not edit files (except temporary ones in a scratch directory outside the repo, for example `/tmp/<slug>-review`). Do not commit anything.

1. Read `build/quality_gate.md` in full. Score the card on K1-K8 on a 0-2 scale against the anchors of the gate.
2. K2: open the links from "Source" and "Example" (WebFetch/WebSearch, browser User-Agent) and check every number, quote, date, name and element title. Mark a check you could not perform as "not verified", never as "correct".
3. K1/K3: `uv run -q python3 build/quality_gate.py skills/<category>/<slug>/card.md` (per-section word limits, see build/quality_gate.md K3; false positives on the words "business"/"strategy"/"team" in titles and links - note them, do not count them as errors). The "See also" section must name only existing tools, each with a phrase (Enhanced by, Alternative to, Preceded by, Followed by, Improved by, Used to improve) and a way to use them together.
4. K7: read SKILL.md and run checks a-d. Trial run in do mode: take the data of the case from "Example", fill the JSON per SKILL.md, run the fill command from the repo root and check the result (`officecli validate`). Review mode: mentally plant one typical mistake into the case artifact and check that the checklist would catch it (the checklist must map one-to-one to "Common mistakes").
5. K8: check the template (exactly one file); for pptx render it with `bash build/render_pptx.sh <ABS> <slug>` (if Keynote says "Application isn't running", run `open -a Keynote`, wait, retry) and look at the PNG; for xlsx check formulas/validation logically. The template must match the scheme in card.md.
6. K6: the catalog, per the rules of `build/quality_gate.md` and `build/classification.md`.

Answer briefly, in English: a K1-K8 table (score + one line of reason), then a numbered list of defects (what, where, how to fix), then "not verified". Verdict: PASS (all 2) or FAIL (which criteria). Do not praise; look for defects.
