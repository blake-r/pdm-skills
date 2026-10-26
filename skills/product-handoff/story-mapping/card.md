# Story Mapping

## Essence

A story map is a layout of product requirements in two dimensions instead of a flat list. Horizontally — the person's path from left to right, in the order in which they use the product. Vertically — the stories under each step, from the most needed at the top to the less needed at the bottom. Horizontal lines cut the map into releases.

Three levels:

1. **Activities:** the person's big tasks — "ship a parcel", "track a parcel".
2. **Tasks:** steps within an activity, in the order of the path. Together with the activities they form the product's "backbone".
3. **Stories:** variants and details of each step, hanging below it like "ribs".

The technique was described by Jeff Patton: first in a 2005 article, then in a 2014 book. The top row of stories gives the smallest system that goes through the whole path — a "walking skeleton", in Alistair Cockburn's phrase. It is built first.

## When to use and when not to

Use it when a product or a large feature has to be discussed as a whole: to build a shared understanding within the team and with customers, to decide what goes into the first version under a fixed deadline, or to plan releases so that each delivers a complete path.

Do not use it for a couple of small changes: in such cases Patton first orders the changes themselves and builds a small map for each. A map handles poorly work that is not related to people's actions — Patton gives as examples a move to another database and a rebrand.

Limits:

- **The backbone is not prioritized.** Asking "what matters more, the engine or the brakes" makes no sense; one chooses what the steps will be, not whether they are needed.
- **The order of steps is not a full account of dependencies.** When slicing a release, check that it does not rely on something from a later one.
- **The map is alive.** Stories move between releases as the team learns new things.

## Scheme

```
             ┌──────────────┬──────────────┬──────────────┐
Activities   │ Activity 1   │ Activity 2   │ Activity 3   │
Tasks   →    │ step  step   │ step         │ step  step   │
             ├──────────────┴──────────────┴──────────────┤
Release 1    │ stories: minimum that covers the whole path│
 goal        ├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤
Release 2    │ stories: next slice                        │
 goal        ├─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤
Release 3    │ stories: later                             │
             └────────────────────────────────────────────┘
               higher — more needed; build left to right
```

## How to apply

1. **Gather everyone:** the team, customers, support. A map drawn by one person does not create a shared understanding.
2. **Name the product goal** and the people whose path you are laying out.
3. **Lay out the activities and tasks** from left to right in the order of the path.
4. **Sketch the stories** under each task together, without criticizing ideas.
5. **Arrange them vertically:** higher — what the path cannot work without; lower — improvements.
6. **Draw the release lines** and write a goal for each: what changes for people and which metric shows it.
7. **Check against the team's capacity:** if it does not fit, narrow the first slice, make the stories thinner.

## Example

Allegro Group, owner of Poland's largest marketplace Allegro, in January 2014 was building a new parcel shipping management platform to replace an old one that could not cope with the load. It had to be integrated with one of Poland's largest ERP systems, and the partner's release cycle was six months.

| Stage | What was recorded |
|---|---|
| Initial estimate | about 2 years for the full scope |
| Participants | a team from three cities, stakeholders, the support service |
| Activities | creating a shipment order, calculating the cost, tracking, personal account, invoices |
| Stories | "calculating the cost" split into fixed and dynamic price lists, standard and additional services, discount codes |
| Lines | the first — minimum viable version; the second — "nice to have"; below — long-term plans |
| Estimate | 120 story points against a team capacity of about 80 |

Decision: cut the first version further and make the stories thinner, building the top row of the map first. Result: the product shipped in June, on time, with most of the needed functions, released in parts after each iteration.

The author also notes a miss: for the minimal scope, data upload in the admin panel was done via CSV files — this took three weeks, while the web interface that replaced it took about a week.

What the case lacks: business metrics after launch and the full map: the article contains only drawings of the process, the prioritization and the roadmap.

Case source: A. Winnicki, [“Eight steps to building Minimum Viable Product with Story Mapping”](https://blog.allegro.tech/2015/01/story-about-delivering-products-part2.html), Allegro Tech Blog, 26.01.2015.

## Common mistakes

- **A map alone.** The product owner draws it, and the team does not share the picture.
- **System functions instead of people's actions.** The top row holds "module", "database" instead of steps of the path.
- **Prioritizing the backbone.** Teams argue about which activity matters more, instead of choosing the variants of each step.
- **The first release does not cover the path.** One step is done in full, the others are empty.
- **No release goal.** Lines are drawn, but it is unclear what result each slice gives people.
- **Drawn and forgotten.** The map is not updated, and postponed stories look abandoned.

## Source

J. Patton, [“It's All in How You Slice It”](https://jpattonassociates.com/wp-content/uploads/2015/01/how_you_slice_it.pdf), Better Software, January 2005; J. Patton, [“The New User Story Backlog is a Map”](https://jpattonassociates.com/the-new-backlog/), 2008; J. Patton, "User Story Mapping", O'Reilly, 2014; J. Patton, [Story Mapping Quick Reference](https://jpattonassociates.com/story-mapping-quick-ref/).

## See also

- Preceded by User Story: Write stories as "As a, I want, so that" and place them under tasks.
- Alternative to Use Case: Use a use case when one complex path with its failures needs full description.
- Enhanced by Product Backlog: Turn the first release's stories, read top to bottom, into the ordered backlog.
- Preceded by Impact Mapping: Start from the features the impact map's branches justify, arranged by user path.
