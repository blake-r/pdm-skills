---
name: customer-survey
description: Plan a customer survey (questionnaire with open and closed questions) and produce a one-slide survey plan with results, or review an existing survey or its readout. Use when a hypothesis about customers needs shares of answers rather than stories, when a questionnaire is being written, when respondents must be screened, or when survey results are turned into a decision.
---

# Customer Survey

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user is designing a survey or reading its results, **review** when the user shows a questionnaire or a readout and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the hypothesis about customers and the decision that depends on the answer;
- who exactly should answer and how to tell them apart from others (a screening question);
- how many people can be invited and through which channel;
- whether answers already exist (then ask for counts per answer and per group);
- what is known from other studies and what must be measured.

If the user needs to understand reasons and has no hypothesis yet, say that a survey measures shares and cannot ask "why" at scale, and ask what they want to decide. Never invent numbers: write "not in the source" for what the user did not give.

### 2. Hypothesis, decision and audience

Write the hypothesis and the decision it feeds. Define the audience and one screening question about recent experience, not intentions.

### 3. Questions

Draft three to eight questions: mostly closed, one open at the end. Pew: one idea per question, plain words without jargon, answer options that do not overlap and cover everything. NN/g: neutral wording without a hinted answer, balanced scales, "don't know" or "not applicable" where needed, recent behaviour instead of predictions. State for each question what decision it serves.

### 4. Trial run, collection, results

Propose a trial run on a few people from the target group (Pew: "essential step"). Vohra's guide: about 40 respondents give a roughly right picture, one practitioner's tip, not a rule. Record how many were invited and how many answered. If results exist, compute shares per answer and per group and always give the number of respondents.

### 5. Conclusion and decision

Separate data from conclusion and label the conclusion as the author's. Name what the data does not show (group sizes, who did not answer). Propose a decision and how to check it by behaviour.

### 6. Show, then write

Show the plan in chat first as a table by template blocks: title, hypothesis, audience, channel, four question rows (question, answers, conclusion), gaps, decision, check. Write a file only after the user confirms. Ask for the output path (default `customer-survey-<topic>.pptx` in the working directory). Save the data as JSON. The example is the Easyvest case from card.md; what the source does not give says so:

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Easyvest: product-market fit survey, about end of 2020",
    "hypothesis": "Sean Ellis threshold: \"very disappointed\" at least 40%. Decision: what to build next",
    "audience": "591 active customers; 120 answered within a week; margin of error \"in the 9% range\", 95% confidence",
    "channel": "Internally built survey tool; the survey date is not in the source",
    "q1": "How would you feel if you could no longer use easyvest? (very / somewhat / not)",
    "q2": "What type of people would most benefit from easyvest? (open)",
    "q3": "What is the main benefit you receive from easyvest? (open)",
    "q4": "How can we improve easyvest for you? (open)",
    "a1": "\"Very disappointed\" 47%, \"not\" 3%; French 49%, Dutch 26%, English 70%",
    "a2": "Persona \"Thomas\": worried about family's long-term finances, wary of traditional bankers",
    "a3": "Simple, affordable passive investing; ease of use; responsive service",
    "a4": "Somewhat group: automation, better Dutch, brand refresh, ESG, active plans",
    "c1": "Fit reached overall, not among Dutch speakers; fans invest 2x more",
    "c2": "These are the people to build for",
    "c3": "The product's strength",
    "c4": "Barriers to remove",
    "gaps": ["Share of \"somewhat\" not in the source", "Survey date not named", "No later score reported"],
    "decision": ["Half of roadmap: simplicity, ease, customer service", "Other half: Dutch support, direct debit, ESG tracking", "Active investing declined; ESG via blog"],
    "check": ["Top metric: an OKR with the PMF share", "Roadmap rebuilt every quarter"]
  }
}
```

Limits that fit the rendered slide: title under 60 characters; hypothesis, audience and channel under 120 each; questions (q1..q4) under 90; answers (a1..a4) under 90; conclusions (c1..c4) under 70; gaps, decision and check: up to three items under 60 each. A list of strings becomes lines, one thought per item. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/customer-survey.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's questionnaire, plan or readout and check it against the common mistakes in card.md, one by one:

1. No screening: the audience is everyone, and shares mix different people.
2. A hint in the question: the wording pushes toward an answer.
3. Two questions in one ("simple and clear").
4. Questions about the future instead of recent behaviour.
5. Only closed questions: the survey is limited by the author's own knowledge.
6. No trial run on a few people from the target group.
7. All answers weighted equally, including those from people for whom the product does not matter.
8. Shares given without the number of respondents.

Items 1, 6, 7 and 8 cannot be judged from the questions alone. First ask who was invited, whether a trial run happened, how answers were weighed and how many people answered; if the user does not know, mark the item "not checked" instead of reporting a finding. Also check that a conclusion is labelled as the author's and separate from data, and that a decision with a check exists. Report findings as a numbered list: what is wrong, why it distorts the answer, the concrete rewrite. End with a verdict: "survey answers the question", "works after changes" or "needs a hypothesis and an audience first".

Example: the question "Is our fast and convenient delivery important to you?" sent to all visitors, no open question. Findings: item 3 — two ideas, split into speed and convenience; item 2 — "our fast and convenient" hints at the answer, reword neutrally; item 1 — ask who actually ordered recently; item 5 — add one open question at the end. Verdict: "works after changes".
