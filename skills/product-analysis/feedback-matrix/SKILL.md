---
name: feedback-matrix
description: Sort customer feedback by tone (positive or negative) and by whether something must be fixed into advice, compliments, critique and suggestions, turn each group into work (fix, improve, collect, keep) and produce a one-slide PPTX, or review an existing feedback breakdown. Use when the team has many reviews, ratings or support comments and must decide what to act on.
---

# Feedback Matrix

The theory, quadrants, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings feedback to sort, **review** when the user brings a finished breakdown or a decision drawn from one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the product, the period and the channels (in-app ratings, support chats, app store reviews, surveys);
- the feedback texts, or a table with text, channel and, if known, customer id;
- the criterion for "must fix": for example, the customer could not finish an action, lost money or time, or says they will leave;
- the owners of product areas, if the decision should name them.

Do not invent feedback or counts. If the user has only a summary, work from it and say the counts are theirs.

### 2. Split and tag

Split each review into statements: one review can praise delivery and complain about payment. Give every statement a topic (payment, delivery, search, support). Merge statements with the same topic and meaning, and count statements and distinct customers.

### 3. Place

For each merged statement decide the tone and apply the agreed "must fix" criterion by the consequence for the customer, not by the anger of the wording. Place it in advice, compliment, critique or suggestion. Neutral statements with no request are left out and counted.

### 4. Decide

Critique: fix first, name the owner and the date, and plan a reply to the affected customers. Advice: add to the improvement backlog. Suggestions: collect and set the count at which a suggestion is treated as critique. Compliments: keep, and do not break them with other changes. Do not promise effects.

### 5. Show, then write

Show in chat first, block by block as they will appear on the slide: the title, the scope and criterion, the four quadrants with counts, and the decision. Write a file only after the user confirms. Ask for the output path (default `feedback-matrix-<topic>.pptx` in the working directory). Save the data as JSON:

```json
{
  "text": {
    "title": "Magnit OMNI: store reviews, tone and severity",
    "scope": ["Source: Magnit Tech article, 2025", "Channel: in-app reviews of offline stores", "Counts: not published", "“Must fix” — the customer says they will not come back"],
    "advice": ["Not singled out in the source"],
    "compliment": ["Positive reviews: to analytics dashboards"],
    "critique": ["Parking: “never set foot here again”"],
    "suggestion": ["Parking: inconvenient but tolerable"],
    "decision": ["Critique: task to the store, store fixes and reports", "Reply to customers: call center tells what was done", "Positive and simple reviews: to manager dashboards"]
  }
}
```

Put the count of customers in brackets after each statement, and order each quadrant by that count (the JSON above is the Magnit case, whose source publishes no counts, so it has none). Keep up to about six statements of under 60 characters per quadrant; list the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/feedback-matrix.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's breakdown in any form and check it against the common mistakes in card.md:

1. The "must fix" criterion is stated and based on consequences, not on tone.
2. Reviews are split into statements; mixed reviews are not placed whole.
3. Every statement sits in the quadrant the agreed criterion gives: check the consequence, not the tone of the wording.
4. Statements carry counts of customers, not only examples.
5. Repeated suggestions are counted and moved to critique above the agreed threshold.
6. Critique has owners and dates.
7. Customers who reported critique get a reply about what was done.
8. The channels cover more than the loudest one.

Items 1 and 8 often need the user's knowledge: ask instead of reporting a finding. Report findings as a numbered list: statement or quadrant, what is wrong, why it changes the decision, the concrete fix. End with a verdict: "decision holds", "decision changes after fixes" or "not enough data to decide".
