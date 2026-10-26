# Single-feature Prototype (Concierge MVP, Wizard of Oz, Third-party product)

## Essence

A way to test a solution hypothesis: build a prototype of one function that covers one customer need, and see whether that need is solved. According to PAF (Product Architecture Framework, Sergey Tikhomirov), the focus is on the fact of the solution, not on the quality of the interface. Three approaches: "Concierge" (manual labour instead of automation; open to the customer — the card author's conclusion), "Wizard of Oz" (manual labour is hidden, the customer believes a program is working), "Third-party product" (part of the function is provided by a ready service, an API or a platform). MVP — minimum viable product.

## When to use and when not to

Use when it is unclear whether a solution will solve the need, and automation is expensive. Needed: a need, a function, participants, a success criterion, a person for the manual work.

According to PAF, the approach is chosen by conditions:

- **Concierge:** customers are online and not well versed in technology; logistics are hard to predict; growth of operating costs requires large investment; the result depends on the satisfaction of each customer.
- **Wizard of Oz:** the end product requires complex algorithms; the field is sensitive (finance, healthcare, dating, law); a two-sided market.
- **Third-party product:** the market is occupied by mature companies; logistics are hard to predict; there are few engineers.

Limitations:

- **A human is more flexible than an algorithm** (card author's conclusion): the quality of automation may be lower.
- **Wizard of Oz hides the human.** Kelley (1984) calls this "low-level deception"; NN/g (2024): participants may guess that there is a person. Whether to disclose the person after the session should be decided by the possible harm (card author's recommendation).
- **Savoia (2011)** calls a hidden human instead of a machine "Mechanical Turk"; an example is a hidden typist in IBM's speech recognition experiment.

## Scheme

```
Need → Hypothesis → Approach → Run → Criterion → Decision
Approach: Concierge (manual labour) | Oz (manual labour hidden) | Third-party (ready service)
Log: what the person did, how many minutes, where they made mistakes
```

## How to apply

1. **Write the hypothesis by the PAF template:** "If I, as <role>, am given <solution>, then this will allow me to achieve <result>, which will confirm <success criterion>, because <reasoning>".
2. **Set the threshold before launch.** The sources give no number; three zones — automate, change, stop (card author's recommendation).
3. **Choose the approach** by the conditions above.
4. **Prepare the run.** For Wizard of Oz according to NN/g: a protocol, a set of answers, a rehearsal of the "wizard", a trial run with a colleague or a real user. For Concierge: a meeting script. For a Third-party product: a list of services.
5. **Add customers one at a time,** as Rosso's team did; write code only for what has become too long to do by hand.
6. **Keep a log of manual actions** (card author's recommendation): time and errors will show what to automate first.
7. **Decide by the threshold:** met — automate the most time-consuming task; not met — change the solution, not the interface.

## Example

Food on the Table (USA): selection of family menus and a shopping list. Grocery retail, not e-commerce and not fintech. Manuel Rosso told the case at the Startup Lessons Learned conference on 23.04.2010 and in the talk "Food on the Table (Concierge MVP)" (undated).

Hypothesis: not in the source (slide 11, Customer Discovery: "No defined hypothesis", 150+ conversations, 20 group discussions). How it was done: a concierge service for one selected participant, then customers were added one at a time; there were 20 first users. The first meeting was in person, the second by phone; recipes and lists were sent by mail, dynamic pages were replaced with Google Apps. Term: not in the source.

Result in figures: not in the source. Rosso's criterion: move on to the next step when the reaction of early customers can be predicted. Decision: code only the tasks that have become too long to do by hand.

M. Rosso, [Food on the Table, SLLC](https://www.slideshare.net/startuplessonslearned/food-on-the-table-case-study-at-sllconf-by-manuel-rosso), 2010; M. Rosso, [«Food on the Table (Concierge MVP)»](https://www.slideshare.net/TheLeanStartup/manuel-rosso-food-on-the-table), undated.

## Common mistakes

- **Testing the interface instead of the solution of the need.** PAF: the focus is on the fact of the solution.
- **Approach chosen against the conditions:** Wizard of Oz where the customer has the right to know about the person (the author's conclusion).
- **The threshold is set after the result:** any figure can be declared a success.
- **The "wizard" improvises.** NN/g: with open-ended answers, session results are hard to compare.
- **Manual actions are not recorded:** it is unclear what to automate.
- **A small group taken for scale:** 20 participants do not guarantee the quality of automation (the author's conclusion).
- **Not checking the terms of someone else's service:** limits, transfer of data to a third party (the author's conclusion).

## Source

Description in PAF (Product Architecture Framework, Sergey Tikhomirov, [productframework.ru](https://productframework.ru/hypotheses/solution), CC BY-SA 4.0, undated). J. F. Kelley, [«An Iterative Design Methodology for User-Friendly Natural Language Office Information Applications»](https://student.cs.uwaterloo.ca/~cs449/s17/p26-kelley.pdf), ACM Transactions on Office Information Systems 2(1), March 1984; the author's term "OZ paradigm". S. Paul, M. Rosala, [«The Wizard of Oz Method in UX»](https://www.nngroup.com/articles/wizard-of-oz/), Nielsen Norman Group, 19.04.2024. A. Savoia, [«Pretotype It»](http://www.pretotyping.org/uploads/1/4/0/9/14099067/pretotype_it_2nd_pretotype_edition-2.pdf), 2nd ed., 2011.

## See also

- Enhanced by Prototyping Process: Use a clickable or paper prototype to check people understand the function first.
- Alternative to Minimum Viable Product: Its manual fulfilment behind a ready-made interface cheaply tests the main assumption.
- Followed by Pilot Project / Sample: Once one function proves the need, run the trial with real clients.
