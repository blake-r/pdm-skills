# Soft Launch

## Essence

Soft Launch is a way to test a solution hypothesis (and a business model) by releasing the solution itself, but in a packaging different from the one that is to be scaled: for a limited audience, region or channel, without loud advertising. The results show the problems and value of the solution; the conclusions are applied to the main launch. The description is based on PAF (Product Architecture Framework, the methodology of Sergey Tikhomirov).

## When to use and when not to

Use when the solution can be released in working form, there is an audience or market similar to the target one, real quantitative data is needed, and a failed launch would strongly hurt reputation (a PAF argument for the business model). Inputs: a working solution, an audience, indicators with thresholds, a term.

PAF limitations: high costs of creating and engaging consumers; a separate marketing strategy may be needed; costs of closing and migrating clients; test values still differ from real ones, and one can choose differences that devalue the experiment.

Non-obvious points (Supercell's experience, see "Example"):

- A large sample does not guarantee transferability. Supercell writes that even 100,000+ players do not give reliable conclusions about global behavior.
- The term must cover the metric of the solution: a month was not enough for long-term retention and monetization.

## Scheme

```
Hypothesis + thresholds → what may change in the packaging (name, design, price, offer)
→ similar audience, no loud advertising → launch → numbers + feedback
→ decision: scale / rework and repeat / close and migrate clients
```

## How to apply

1. **Hypothesis and thresholds before the start.** Card author's recommendation: 2–3 indicators, a threshold, a term. Retention is the share of users who return on day N after the first entry (D1, D3, D7 — day 1, 3, 7).
2. **Packaging.** PAF for the business model: you may change the name, design, price, or the wording of the offer, if this does not affect the target metrics. Do not touch the essence of the value.
3. **Audience.** Similar to the target one (PAF for the business model: a market different from the target but close to it); record the differences.
4. **Connect analytics** before the launch.
5. **Term** — not shorter than the horizon of the main metric (card author's recommendation).
6. **Launch without loud advertising.** Collect numbers (what happened) and feedback (why).
7. **Decision.** Above the threshold — scale, transferring the conclusions to the main product; near it — rework and repeat; below — close and migrate clients.

## Example

The case is not from e-commerce or fintech: a public case with soft launch figures could not be found there. The mobile game Squad Busters by Supercell (Finland) was taken.

- **Hypothesis** is not formulated in the sources. Eino Joas (from the game team): they wanted a game "for everyone".
- **Before the soft launch.** Closed test, February 2023, 5,000 players: D7 — 29%, below the target (the target is not named). After fixes, a second test, May 2023, more than 140,000 players: D1 — 61%, D3 — 44%, D7 — 38%.
- **Soft launch.** From 23 April 2024, iOS and Android, 8 countries: Canada, Finland, Denmark, Norway, Sweden, Spain, Mexico, Singapore. About a month. The soft launch figures were not published; there are no packaging differences in the sources.
- **Criterion.** Not in the source.
- **Decision.** The global launch on 29 May 2024 was announced on 25 April, two days after the start. The basis for the decision from the soft launch results is not named in the source. Ilkka Paananen (CEO of Supercell) writes about pressure in favour of bold risks: six years without a successful launch. The link to the date is not named in the source; by the card author's assumption, the date was set before the results.
- **Result.** 40 million pre-registrations and 75 million downloads in the first year; Paananen: "not a lot of those players stuck around"; Joas: players "didn't find what they were looking for". Retention after the launch did not match the tests; no figures. On 30 October 2025 Mobilegamer reported that the game was being shut down. The estimates differ: the blog reports more than $100 million in player spending, AppMagic (an analytics service) about $68 million in revenue; the comparability of the definitions is not disclosed.

## Common mistakes

- **No thresholds before the start.** The decision is made up after the result; the case has no thresholds.
- **The test audience taken for the market.** Similar countries and big samples do not guarantee the same behavior.
- **Term and metrics shorter than the decision.** Only D7 was checked, not long-term retention and monetization.
- **Loud advertising and a fixed date before the results.** The test becomes the launch.
- **A significant change in the packaging.** Price or key benefit affects the metrics, and the result does not transfer (a PAF risk).
- **No analytics and no exit plan.** Without measurement there is no conclusion; without client migration closing is expensive.

## Source

Description in PAF (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, undated): [solution hypotheses](https://web.archive.org/web/20241204101338/https://productframework.ru/hypotheses/solution) (the live page returns 403, the web.archive.org snapshot is available) and [business model hypotheses](https://productframework.ru/hypotheses/business_model). PAF does not name the author of the method or the year.

Ilkka Paananen, [«The Best Games Haven't Been Made Yet»](https://supercell.com/en/news/the-best-games-havent-been-made-yet/), Supercell blog, 10.02.2026. Neil Long, Mobilegamer.biz: [8.04.2024](https://mobilegamer.biz/supercells-squad-busters-soft-launches-on-april-23/) (countries), [25.04.2024](https://mobilegamer.biz/supercells-squad-busters-launches-globally-on-may-29/), [30.10.2025](https://mobilegamer.biz/supercell-is-killing-squad-busters/) (AppMagic estimates).

## See also

- Preceded by Minimum Viable Product: Test the main assumption with an MVP first, then release it softly.
- Enhanced by AARRR Metrics: Use its retention and revenue groups to choose the indicators and thresholds.
- Enhanced by Cohort Analysis: Group users by install date to read retention on days 1, 3 and 7.
- Preceded by Pilot Project / Sample: Release the solution to a similar market only after the pilot shows value.
