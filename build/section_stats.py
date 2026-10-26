"""Word counts per card section across all cards, with recommended limits.

Usage: uv run -q python3 build/section_stats.py

For every section of the seven, prints min, median, 90th percentile and max
word count over skills/*/*/card.md (URLs excluded, counted like build/scan.py).
The recommended limit is the maximum rounded up by the rule: two-digit values
to a multiple of 10, three-digit values to a multiple of 50 (so 150, 250, 400).
Compare it with the limits in build/quality_gate.md (K3).
"""

import glob
import math
import re
import statistics

ORDER = ["Essence", "When to use and when not to", "Scheme", "How to apply", "Example", "Common mistakes", "Source", "See also"]


def count(text):
    return len(re.findall(r"[A-Za-z0-9]+(?:[-–][A-Za-z0-9]+)*", text))


def round_up(n):
    return math.ceil(n / 10) * 10 if n < 100 else math.ceil(n / 50) * 50


rows = []
for path in sorted(glob.glob("skills/*/*/card.md")):
    text = re.sub(r"\(http[^)]*\)", "", open(path, encoding="utf-8").read())
    sections = {}
    for part in re.split(r"^## ", text, flags=re.M)[1:]:
        name, _, body = part.partition("\n")
        sections[name.strip()] = count(body)
    rows.append(sections)

print(f"cards: {len(rows)}")
print(f"{'section':32s} {'min':>5s} {'median':>7s} {'p90':>5s} {'max':>5s} {'recommended':>12s}")
total = 0
for name in ORDER:
    values = sorted(r.get(name, 0) for r in rows)
    p90 = values[min(len(values) - 1, int(0.9 * (len(values) - 1)))]
    limit = round_up(values[-1])
    total += limit
    print(f"{name:32s} {values[0]:5d} {statistics.median(values):7.0f} {p90:5d} {values[-1]:5d} {limit:12d}")
print(f"{'sum of recommended limits':32s} {'':5s} {'':7s} {'':5s} {'':5s} {total:12d}")
