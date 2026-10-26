# Field Research

## Essence

Field research is observation of a person in their "natural habitat": at home, in a store, at a bank branch, or while working with an app. The researcher watches what the person actually does and records step by step how they handle the product. The method tests qualitative hypotheses about the consumer (assumptions about how they behave and why). According to the description in PAF (Product Architecture Framework): the observer stays silent or clarifies the reasons for actions with questions; "immersion" can be full or partial.

## When to use and when not to

Use it to see behaviour the person would not tell you about: habits, workarounds, obstacles. Inputs: a hypothesis ("in situation X the person does Y"), a place, the participants' consent.

Do not use it:

- **For shares and numbers.** PAF: the method does not assess behaviour quantitatively. A few visits produce hypotheses, not percentages.
- **When behaviour is distorted by an outside eye.** NN/g (Nielsen Norman Group): an observer can make the situation intimidating or awkward; with remote observation you only see what falls within the camera.
- **When there is no time or money.** NN/g: the method is expensive and hard; PAF: it is burdensome for both the researcher and the participant.

A nuance: the observer sets aside their own impressions (PAF), so facts and interpretations are written separately.

## Scheme

```
Hypothesis + observer role (silent / clarifies)
  → place, person, visit time
  → log: fact │ person's words │ interpretation (separately)
  → repetitions across visits
  → hypothesis: yes / no / unclear → decision + check
```

## How to apply

1. **Formulate the research question** and the visit plan: without agreed questions and a goal, it is easy to observe the wrong thing (NN/g).
2. **Choose the place** where the person naturally performs the task, and obtain permissions (NN/g).
3. **Decide the role.** Passive: you do not intervene. Active: you ask clarifying questions as things happen (PAF). For the second case, Beyer and Holtzblatt described contextual inquiry with four principles: context, partnership, interpretation, focus (as summarised by NN/g).
4. **Observe** the order of actions, people's words and workarounds; in the passive role keep talk to a minimum.
5. **Keep a log** following the scheme above; in an active role, check the interpretation with the person on the spot.
6. **Repeat the visits.** A visit lasts from an hour or two up to several days (NN/g, contextual inquiry); the sources do not set a number of visits. Stop when new things stop appearing (recommendation of the card's author).
7. **Consolidate the repetitions**, note what was not confirmed, and make a decision with a check by behaviour (author's conclusion).

## Example

Bank of America (USA, a bank) commissioned the agency IDEO to come up with a way to attract clients (2004, per a retelling). IDEO, together with bank employees, observed women with children ("boomer-age", the age of the baby boom generation) in Atlanta, Baltimore and San Francisco; per a single retelling, a dozen families were observed, including while shopping and eating.

| Observation | Conclusion | Decision |
|---|---|---|
| People round payments up to the dollar. Retelling: a woman from Atlanta wrote rounded amounts into her chequebook | Rounding simplifies the accounting and creates a buffer | The Keep the Change service: purchases made with a Visa debit card are rounded up to the dollar, and the difference goes from the current account to a savings account |
| Many mothers find it hard to save | The bank does not meet this need (interpretation of sources) | The same |

Tim Brown (IDEO): clients had not asked for this; the possibility was revealed by observing a habit. Results (sources disagree, not reconciled): Core77, 2007 — 2.5 million clients; Brown, 2010 — 10 million and $1.8 billion in savings; 2018 — over 12 million and $2 billion.

Not in the sources: an observation log, the number of visits and rounding cases, independent verification. Atlanta and the dozen families come only from a retelling.

Sources: [Forbes, interview with Tim Brown, 14.01.2010](https://www.forbes.com/2010/01/14/tim-brown-ideo-leadership-managing-design.html); [Core77, 20.02.2007](https://www.core77.com/posts/5564/Bank-of-America-enlists-IDEOs-servicesFTW); [This is Design Thinking, 2018](https://thisisdesignthinking.net/2018/09/feeling-in-control-bank-of-america-helps-customers-to-keep-the-change/).

## Common mistakes

- **Interpreting on the spot.** Writing "he was uncomfortable" instead of "went back to the previous screen" replaces a fact with an opinion (PAF requires setting interpretation aside).
- **Waiting for requests.** In the case, nobody asked for the feature: the idea came from what was seen, not what was said.
- **Taking one case as the rule:** repetitions are needed.
- **Forgetting the observer effect** (NN/g): note where it is noticeable.
- **Looking for numbers.** Visits do not give shares.
- **Not obtaining permissions and not agreeing on rules for observers** (NN/g).
- **Stopping at the log.** Without a decision and a check, it stays an archive.

## Source

Hugh Beyer, Karen Holtzblatt, *Contextual Design: Defining Customer-Centered Systems*, Morgan Kaufmann, San Francisco, 1997 (on the Elsevier publisher's site — September 1997; in library catalogues ©1998): [book page](https://www.elsevier.com/books/contextual-design/beyer/978-1-55860-411-7). The method is linked to ethnography (the study of groups of people in their environment): NN/g calls contextual inquiry a type of ethnographic field research. Nielsen Norman Group: Susan Farrell, Therese Fessenden, [«Field Studies»](https://www.nngroup.com/articles/field-studies/), 2024; Kim Flaherty, [«Contextual Inquiry»](https://www.nngroup.com/articles/contextual-inquiry/), 2020 (the book is dated 1990 there, which is an inaccuracy). Description in PAF (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, no date).

## See also

- Alternative to Diary Study: Use a diary to record behaviour over days or weeks, beyond a short visit.
- Enhanced by In-Depth Interview: Pair observation with an interview that asks about the reasons behind actions the observer saw.
- Followed by Empathy Map: Put the logged observations into the observable sectors of an empathy map for one person.
