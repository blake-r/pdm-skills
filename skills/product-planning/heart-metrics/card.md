# HEART Metrics

## Essence

HEART is a set of five categories of user-experience metrics: Happiness, Engagement, Adoption, Retention and Task Success. Together with the "goals → signals → metrics" process, it helps move from a general "make the product easier to use" to several measurable indicators tied to the goal of the product or feature. The method was devised at Google based on experience with more than 20 products.

## When to use and when not to

Use it when you need to choose metrics for a product, feature or redesign; when the team sees only general indicators (visits, revenue); when there are too many metrics and it is unclear which ones matter.

Do not use it as a mandatory set of five metrics: for many products some categories are not needed. It does not replace conversations with users.

Limitations:

- **Behavioral metrics do not explain causes.** Growth in visits can come from interest, or from the fact that the needed thing is hard to find.
- **Satisfaction requires surveys.** It cannot be obtained from logs; a regular questionnaire of the same form is needed.
- **Task success is hard to count from logs** if it is unclear which task the user was solving.

## Scheme

A table: rows — the five categories, columns — goals, signals, metrics.

| Category | What it measures | Example metric |
|---|---|---|
| **Happiness** | attitude: satisfaction, visual appeal, willingness to recommend, perceived ease | average score in a regular survey |
| **Engagement** | frequency, intensity and depth of use | share of active users who visited 5+ days in a week |
| **Adoption** | how many new users started using it | new accounts over 7 days |
| **Retention** | how many users stay | share active weekly, and still active after three months |
| **Task Success** | efficiency, effectiveness, errors | time to complete, share of completed tasks, error rate |

Columns: **Goals** — what we want to achieve for the user; **Signals** — which action or attitude will show success or failure; **Metrics** — how the signal is calculated and over what period.

## How to apply

1. **Formulate the goals** of the product or feature from the user's point of view. Resolve disagreements about goals now.
2. **Choose the categories.** Keep only those important for this goal (in practice often two or three) and explain why the others are not needed.
3. **For each goal, find signals:** which actions or responses will show success; check that the data for them exists.
4. **Turn the signals into metrics:** formula and period. Calculate engagement as a per-user average; compare other counts with a baseline or turn them into shares.
5. **Record the current values** and agree which change counts as success.
6. **Read the changes.** After a redesign, satisfaction often first drops from unfamiliarity: decide by whether it recovers. Adoption and Retention show whether growth came from new arrivals or from returning users. If a metric has not moved, decide together with qualitative data.

## Example

Open Targets Platform — an open web platform for scientists looking for drug targets (a partnership of GSK, EMBL-EBI and the Wellcome Trust Sanger Institute). The team chose its metrics with HEART so that the list would not become unmanageable. This case is from drug discovery, not e-commerce or fintech.

Decision on categories: focus on adoption, engagement and retention (in that order): they can be tracked regularly with web analytics. Task success was not included in the quantitative metrics as less important: work with the platform is open-ended, unlike, for example, buying online with a clear completion action. Satisfaction was assessed from user feedback, and a periodic NPS (Net Promoter Score — an index of willingness to recommend) survey was planned between major updates.

For external participants, the team replaced the goal and signal columns with a simple question:

| Category | Question | Metrics (average, April 2016 – March 2017) |
|---|---|---|
| **Adoption** | do people come and look at pages? | 816 visits and 530 unique visitors a week |
| **Engagement** | do they use the site: search, downloads, moving to the evidence? | average visit 6 min 49 s, bounce rate (single-page visits) 25.6%, 11.3 actions per visit |
| **Retention** | do they come back? | 460 repeat visits a week, 56.67% of all visits |

The table is filled with figures from the source; the choice of categories is a visible decision. What the source does not show: any product change made from these values. The authors only conclude that the platform was used substantially, in line with positive feedback, and mention that Biogen joined the partnership soon after the public release (they do not present it as a result of the metrics).

Source of the case: [Karamanis N. et al., "Designing an intuitive web application for drug discovery scientists", bioRxiv preprint](https://www.biorxiv.org/content/10.1101/169193v1.full.pdf) (27 July 2017; journal version — Drug Discovery Today, 2018).

## Common mistakes

- **All five categories out of habit.** Metrics are collected, but decisions are not made on half of them.
- **Metrics without goals.** One starts with what is easy to count and then cannot explain what a change means.
- **Raw counts without a baseline.** Growth from an inflow of new users is presented as growth in engagement.
- **No baseline value.** Without current figures it is not visible whether the change helped.

## Source

Kerry Rodden, Hilary Hutchinson, Xin Fu, Google, ["Measuring the User Experience on a Large Scale: User-Centered Metrics for Web Applications"](http://research.google.com/pubs/archive/36299.pdf), CHI 2010 conference.

## See also

- Enhanced by Metric Pyramid: Find the North Star in the pyramid, then choose HEART categories for its branches.
- Alternative to AARRR Metrics: Use AARRR for the path from acquisition to revenue, not user experience.
- Enhanced by Cohort Analysis: Measure adoption and retention by cohort so new arrivals are not counted as growth.
- Enhanced by Customer Survey: Collect the Happiness metric through a regular questionnaire, since logs cannot show satisfaction.
