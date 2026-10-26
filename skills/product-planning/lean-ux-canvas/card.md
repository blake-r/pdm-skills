# Lean UX Canvas

## Essence

The Lean UX Canvas is a sheet of eight numbered blocks that turns the task "build such-and-such feature" into a business problem, testable hypotheses and a first experiment. The blocks are filled in order: the business problem, how we will measure it, what counts as solved, for which users, what they will get, which solutions are possible. From this the hypotheses are assembled using the author's formula, the riskiest assumption is chosen, and a minimal experiment is designed to test it. Everything on the sheet is an assumption until confirmed; that is why the header has an "Iteration" field: the sheet is refilled after every experiment.

## When to use and when not to

Use it at the start of an initiative, when a team has been handed a ready-made solution or a vague goal; when you need to agree what to test first; in every work cycle — to check what has changed after an experiment.

Do not use it when a solution is already confirmed by data and only needs to be built, or when the task is fixing a bug. The sheet does not estimate effort and does not replace a work plan.

Limitations:

- **Everything rests on boxes 1 and 2.** Without a problem and a measurable result, the hypotheses have nothing to be compared against.
- **One hypothesis — one feature.** The author asks not to mix them: otherwise the experiment will not show what worked.
- **The riskiest assumption is chosen by value,** not by implementation complexity: at an early stage, what matters more is whether people need it.

## Scheme

| Box | Question |
|---|---|
| **1. Business problem** | which business problem we are solving; what has changed in the market, among competitors, in customer behaviour |
| **2. Business outcomes** | how we will know we have solved it; what people will do differently, which metrics |
| **3. Users** | which users and customers we look at first |
| **4. User outcomes and benefits** | why they need the product, what they will get, which change in behaviour will show that the goal is reached |
| **5. Solutions** | what we can do for the business and the users at the same time |
| **6. Hypotheses** | "We believe that [business outcome] will be achieved if [user] gets [benefit] with [feature]" |
| **7. Most important thing we need to learn first** | the riskiest assumption: if it is wrong, the whole idea collapses |
| **8. Least amount of work needed to learn the next most important thing** | the experiment that will most quickly show whether the assumption is correct |

On the sheet, boxes 1 and 3 are on the left, 2 and 4 on the right, 5 is in the centre across two rows, and 6–8 are in the bottom row.

## How to apply

1. **Assemble the team** — product, design, development — and fill in boxes 1–4 together.
2. **Write the solutions** in box 5, without yet choosing the best one.
3. **Assemble the hypotheses** using the formula from boxes 2–5: one per feature.
4. **Choose the riskiest assumption** in the most important hypothesis.
5. **Design the minimal experiment:** what to do, on whom, for how long, and which result will confirm or refute the assumption.
6. **Run the experiment and refill the sheet** with the next iteration number.

## Example

Etsy, a marketplace for handmade goods, tested whether to change the order of steps when creating a listing. Etsy did not use this sheet; below, its description of the experiment is laid out by box.

| Box | Etsy |
|---|---|
| **1. Business problem** | not named in the source; Etsy's experiments check that a change will help sales and traffic or simplify the tools |
| **2. Business outcomes** | sellers finish listings faster and create more of them |
| **3. Users** | sellers who create listings |
| **4. Benefits** | time saved: according to research, many sellers first upload a photo so they can check against it when writing the description |
| **5. Solutions** | make photo upload the first step |
| **6. Hypothesis** | photo as the first step will save sellers time |
| **7. Learn first** | not stated this way in the source; the experiment was built to prove that the result comes precisely from moving the photo |
| **8. Least amount of work** | several days: 25% of sellers saw the photo step at the top of the page, 25% at the bottom, and 50% in the middle, as before |

Decision: the change that would affect all sellers was first tested on part of them; a control group separated the effect of moving the photo from the other factors.

Result: sellers for whom the photo was the first step finished listings faster and created more of them than in the other groups. Etsy concluded that the change would benefit most sellers. The article does not give the numbers.

Source of the case: [«Building Better Tools With Experiments»](http://web.archive.org/web/20240114225553/https://www.etsy.com/seller-handbook/article/building-better-tools-with-experiments/128628130971), Etsy seller handbook (date not given, in the archive since May 2021).

## Common mistakes

- **Starting with box 5.** The solution is written before the problem, and the sheet is fitted to it.
- **A business outcome without a metric.** "Happy customers" will not show whether the hypothesis worked.
- **The experiment tests an easy assumption.** It is checked that the feature can be built, not that it is needed.
- **The sheet is not refilled.** After an experiment the assumptions remain the same.

## Source

Jeff Gothelf, [«Lean UX Canvas v2»](https://jeffgothelf.com/blog/leanuxcanvas-v2/), the author's blog, 9 September 2019; the first version — [15 December 2016](https://jeffgothelf.com/blog/leanuxcanvas/); the hypothesis formula is given in the post [Outcomes are the success criteria for your hypotheses](https://jeffgothelf.com/blog/outcomes-are-the-success-criteria-for-your-hypotheses). The third edition of the book by Jeff Gothelf and Josh Seiden, "Lean UX", 2021, [is built around the canvas](https://jeffgothelf.com/blog/whats-new-lean-ux-book-3rd-edition/).

## See also

- Alternative to Feature Canvas: Use it when a feature idea needs fuller analysis of 15 blocks before design.
- Followed by Experiment Card: Record the box 8 experiment on a card to test the riskiest assumption.
- Preceded by Impact Mapping: Set goal and actors in an impact map, then fill the problem and user boxes.
