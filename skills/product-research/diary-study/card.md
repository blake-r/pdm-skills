# Diary Study

## Essence

A diary study is a method in which participants themselves record their actions, thoughts and emotions at the moment of an event, over several days or weeks. The researcher sees behaviour over time, not a retelling. According to the description in PAF (Product Architecture Framework, a catalogue of product methods), the diary captures an action, a thought or an emotion in the context of the study.

## When to use and when not to

Use it when behaviour is spread over time or hidden from the researcher: habits, a change of attitude towards a product, the purchase path across different channels (NN/g, Nielsen Norman Group). Inputs: a question, participants, a period, a medium.

Do not use it:

- **For shares and numbers.** PAF: the method does not assess behaviour quantitatively; in NN/g, groups range from 5–12 to 30–50 people.
- **If it must be fast and cheap, or participants are not ready to keep records.** PAF: the method is burdensome for both sides and requires high responsibility from participants; participants drop out more often than in usability tests (NN/g).

A nuance: an example entry in the instruction pushes participants towards entries of the same kind (NN/g). Participants were reluctant to report income (Lewis and Perry).

## Scheme

```
Question → participants and period → entry type (event / interval / signal)
  → entries: what was done │ what was thought, felt
  → reading the entries as the study goes
  → closing interview over the diary
  → conclusion (marked) → decision and check
```

## How to apply

1. **Formulate the question and the period.** The period depends on how often the behaviour occurs (in NN/g examples, 1–3 weeks; Czerwinski and co-authors, 2004, one week).
2. **Choose the entry type** (NN/g): by event, by interval or by a reminder signal; they can be combined.
3. **Choose the medium:** text, table, messenger, photo, audio. It affects what and how people record (Carter, Mankoff, 2005); let the participant choose.
4. **Define the entry fields:** time, action, place, thought, emotion.
5. **Recruit participants with a reserve for dropout** (NN/g): 5–12 for a homogeneous group, 12–30 for a heterogeneous one; for a period longer than a week, pay in instalments.
6. **Run a pilot,** read the entries as they arrive and clarify them while the event is still fresh.
7. **Hold a closing interview** with the diary in front of both of you: clarify what is unclear and the reasons.
8. **Analyse:** separate fact from conclusion, note repetitions, decide what to change and how to check it (recommendation of the card's author).

## Example

Makayla Lewis and Mark Perry (Brunel University London) studied personal finance: 12 people from England kept a ten-day diary of all money transactions (May — July 2018): date, time, amount, place, payment method, feelings. Participants chose the medium themselves: table, document, WhatsApp. After the diary came an interview (on average 90 minutes) over a printout of the entries.

367 transactions were recorded (30.58 per person): expenses 70.7% (£15,239.24), income 29.3% (£6,326.35, probably understated). The most frequent payment was by contactless debit card (164), followed by cash (80). One source; 367 / 12 = 30.58. The shares describe only this sample and are not transferred to the market.

| Entry | Conclusion | Decision (authors' proposal) |
|---|---|---|
| May turned on bank app notifications; in the interview: statement — "a huge amount… makes me confused", switched from a stream of notifications to a daily summary | Digital payments made money intangible; people are less aware of their spending | A panel with a structured history of transactions, not a stream of notifications |
| Liam and Charlotte enter payments manually into a shared household spreadsheet: bank data is not imported | Shared spending requires manual work: bank data cannot be imported | A shared payment system with adjustable access |

What the case does not have: a company decision and the result of implementation; this is an academic work with proposals, and the example is not carried through to a decision.

Case: Lewis, Perry, [«Follow the Money: Managing Personal Finance Digitally»](https://doi.org/10.1145/3290605.3300620), CHI 2019 (ACM conference on Human Factors in Computing Systems).

## Common mistakes

- **Expecting numbers.** Entries from 12 people do not give shares.
- **An unrealistic minimum of entries, or uncapped extra payment for surplus entries.** A minimum should be realistic, and extra payment for surplus entries needs a cap (NN/g).
- **Hinting with example entries.** They bias participants towards entries of that kind (NN/g).
- **Reading entries only at the end.** Clarification is possible only while the event is fresh.
- **Skipping the closing interview.** Without explanations, the entries are ambiguous.
- **Taking a participant's words as fact.** "Notifications overload me" is the words of one participant, not a pattern.
- **Ignoring the effect of the diary.** Charlotte: "it has made me realise how transactions can stack up quickly"; keeping the record changes attention to spending (conclusion of the card's author).

## Source

Kim Flaherty, [«Diary Studies: Understanding Long-Term User Behavior and Experiences»](https://www.nngroup.com/articles/diary-studies/), Nielsen Norman Group, page date — 29.03.2024. Scott Carter, Jennifer Mankoff, «When Participants Do the Capturing: The Role of Media in Diary Studies», CHI 2005, pp. 899–908, [doi](https://doi.org/10.1145/1054972.1055098). Mary Czerwinski, Eric Horvitz, Susan Wilhite, [«A Diary Study of Task Switching and Interruptions»](https://erichorvitz.com/taskdiary.htm), CHI 2004 (one-week diary). Description in PAF (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, no date).

## See also

- Alternative to Field Research: Use observation for behaviour a few visits show; a diary suits behaviour over weeks.
- Enhanced by In-Depth Interview: Hold a closing interview to clarify unclear entries and the reasons behind them.
- Followed by Empathy Map: After reading the entries, fill an empathy map of thoughts and feelings they recorded.
