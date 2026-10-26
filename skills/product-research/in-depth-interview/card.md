# In-Depth Interview

## Essence

An in-depth interview (in startups — CustDev, from Customer Development) is a one-on-one conversation following a prepared script: the interviewer asks questions and clarifies the answers in order to understand the person's context — what they do, why they make decisions, what they see as a problem and where they see value. The method tests qualitative hypotheses (assumptions about the customer).

## When to use and when not to

Use it when little is known about the customer, or when metrics show what the customer does but not why. Inputs: a hypothesis or goal, respondents.

Do not use it:

- **For shares and numbers.** PAF (Product Architecture Framework): does not assess behaviour quantitatively.
- **For choosing among options.** Nielsen: you cannot learn the colour of a button from an interview.
- **To learn what people actually do.** NN/g (Nielsen Norman Group): an interview gives reported behaviour, which is affected by memory and the wish to look good.

A nuance: if the interviewer describes their own idea, the respondent goes along with it (Fitzpatrick). PAF: an interview lasts 30 minutes to 1.5 hours and requires a prepared interviewer.

## Scheme

```
Goal + hypothesis → Guide: 3–5 themes
  theme → "Tell me about the last time when…"
       → clarifications: when, how much time and money, what next
       → "Tell me more"
Record: fact │ quote │ signal │ data type
Series → repetitions → hypothesis: yes / no / unclear
```

## How to apply

1. **Set the goal and the hypothesis** in the form "<role> does X because Y". The goal is not "learn about users" (NN/g).
2. **Select respondents** of one segment; record roles separately. Stop when nothing new appears (author's recommendation).
3. **Build the guide:** for each theme, one open question about a concrete past case and clarifications ("When was that?", "How long did it take?"). NN/g.
4. **Run a pilot** with a colleague: fix unclear questions (Rosala and Pernice, NN/g, 2023).
5. **Conduct the interview.** Fitzpatrick's rules: talk about the person's life, not your idea; ask about a concrete past; listen more. Explore a strong emotion or a request for a feature with the question "why".
6. **Record in a table:** the fact, the verbatim quote, the signal (time or money spent, emotion), the data type: fact from the past, opinion or intention, idea or request, compliment. The types are the author's adaptation; Fitzpatrick names bad data as compliments, fluff and ideas.
7. **Consolidate the series.** A hypothesis holds if several respondents independently described one behaviour with concrete cases; opinions and compliments alone do not support it. The result is a hypothesis for a numeric check or a decision on the next step, not a conclusion about the market (author's recommendation).

## Example

The A3 payment service (regular payments) wanted to understand whether its "Supplier's personal account" was needed by other industries. Interviews were held with 24 respondents: an online foreign language school, foundations, accommodation booking, travel agencies, kindergartens, online shops, and online psychotherapy.

According to the source, the guide themes were: the way of accepting payments; payment acceptance partners and why; additional functionality (instalment payments, payment hold, SBP (Faster Payments System), SberPay); related services.

Five insights from the source: some companies are considering instalment payments, but the commission holds them back; for BNPL (buy now, pay later), the high rate is a barrier; the payment process needs to be optimised, including the collection of information; integrating acquiring (card acceptance) with CRM (customer management system) slows down processes; cross-border payments are relevant. The roles (owners, product managers, accountants, sellers) have similar needs, with different emphases.

Decisions by A3's own account: take roles into account in positioning; products around acquiring are a promising development direction; the company is ready to expand its products into other niches; offer a payment widget to those who gave up acquiring.

The guide themes, conclusions and decisions are visible; there is no log of answers: no answers by respondent, no quotes, no question wording, no results of decisions. This is the company's own account; online shops are one of the groups.

Source: A3, [«Why conduct CustDev and how to get insights?»](https://vc.ru/id2003272/1698926-zachem-provodit-custdev-i-kak-poluchit-insaity), vc.ru, 10.12.2024.

## Common mistakes

- **Telling the idea and asking "would you buy it?".** Instead of data you get compliments and promises (Fitzpatrick).
- **Asking for an opinion and a forecast instead of a case.** Nielsen: only what a person does now is reliable.
- **Taking a feature request for a need.** Nielsen: most of the "new" features requested for Office 2007 were already in Office 2003.
- **Pressing and prompting.** Nielsen: asked a question, a person will come up with an opinion on anything (query effect).
- **Drawing shares from dozens of interviews.** PAF: the method does not give a quantitative estimate.
- **Mixing roles into one summary.** In the A3 case, the emphases of the roles differ.
- **Not checking against real behaviour.** Compare the stories with product statistics.

## Source

Rob Fitzpatrick, the book «The Mom Test» (2013): [momtestbook.com](https://www.momtestbook.com/). Jakob Nielsen, [«Interviewing Users»](https://www.nngroup.com/articles/interviewing-users/), NN/g, 25.07.2010. Maria Rosala, Kara Pernice, [«User Interviews 101»](https://www.nngroup.com/articles/user-interviews/), NN/g, 17.09.2023.

Description in PAF (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, no date): [Customer Hypotheses](https://productframework.ru/hypotheses/customer). "Author's recommendation" is a conclusion that is not in the sources.

## See also

- Preceded by Awesome Problem Interview Script: Prepare the script first, then run each conversation as an in-depth interview.
- Alternative to JTBD Interview: Use the switch interview when asking why recent buyers chose or switched.
- Followed by Customer Survey: Once interviews show a hypothesis, measure how many customers share it with a survey.
- Followed by Maxwell USP Formula: Use the objections the interviews reveal as the third part of the Maxwell phrase.
- Followed by Buyer Persona: Sort the answers into the persona's blocks, which describe how the buyer decides.
- Enhanced by Diary Study: Use the closing interview to clarify unclear diary entries and the reasons behind them.
- Alternative to Expert Interview: Choose consumer interviews over expert ones when the question is about consumers' own behaviour.
- Enhanced by Field Research: Ask about the reasons behind the actions the observer saw, which observation alone cannot show.
- Enhanced by Empathy Map: Keep the canvas in view so its sectors show what to ask and look for.
