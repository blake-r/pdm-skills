---
name: value-chain-and-nets
description: Build or check a value chain (Porter), an industry chain of participants, or a value network of a mediating firm, and produce a one-slide chain map with cost, time, client-visible value and a decision per link; or review an existing chain map. Use when you need to see where price and delay come from, which link to improve, take over, replace or remove, or how a bank, marketplace or payment network creates value.
---

# Value Chain & Nets

The theory, the two meanings of "value network", limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user wants a chain or network built, **review** when the user shows a finished map or description and wants it checked.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the level: a product from the client's side, one company, or an industry;
- what the client gets at the end, at what price and in what time;
- the links: company activities, or participants in the order the product or money passes through them;
- cost, time and what the client sees for each link, and where each number comes from;
- whether the firm moves a product (chain) or connects clients to each other (network), and which meaning of "network" the user needs;
- the decision the user is facing.

Do not invent costs of links. A number that has no source is marked "unknown", never estimated.

### 2. Choose the configuration

Say in one line whether this is a chain or a network and why (card.md, "When to use and when not to"). For a mediating firm, replace links with the three network activities: network promotion and contracts, service provision, infrastructure operation. If the user needs the diamond of customers, suppliers, competitors and complementors, say that it is a different model and ask which one is wanted.

### 3. Fill the links

For a company use the five primary and four support activities from card.md. For an industry use participants in order. For each link write: who and what it does, cost and time (with source), what the client sees. Margin is the value at the end minus the cost of all links.

### 4. Find the links without value

Mark links where cost and delay grow, but the client does not see the benefit or the firm does not control the link. Check neighbors: a change in one link moves the cost of others.

### 5. Decision and check

For each marked link choose: improve, take over, replace, remove. Name the client figure (price, time, transparency) that must change and the date to check it.

### 6. Show, then write

Show the map in chat first as a table: one row per link with the columns "does", "cost and time", "client sees", then value for the client, links without value, decision, check, sources. Write a file only after the user confirms. Ask for the output path (default `value-chain-<name>.pptx` in the working directory). Save the data as JSON. The example is the Wise case from card.md; where the source gives nothing, it says so. Leave unused fields out of the JSON or set them to null.

The JSON below shows the format only. Its values come from the example case named above, not from the user's task: use them only when the user explicitly asks to see an example. Otherwise fill each field with the user's facts and write "N/A" for a field with no fact.

```json
{
  "text": {
    "title": "Wise: transfer of £200 to Singapore, FY2024 report",
    "n1": "Sender's bank",
    "n2": "Internal correspondent",
    "n3": "International correspondent bank",
    "n4": "Singapore bank",
    "n5": "Recipient's bank",
    "r1": "Sends £200",
    "r2": "not described",
    "r3": "not described",
    "r4": "not described",
    "r5": "Credits the recipient",
    "c1": "not given per link",
    "c2": "not given per link",
    "c3": "not given per link",
    "c4": "not given per link",
    "c5": "not given per link",
    "s1": "pays £200",
    "s2": "not visible",
    "s3": "not visible",
    "s4": "not visible",
    "s5": "receives S$306.91",
    "value": ["£200: S$336.01 at Wise, S$306.91 at banks", "Bank route: rate 1.6604, fee £8.63, markup £6.53, total £15.16", "62% — under 20 seconds, 95% — within 24 hours (banks: up to 5 days)"],
    "waste": ["Three intermediary banks between sender and recipient", "Each has its own rate, fee or markup"],
    "decision": ["Own network instead of correspondents", "5 direct payment systems by FY2024", "90+ local banks, 65+ licenses"],
    "check": ["£200: S$336.01 against S$306.91 at banks", "Review: Wise FY2025 report (proposed by us)"],
    "sources": "Wise plc, Annual Report 2024, pp. 14, 15, 30; Wise FY2024 = year to 31.03.2024; bank figures: average of 4 banks, May 2024"
  }
}
```

The template has six links; the sixth link, the four support-activity boxes and the margin strip sit in optional groups that are removed when n6, sup_* or margin are not given. The Wise case has no support activities or margin per link, so they are left out. Limits that fit the rendered slide: title under 60 characters; link name (n1..n6) under 32; "does" (r) under 30; "cost and time" (c) under 40; "client sees" (s) under 30; support fields (sup_infra, sup_hr, sup_tech, sup_proc) under 60; margin under 90; value up to three items under 75, waste up to three items under 60, decision up to three items under 40; check up to two items under 60; sources under 130. Put the rest in chat. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/value-chain-and-nets.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's map, table or description and check it against the common mistakes in card.md:

1. A mediating firm (bank, marketplace, payment network) is drawn as a chain of purchase, production and sale, so the connection of clients is lost.
2. The two meanings of "value network" are mixed: the three-activity model of a mediator and the diamond of four players.
3. The map draws a process, not value: it is not said what the client sees in a link and what he pays for.
4. Costs of links are invented: a number for someone else's link has no source.
5. Support activities are forgotten, although they affect every primary link.
6. A link is optimized alone, without the effect on its neighbors.
7. One author's comparison is taken for the picture of the market: one route, one date, an average of a few players.

Items 4, 6 and 7 usually cannot be judged from the description alone: ask where the numbers come from, what else changes with the link and how many routes and dates the comparison covers, instead of reporting a finding. Also check that the end value for the client is stated with price and time, that margin is not confused with revenue, and that each marked link has a decision and a check. Report findings as a numbered list: what is wrong, how it changes the decision, the concrete correction. End with a verdict: "map supports the decision", "works after changes" or "numbers and links do not support the decision".

Example: an online marketplace is drawn as "supplier, warehouse, delivery, client" with costs per link and no source, and the verdict is "remove the warehouse". Findings: item 1 — the marketplace connects sellers and buyers, check which activities are network promotion, service provision and infrastructure; item 4 — ask where the costs come from; item 6 — ask how delivery time and returns change without the warehouse. Verdict: "works after changes".
