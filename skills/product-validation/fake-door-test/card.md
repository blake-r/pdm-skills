# Fake Door Test

## Essence

A way to test a value proposition (the benefit the product promises the user) in a product that is already running. A button, menu item or banner appears in the interface that looks like a ready feature, but nothing happens on click or a stub screen opens. The share of those who clicked among those shown the element is measured. English names: fake door, painted door.

## When to use and when not to

Use when a live product has traffic and the idea of a benefit must be checked on your own users before development. Needed: a hypothesis, a screen and audience, a display period, a decision threshold. Needed: a product change and simple click analytics.

Limitations:

- **Traffic is needed.** PAF requires reaching statistical significance (enough data for the result not to be random). Guideline (recommendation of the card's author): for a share of about 5% with an accuracy of ±1.5 percentage points, roughly 800 views are needed (95% confidence interval, normal approximation; for the 3.5% from the case, about 577); with little traffic, extend the duration.
- **A click measures interest, not readiness to pay or to use** (the card author's conclusion).
- **There is a risk of negative reaction.** PAF: the user was shown a "key picture".
- **Do not place a fake door in an urgent scenario.** Habr (2025): a fake "Download receipt" button must not be inserted into a completed operation.

## Scheme

```
Hypothesis → Element in the interface → Click → Stub
(for whom,     (place, text like       │      (honest message,
 what,          the real feature's)    │       contact if wanted)
 threshold)                            ▼
   Share of clicks = clicked ÷ saw → threshold → decision
```

## How to apply

1. **Formulate the hypothesis and the threshold before launch:** "users [segment] want [benefit]; at least X% will click". Optimizely describes outcomes qualitatively: positive — you can build, negative — change the approach, neutral — dig deeper. The source gives no threshold number: set it with the team (the card author's recommendation: three zones — build, repeat with another wording or segment, or drop).
2. **Place the element** where the user would expect the feature. The text must not create the impression that the feature works (Optimizely).
3. **Prepare the stub:** tell the truth that the feature does not exist yet; you may offer to leave a contact (PAF). Do not give a reward for the click: it will collect clicks for the reward.
4. **Choose the audience and the duration.** Show the element to parts of the users; Habr: conditionally one such test per person per quarter or half a year (the article author's estimate, not a rule).
5. **Calculate** the share = clicked ÷ saw, overall and by segment. Watch the main metric.
6. **Decide** by the threshold: build, reword or stop. After the period, remove the element or replace it with the real feature.

## Example

Notino, a European online cosmetics store. In 2019 it opened notino.ch in German; Switzerland is multilingual, and the team was deciding whether to invest in an expensive multilingual site. Analytics showed that visitors with other browser languages were not the majority, and their purchase share differed little.

Hypothesis (reconstructed from the text): the interest in other languages is enough for development. Element: a language switcher with French and Italian (Romansh was not included). Stub: a window with the truth that the options are not yet available. The discount for a click was dropped: people would click for it. The test ran 7–21.10.2019; preparation took about a day and a half.

Reaction: the switcher was clicked by 3.5%; probably some only opened the list (the sum of clicks on languages is smaller than the clicks on the switcher). The purchase share after the test was slightly above average. The decision about the site is not named in the source; the author's conclusion: adding languages will not increase the number of purchases.

Deviation from step 1 of the card: the text contains no threshold set before launch and no number of views; there are also no clicks broken down by language.

Case source: M. Augustin, [«Why and how to run a fake door test»](https://uxdesign.cc/how-we-run-a-fake-door-test-in-notino-ux-case-study-c7138940c1ec), UX Collective, 1.01.2020.

## Common mistakes

- **The threshold is set after the result:** any figure can be declared a success.
- **A click is taken for demand.** At Notino, according to the article author's assumption, some of those who clicked only opened the list of languages.
- **A reward for the click** (discount, bonus) distorts the measurement: the Notino team refused it.
- **The fake door misleads or sits in an urgent scenario,** and the stub does not tell the truth.
- **Too few views:** the share is noisy.
- **Only the total share is read.** Segments can differ strongly (the card author's conclusion).
- **The main metric is not watched.** Gousto (a meal-kit delivery service) in its first experiments had non-working payment buttons that caused a small drop in sign-ups (Conversion, 2024; no figures given), while Notino checked the effect on the purchase share.

## Source

Description in PAF (Product Architecture Framework, Sergey Tikhomirov, [productframework.ru](https://productframework.ru/hypotheses/value_proposition), CC BY-SA 4.0, undated). Origin of the name: A. Savoia, [«Pretotype It»](http://www.pretotyping.org/uploads/1/4/0/9/14099067/pretotype_it_2nd_pretotype_edition-2.pdf), 2nd ed., October 2011; the term is taken from a talk by Jess Lee (Polyvore). Optimizely, [Painted door test](https://www.optimizely.com/optimization-glossary/painted-door-test/), glossary, undated. Serick, [«Fake door tests in mobile apps»](https://habr.com/ru/articles/889342/), Habr, 9.03.2025. H. Brown, [«Unlocking Insights: The Power of Painted Door Tests»](https://www.conversion.com/blog/unlocking-insights-the-power-of-painted-door-tests/), Conversion, 28.10.2024.

## See also

- Alternative to Landing Page Test: For a product not yet built, test the value proposition on a landing page.
- Alternative to A/B Testing: Use it when the feature does not exist yet and demand must be measured.
- Enhanced by Experiment Card: Record the hypothesis and the decision threshold on the card before showing the element.
