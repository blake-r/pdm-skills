---
name: project-canvas
description: Define a project on one page with Jim Kalbach's Project Canvas (motivation, participants, goals with success metrics, users and their benefits, activities, deliverables, risks with mitigations, milestones, constraints, scope in and out, project end) and produce a one-slide PPTX, or review an existing project canvas or project brief. Use at a project kick-off or client briefing, when the team lacks a shared view of goals and boundaries, or when scope keeps growing.
---

# Project Canvas

The theory, blocks, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a project to define, **review** when the user brings a filled canvas or a project brief.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- what the project is and what prompted it;
- who sponsors it, who does the work, who else is affected;
- the users it serves and what they should gain;
- known dates, legal or technical constraints, and what is definitely out of scope.

Do not invent names, dates or metrics. Mark gaps as "to clarify" and name who can answer.

### 2. Motivation and users

Write the motivation in one or two sentences: the trigger and the intent. List the user groups and, for each, the concrete benefit when the project is done.

### 3. Goals

Write two to four goals, each with a success metric and, if known, a target and date. If a goal has no metric, say so and propose one.

### 4. Participants, activities, deliverables

Split participants into core team, stakeholders and other parties, with names where the user gives them. List key activities and the deliverables others will see; leave out internal working files.

### 5. Risks, milestones, constraints, scope

For each risk give a mitigation. List milestones as dates or events, not a task plan. Constraints are exceptional external conditions, not the usual time and money. In scope, write both what is in and what is out.

### 6. Project end

Name the date or the decision that closes the project, and who takes it.

### 7. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, motivation, participants, goals, users, benefits, activities, deliverables, risks, milestones, constraints, scope and project end. Write a file only after the user confirms. Ask for the output path (default `project-canvas-<project>.pptx` in the working directory). Save the data as JSON (the example is the Open Banking case from card.md):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Open Banking: access to accounts through standards",
    "motivation": "Make banks compete harder for customers (CMA report, 2016)",
    "participants": ["Team: 9 largest banks", "Implementer: OBIE and trustee", "Oversight: CMA, FCA, HM Treasury"],
    "goals": ["Open Banking by early 2018", "Metric: not set, to clarify"],
    "users": ["Retail customers", "Small business"],
    "benefits": ["Share data safely", "Compare and switch"],
    "activities": ["Developing standards", "Implementation in banks"],
    "deliverables": ["Open API standards", "Security arrangements"],
    "risks": ["Banks fall behind: directions"],
    "milestones": ["Early 2018: first interfaces", "May 2020: revised roadmap"],
    "constraints": ["CMA order of 2017", "Security and privacy"],
    "scope": ["In: Roadmap for the 9 banks", "Out: expansion beyond the Order"],
    "project_end": "CMA decision: roadmap completed"
  }
}
```

Keep the title under 50 characters, the motivation and the project end to one line of under 90 characters, participants, goals, activities and deliverables to five items of under 35 characters, users and benefits to three items of under 25, risks, milestones, constraints and scope to five items of under 40; list the rest in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/project-canvas.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's canvas or brief in any form and check it against the common mistakes in card.md:

1. The motivation names the trigger, and the users and their benefits are concrete.
2. Every goal has a success metric.
3. Scope says what is out, not only what is in.
4. Every risk has a mitigation.
5. Milestones are dates or events, and the project end is named.
6. Participants include the people who decide, not only those who do the work.
7. The canvas reflects the current dates and scope.

Item 7 usually cannot be judged from the canvas alone: ask the user instead of reporting a finding. Report findings as a numbered list: block, what is wrong, why it matters for the project, the concrete fix. End with a verdict: "canvas is ready", "canvas is ready after fixes" or "not enough data".
