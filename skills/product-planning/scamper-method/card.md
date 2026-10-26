# SCAMPER Method

## Essence

SCAMPER is a list of seven questions asked about an existing product, feature or process in order to get ideas for changing it. Each letter is a separate technique: substitute, combine, adapt, modify, put to another use, eliminate, reverse. The method does not look for ideas from a blank slate; it makes you look at what exists from seven angles.

## When to use and when not to

Use it when there is a concrete object to improve (a screen, a feature, a tariff, a delivery process) and the team is stuck on the same solutions; when you need to quickly generate many options before selection; when a product is moved to a new channel or a new audience.

Do not use it when the problem is not formulated or it is not yet clear whether anything needs to change at all: the method gives options, not a diagnosis. Do not use it to choose between ready-made options.

Inputs: the object of the change, the goal (which customer or business problem we solve), known constraints, data on what does not work now.

Limitations:

- **The questions are not equally useful.** For one task three or four letters give ideas, and the rest stay empty; filling them by force is pointless.
- **The method does not select ideas.** Selection and verification are done separately, by goal and data.
- **Ideas are limited by the original object.** For a fundamentally new product the method is weak.

## Scheme

| Letter | Technique | Question for the object |
|---|---|---|
| **S** | Substitute — replace | what can be replaced: material, step, channel, performer? |
| **C** | Combine — merge | what can be combined with another feature, product, process? |
| **A** | Adapt — adjust | what can be borrowed from another product, industry or channel? |
| **M** | Modify — change | what can be increased, decreased, changed in form or properties? |
| **P** | Put to other uses — apply differently | for whom or for what else could it serve? |
| **E** | Eliminate — remove | what can be removed or simplified without losing the essentials? |
| **R** | Reverse / Rearrange — reverse, reorder | what can be swapped around or done in reverse order? |

## How to apply

1. **Describe the object and the goal** in one or two sentences: what we are changing, for whom, and which problem we are solving.
2. **Go through all seven questions** in turn; for each, several ideas without evaluation. Leave empty letters empty. Usually this is 3–6 people and 45–90 minutes; the facilitator does not let ideas be evaluated at this step.
3. **Refine the ideas:** each one is a concrete change, understandable without its author.
4. **Select** by goal, constraints and effort, naming the criterion explicitly.
5. **Test** the selected ideas on part of the customers or on a rough version of the screen, with a metric and a deadline.

## Example

T-Bank, an internet bank at tbank.ru. In November 2022, after the apps of Russian banks were removed from app stores, the bank decided to develop its web account; previously few people used it. Problems: some app functions were missing on the web, and logging in via an SMS code and password felt like an "obstacle course". The object was the web account, the goal was to give customers without the app the same experience. The team did not use SCAMPER; below, its documented decisions are laid out by the method's letters to show its form.

| Letter | The team's decision |
|---|---|
| **S** | the complicated login via SMS code and password was simplified: a PIN code login was added |
| **C** | the desktop and mobile versions began to be built together, so as not to maintain very different versions of the site |
| **A** | the mobile version was made a progressive web app (PWA) to be "as similar to the app as possible"; card details viewing was added (it was in the app but not on the web), QR code scanning, contact selection in transfers, tab bar navigation (a panel of tabs at the bottom of the screen) |
| **M** | the web account's components were moved from a grey to a white background, as in the app (a plugin helped the design system make the move) |
| **P** | no data |
| **E** | they abandoned turning the phone over to hide balances |
| **R** | no data |

Decision: subordinate the work to the goal "the mobile web should match the app as closely as possible, while the desktop supports the system with its own specifics"; build the mobile version as a PWA, and build the desktop and mobile web together.

Result: by autumn 2024, more than 100 screens had been released in the new design, and more than 80 designers were working on the web instead of one; after the tab bar appeared, conversion into the account sections grew (figures not published). The team admits a mistake: too much time went to the desktop, which lagged behind the mobile version in traffic.

Source of the case: ["Design in a crisis: how we made mistakes but still redesigned the internet bank", Maria Safronova, T-Bank, Habr](https://habr.com/ru/companies/tbank/articles/853498/) (29 October 2024).

## Common mistakes

- **A blurred object.** The questions are asked about "the product as a whole", and the ideas come out generic.
- **Evaluation during generation.** Ideas are discarded at once, and half the letters stay empty because of criticism rather than because of the task.
- **Forced ideas.** Every letter is filled at any cost, and the list gets cluttered.
- **A list without selection.** There are many ideas, but nothing is chosen for doing first and no way to test it.

## Source

Bob Eberle, a book of games for developing children's imagination, [«Scamper: Games for Imagination Development»](https://archive.org/details/scampergamesfori0000eber) (1971; the link is to the 1996 Prufrock Press reissue). The year 1971 is confirmed by the [Wikipedia article](https://en.wikipedia.org/wiki/SCAMPER), not by the reissue page. Eberle built the method on the basis of the list of checklist questions by Alex Osborn in "Applied Imagination" (1953).

## See also

- Alternative to Morphological Analysis: Use it for seven prompts on one existing object; morphological analysis covers combinations.
- Alternative to Theory of Inventive Problem Solving (TRIZ): Use TRIZ when options hit a contradiction, such as speed against safety; SCAMPER only generates.
- Followed by Experiment Card: Record each selected idea as one hypothesis with its metric and deadline.
- Followed by Six Thinking Hats: Test the options SCAMPER generated with the black and yellow hats, for risks and benefits.
