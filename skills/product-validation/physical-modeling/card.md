# Physical Modeling

## Essence

Physical modeling is a way to test a solution hypothesis on a physical model of a product or environment, without developing the solution in full. The model is made with dimensions and properties as close to reality as possible, with props if needed. Scenarios and success criteria are prepared in advance, the scenarios are run on the model, measured, fixes are made immediately and the runs are repeated. This is how the PAF method (Product Architecture Framework, the framework of Sergey Tikhomirov) describes it.

## When to use and when not to

Use for solutions in space or in hand: a bank branch, a pick-up point, a warehouse, a checkout, a terminal, packaging. Needed: a hypothesis, dimensions, scenarios, criteria, props, participants.

Limitations according to PAF:

- **The cost grows with complexity.** The more complex the physical product, the more expensive the model and the longer the feedback cycle.
- **Scenarios must cover the subject area.** Composing such scenarios is a separate competence.

The card author's conclusion: the model shows convenience in the given scenarios, but not demand or behavior over months.

## Scheme

| Scenario | Criterion (before the run) | Run 1 | Fix | Run 2 |
|---|---|---|---|---|
| Participant situation | Threshold | Measured | What we changed | Measured |

Above the table: hypothesis, model, participants, term. Below it: decision.

## How to apply

1. **Formulate the hypothesis** and single out what is physical in it: dimensions, placement, shape, a person's path.
2. **Compose scenarios** so that they fully cover the subject area (PAF); include rare situations (card author). For each one, write the success criterion before the run; examples (card author): operation time, number of errors.
3. **Make the model** as close to reality as possible: dimensions, properties, props (PAF). Material according to budget: cardboard, 3D printing, a marked-out room (examples from the card author).
4. **Run the scenarios** and measure effectiveness (PAF); participants are future users and staff (card author).
5. **Make fixes immediately** and run the scenarios again (PAF).
6. **Make the decision** (card author's recommendation). Criteria met in all scenarios — move to development. Not met after fixes — rethink the solution.

## Example

The bank Intesa Sanpaolo and the agency frog, 2014–2015: a new branch model.

- **Hypothesis.** Not formulated in the source; the card author's conclusion: the new model is understandable to customers and staff.
- **What was done.** In November 2014, over eight weeks, a service design strategy was developed; also 60+ hours of interviews with customers and staff and 70 hours of joint workshops (when exactly is not given in the source). In March 2015 — five weeks of trials and quick iterations in a full-size branch model; 600+ customers and 300+ staff took part; the design was refined along the way.
- **Result.** No figures. frog: clear navigation and communication design "proved a key role" in building trust between the bank and customers; the fixes are not named.
- **Criterion.** Not named in the source.
- **Decision.** In June 2015 the new design was launched for the public. The link to the trials is not named in the source.

Discrepancy between sources. frog: 50 branches launched in 2015, another 1,000 planned for 2016. The bank (27.10.2015): by the end of the year it would fully update 50 medium and large branches, with a goal of about 1,000 without a deadline; after three pilot branches (Milan, Rome, Turin). The release does not mention frog; that it is the same program follows from the context.

What is missing: the hypothesis, criteria, model material, scenarios, result figures. The frog page is agency material, undated.

Sources: [frog](https://www.frog.co/work/reinventing-the-banking-experience-branch-design-intesa-san-paolo); [bank press release](https://group.intesasanpaolo.com/en/newsroom/press-releases/2015/10/CNT-05-00000002CFBC0).

## Common mistakes

- **Criteria are set after the run.** The threshold is fitted to what was seen. PAF: prepare in advance.
- **The model is far from reality.** Wrong dimensions and height — the conclusion does not transfer to the product (PAF requires closeness to reality).
- **Scenarios do not cover the subject area.** Typical cases were checked, but a queue, an error, a non-standard customer were not.
- **Fixes are not re-run.** It is unknown whether the fix helped.
- **Wrong participants.** Card author's conclusion: one's own team knows the idea and prompts itself.
- **Usability is taken for demand.** Card author's conclusion: a successful run does not prove that customers will pay.
- **Modeling everything at once.** A complex product as a whole makes the model expensive and lengthens the cycle (PAF); take a testable part (card author's advice).

## Source

Description in PAF (Sergey Tikhomirov, [productframework.ru](https://productframework.ru/hypotheses/solution), CC BY-SA 4.0, undated): the section "Physical Modeling" on solution hypotheses; there are no examples there. PAF does not name the author of the method or the year.

Case: frog page (undated) and Intesa Sanpaolo press release of 27.10.2015, links in "Example".

## See also

- Alternative to Prototyping Process: For a digital solution, test a clickable prototype instead of a physical model.
- Preceded by User Flow: Map user steps first, then turn them into scenarios run on the model.
- Followed by Pilot Project / Sample: Once the model meets all criteria, hand a trial solution to real users.
