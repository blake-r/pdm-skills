---
name: pestel-analysis
description: Describe the external environment of a company, product or market by six groups of facts (political, economic, social, technological, environmental, legal), turn them into threats, opportunities and a decision, and produce a one-slide PPTX; or review an existing PESTEL. Use when entering a new country or industry, revisiting strategy, launching a product in a regulated area such as payments or lending, or when outside conditions change sharply.
---

# PESTEL Analysis

The theory, limits and a worked case are in [card.md](card.md). Read it before either mode and do not contradict it. Reply in the user's language.

Pick the mode from the request: **do** when the user brings a subject and a country to analyse, **review** when the user brings a finished PESTEL.

## Mode: do

### 1. Collect inputs

Ask in one message for anything missing:

- the subject: company, product or market, and the country (one country per analysis);
- the horizon and the decision the analysis must prepare;
- the sources the user already has: reports, laws, statistics, news with dates.

If the user wants to choose a feature or compare competitors, say that PESTEL covers only the external environment and ask what decision it should serve. Do not invent facts, numbers, dates or sources: if a block has none, write it as "not searched" or "nothing found", never as "no impact". If this skill runs inside pdm-brief, the questions above are answered by pdm-brief's fallback.

### 2. Facts by block

For each of the six blocks write one fact per line: an event or a rule with a date, a number and a source, not an opinion. Each fact goes in one block only: a legal norm goes to L even if a political body passed it. Questions per block: P, sanctions, taxes, trade policy; E, growth, inflation, rates, exchange rates, incomes; S, demography, habits, trust; T, new technology and standards, cyber threats; E (environmental), climate and ESG requirements; L, laws, licences, data protection.

### 3. Threats, opportunities, decision

Mark every fact as a threat, an opportunity or unclear, and say through what it acts: demand, costs or allowed actions. The method gives facts without priority; if the user wants a ranking, rate each threat and opportunity by strength and probability and say that this goes beyond the method. Then name the decision: what to do, what only to watch, who is responsible, by when, and which event or number triggers a revision. Mark unknown owners and dates as unknown.

### 4. Show, then write

Show the analysis in chat first as a table by template blocks: title, six blocks of facts, threats, opportunities, decision. Write a file only after the user confirms. Ask for the output path (default `pestel-<subject>.pptx` in the working directory). Save the data as JSON. The JSON below shows the format only: its values are the Tinkoff case from card.md, not data for this analysis; use them only when the user explicitly asks to see an example. Fill each field from the user's facts. A block with no fact is written as "N/A", and the chat names what is missing and where to find it:

```json
{
  "text": {
    "title": "Tinkoff, Russian banks, 2022",
    "p": [
      "Sanctions from 24.02.2022: no Visa, Mastercard, SWIFT",
      "Assets of some banks frozen (Gazprombank, Sberbank)"
    ],
    "e": [
      "S&P lowered credit ratings of Russian banks",
      "Foreign investors sold Russian shares",
      "GDP growth unstable since 2008"
    ],
    "s": [
      "Over $1.3 billion withdrawn from accounts in a few days",
      "Tinkoff transfers were delayed, operators were silent"
    ],
    "t": [
      "Mobile payments (NFC)",
      "Cashback with partners",
      "Crypto wallets: use restricted in Russia",
      "Ecosystems around the bank"
    ],
    "env": [
      "Emissions reduction",
      "ESG standards: harder to attract capital without them"
    ],
    "l": [
      "From 1.06.2022: clients warned of investment product risks",
      "Cyber threats: stronger customer checks (EU — PSD2)"
    ],
    "threats": [
      "Sanctions",
      "Weaker partnerships in the crisis",
      "Takeover risk",
      "Slower growth of indicators"
    ],
    "opportunities": [
      "25–30 banks exit in 2022: clients may join Tinkoff",
      "Softer stance on crypto: own wallet",
      "Central bank and government measures"
    ],
    "decision": [
      "Warn shareholders about weaker indicators",
      "Develop the ecosystem, studying Sberbank services",
      "Check partners in the crisis",
      "Avoid drawing Western attention to the new owner",
      "Deadlines and responsible persons not specified"
    ]
  }
}
```

Limits that fit the rendered slide: title under 50 characters; each of the six blocks up to five items under 60 characters; threats, opportunities and decision up to five items under 55 characters. A list of strings becomes lines, one thought per item. Put the rest in chat. Write "N/A" for a block with no data. Run from this skill's directory:

`example.json` next to the template is a sample that shows what the finished result looks like. Use it to fill the template only when the user explicitly asks to see an example of this result; otherwise fill the placeholders with the user's own data.

```bash
uv run ../../../scripts/fill_pptx.py <this skill dir>/pestel-analysis.pptx data.json <output>.pptx
```

`uv run ../../../scripts/fill_pptx.py <template> --list` prints every placeholder and its hint.

## Mode: review

Take the user's PESTEL in any form and check it against the common mistakes in card.md:

1. Facts without "so what": there are no threats, opportunities or decision that follow from them.
2. Opinions instead of facts: no number, date or source.
3. Equal weight of blocks: blocks filled for form's sake bury the main ones.
4. Internal matters instead of environment: competitors, prices and the company's own weaknesses.
5. Double counting: one law is listed both in politics and in law.
6. A stale snapshot: no date of the analysis, no sign of when to revisit it.
7. Several countries in one analysis.
8. Retellings instead of the primary source: media instead of the law or the regulator's report.

Items 6 and 8 usually cannot be judged without the dates and links: ask for them instead of reporting a finding. Also check that empty blocks are marked "not searched" and that the decision has an owner, a date and a revision trigger. Report findings as a numbered list: block or fact, what is wrong, why it matters for the decision, the concrete fix. End with a verdict: "analysis supports a decision", "sound after fixes" or "not enough facts".

Example: the economic block says "the market is unstable", the politics block repeats a law that also sits in the legal block, and there is no decision. Findings: item 2, replace the opinion with a fact that has a number and a date; item 5, keep the law in the legal block only; item 1, add threats, opportunities and a decision. Verdict: "sound after fixes".
