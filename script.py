import json
import os
from collections import defaultdict
from operator import itemgetter

with open("warnings.json") as f:
    warnings = json.load(f)


grouped = defaultdict(list)

cyclic = []

for w in warnings:
    grouped[w["path"]].append(w)
    if w.get("symbol") == "cyclic-import":
        cyclic.append(w)

for path, warns in grouped.items():
    warns.sort(key=itemgetter("line"))
    full_dir = os.path.dirname(path)
    if full_dir:
        os.makedirs(full_dir, exist_ok=True)
    output_path = f"{path}.pylint.json"
    with open(output_path, "w") as f:
        json.dump(warns, f, indent=4)

if cyclic:
    with open("cyclic-imports.json", "w") as f:
        json.dump(cyclic, f, indent=4)