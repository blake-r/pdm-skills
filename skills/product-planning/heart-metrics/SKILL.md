---
name: heart-metrics
description: Choose user-experience metrics for a product, feature or redesign with Google's HEART framework (Happiness, Engagement, Adoption, Retention, Task Success) and the goals → signals → metrics process, pick the categories that matter, and produce a one-slide PPTX, or review an existing HEART table or metrics set. Use when a team needs metrics for a feature or redesign, watches only totals like visits or revenue, or has too many metrics to act on.
---

# HEART Metrics

The theory, categories, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a product, feature or redesign that needs metrics, **review** when the user brings a HEART table, a metrics dashboard or a decision drawn from one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product, feature or redesign and what it should change for users;
- the data available: logs and product analytics, surveys, support contacts;
- current values of the metrics already tracked, with the period;
- who will look at the metrics and which decisions depend on them.

### 2. Set goals

Write one to three goals from the user's point of view ("new customers find the right size without help"). If people disagree on a goal, point it out now. Do not invent goals the user has not confirmed.

### 3. Pick categories

Keep only the categories that match the goals (often two or three) and say in one phrase why each of the others is left out. Happiness needs a recurring survey of the same form; Task Success needs a known task or path. If the data for a category does not exist, say so instead of leaving a metric nobody can compute.

### 4. Signals and metrics

For each kept category write the signal (an action or an attitude that shows success or failure) and the metric: formula, period and the current value if known. Report Engagement as a per-user average; compare other counts, such as new users for Adoption, with a baseline or turn them into shares. Do not invent numbers: mark missing baselines "no data" and say how to get them.

### 5. Decide

Say what change counts as success, when to look, and what the team will do if the metric moves or does not. After a redesign, Happiness often dips at first from change aversion: judge by whether it recovers, not by the first weeks. Use Adoption and Retention to tell growth from new users apart from returning ones. Say that metrics show what changed, not why: if a metric does not move, decide together with qualitative data.

### 6. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, five rows with goal, signal and metric, the focus and the decision. Rows for categories left out get a dash in the goal and nothing else. Write a file only after the user confirms. Ask for the output path (default `heart-<product>.pptx` in the working directory). Save the data as JSON:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Open Targets Platform: HEART metrics",
    "h_goal": "Do users like the platform?",
    "h_signal": "User feedback",
    "h_metric": ["Qualitative feedback now", "NPS survey planned"],
    "e_goal": "Do people use the site?",
    "e_signal": "Searches, downloads, evidence clicks",
    "e_metric": ["Visit: 6 min 49 s", "Bounce rate: 25.6%", "11.3 actions per visit"],
    "a_goal": "Do people visit and view pages?",
    "a_signal": "Visits and unique visitors",
    "a_metric": ["816 visits a week", "530 unique visitors a week"],
    "r_goal": "Do people come back?",
    "r_signal": "Returning visits",
    "r_metric": ["460 returning visits a week", "56.67% of all visits"],
    "t_goal": "—",
    "focus": ["Adoption, engagement, retention", "Task success out: open-ended use", "Happiness: feedback, NPS planned"],
    "decision": ["Metrics: substantial use", "Matches positive user feedback", "Averages, Apr 2016 - Mar 2017"]
  }
}
```

The example is the Open Targets case from card.md (averages April 2016 - March 2017). The source replaced goals and signals with a question for external readers, so the goal cells hold that question and the signals are named from the metric names; say so in chat. If a goal or signal is not published, write "not published" rather than inventing one.

Keys are `h`, `e`, `a`, `r`, `t` with `_goal`, `_signal`, `_metric`. Keep each cell to three lines of under 35 characters, the focus and the decision to four items of under 40 characters each, and the title to one line of under 70 characters; list the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Unused keys may be left out: the script leaves them empty and names them in a warning. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/heart-metrics.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's table or metrics in any form and check them against the common mistakes in card.md:

1. Every metric traces back to a stated goal through a signal.
2. Only the categories that matter are kept, and the rest are dropped for a reason.
3. Engagement is a per-user average; other raw counts have a baseline or are turned into shares.
4. Each metric has a formula, a period and a baseline.
5. Happiness comes from a recurring survey of the same form; Task Success has a known task.
6. The decision says what counts as success and when to look.

Item 1 often needs the user's knowledge of the goals: ask instead of reporting a finding. Report findings as a numbered list: category, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
