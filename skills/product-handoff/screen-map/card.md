# Screen Map

## Essence

A screen map is a diagram in which each screen of a product is shown as a node and the transitions between screens as arrows. It turns a user scenario into concrete interface decisions: which screens exist, what states they can be in, and how to get from one to another. It is used to set requirements for development and as documentation.

## When to use and when not to

Use it when the user scenario is already clear and needs to be implemented in the interface: updating a mobile app, moving a function to another screen, merging or splitting screens. Inputs: the scenario, the list of screens, the company's design system.

Do not use it:

- **For the content structure of a website.** A sitemap shows the hierarchy of pages and, according to the Nielsen Norman Group (NN/g), does not show small navigation elements. A screen map goes down to the level of screens, their states and transitions.
- **As a replacement for a detailed screen description.** The map shows composition and links, not the layout.

Caveat: the map shows structure, not usability; clarity is checked with people.

## Scheme

```
[Entry] → Screen A ──tap──→ Screen B ──system──→ Screen C
              │                 states: loading · data · empty · error
              └─tap─→ Screen D (new)
Legend: existing · new · another team · user transition · system transition
```

For each node: name, composition, list of states. For each arrow: who triggers the transition and how.

## How to apply

1. **Take the user scenario** and the list of current screens. Mark the entry and the end.
2. **Place the existing screens** by hierarchy: main screen, section, detail.
3. **Add the new screens** and the screens of other teams that the change may affect. Mark them with the legend.
4. **For each screen, write its states:** loading, data, empty, error.
5. **Draw the transitions** and label the initiator: user or system.
6. **Build the nodes from design-system components,** so the map can be used to estimate the volume of work.
7. **Read the map:** long chains before the target action, screens without an exit, transitions without a reason, redundant pairs of screens. The decision is to merge, remove or move; check it on customers.

## Example

OTP Bank, the card screen in the mobile app. The article has no screen map; the chain below was restored from its text. One of the reasons: on the already updated main screen, the central entity became the account, not the card.

- **Before the changes.** The main screen shows cards, and a tap leads to the card screen. The contractor built it from two glued-together screens. CSI (Customer Satisfaction Index, a 10-point customer satisfaction scale) was 8.2; the expected value in the test was 8.5.
- **Option 1.** Two screens: the account with linked cards, and the card separately. Judging by the description of the changes, the tabs "history", "payment", "terms" and the three-dot menu were removed. Research with current customers: "it is unclear why there are separate screens for the account and the card".
- **Option 2.** The account and the card on one screen; the extra navigation was removed.

Test: iOS only, two weeks, a small share of traffic, debit and credit cards analysed separately. CSI for debit cards 8.3 (8.4 after filtering out irrelevant reviews), for credit cards 8.1 (8.5). For debit cards, conversion into payment and PIN change went up, top-up and viewing of details went down; account closure also went down, which is the desired decrease. For credit cards, top-up went up, details and PIN are unchanged. Decision: one screen, fixes (removed the coloured header background, added a loading skeleton, changed the order of blocks) and a gradual rollout. The author: conversions "recovered", CSI "grew significantly".

What is missing: the map itself, the number of respondents, the share of traffic, the final CSI value (only a chart).

Source: D. Gavrilenkov, [“The story of one redesign. The card screen in the OTP Bank mobile app”](https://habr.com/ru/companies/otpbank/articles/909442/), OTP Bank blog on Habr, 14.05.2025.

## Common mistakes

- **A map without states.** Loading, empty and error screens are left to the developer's discretion, although an empty and a filled screen require different decisions.
- **Only the happy path.** No transitions on errors and on system actions.
- **Only the new is drawn.** Affected screens of other teams are not shown, so the volume of work is understated.
- **Blocks instead of design-system components.** Such a map cannot be used to estimate the volume of work.
- **Looks taken for clarity.** Customers liked the look, but the separation of account and card remained unclear. The structure is checked with people.
- **A test result extended to everything.** The test ran only on iOS and on a small share of traffic: on Android the result may differ.
- **The map is not updated,** and it stops being documentation.

## Source

PAF description (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, undated): a screen map displays the implementation of a user scenario through concrete interface decisions, includes element states and transitions, and is assembled from the design system. Samhita Tankala, [“Information Architecture vs. Sitemaps”](https://www.nngroup.com/articles/information-architecture-sitemaps/), Nielsen Norman Group, 03.09.2023: an adjacent method, the site map; the boundary of applicability. M. Gorgots, [“From chaos to order: the artifacts of SberHealth systems analysts…”](https://habr.com/ru/companies/docdoc/articles/916772/), SberHealth blog on Habr, 09.06.2025: definition and composition of the map (screen hierarchy; existing, new, and neighbouring teams' screens).

## See also

- Enhanced by User Flow: Draw the user flow first, then turn its steps into screens and transitions.
- Preceded by Use Case: Take the main scenario and extensions from the use case, then place their screens.
- Followed by Sequence Diagrams: Once transitions are fixed, draw a sequence diagram for each system call.
- Enhanced by State Modelling: Use an entity's state diagram to define loading, empty and error screen states.
