---
name: diary-study
description: Plan, structure or review a diary study (participants keep a diary of their actions, thoughts and emotions over days or weeks to study consumer behaviour over time and in context, e.g. shopping, personal finance, app use) and produce a one-slide diary log. Use when the team needs behaviour over time that interviews cannot recall, or when someone brings diary entries or a study plan to check.
---

# Diary Study

The theory, limits and a worked case (Lewis and Perry, personal finance diary, CHI 2019) are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user is planning a diary study or summarising its entries, **review** when the user brings a plan, entries or a log and wants them checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the research question: which behaviour, thought or emotion, and why it must be seen over time;
- who the participants are and how many; the period;
- the entry type (event, interval or signal) and the medium (text, table, messenger, photo, audio);
- what has been collected already: entries, interview notes;
- what the team will decide from it.

If the user wants shares or numbers ("what percent do this"), say that the card does not give quantities and offer to describe the behaviour only. Never invent entries, quotes or numbers: what the user did not give is marked "not in the source".

### 2. Plan the study

Give a short plan following card.md: question, period, entry type, medium, entry fields (time, action, place, thought, emotion), participants with a reserve for dropout, a pilot, how entries are read during the study, and the closing interview over the diary. Keep example entries out of the instruction, or warn that participants are biased towards entries of that kind.

### 3. Fill the log

For each entry write three things: what the person did (day, time), their own words about thoughts and feelings (verbatim or "not in the source") and the researcher's conclusion, marked as a conclusion. Do not mix them.

### 4. Interview, gaps, decision

State what the closing interview clarified, what weakens the data (dropout, gaps, a person's reluctance to report, the diary itself changing attention) and one decision with a check by behaviour. Do not state shares.

### 5. Show, then write

Show the result in chat first as a table by template blocks: title, question, participants and period, entry type, three log rows, interview, gaps, decision. Write a file only after the user confirms. Ask for the output path (default `diary-study-<topic>.pptx` in the working directory). Save the data as JSON. The example is the Lewis and Perry case from card.md; the decision column holds the authors' design proposals, not a company decision, and what the source does not give says "not in the source":

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Lewis and Perry: personal finance diary, England, 2018",
    "question": "How people spend, save and share money in a digital environment and what systems they need",
    "sample": "12 people from England, 10 days; the source does not say anything about dropout",
    "entry": "At a convenient time, if possible right after the event; table, document, WhatsApp, email",
    "a1": "May turned on bank app notifications about spending (interview)",
    "a2": "Liam and Charlotte enter payments manually into a shared household spreadsheet",
    "a3": "Charlotte wrote about contactless payment when entering the station",
    "t1": "Statement — \"a huge amount… makes me confused\"; switched to a daily summary",
    "t2": "not in the source (reason: bank data is not imported, according to the authors' account)",
    "t3": "\"contactless so payment was easy\"",
    "c1": "People are less aware of their spending, money has lost its tangibility (authors' conclusion)",
    "c2": "Shared spending requires manual work: bank data cannot be imported (authors' account)",
    "c3": "Participants found contactless payment convenient and fast (per the authors' text)",
    "interview": "Within 7 days, on average 90 minutes, using a printout of the diary; participants created 83 categories themselves",
    "gaps": "Income understated (probably); 12 people, shares by sample (164 of 367 — contactless); no company decision",
    "decision": [
      "A panel with a structured history of transactions, not a stream of notifications",
      "A shared payment system with adjustable access",
      "These are the authors' proposals; the article has no implementation or check"
    ]
  }
}
```

Limits that fit the rendered slide: title under 70 characters; question, sample and entry under 110; each of a1..a3 and c1..c3 under 90; t1..t3 under 80; interview, gaps under 120; decision: up to three items under 110. A list of strings becomes lines. Use "not in the source" for an empty block, not null or an empty string. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/diary-study.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's plan, entries or log and check them against the common mistakes in card.md:

1. Numbers or shares are expected from a handful of participants.
2. The diary is too long or the minimum number of entries is rigid, so people drop out.
3. Example entries in the instruction bias participants towards entries of that kind.
4. Entries are read only at the end, so nothing could be clarified while the event was fresh.
5. There is no closing interview over the diary.
6. A participant's words are taken as fact or as a pattern.
7. The effect of the diary itself on attention and behaviour is ignored.

Items 2, 4 and 7 usually cannot be judged from the entries alone: ask the period, the required number of entries, when the researcher read the entries and whether participants said that keeping the diary changed their habits, instead of reporting a finding. Also check that the question, participants, entry type and medium are named and that facts, words and conclusions are written apart. Report findings as a numbered list: what is wrong, why it distorts the picture, the concrete change. End with a verdict: "diary supports a decision", "works after changes" or "needs a closing interview first".

Example: a plan with 12 people, "30 entries a day required", a sample entry in the instruction, no interview, and a conclusion "69% pay by card". Findings: item 1 — no shares from 12 people; item 2 — a rigid minimum is unrealistic; item 3 — remove or warn about the example; item 5 — add the interview. Verdict: "needs a closing interview first".
