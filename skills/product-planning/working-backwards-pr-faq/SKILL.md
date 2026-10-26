---
name: working-backwards-pr-faq
description: Write or review an Amazon-style Working Backwards PR/FAQ - a mock press release plus external and internal FAQ written before building - and produce a one-slide PR/FAQ, or check an existing one. Use when the user wants to test a product idea from the customer's side, write a press release for an unbuilt product, prepare a PR/FAQ review, or says "working backwards", "PR/FAQ", "пресс-релиз из будущего", "обосновать идею".
---

# Working Backwards PR/FAQ

The theory, the review rules and the case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user has an idea and wants a PR/FAQ, **review** when the user shows a finished one.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the idea: product or initiative, who the customer is, the problem in the customer's words;
- what the customer uses today and why it is not enough;
- the expected launch date and place (city, outlet);
- market size, price, unit economics, upfront investment, dependencies, legal issues, if known;
- the known risks and the three likeliest reasons to fail.

Do not invent numbers or quotes. Mark what the user did not give as N/A. If the customer or the problem is missing, stop and help define them first; if the user only has a feature list, ask which customer problem each feature solves.

### 2. Draft by blocks

Write in this order: heading, subheading, summary, problem (from the customer's side), solution (and how it differs from current options), company quote, customer quote, how to start. Then the external FAQ (price, how it works, support, where to buy) and the internal FAQ (market size, unit economics, upfront investment, dependencies, legal, time to profit, assumptions, top three reasons to fail). Keep the press release under one page and the FAQ within five pages.

### 3. Decision slot

State what the review must decide: go, more investigation, or set aside. If the user has no decision yet, write N/A; do not invent one.

### 4. Show, then write

Show the draft in chat first as a table by template blocks. Write the file only after the user confirms. Ask for the output path (default `pr-faq-<product>.pptx`). Save the data as JSON. The JSON below shows the format only. Its values come from the example case in card.md (Fulfillment by Amazon), not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" where there is none.

```json
{
  "text": {
    "title": "Fulfillment by Amazon (FBA): two PR/FAQs, seller view and buyer view",
    "heading": "N/A: the PR/FAQ text is not published",
    "subheading": "N/A",
    "summary": "N/A",
    "problem": "N/A",
    "solution": "N/A",
    "quote_company": "N/A",
    "quote_customer": "N/A",
    "start": "N/A",
    "faq_ext": ["N/A: not published for FBA"],
    "faq_int": ["N/A: not published for FBA"],
    "decision": ["Developed using two PR/FAQs: one from the seller perspective, one from the buyer perspective", "Outcome of the review, date and changes: N/A"]
  }
}
```

Length limits that fit the slide: title under 80 characters; heading under 70; subheading under 120; summary under 220; problem and solution under 200 each; quotes under 110 each; start under 90; faq_ext and faq_int up to five items under 70 each; decision up to three items under 80. A list of strings becomes lines. Put the rest in chat. Run from the repository root:

`example.json` next to the template is a sample of a finished result. Use it only when the user explicitly asks to see an example; otherwise fill the placeholders with the user's own data.

```bash
uv run scripts/fill_pptx.py skills/product-planning/working-backwards-pr-faq/working-backwards-pr-faq.pptx data.json <output>.pptx
```

`uv run scripts/fill_pptx.py <template> --list` prints every placeholder and its hint. If the customer is still unclear, Jobs-to-be-Done or Value Proposition Canvas come first; once approved, User Story splits the work.

## Mode: review

Check the user's PR/FAQ against the common mistakes in card.md:

1. It writes about features, not the customer's problem, or is not clearly different from current products.
2. The press release sells: hype, unsupported claims.
3. The internal FAQ is thin: no unit economics, upfront investment or top three reasons to fail.
4. It is too long: the press release over one page, the FAQ over five, appendices of charts.
5. The review is run with pre-reading or seniors speaking first.
6. It is treated as final after the first draft.
7. Approval is taken as proof, and the document is not revised as facts change.

Items 5 to 7 usually cannot be read from the text: ask how the review was run and when it was last revised, instead of reporting a finding. Report findings as a numbered list: what is wrong, why it matters, the concrete rewrite. End with a verdict: "ready for review", "works after changes" or "back to the customer and problem".

Example: a draft lists twelve features, has no customer quote and an internal FAQ with only a launch date. Findings: item 1, rewrite the problem in the customer's words and name the difference from today; item 3, add market size, per-unit economics, investment and three failure reasons. Verdict: "works after changes".
