---
name: gartners-hype-cycle
description: Place technologies on Gartner's Hype Cycle (innovation trigger, peak of inflated expectations, trough of disillusionment, slope of enlightenment, plateau of productivity) with the years to plateau, turn the position into an action - watch, pilot or adopt - and produce a one-slide PPTX; or review an existing hype cycle or a decision to invest in a new technology. Use when deciding whether and when to invest in an emerging technology, when management expectations of a fashionable technology need calibrating, or when comparing several technologies for the roadmap.
---

# Gartner's Hype Cycle

The theory, phases, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings one or more technologies to assess, **review** when the user brings a filled curve or a decision about a technology.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the technologies and the area (industry, function);
- the problem each technology should solve for the user, and the date of the decision;
- the latest Gartner Hype Cycle for this area the user can access, if any, with its year;
- the user's appetite for risk and what is already being piloted.

Do not invent Gartner positions or years to plateau. If the user has no Gartner curve, you may place technologies yourself by the phase signs in card.md, but label every such position "our estimate" and name the evidence: products on the market, pilots, reported failures.

### 2. Place

For each technology, name the phase, the years to plateau and the source of the position (Gartner report and year, or "our estimate").

### 3. Check against the task

For each technology, say which of the user's problems it solves and whether ready products exist for it. The phase describes the market, not the user's project.

### 4. Choose the action

Recommend watch, pilot or adopt for each technology, with the reason and the date to revisit. The earlier the phase, the smaller the recommended commitment.

### 5. Show, then write

Show in chat first, phase by phase as they will appear on the slide, then the actions. Write a file only after the user confirms. Ask for the output path (default `hype-cycle-<area>.pptx` in the working directory). Save the data as JSON (the example is the Gartner August 2017 release from card.md, the moment before ASX's decision):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "New technologies by Gartner · August 2017",
    "phase1": ["Quantum computing — climbing the trigger (5–10 yrs)"],
    "phase2": ["Blockchain — past the peak (5–10 yrs)"],
    "phase3": [],
    "phase4": [],
    "phase5": []
  }
}
```

Keep the title under 45 characters. Keep each phase to five items of under 40 characters: the technology, then its position within the phase or the years to plateau in brackets. Leave a phase as an empty list when nothing is placed there. List actions and anything that does not fit in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/gartners-hype-cycle.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's curve or decision in any form and check it against the common mistakes in card.md:

1. The position is read as the market's expectations, not as the forecast for the user's project.
2. Adopting at the peak is backed by the user's own problem and ready products, not by fear of missing out.
3. A technology is not dropped in the trough if it already solves the user's problem.
4. The years to plateau are not used as the project's timeline.
5. The curve is the latest available, and every position names its source and year.

Report findings as a numbered list: technology, what is wrong, why it matters for the decision, the concrete fix. End with a verdict: "decision is sound", "sound after fixes" or "not enough data".
