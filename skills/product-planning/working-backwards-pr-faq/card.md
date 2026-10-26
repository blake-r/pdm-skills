# Working Backwards PR/FAQ

## Essence

Working Backwards is a way for a team to decide whether an idea deserves to be built. Before any design or code, the author writes a short mock press release (PR) announcing the finished product to its customers, followed by frequently asked questions (FAQ). Amazon's own description: the PR/FAQ is "a second form of written narrative" that shifts the view from the company to the customer, and a typical executive test is "so what?": a product that is not clearly faster, easier or cheaper than the alternatives is not worth building.

## When to use and when not to

Use it at the start of a new product, feature or initiative, when the customer, the problem and the reason to fund the work are still open. Inputs: a candidate customer and problem, what that customer uses today, and a rough idea of market size, cost and risks. The method also fits non-product ideas, for example a compensation policy.

Do not use it to document a decision already taken or to write sales copy: the press release is not a real announcement.

Limitations:

- **Most PR/FAQs are not approved.** Amazon calls this "a feature, not a bug": the form protects scarce resources. A team that treats a rejection as failure will soften the FAQ to get a yes.
- **It judges the idea on paper.** A strong press release says nothing about whether the team can deliver; the internal FAQ must carry the cost and feasibility.
- **A large initiative may need several documents.** Amazon built Fulfillment by Amazon from two PR/FAQs, one for sellers and one for buyers.
- **Customer-first can still pick the wrong problem.** workingbackwards.com cites the Fire Phone: a great product for a problem customers did not have.

## Scheme

```
PRESS RELEASE (under one page)
  Heading · Subheading · Summary (city, date)
  Problem · Solution · Quote from the company
  Quote from a customer · How to get started
FAQ (five pages or less)
  External: what customers and press ask (price, how it works, support, where to buy)
  Internal: what every department asks (market size, unit economics, investment, risks)
Review: silent reading -> discussion -> go / more work / set aside
```

## How to apply

1. **Define the customer and the problem** in the customer's terms, before the solution. Note what the customer uses today.
2. **Write the heading and subheading** so the target customer understands the product name, who it is for and the benefit.
3. **Write the summary** with a city, a media outlet and a launch date you expect to hit.
4. **Write the problem paragraph** from the customer's point of view, then the solution paragraphs: how it solves the problem and how it differs from current options. Avoid a list of features.
5. **Add two quotes**, one from the company and one from a hypothetical customer, and how the customer gets started.
6. **Write the external FAQ**: price, how it works, support, where to buy.
7. **Write the internal FAQ** with the hard questions: market size (TAM, total addressable market: customers times what each pays), per-unit economics, upfront investment, dependencies, legal issues, time to profit, assumptions, top three reasons it could fail.
8. **Review.** Send no pre-read. Read in silence (15 to 20 minutes), then discuss (about 40 minutes); the most senior attendees speak last. Expect many drafts.
9. **Read the outcome:** go, more investigation, or set aside. Typical reasons for no: a copycat product, small TAM, high upfront risk, a problem that cannot be solved yet, or lower priority than the backlog.

## Example

Case: Fulfillment by Amazon (FBA), Amazon's service for storing and shipping sellers' goods. The only public statement found: "Fulfillment By Amazon was developed using two PR/FAQs, one from a seller perspective and one from a buying perspective." The source uses it to show that a complex project can need more than one PR/FAQ.

Form on the slide: the two documents (seller view, buyer view) with their structure from the Scheme above.

What the case lacks, honestly: the text of both PR/FAQs, their headings, the questions, the review date and the decision are not published. Amazon's own pages and the Bryar and Carr site show no real Amazon PR/FAQ text; the sample documents there are hypothetical. The example therefore shows the decision only as "built from two PR/FAQs", and every other field in the template is N/A.

Case source: [workingbackwards.com, "The Amazon Working Backwards PR/FAQ Process"](https://workingbackwards.com/concepts/working-backwards-pr-faq-process/).

## Common mistakes

- **Writing about features.** The source asks for the customer's problem and a clear difference from current products; a laundry list of features hides a copycat.
- **A press release that sells.** Reviews are for truth-seeking, not selling; hype and unsupported claims should be cut in the review.
- **A thin internal FAQ.** Skipping unit economics, upfront investment and the top three reasons to fail turns the document into marketing.
- **Too long.** The press release is under one page and the FAQ at most five pages; appendices of charts let writers dodge choices.
- **Pre-reading and junior-first discussion.** Seniors speaking first sway the room.
- **Treating the first draft as final.** Ten or more drafts are normal; the first takes hours, not days.
- **Taking approval as proof.** The document is living; revise it as facts change.

## Source

Colin Bryar and Bill Carr, "Working Backwards: Insights, Stories, and Secrets from Inside Amazon", St. Martin's Press, 2021; Amazon, ["An insider look at Amazon's culture and processes"](https://www.aboutamazon.com/news/workplace/an-insider-look-at-amazons-culture-and-processes), excerpt of the book on About Amazon (page undated); Bryar and Carr, [workingbackwards.com](https://workingbackwards.com/concepts/working-backwards-pr-faq-process/), the PR/FAQ template, standard questions and reasons for rejection; Colin Bryar, [PR/FAQ guide](https://docs.superhuman.com/@colin-bryar/working-backwards-how-write-an-amazon-pr-faq). The method grew at Amazon after 2004. There is no page for this tool in PAF (Product Architecture Framework, productframework.ru); the card is built from the primary sources above. Amazon's own pages disagree slightly with the authors' site on review timing (one hour in total versus 20 plus 40 minutes), which is compatible.

## See also

- Preceded by Jobs-to-be-Done: the job and the customer's struggle feed the problem paragraph.
- Enhanced by Value Proposition Canvas: use its gains and pains to write the solution paragraph.
- Enhanced by Storytelling: tell the customer story in the press release.
- Followed by User Story: an approved PR/FAQ is split into stories for the team.
