# Jobs-to-be-Done

## Essence

Jobs-to-be-Done (the customer's job) is a view of a product in which the customer does not "belong to a segment" but "hires" a product to make progress in a specific situation. Clayton Christensen defined a job as the progress a person wants to make in certain circumstances. If a product fails at the job, it is "fired" and another is hired — sometimes not a competitor, but a workaround: a trip to a branch, a spreadsheet, a call to a friend.

A job is written in the job story format:

> **When** <situation>, **I want to** <what to do>, **so that** <what result to get>.

The key to the format is the situation. Not "a mother of two children wants to see the balance", but "when I am standing at the checkout in a store". The situation explains why it must be quick, what gets in the way, and how the result is measured.

## When to use and when not to

Use it when you need to understand why customers come to the product and what they do instead of it. When the product is overloaded with features and simple actions are hard to perform. When the team describes users by age and income and no decisions follow from it.

Do not use it for minor interface tweaks where the job is obvious. It is not a substitute for research: jobs invented by the team look convincing and are almost always wrong.

Limitations:

- **The format does not replace a conversation.** Job stories are written from interviews about recent real cases, not from a survey of "what do you need".
- **Many jobs, few resources.** The format does not say which job to close first; frequency and importance of a job are assessed separately.
- **One job — one situation.** A general wording like "manage finances" does not suggest a single decision.

## Scheme

```
┌────────────────────────────────────────────────┐
│ WHEN      I am at the checkout in a store      │  situation
│ I WANT    to quickly check how much money I have│  action
│ SO THAT   I am sure there is enough for shopping│  outcome
├────────────────────────────────────────────────┤
│ WHAT WE DID  balance is visible right after login│  solution
└────────────────────────────────────────────────┘
```

## How to apply

1. **Choose customers** who recently hired or fired the product: started using it, left it, or went around it.
2. **Conduct interviews** about a specific recent case: where the person was, what happened, what they tried, what stopped them.
3. **Write the job stories:** when, I want to, so that. One situation — one story, without product feature names.
4. **Group similar jobs** and assess how often they occur and how badly they are solved now.
5. **For the main jobs, design a solution** and write it next to the story.
6. **Check the result on behaviour:** how many people do this in the product instead of the workaround.

## Example

The Bank of Jordan app was overloaded with features. Clients could not quickly check their balance, went to a branch to pay bills, and the app's Google Play rating was 2.8. The bank, together with the design agency UXDA, redesigned the app. The agency described typical clients, among them a mother of two who combines work and family, and for each, applied the Jobs-to-be-Done method to build scenarios. Three of the published ones (the wording is shortened by a few words; the source shows them as an image):

| When | I want to | So that |
|---|---|---|
| shopping in the grocery store | quickly check how much money I have available | I can be sure I have enough to pay for everything I want to buy |
| managing household bills | know which bill payments, with what amount, I still have unpaid this month | I can immediately handle them |
| my daughter calls because I have forgotten to give her money for her piano lessons | quickly transfer money to her | she doesn't have to miss the lesson |

Decisions the bank and the agency made together: make the balance quick to reach, since users have no patience to search the app; give transfers to a recipient the client has already added a new path of a few taps.

Result, according to the agency: over six months, the Google Play rating rose from 2.8 to 4.7; the article says the App Store rating also reached 4.7 and has held.

Caveats: the result was published by the agency itself; the relaunch date is not given in the article. What decision was taken on bill payments is not described. The rise in rating is the outcome of the whole redesign, not of the job stories alone.

Source of the case: UXDA, [«Bank of Jordan UX Case Study: Middle East Banking Redesign of Mobile UX»](https://theuxda.com/blog/mobile-banking-ux-case-study-hated-loved).

## Common mistakes

- **Writing the job through a feature.** "I want a transfer button" is a solution, not a job; the job is to transfer money to a daughter before the lesson.
- **Losing the situation.** Without "when", the story turns into a wish and does not indicate what matters: speed, accuracy or calm.
- **Inventing jobs in a meeting room.** Stories without interviews repeat the team's ideas.
- **Wording too broadly.** "Manage money" is not a job, it is an area.
- **Not checking the solution.** A story is closed when the feature is released, not when people stop going around.

## Source

C. M. Christensen, T. Hall, K. Dillon, D. S. Duncan, [«Know Your Customers' "Jobs to Be Done"»](https://hbr.org/2016/09/know-your-customers-jobs-to-be-done), Harvard Business Review, 2016. The job story format was proposed by A. Klement in a [2013 article](https://medium.com/the-job-to-be-done/replacing-the-user-story-with-the-job-story-af7cdee10c27) in the Jobs to be Done publication on Medium.

## See also

- Preceded by JTBD Interview: Collect recent-case stories with the switch interview, then write job stories from its log.
- Enhanced by Forces of Progress: Use the forces to explain why a job stays unsolved beside its job story.
- Followed by Value Proposition Canvas: Match pains and gains of each main job with the product offer.
