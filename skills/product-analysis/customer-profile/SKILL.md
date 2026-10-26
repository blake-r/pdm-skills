---
name: customer-profile
description: Describe a typical customer of one segment on one page in four parts (about, context, value, problems) around a named persona, add the data sources and the product implications, and produce a one-slide PPTX, or review an existing profile or persona. Use when a team designs a product or feature and must agree who it is for, enters a new segment, or sees customers that differ too much for one solution.
---

# Customer Profile

The theory, quadrants, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings research data about customers, **review** when the user brings a finished profile or persona.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product and the segment the profile describes;
- the data: surveys, interviews, product analytics, CRM; sample size and date for each;
- if customers differ a lot, how the user splits them into segments.

Do not invent facts or shares. If the user has only the team's assumptions, fill the profile but mark every such line "hypothesis" and say how to check it.

### 2. One segment per profile

If the data mixes groups that differ in context, goals or problems, make one profile per group rather than an average. Say how the groups were split.

### 3. Fill the quadrants

- **About:** who the customer is — age or role, experience, scale of business or income, spending, habits.
- **Context:** how, where and with what the customer uses the product; when the need arises.
- **Value:** what matters to the customer, the goals and how the customer judges success.
- **Problems:** what gets in the way, where the customer loses money, time or nerves.

Write concrete facts with the share and the source in brackets, not adjectives: "sells up to 100 items", not "small business". Put demographics only in About and only if they change a product decision.

### 4. Name the persona and draw the implications

Give the persona a name, one line that sets this segment apart, and the segment. Write the product implications: which of this customer's problems the product solves, what it does not do for them, and what to check next. Do not promise effects.

### 5. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, the persona, the four quadrants, the data and the implications. Write a file only after the user confirms. Ask for the output path (default `customer-profile-<segment>.pptx` in the working directory). Save the data as JSON:

```json
{
  "text": {
    "title": "…",
    "persona": ["Irina, 46–55 years old", "“I sell on three marketplaces”", "Turnover > 1M ₽"],
    "about": ["46–55 years old", "Over 3 years of experience"],
    "context": ["Several marketplaces", "Own warehouse"],
    "value": ["Turnover (25%)", "Margin (22%)"],
    "problems": ["Returns (22%)", "Dishonest buyers (22%)"],
    "sources": ["Survey of 709 sellers, Tochka and Data Insight, 2025"],
    "implications": ["We solve: …", "We do not do: …", "Check: …"]
  }
}
```

Keep up to about five lines of up to about 32 characters per quadrant, up to three short lines for the persona and up to four lines in the implications; list the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/customer-profile.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's profile in any form and check it against the common mistakes in card.md:

1. The profile describes one segment, not an average of different groups: wide ranges such as "36–55 years" or "1–3 marketplaces" are a finding.
2. Every fact has a source and a date; assumptions are marked as such.
3. Quadrants hold concrete facts, not adjectives.
4. Context and problems are filled, not only demographics.
5. The persona line sets this segment apart from others.
6. The profile ends with product implications: what is solved and what is not.

Items 1 and 2 often need the user's knowledge: when the profile itself does not show the problem, ask instead of reporting a finding. Report findings as a numbered list: quadrant or line, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "profile is usable", "usable after fixes" or "not enough data".
