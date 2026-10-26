---
name: pilot-project
description: Plan or review a pilot project / sample - checking a value-proposition hypothesis by building a trial solution with the minimum set of features and handing it to real users or clients, then deciding to scale, rework or stop - and produce a one-slide pilot card. Use when the user wants to test a service, integration or process with real participants before a full build, including a bank-fintech or retailer pilot.
---

# Pilot project / sample

The definition, steps, the worked case (Virgin Money and Twenty7Tec, mortgage applications, 2020-2021) and its limits are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language. The card avoids the word "prototype"; say "trial solution / sample".

Pick the mode from the request: **do** when the user wants to design a pilot, **review** when the user brings a pilot plan or results and wants them checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the idea and the hypothesis: which group gets which benefit from which result;
- what the trial solution can contain at minimum, and what will be done by hand;
- participants: who, how many, how they are chosen, are they close to the target group;
- success measures (2-3), threshold, term and the person who decides;
- how feedback is collected next to the numbers.

If the question can be answered with something cheaper than a working sample, say so (card.md: PAF names the cost as the main limit) and ask whether to continue. Do not invent numbers: mark unknown values as "not in source" or "unknown".

### 2. Criteria

Set measures, threshold and term before launch; say that this is the card author's recommendation, not a rule of the source. Define conversion as the share of participants who reach the target action out of all who received the sample.

### 3. Run and read

Describe how numbers and feedback are collected. Explain the reading: above the threshold - scale, but check integration and load separately; near it or no clear reason - rework and repeat; below - stop. Warn that success among the first willing participants does not prove demand in the whole market.

### 4. Show, then write

Show the card in chat first as a table by template blocks: title, hypothesis, trial solution, participants, term and conditions, criteria and threshold, result in numbers, result in feedback, decision. Write a file only after the user confirms. Ask for the output path (default `pilot-project-<idea>.pptx` in the working directory). Save the data as JSON. The example is the case from card.md; what the source does not give says "not in source":

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Broker applications at Virgin Money, 2020-2021",
    "hypothesis": "Not in source. In meaning: brokers find it more convenient to submit applications to Virgin Money from their working platform (card author's conclusion)",
    "trial": "APPLY integration in the CloudTwenty7 platform: request for a mortgage decision in principle and submission of a full application",
    "people": "Two intermediaries: Connells and Mortgage Advice Bureau",
    "term": "Duration not given in the source; announcement 1.12.2020, decision in March 2021",
    "criteria": "Not in source: the threshold and indicators are not published",
    "numbers": "More than 1,000 applications to Virgin Money via APPLY; share of possible ones not in source",
    "feedback": "Simon Wallace (Virgin Money): brokers submit applications quickly; other feedback not in source",
    "decision": "Integration opened to all CloudTwenty7 users (messages of 15 and 16.03.2021). Basis: only the March 2021 messages call it a successful pilot (the 1.12.2020 release does not contain the word \"pilot\"); the criterion is not published"
  }
}
```

Limits that fit the rendered slide: title under 60 characters; hypothesis under 130; trial, people and term under 110 each; criteria, numbers and feedback under 130 each; decision under 260. A list of strings becomes lines. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/pilot-project.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's plan or results and check them against the common mistakes in card.md:

1. No criteria and term set before launch.
2. Participants do not resemble the market (only willing or loyal ones).
3. Volume is read without a denominator (the share of possible participants).
4. The sample lacks the key benefit or carries extras.
5. Demand and execution are mixed, so a failure has no clear cause.
6. No decision after the pilot (scale, rework or stop), no check of integration and load before scaling.

Items 1 and 3 cannot be judged from a description alone: ask when the threshold was set and how many could have taken part. Report findings as a numbered list: what is wrong, why it distorts the result, the concrete change. Also check that the hypothesis names a group and a benefit and that numbers are paired with feedback. End with a verdict: "result can be trusted", "trust after changes" or "run the pilot again".

Example: a bank-fintech pilot ends with "1 200 users registered, success", with no threshold. Findings: item 1 - ask for the threshold and term set before launch; item 3 - how many were invited; item 6 - write scale, rework or stop. Verdict: "trust after changes".
