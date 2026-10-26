---
name: gantt-chart
description: Build or review a project plan as a Gantt chart with tasks, owners, dependencies, milestones and the critical path, and produce a filled Gantt slide with a native chart. Use when the user needs a dated plan for a project with a deadline or wants to check whether a plan holds.
---

# Gantt Chart

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a project to plan, **review** when the user brings a plan or chart.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the goal, the start date and any fixed external dates (milestones);
- the list of work with an owner for each item;
- duration estimates in days;
- dependencies: what cannot start before what finishes;
- who is shared between tasks or teams.

If the scope is still unknown (discovery work), say that dates will be false precision. Plan only the known part and keep the rest as one coarse task with an explicit buffer. For day-to-day flow of work, suggest the `kanban-board` skill; to agree scope, goals and risks first, `project-canvas`.

### 2. Build the plan

1. Split work into tasks of a few days to two or three weeks, each with a clear result; aggregate anything smaller.
2. Schedule each task right after its predecessors finish (finish-to-start), counting calendar days from the start date.
3. Order rows by start date.
4. Mark milestones as zero-length events.
5. Find the critical path: the longest chain of dependent tasks. Its length is the project duration. Name the tasks on it and the slack of the others.
6. Check load: if one owner has overlapping bars, move a task or reassign it and recompute.
7. Put the buffer at the end of the critical path as one visible item, not hidden in every estimate.

Do not invent durations or dependencies; ask. If an estimate is a guess, say so in the risks.

### 3. Show, then write

Show the plan in chat first:

| Task · owner | Start (day) | Duration (days) | Start date | End date | Depends on | Critical |
|---|---|---|---|---|---|---|

followed by the milestones, the critical path, the finish date and the main schedule risks.

Write a file only after the user confirms. Ask for the output path (default `gantt-<project>.pptx` in the working directory). Save the data as JSON:

```json
{
  "text": {
    "title": "…",
    "start_date": "…",
    "milestones": ["dd.mm — event"],
    "dependencies": ["Task 3 waits for 1", "Critical path: 1 → 3 → 4"],
    "risks": ["…"]
  },
  "charts": {
    "gantt": {
      "categories": ["1. Task · owner", "2. Task · owner (after 1)", "◆ Milestone: launch"],
      "series": [
        {"name": "Start, day offset from start", "values": [0, 10, 24]},
        {"name": "Duration, days", "values": [10, 14, 0]},
        {"name": "Milestone", "values": [0, 0, 0.5]}
      ],
      "value_axis": {"minimum": 0, "maximum": 28, "major_unit": 7}
    }
  }
}
```

Chart rules:

- Series order is fixed. "Start" holds day offsets from the start date and is invisible; "Duration" holds durations; "Milestone" draws a dark mark on milestone rows.
- A milestone row has duration 0 and a "Milestone" value of about 1% of the horizon (at least 0.5), starting at the milestone's day. Prefix its label with "◆".
- Number task rows and show dependencies in the label: "4. Task · owner (after 2, 3)". The chart cannot draw arrows.
- Always pass `value_axis`. `maximum` is the larger of the finish day and the last milestone's day plus its "Milestone" value, rounded up to a multiple of `major_unit`; otherwise a milestone on the finish day is clipped. `major_unit` is 7 for horizons up to about ten weeks, 30 up to a year, 91 beyond. PowerPoint honours the unit; a 7-day unit on a year-long plan makes unreadable labels.
- The template has no "today" line or progress fill. When reviewing a plan in progress, put the status date and percent done in the title or in the risks.
- The template fits about 12 rows legibly; aggregate beyond that.

Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/gantt-chart.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's plan in any form and check it against the common mistakes in card.md:

1. Tasks are sized for decisions: neither one giant bar nor hundreds of rows.
2. Dependencies are explicit; nothing runs in parallel that in fact waits.
3. No owner has overlapping bars beyond their capacity.
4. The critical path is identified and the finish date follows from it.
5. Uncertain work is coarse and carries an explicit buffer; precision matches knowledge.
6. The buffer is visible and sits at the end of the critical path.
7. External dates are marked as milestones.
8. The plan shows progress and a "today" marker, or says when it was last updated.

Report findings as a numbered list: task or row, what is wrong, how it moves the finish date, the concrete fix. Recompute the critical path and the finish date after fixes. End with a verdict: "plan holds", "finish date moves to …" or "plan cannot be dated yet".
