# Service Blueprint

## Essence

A service blueprint is a diagram of one service scenario: under each customer step you can see what employees, systems and partners do at that moment, both visible and invisible to the customer. The method was proposed by Lynn Shostack, senior vice president at Bankers Trust, formerly Citibank, in Harvard Business Review in 1984, to manage the service process and find failure points in advance. The classic five-layer form was described by Mary Jo Bitner, Amy Ostrom and Felicia Morgan (2008).

## When to use and when not to

Use it when a service relies on several departments and systems and complaints repeat for a hidden reason, or when a new service has to be designed and handed over to teams.

Do not use it for a single screen or a simple action without a backstage: the diagram will restate the obvious.

Limits:

- **One scenario — one diagram.** Nielsen Norman Group recommends a small or medium scope: up to five touchpoints.
- **Research is needed.** How work should go rarely matches how it actually goes. The backstage — work hidden from the customer — is learned by observing employees, not from regulations.
- **The diagram has to be maintained.** GOV.UK warns that updating takes time, which must be built into the team's work.

## Scheme

```
                 Step 1       Step 2       Step 3
Evidence         screen       email        …
Customer         ●──────────→ ●──────────→ ●
- - - - - - - - - interaction line - - - - - -
Frontstage       agent        …
- - - - - - - - - visibility line - - - - - - -
Backstage        check        …
- - - - - - - - - internal interaction line
Support          customer base, warehouse, bank
Failures & time  ⚠ waits 2 days ⏱ 5 min
```

Layers from top to bottom: evidence — what the customer sees and holds; customer actions — the frame of the diagram; frontstage — actions of employees and systems in full view of the customer; backstage — hidden actions; support — systems, data, other departments, partners. Where the interaction line is crossed is the "moment of truth", the customer's direct contact with the service. Everything above the visibility line is visible to the customer.

## How to apply

1. **Choose one scenario and one customer,** decide whether you are drawing the current or the future state. Formulate the goal: remove duplication, reduce waiting.
2. **Gather the data:** at least two methods with direct observation of employees, plus support requests and interviews.
3. **Write the customer's actions** in order — this is the frame.
4. **Add the frontstage, backstage and support** under each step. Indicate who owns the step.
5. **Draw the links** between the layers and the lines.
6. **Mark failure points, time and metrics:** where the customer waits, where errors happen, what it costs.
7. **Add the evidence** — it is placed last.
8. **Decide:** which failures to fix first — by frequency and severity — what the future diagram will be, who is responsible for what.

Draw the diagram with a team from different departments; record the disagreements.

## Example

Airbnb, a marketplace for travel accommodation, in spring 2023 rebuilt its core service for guests and hosts.

| Stage | What was done |
|---|---|
| Blueprint | storyboarded the guest's and host's path from registration to check-out; mapped about 150 app and website screens, 72 user policies (per the Q1 2023 shareholder letter), every customer-support interaction |
| Failures | millions of support requests were broken down by the blueprint's steps, thousands of social media posts were added |
| Decision | chose the most frequent and severe problems and went through the list |
| Changes | over 50 new features and upgrades: check-out instructions are visible before booking, 24/7 support during the trip, with the aim of answering 90% of calls in English within two minutes |

What the case lacks: the diagram itself — its layers and lines are not shown. The result is not directly tied to the diagram: host cancellations fell by 36% (Q4 2023 vs. 2022), but this is the outcome of more than 430 new features and upgrades over three years.

Case source: [Airbnb Newsroom](https://news.airbnb.com/en-au/airbnb-2023-may-release-introducing-airbnb-rooms), 03.05.2023; Airbnb, shareholder letters for [Q1](https://s26.q4cdn.com/656283129/files/doc_financials/2023/q1/Airbnb_Q1-2023-Shareholder-Letter_Final.pdf) and [Q4](https://s26.q4cdn.com/656283129/files/doc_financials/2023/q4/Airbnb_Q4-2023-Shareholder-Letter_Final.pdf) 2023.

## Common mistakes

- **Invented backstage.** The diagram is drawn from assumptions, without observing employees.
- **Lost the customer.** Bitner: participants get absorbed in internal steps and forget the customer.
- **Several services on one diagram.** Complexity is mistaken for accuracy.
- **No lines.** Without the visibility line it is not clear what the customer notices.
- **No failures or time.** The diagram describes the process but does not show where it breaks.
- **Current and future state mixed together.**
- **Drawn and forgotten.** The diagram is not updated, and it stops describing the service.

## Source

G. L. Shostack, [“Designing Services That Deliver”](https://hbr.org/1984/01/designing-services-that-deliver), HBR, 1984 (the essence is taken from Bitner); M. J. Bitner, A. L. Ostrom, F. N. Morgan, [“Service Blueprinting: A Practical Technique for Service Innovation”](https://doi.org/10.2307/41166446), California Management Review, 50(3), 2008; S. Gibbons, [“Service Blueprints: Definition”](https://www.nngroup.com/articles/service-blueprints-definition/), 2017, and [“The 5 Steps to Service Blueprinting”](https://www.nngroup.com/articles/5-steps-service-blueprinting/), 2018; A. Kendrick, [“Service Blueprints: How to Choose What Experience to Visualize”](https://www.nngroup.com/articles/service-blueprints-choose-what-experience/), 2021; L. Nilsson, [“5 benefits of making blueprints”](https://services.blog.gov.uk/2021/03/17/5-benefits-of-making-blueprints-when-you-build-or-improve-a-service/), GOV.UK, 2021; M. Stickdorn, [“Service blueprint”](https://www.smaply.com/blog/service-blueprint), Smaply (blog of a service-diagramming tool developer), 2026.

## See also

- Preceded by Customer Journey Map: Take its steps as the frame, then add frontstage and backstage under each.
- Enhanced by Sequence Diagrams: Detail the system layer as a sequence diagram of messages between services.
- Alternative to Value Chain & Nets: The value chain suits physical products; this lays out services step by step.
