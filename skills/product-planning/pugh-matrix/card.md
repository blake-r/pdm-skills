# Pugh Matrix

## Essence

The Pugh matrix is the matrix of Stuart Pugh's method of controlled convergence for concept selection. Criteria run down the vertical axis and concepts across the horizontal axis. Every concept is compared, criterion by criterion, with one reference concept, the datum: better (+), worse (-) or same (S). The pattern of +, - and S per concept is for guidance only. It is a way to sort ideas, not to compute a winner: the team attacks the negatives of strong concepts, adds improved concepts, drops weak ones and repeats with the strongest concept as the new datum, until a few remain. Pugh built it for engineering design, where a team has several concepts of the same product and no numbers yet.

## When to use and when not to

Use it when a team must choose among alternatives (designs, solution approaches, vendors), all aimed at the same requirements, and the data is directional. Inputs: a written list of requirements (in Pugh, the product design specification), alternatives sketched at the same level of detail, a datum, and criteria taken from the requirements.

Do not use it when:

- **Real figures exist.** With measured costs and volumes, compare numbers instead of signs.
- **Alternatives differ in level or kind.** A detailed concept beats a vague one only because it is detailed; concepts must be on the same generic level.
- **There is no sensible datum.** Pugh takes an existing design if there is one, else the concept the group thinks best; rerun with another datum to see whether the pattern holds.
- **Criteria overlap.** Pugh: when no concept stands out, a criterion often contains another; split it.

Nuances:

- **Counts are guidance, not scores.** Pugh: the numbers must not be treated as absolute or summed algebraically.
- **The matrix does not decide.** Control stays with the participants.
- **Numeric weights are not Pugh's.** He grades criteria as important, moderately important or desirable (high, medium, low) and says numeric rating and weighting give false precision; he keeps it for stable product lines with known customer priorities.
- **One run is not enough.** Pugh's projects typically take five or six evaluations over three levels of detail.

## Scheme

| Criterion | Importance (optional) | Datum | Concept A | Concept B | Concept C |
|---|---|---|---|---|---|
| Criterion 1 | High | S | + | S | - |
| Criterion 2 | Low | S | S | + | - |
| Count of +, S, - | | | counts | counts | counts |

Criteria are rows, concepts are columns, the datum column is always S. The result is the pattern of counts per concept, read together with where the minuses sit. Under the table: the concepts dropped, the improved or combined concepts added, and the next datum. Net and weighted net sums are later practice, not Pugh's, and are secondary in the template.

## How to apply

1. **Write the requirements** the concepts must meet, before any solution is generated.
2. **Sketch every concept** at the same level of detail, with a short description, and put the sketches into the matrix.
3. **Choose criteria** from the requirements: unambiguous, accepted by all participants, written down. Optionally grade each as High, Medium or Low importance.
4. **Choose the datum:** an existing design if there is one, else the concept the group thinks best.
5. **Mark each concept against the datum:** + better, - worse, S same; use S when in doubt. Count +, S and - per concept. Do not sum them as scores.
6. **Read the pattern:** strong and weak concepts, and which criteria separate them.
7. **Improve:** for strong concepts, ask how to reverse the negatives without losing positives; add the modified concept as a new column (keep the old one). Do the same for weak ones, against the datum, not an absolute.
8. **Eliminate** the truly weak concepts.
9. **If no concept stands out:** criteria may be ambiguous or overlap (split them), or concepts may be the same thing in two forms.
10. **Re-datum:** rerun with the strongest concept as the datum. If the pattern persists, it confirms the first run.
11. **Phase II:** develop the strongest concepts in more detail, refine the criteria, rebuild the matrix, repeat.
12. **Work in the open:** one large display, all team members taking part. Then decide; the matrix only guides.

## Example

