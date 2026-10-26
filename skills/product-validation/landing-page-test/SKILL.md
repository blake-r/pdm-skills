---
name: landing-page-test
description: Plan or review a landing page test - checking a value-proposition hypothesis with a page or presentation that fully describes the offer and asks visitors for a target action (leave contacts, choose a paid plan, give card details, pre-order) before the product exists - and produce a one-slide test card. Use when the user wants to test demand with a landing page, a waitlist, a coming-soon page, a pre-order page or a presentation before building.
---

# Landing page test (landing page / presentation / contact collection)

The definition, steps, limits and the worked case (Buffer, 2010) are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants to design the test, **review** when the user brings a finished plan or results and wants them checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the idea and the hypothesis: who needs what and why (PAF form: "We believe that [offer] will interest [group], which will be confirmed by [criterion], because [reason]");
- the page or presentation: what it will say and show, who will make it, how clear it is to outsiders;
- the target action and its steps (e-mail, choice of a plan, card, pre-order);
- where visitors come from, which group, how many can be brought in what time, the budget;
- the threshold and the number of visitors, if the user already has them.

If the user wants to know whether the solution works or whether people will keep using it, say that the test measures interest in the description (card.md) and ask what they want to prove. Do not invent numbers: mark unknown values "not in source" or "unknown".

### 2. Hypothesis, steps, measure

Write the hypothesis in the PAF form. Lay out the steps from a view to the most costly action and name the conversion of each step (people who did the step divided by people who saw the page, or by the previous step). Say that e-mail costs the visitor nothing and that a paid step gives a stronger signal.

### 3. Page and visitors

List what the page must contain: headline with the benefit, the problem, the offer, terms, one button. For a presentation, the same content. Plan to talk to some consumers before and after about whether the text is clear (PAF), and to the people who left contacts. Visitors must come from the target group, not only friends.

### 4. Threshold and volume

Set the threshold and the number of visitors before launch. Say that the figures are the card author's advice, not a rule of the source: hundreds of visitors; the 95% confidence interval for the true conversion at an observed 10% is about 5-17% with 100 visitors and 7-13% with 400 (author's calculation, Wilson method).

### 5. Reading the result and the decision

Explain how to count steps and sources and compare with the threshold. Decide: check the solution itself, change the offer or the group, or stop. A zero on a paid step is a reason to seriously reconsider the group and the offer; Ries: it does not necessarily mean there is no business. If the offer cannot be fulfilled, advise to apologise to the people who responded.

### 6. Show, then write

Show the card in chat first as a table by template blocks: title, hypothesis, page, visitors, target action, up to four step rows (step, people, share of the previous step, share of views), threshold and volume, result, decision. Write a file only after the user confirms. Ask for the output path (default `landing-page-test-<idea>.pptx` in the working directory). Save the data as JSON. The example is the Buffer case from card.md; text fields the source does not give say "not in source"; unused cells are "—" (the template has no counted columns or formulas):

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Buffer: tweet queue, Joel Gascoigne, 2010",
    "hypothesis": "People will want to use an app for a tweet queue, and then agree to pay",
    "page": "Description of the idea, then a page with plans, then a form \"we'll let you know at launch\"",
    "traffic": "A link on Twitter asking to rate the idea; number of visitors: not in source",
    "action": "Choose a plan and leave an e-mail; later — pay the subscription",
    "s1": "Page visitors", "n1": "not in source", "p1": "—", "t1": "—",
    "s2": "Signed up (over seven weeks, article 2013)", "n2": "120", "p2": "not in source", "t2": "not in source",
    "s3": "Started using at launch", "n3": "50", "p3": "41.7% (calculation: 50 of 120)", "t3": "not in source",
    "s4": "Paid 3 days after launch", "n4": "1", "p4": "2% (calculation: 1 of 50)", "t4": "not in source",
    "threshold": "Not in source: the threshold and volume are not set. Clicks on paid plans — \"a small number\", no figure",
    "result": "People went through the plans page and left an address; Gascoigne wrote to each one personally. Discrepancy: first payment \"within 4 days\" (2011) and \"after 3 days\" (2013)",
    "decision": "Start development \"without hesitation\"; launch 30 November 2010. After 2.5 months: over 500 users, about 4% pay"
  }
}
```

Limits that fit the rendered slide: title under 60 characters; hypothesis under 130; page, traffic and action under 110 each; steps (s1..s4) under 60; people (n) under 20; shares (p, t) under 26; threshold, result and decision under 190. A list of strings becomes lines. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/landing-page-test.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's plan or results and check them against the common mistakes in card.md:

1. The page is made for addresses: no price step, no conversations, the aim is the number of signups, not learning.
2. An e-mail address is taken for demand; paid steps are not looked at.
3. The threshold and the number of visitors were not set before launch.
4. The sample is small: tens or about a hundred visitors give a wide range of the true conversion.
5. Low conversion is read as "the idea is not needed", although the text may be unclear or the request for a card may not be trusted.
6. Only friends and acquaintances came to the page.
7. The people who responded are forgotten: nobody wrote to them, and nobody apologised when the offer could not be fulfilled.

Items 3, 4 and 6 usually cannot be judged from the description alone: ask when the threshold was written, how many visitors there were and where they came from. Also check that the hypothesis has a criterion, the steps are counted per step and the decision follows from the numbers. Report findings as a numbered list: what is wrong, why it misleads, the concrete change. End with a verdict: "test supports a decision", "works after changes" or "needs a threshold and visitors first".

Example: a "coming soon" page with an e-mail form, 40 signups from friends, no threshold, verdict "demand confirmed". Findings: item 1 - the page only collects addresses, add a plan choice and talk to people; item 2 - e-mail costs nothing; item 3 - no threshold, set one and the volume; item 4 - 40 signups are too few for a conversion; item 6 - friends inflate the result. Verdict: "needs a threshold and visitors first".
