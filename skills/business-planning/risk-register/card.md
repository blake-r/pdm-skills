# Risk Register

## Essence

A risk register is a living table with one row per risk: what could happen, why, what it would cause, who owns it, how likely and how severe it is, what is being done about it, and its status. NIST, quoting the US Office of Management and Budget (OMB) Circular A-11, defines it as "a repository of risk information including the data understood about risks over time". A risk here is an uncertain event that would affect an objective if it happened. Likelihood is how probable the event is; impact is how much it matters; their combination gives a score, which NIST calls exposure. The register does not find or analyze risks. It keeps them in one comparable list, with one owner and one recorded response each, so that a team or an executive committee can see the risk landscape and revisit it.

## When to use and when not to

Use it when a launch, migration, partnership, market entry or whole product line carries more risks than people can hold in their heads, and someone must own, rank and review them. Inputs: the objective at stake, a first list of risks (from a pre-mortem, incident history, audits, interviews), and a scale for likelihood and impact agreed before scoring.

Do not use it:

- **As the analysis itself.** NIST keeps the register a summary and adds a separate risk detail record for scenarios, assumptions and history.
- **To compare unlike risks by a bare number.** NIST notes that dissimilar exposures, such as staff retention and disaster recovery, are hard to compare and are often translated into financial impact.
- **As a one-time document.** An unreviewed register shows last quarter's picture as if it were current.

Nuances:

- **Scores are ordinal.** On a 1-5 scale, 20 is not twice 10. NIST's own examples differ: Table 9 uses probabilities (.9 and .9), Table 10 uses High/Medium/Low.
- **Score is not appetite.** Risk appetite is how much risk the organization accepts in pursuit of its goals; a high score may be acceptable and a middle one not.
- **Fields vary.** NIST says a register may hold many more or fewer fields.

## Scheme

| ID | Risk statement | Cause | Effect | Category | Owner | Likelihood (1-5) | Impact (1-5) | Score | Rating | Response type | Response | Status | Dates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

One row per risk. Score = likelihood x impact, computed. Rating (Low, Medium, High) comes from agreed score bands, and priority rank orders the rows. Response type is accept, transfer, mitigate or avoid. Dates are raised, last reviewed, next review.

The template follows the NIST elements (ID, priority, description, category, likelihood, impact, exposure rating, response type, response description, owner, status). Cause and effect, 1-5 scales, rating bands and dates are adaptations.

## How to apply

1. **Fix the scale.** Write what each level of likelihood (1 rare to 5 almost certain) and impact (money, customers, delay) means, and the score bands: the template uses Low up to 5, Medium 6-12, High 15 and above; change them to your agreement.
2. **List risks.** Write each as event, cause, effect, in common phrasing, so rows can be compared.
3. **Name one owner** per risk: the person accountable for keeping it within requirements. A risk manager may monitor the response.
4. **Score the current risk**, as it stands with existing controls. Two people score separately; discuss gaps, do not average.
5. **Read score and rank.** The template computes score = likelihood x impact, the rating and the priority rank (1 is highest).
6. **Choose a response** for each risk above your threshold: accept (only monitor, within tolerance), transfer (share the consequences, for example insurance), mitigate (reduce likelihood or impact), avoid (do not take the action). For opportunities NIST lists realize, share, enhance, accept. Write the response, who does what, and by when.
7. **Set status and dates:** raised, last reviewed, next review. The template flags rows past the review date.
8. **Review on a fixed cadence**, rescore after a response is in place, close risks that ended.

Interpretation: top-ranked and above-appetite risks go to the decision-maker with a proposed response; the output is a decision per risk (accept, fund a response, escalate), not the table.

## Example

Highland Community Planning Partnership (public bodies working together in the Highlands, Scotland), Strategic Risk Register as at January 2026, reported to its Board on 10 March 2026 ([report CPPB/8/26](https://www.highland.gov.uk/download/meetings/id/86555/Item%252013.%2520Strategic%2520Risk%2520Register)).

Form: eight risks with ID, title, description, link to the outcome plan, likelihood, impact, score, current controls, planned actions, responsible group and monitoring frequency. Scores are likelihood x impact: Financial Sustainability & Funding Alignment 4 x 5 = 20, Cost of Living & Poverty 4 x 5 = 20, Implementation of Scottish Government Policies 4 x 4 = 16, Failure to Deliver the Outcome Improvement Plan 4 x 3 = 12, Partnership Capacity & Skills 3 x 2 = 6. The planned action for the funding risk: agree budget arrangements beyond May 2027.

Decision: the report says early review puts financial sustainability, policy implementation capacity and data sharing above the new risk appetite. The Board noted the update and agreed the revised approach, including the Risk Appetite Statement applied to all strategic risks; the Chair said appetite use needed further discussion. This is from the [minutes of 10 March](https://www.highland.gov.uk/download/meetings/id/87097/Item%25203.%2520Minutes%2520of%2520Meetings), which the 12 June 2026 papers still list "for approval".

What the case lacks: the register names owning groups, not people, and has no status, dates, response type or separate residual score. The decision concerns the register's approach and risk appetite, not a funded response to one risk, and the minutes are not yet approved.

## Common mistakes

- **Risks without owners.** A group or "everyone" owns nothing; name a person.
- **Vague statements.** "Supplier issues" cannot be scored; state event, cause and effect.
- **Scoring once.** Unreviewed scores go stale; review on a date.
- **Reading score as a verdict.** A 20 above appetite and a 20 within it need different decisions.
- **Mixing inherent and current scores.** Say whether controls are counted, and keep the same basis in every row.
- **Hiding a long tail.** Hundreds of rows with no ranking bury the few that matter.
- **No response or cost.** A scored risk with no response is only a list of worries.
- **Treating the table as the record.** Detailed scenarios belong in a separate detail record.

## Source

NIST Interagency Report 8286r1, "Integrating Cybersecurity and Enterprise Risk Management (ERM)", by Stephen Quinn, Julie Chua, Nahla Ivy, R. K. Gardner, Karen Scarfone, Matthew C. Smith and Greg Witte, National Institute of Standards and Technology, December 2025. [DOI](https://doi.org/10.6028/NIST.IR.8286r1), [PDF](https://nvlpubs.nist.gov/nistpubs/ir/2025/NIST.IR.8286r1.pdf), [landing page](https://csrc.nist.gov/pubs/ir/8286/r1/final). It supersedes the 2020 edition. The PDF was opened and checked for the definition (footnote 1 and glossary, quoting OMB Circular A-11), the notional cybersecurity register (Table 1 and Table 9, and the Fig. 4 caption) and enterprise register (Tables 5, 6 and 10), and the response types (Tables 2 and 4). The text covers cybersecurity and enterprise risk management, not product work. The enterprise register as a general artifact and the cybersecurity register as a variant is my framing; cause and effect columns, the 1-5 scales, rating bands, the review flag and the date columns (NIST puts dates in the risk detail record) are adaptation. Table 9 shows .9 and .9 as 80%, though the product is 81%. OMB Circular A-11 is quoted through NIST. There is no page in PAF (productframework.ru; its sitemap was checked).

## See also

- Preceded by Pre-mortem: The reasons the team writes down become the first register entries.
- Followed by Cost / Benefit Analysis: Compare the cost of a response with the exposure it removes.
- Enhanced by RAPID Decision Rights: Name who decides to accept, fund or escalate a high risk.
