import json, os, sys, tempfile

# The report lives outside the repository; QUALITY_REPORT overrides the default.
P = os.environ.get("QUALITY_REPORT", os.path.join(tempfile.gettempdir(), "pdm-skills", "quality_report.md"))
entries = json.load(open(sys.argv[1]))
L = open(P).read().split("\n")

def last_row_before(marker, nth):
    idx = [i for i, l in enumerate(L) if l == marker][nth]
    j = idx - 1
    while not L[j].startswith("| "):
        j -= 1
    return j

for e in entries:
    name = e["path"].split("/")[1]
    s = e["scores"]
    row = f"| {e['path']} | " + " | ".join(map(str, s)) + f" | {e['verdict']} |"
    j = last_row_before("## Score history", 1); L.insert(j + 1, row)
    h = f"| {name} | {e['h1']} | {e['h2']} |"
    j = last_row_before("## What was fixed", 1); L.insert(j + 1, h)
    k = L.index("**Common to scripts and skills.**")
    L[k:k] = [f"**{name}.**", ""] + e["fixed"] + [""]
    if e.get("gap"):
        while L[-1] == "": L.pop()
        L.append(f"| {e['path']} | {e['gap'][0]} | {e['gap'][1]} | {e['gap'][2]} |")
        L.append("")
open(P, "w").write("\n".join(L))
