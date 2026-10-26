# Theory of Inventive Problem Solving (TRIZ)

## Essence

TRIZ (theory of inventive problem solving) is an approach to hard problems in which a strong solution is sought not by enumerating options but through a contradiction. A problem becomes hard when improving one property worsens another: faster means riskier, more powerful means more expensive. A compromise leaves both sides worse off than one would like. TRIZ proposes to state the contradiction explicitly and resolve it: separate the requirements in time, in space or by conditions, using the resources that already exist in the system.

## When to use and when not to

Use it when obvious solutions run into an either-or and the team is choosing what to sacrifice: speed or safety, convenience or control, capacity or cost. It suits products, interfaces, processes and services, not only engineering.

Do not use it when the problem is not formulated, or when the solution is already known and is held back only by resources. For a simple expansion of a list of ideas, a free discussion is enough.

Inputs: a description of the system and its elements, what must be improved, what gets worse as a result, which resources are available (data, time, place, participants).

Limitations:

- **The method requires training.** Formulating contradictions and selecting techniques are learned on dozens of problems.
- **Techniques are hints, not answers.** They point the direction; the solution still has to be devised and checked.
- **The classical apparatus was created for engineering.** For services, some techniques have to be translated.

## Scheme

| Step | What is recorded |
|---|---|
| **Contradiction** | the element that must be A for the benefit X and not-A for the benefit Y |
| **Ideal final result (IFR)** | the element itself provides both X and Y, without harm and without cost |
| **Resources** | what already exists in the system and around it: time, place, information, substances, fields |
| **Resolution** | separation of requirements in time, in space, by conditions; one of the 40 techniques (for example "preliminary action", "fragmentation", "asymmetry") |
| **Solution and check** | what was changed and how the result was checked |

## How to apply

1. **Describe the problem** in one phrase and the elements of the system.
2. **Find the contradiction:** what we improve and what gets worse at the same time; formulate what the element must be and for what purpose, and what it must be the opposite of.
3. **Formulate the IFR:** what it would be like if the element itself provided both benefits.
4. **List the resources**, especially free ones: what is already happening or known.
5. **Separate the requirements:** when, where or under which conditions A is needed, and when not-A. Pick a technique.
6. **Describe the solution and check** it on real data.

## Example

Monzo, a British digital bank, in 2019 launched Get Paid Early — payment of salary a day early. The team did not use TRIZ; below, its solutions described in the bank's blog are laid out by the method's steps.

| Step | Salary paid early | Platform load |
|---|---|---|
| **Contradiction** | the money must reach the customer earlier — for convenience; and must not — until the bank is sure it will arrive | capacity must be high — a wave of requests arrives exactly at 16:00, traffic can grow by more than 500% within seconds, and autoscaling reacts too slowly; and low — for cost and energy the rest of the time |
| **IFR** | the customer gets the money early, and the bank takes no risk | capacity exists exactly when it is needed |
| **Resources** | by 16:00 the day before, the bank sees an incoming payment in the Bacs payment system and is sure it will arrive | the number of payments for the next day is known in advance; there is history of server load on past paydays and traces that show every service involved in a request |
| **Resolution** | separation in time: before 16:00 the day before — no, after — yes | separation in time and the "preliminary action" technique: increase capacity before the peak and scale back after it |
| **Solution** | from 16:00 the day before, the customer can request the money in the app | an automatic plan: based on a day with a similar number of payments, determine which services to scale up and by how much; increase around noon, scale back after the peak |

Result: on the largest payday up to that point, before Christmas, more than 260,000 customers received their pay early, totalling £210 million; the platform was not overloaded, and its costs, according to the author, fell sharply.

Sources of the case: Monzo blog — [launch of the feature](https://monzo.com/blog/2019/08/20/monzo-now-lets-you-get-paid-a-day-early-for-free) (Jarno Wolf, 21 August 2019) and [platform preparation](https://monzo.com/blog/2023/01/26/preparing-for-spikes-in-traffic-as-millions-get-paid-early) (Joe Rowe, 27 January 2023).

## Common mistakes

- **A compromise instead of a resolution.** A "middle" value is chosen, and both sides suffer.
- **The contradiction is not formulated.** Techniques are enumerated right away and a set of random ideas results.
- **Resources forgotten.** The solution requires new costs, although what is needed already exists in the system.
- **A solution without a check.** A neat idea is not checked against data.

## Source

Genrich Altshuller and Rafael Shapiro, ["On the psychology of inventive creativity"](http://www.altshuller.ru/triz/triz0.asp), Voprosy Psikhologii, 1956, No. 6; Genrich Altshuller, ["Algorithm of invention"](https://fantlab.ru/edition80362) (Moskovsky Rabochiy, 1969) — techniques for eliminating technical contradictions.

## See also

- Alternative to SCAMPER Method: Use SCAMPER for many quick change ideas on an object, not resolving contradictions.
- Followed by A/B Testing: After a TRIZ solution is described, check it on real users with a controlled comparison.
