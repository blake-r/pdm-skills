# Test Case

## Essence

A test case is a description of one check: what must be true before it starts, which actions to perform, and what should result. A test condition is what can be checked: a function, an operation, a quality attribute. The ISO/IEC/IEEE 29119-3 standard defines it as a set of preconditions, input data (including actions) and expected results.

## When to use and when not to

Use when the behavior is known from the requirement, and the check will be repeated by others or will go into regression (re-checking after changes).

Limitations:

- **A case is not a test.** James Bach: testing is an action, not a document. Michael Bolton: a test is what the tester thinks and does. The approach where tests are only explicit rules ("factory school"), according to Bach, produces expensive artifacts that find few bugs.
- **Cases age.** Cem Kaner (2003): a regression case that has passed many times without code changes tells almost nothing.
- **The number of cases is not a measure of work.** Bolton (comment on the article, 2017): a case has no scale, and cases of different sizes are not equal.

## Scheme

```
Requirement or task
   └─ what can be checked (test condition)
        └─ Test case
             ├─ ID (code), goal-name, type, priority
             ├─ preconditions: environment state and data
             ├─ steps: action → expected result
             ├─ expected outcome
             └─ during run: actual result, verdict
```

## How to apply

Inputs: requirement, risk, environment, data.

1. **Identify test conditions,** check each one with one or more cases (ISTQB, International Software Testing Qualifications Board).
2. **Select the cases.** Equivalence partitioning divides data into classes the system treats the same way: one check per class is enough; check boundaries with boundary value analysis (ISTQB). Types, as in the Banki.ru prompt: main, negative, data validation, edge (boundary).
3. **Name the case by its goal:** what we check and under which condition.
4. **Describe the preconditions:** environment and data before the first step.
5. **Write steps as "action → expected result" pairs** with concrete values.
6. **Take the expected result from the requirement.** The test oracle per ISTQB is the manual, specialist knowledge, a reference system, but not the system's code.
7. **At the run, record the actual result and the verdict.**

How to read the outcome (the author's conclusion): a case without an expected result must be rewritten or deleted; it is not a check. Review a case that has passed for a long time (Kaner).

## Example

Banki.ru is a financial marketplace. A QA engineer (tester) read the documentation, came up with scenarios, recorded them in Allure TestOps (a test case storage system) and linked them to a task in Jira (a tracker): up to 1.5 hours per case. The author and the QA team built in about two weeks a bot on n8n (an automation builder) with a Claude model: it writes 8–12 cases per task, and an engineer reviews them. The sample that the team put into the bot's prompt as a reference (the article has a production example). API is the service interface, POST is the request for sending data, leadId is an identifier:

| Field | Value |
|---|---|
| Name | /depositAccount - Request the client's bank details by leadId with an active contract |
| Preconditions | A deposit application is created and a contract is signed, for example for Sinara Bank |
| Step 1 | Send POST /depositAccount with the leadId of an active contract → Response code 200 |
| Step 2 | Check that the accountNumber, bik, bankName fields are present in the response body → All fields are present and not empty |
| Step 3 | Check the record in the midb.deposit_account table → The record matches the API response |
| Outcome | The method returns the correct client bank details with code 200 |

Decision: assign drafts to the bot. Since April 2026 the time per case dropped from 1.5 hours to 10 minutes; 40% of cases go into work after a minimal review.

What the case does not contain: the number of cases in the database, coverage, regression time, defects found, the fate of the remaining 60%. In the sample the outcome is vague ("correct bank details"), and the description says "check the correctness of the method's work" (the article calls such a thing useless). The figures are self-reported. The case is about producing test cases, not about a decision based on the run results.

Source of the case: morcos, [«We handed the routine to a bot: working with test cases now runs on n8n»](https://habr.com/ru/companies/banki/articles/1045336/), Banki.ru blog on Habr, 9.06.2026.

## Common mistakes

- **Vague expected result.** "Check the correctness of the method's work" can neither be passed nor failed; Banki.ru's example for a checklist: "POST /api/v1/deposits with amount=0 → error 400 "Amount must be greater than 0"".
- **Many actions in one step, result only at the end.** It is not visible where it failed (TestDevLab).
- **The reference is taken from the system.** The case confirms the code, not the requirement (ISTQB).
- **The case taken for the test, the number of cases for the measure** (Bach, Bolton).
- **Cases are not reviewed.** Old regression cases give little information (Kaner).

## Source

ISO/IEC/IEEE, [«29119-3:2013, Test documentation»](https://www.iso.org/standard/56737.html), 2013, replaced by the 2021 edition ([copy of the text](https://wildart.github.io/MISG5020/standards/ISO-IEC-IEEE-29119-3.pdf)); ISTQB, [«Standard glossary of terms used in software testing»](https://astqb.org/assets/documents/ISTQB_glossary_of_testing_terms_2.3.pdf), version 2.3, 2014; ISTQB, [«Certified Tester Foundation Level Syllabus v4.0.1»](https://astqb.org/assets/documents/ISTQB_CTFL_Syllabus_v4.0.1.pdf), 2024; C. Kaner, [«What Is a Good Test Case?»](https://www.kaner.com/pdfs/GoodTest.pdf), 2003; J. Bach, [«A Test is a Performance»](http://www.satisfice.com/blog/archives/1346), 2014; M. Bolton, [«The Test Case Is Not The Test»](https://developsense.com/blog/2017/02/the-test-case-is-not-the-test), 2017. Secondary source: TestDevLab, [«How to write good test cases»](https://www.testdevlab.com/center-of-excellence/test-management/best-practices/how-to-write-good-test-cases), no author or date.

## See also

- Preceded by Product Requirements Document: Take each expected result from the PRD requirement, not from the system code.
- Followed by Definition of Done: Count work as done only when its cases pass and the shared list is met.
