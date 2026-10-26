# Retrospective Meeting

## Essence

A retrospective is a regular team meeting at which the team reviews the past period of work: what helped, what got in the way, and what to change. The outcome of the meeting is not a list of complaints but one to three concrete actions, each with an owner and a deadline, which the team will complete before the next retrospective.

## When to use and when not to

Use regularly at the end of each iteration or stage (usually every one to four weeks), and also after a release, an incident or the completion of a project. The meeting is useful to any team that has worked together for more than a couple of months and can change its own process.

Inputs: the period under review, the facts for it (deadlines, metrics, incidents, customer requests), and the participants: the whole team that did the work.

Do not use it:

- **As a witch hunt.** If participants are afraid to speak openly, the meeting turns into a ritual. Safety comes first: we discuss the process, not people.
- **When the team cannot change anything.** If all decisions are made from outside, the retrospective only builds up irritation. Take the problems to whoever decides.
- **For one deep problem.** A retrospective covers the period as a whole and finds themes. The cause of a complex failure is analyzed in a separate meeting.

## Scheme

A board of three columns, with actions at the bottom:

| What's good? (What went well?) | What's bad? (What went badly?) | How to improve? |
|---|---|---|
| stickers with facts | stickers with facts | ideas for the most important problems |
| votes: +3 | votes: +5 | |

**Actions before the next retrospective:** what we do — who is responsible — deadline — how we will know it worked.

## How to apply

1. **Set up the meeting.** Remind everyone of the goal and the rule: we discuss the process, not people. Duration: up to three hours for a monthly period, less for short iterations.
2. **Check the previous actions.** Were they done, and did they help?
3. **Collect the data.** Each person silently writes stickers into the "good" and "bad" columns, then they are grouped by theme. Rely on facts: dates, numbers, events.
4. **Vote.** Each person casts a limited number of votes (usually three) for the themes that matter most to improve.
5. **Discuss the two or three main themes:** find out why it happened, and collect ideas in the "how to improve" column.
6. **Decide what to do.** Choose one to three actions, each with an owner, a deadline and a sign of success. Take the most important improvements into work right away.
7. **Close the meeting.** Briefly: what we keep, what we change; you can ask how useful the meeting itself was.

## Example

Zalando, product area Customer Inbox (personal messages to customers about fashion across several channels), 2018. Four teams had been built around technical components: ten separate task lists with 400 items and four planning sessions per cycle, where key people became a bottleneck. Work took 50% longer than planned on average. Participants rated the planning sessions at −70 on NPS (Net Promoter Score, willingness to recommend, scale from −100 to +100).

The area's management held a joint retrospective and, for the analysis, built a causal loop diagram: a scheme where arrows show how some factors reinforce or dampen others. The diagram showed how scattered lists and planning sessions create delays, and management explained the conclusions to the teams. Decisions: merge tasks and technical debt into one shared list; introduce a "zero bug policy", where bugs found during feature development are fixed immediately, without discussion; replace the four planning sessions with a shared requirements review and one planning session of 60–90 minutes.

Result: together with paying off part of the technical debt, the list shrank from 400 to 100 tasks, the rating of the planning sessions rose from −70 to +30, and the plans began to come true.

The post describes the retrospective and its decisions and figures, but does not show the retrospective board or the action list; the causal loop diagram is only embedded as images. The post also speaks of a shared refinement session and a shared planning session of 60–90 minutes each. This case is e-commerce.

Case source: [Samir Hanna, Marcel Wieczorek — Growing a product area (Zalando Engineering Blog, 2018)](https://engineering.zalando.com/posts/2018/10/growing-product-area.html).

## Common mistakes

- **No actions, or too many.** A list of problems without actions comes back as the same stickers; nobody completes ten items.
- **Previous actions are not checked.** The team stops believing the meeting changes anything.
- **Blame instead of facts.** "Vasya missed the deadline again" instead of "the task waited four days for review" — and people fall silent.
- **Memory of the last days.** Participants remember the end of the period and forget the beginning. Reconstruct the timeline from data before the discussion.
- **A manager in the room.** The presence of the person who evaluates participants suppresses candor; decide in advance who is invited.
- **Votes as a measure of importance.** Voting shows what concerns many, not what influences the result most. Check the vote leaders with facts.
- **The same format every time.** Change the questions and exercises, or the answers become formulaic.

## Source

Norman Kerth described the practice of project retrospectives in the book [«Project Retrospectives: A Handbook for Team Reviews»](https://openlibrary.org/works/OL8022412W) (2001). The five stages of the meeting — setting the stage, gathering data, generating insights, deciding what to do, closing — were proposed by Esther Derby and Diana Larsen in the book [«Agile Retrospectives: Making Good Teams Great»](https://pragprog.com/titles/dlret/agile-retrospectives/) (2006). The meeting goal and the time limit follow the [Scrum Guide 2020](https://scrumguides.org/scrum-guide.html).

## See also

- Preceded by Sprint: Hold it at the end of each sprint to pick changes for the next.
- Enhanced by Team Canvas: actions from the retrospective can change the working rules the team agreed on the canvas.
- Enhanced by Kanban Board: the board's flow metrics are facts to bring to the retrospective.
- Enhanced by 5 Whys: Run 5 Whys on the costliest problem the retrospective names.
