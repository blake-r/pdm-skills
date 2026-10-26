---
name: team-canvas
description: Prepare, run or write up a Team Canvas session — nine blocks a team fills in together (people and roles, common and personal goals, purpose, values, strengths, weaknesses, needs and expectations, rules and activities) — and produce a filled canvas slide, or review an existing canvas. Use when a team starts, gets a new member, loses alignment on goals or builds up tension.
---

# Team Canvas

The theory, the order of blocks, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants to prepare a session or write up its results, **review** when the user brings a filled canvas.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the team: size, roles, how long it has worked together, who is new;
- the occasion: kick-off, a new member, blurred goals, tension;
- the format: in person or remote, how much time there is, who facilitates;
- for a write-up: the stickers or notes from each block, in the team's own words.

If the team has more than ten people, plan subgroups and a joint summary. If the occasion is an escalated conflict, say that the canvas needs basic willingness to talk and suggest a separate mediated conversation first. Never fill the team's answers yourself: the canvas holds what the team said, not your guesses.

### 2. Pick the version

Full version: 90–120 minutes, nine blocks, for alignment, tension or a long project. Basic version: 30–45 minutes, five blocks (goals, roles and skills, purpose, values, rules), for a short project or a quick kick-off. Both are for 2–8 people.

### 3. Prepare the session

Give the facilitator a plan: materials (board or A0–A1 sheet, stickers of different colours for each person, a timer), the conversation rules, then the blocks in the canvas order with the minutes and the authors' questions from the table in card.md, and five minutes of wrap-up. Mark which blocks the whole team must agree on (people and roles, goals, purpose, values, rules) and which each person may fill alone. Add a parking list for long disputes.

### 4. Write up the results

Sort the team's notes into the nine blocks. Keep the team's wording; merge only exact duplicates. For each value, ask what it means in behaviour and record the answer. Check that the rules answer the weaknesses and needs named above; list any weakness or need without a rule as an open question. Record the parked topics and the date of the next session.

### 5. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, the nine blocks, then the open questions, the parked topics and the next date. Write a file only after the user confirms. Ask for the output path (default `team-canvas-<team>.pptx` in the working directory). Save the data as JSON. The example is the Retail Rocket case from card.md; the company did not publish the canvas itself, so most blocks say so instead of guessing, and the rules block holds only the two decisions the article reports. The conversation rules of the session itself are not canvas content:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Retail Rocket: developers and analysts, full version",
    "people": ["Developers and analysts", "Some in Moscow, some remote", "There are newcomers: under six months", "Names and roles not published"],
    "common_goals": "Not published",
    "personal_goals": ["Not published", "Everyone develops at a different pace", "→ into employee development plans"],
    "values": ["The hardest to agree on", "«Best product» — by what measures?", "Final wording agreed, not published"],
    "purpose": "Agreed by the whole team; text not published",
    "needs": ["Different perceptions of the office and environment", "→ into employee development plans"],
    "rules": ["Questions from the session — close them with rules", "Repeat the session every six months"],
    "strengths": "Not published",
    "weaknesses": "Not published"
  }
}
```

Keep the title under 60 characters and the purpose under 60. People: up to six items under 45 characters; common goals, personal goals, values and needs: up to five items under 35; rules: up to eight items under 50; strengths and weaknesses: up to six items under 60. Put personal goals as "goal — name" when the team shares names. List the rest, the open questions and the parked topics in chat. Keep one thought in one list item: each item becomes its own paragraph on the slide. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/team-canvas.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's canvas in any form and check it against the common mistakes in card.md:

1. Purpose and values were set before the rules, and the rules follow from them.
2. Every value says what it means in behaviour.
3. The canvas has a date for the next session and is kept where the whole team sees it.
4. The group was small enough for everyone to be heard, or worked in subgroups.
5. Every important rule says what happens when it is broken.
6. Weaknesses describe each person's own areas, not complaints about others.

Items 3 and 4 usually cannot be judged from the canvas alone: ask the user instead of reporting a finding. Also check that the rules cover the weaknesses and needs listed on the canvas. Report findings as a numbered list: block, what is wrong, why it matters for the team, the concrete fix. End with a verdict: "canvas is ready", "ready after fixes" or "needs another session".

Example: values "Openness, trust" with no behaviour, and rules "Call on Mondays, code review within the day" while weaknesses list "we are afraid to report problems". Findings: item 2 — the values do not say what openness means in practice, fix with "we tell about bad news the same day"; the rules do not answer the stated weakness, add a rule on how problems are raised; item 5 — no consequence for a broken rule. Verdict: "ready after fixes".