Team 506 of the FAMU-FSU College of Engineering (2023) worked for Corning on short ceramic parts that fall off a conveyor pallet during stops and vibration; the current plexiglass T supports need extra labor. The team marked eight concepts against seven criteria, with the current T system as the datum. Counts of pluses, S and minuses: Magnetic Swivel 5, 1, 1; Pincer 3, 3, 1; 4 Bar 4, 2, 1; Sand Bag 3, 4, 0; Sensor Gate 1, 5, 1; 2 Long Poles 3, 3, 1; Swedish Wheels 4, 2, 1; Self-nesting T 4, 2, 1.

Decisions recorded: Sensor Gate was dropped for meeting the fewest customer needs. Swedish Wheels was dropped for negative scoring on protecting the ceramic; the published table shows S in that row and a minus only on Material Choice, so the text and the table disagree. The Magnetic Swivel, with the most pluses, became the datum of the next chart. The final chart, with the Pincer as datum, left the Magnetic Swivel, Pincer and Self-nesting T; the Self-nesting T scored 2 pluses, 2 S and 3 minuses against the Pincer. The final choice was therefore made not by Pugh counts but by a weighted Analytic Hierarchy Process step (alternative values 0.362, 0.329, 0.320), and the team chose the Self-nesting T, also because the advisor supported a proven approach.

What the case lacks: the Pugh chart narrowed the field and changed the datum, but did not pick the winner; the middle charts are in an appendix. I found no public case where the Pugh result alone decided.

Source: [Concept Selection, Team 506](https://web1.eng.famu.fsu.edu/me/senior_design/2023/team506/assets/deliverables/contenttodate/conceptselection.pdf) and the [project page](https://web1.eng.famu.fsu.edu/me/senior_design/2023/team506), updated April 21, 2023.

## Common mistakes

- **Summing marks as absolute scores.** Pugh says they are for guidance and must not be summed; a concept with the most pluses can fail on the criterion that cannot be missed.
- **Weak datum, never changed.** Everything looks better than a bad baseline; rerun with the strongest concept as datum.
- **Uneven concepts.** A well-specified concept gains pluses from detail alone; keep one level of detail and one generic level.
- **Overlapping or vague criteria.** Two criteria that contain each other count a thing twice; a vague one is marked differently by each person.
- **Numeric weights added late.** Weights set after the first result justify a preferred option, and numbers add false precision.
- **Stopping at one run.** The first run is a filter; expand with improved concepts, drop weak ones, re-datum.
- **Letting the matrix decide.** It guides; the team decides, and writes down what is dropped and what goes on.

## Source

Stuart Pugh, Total Design: Integrated Methods for Successful Product Engineering, Addison-Wesley, 1991 (first printed 1990), ISBN 0-201-41639-5; the method of controlled convergence is in Section 4.8.1, pp. 74-81, and numeric rating and weighting in Sections 4.8.4-4.8.5, pp. 92-94. The early form is Pugh, "Concept selection - a method that works", Proceedings of ICED 81, Rome, pp. 497-506 (as listed in the book's bibliography). The book was read for this card: the procedure, the +/-/S legend, the rule not to sum the marks, re-datuming, and the view on weighting come from it. The net total and the weighted net in the template are not in Pugh's method; they come from the weighted decision-matrix tradition and from later guides such as [Umbrex](https://umbrex.com/resources/frameworks/decision-making-frameworks/pugh-matrix/), [LogRocket](https://blog.logrocket.com/product-management/pugh-selection-matrix) and a public weighted matrix on the [RedLine13 blog](https://www.redline13.com/blog/2022/11/jmeter-alternatives-k6-and-gatling/). There is no description in PAF (Sergey Tikhomirov, productframework.ru, CC BY-SA 4.0, undated): none was found.

## See also

- Alternative to RICE Scoring: Use RICE to rank many initiatives with numbers; use Pugh to compare few alternatives.
- Alternative to Impact / Effort Matrix: Use the matrix to plot ideas on two axes; Pugh compares alternatives on many criteria.
- Followed by Cost / Benefit Analysis: Take the alternatives left after the last round and calculate their payback.
