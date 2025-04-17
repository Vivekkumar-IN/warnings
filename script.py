import json
import os
from collections import defaultdict
from operator import itemgetter

with open("warnings.json") as f:
    warnings = json.load(f)

grouped = defaultdict(list)
for w in warnings:
    grouped[w["path"]].append(w)

for path, warns in grouped.items():
    warns.sort(key=itemgetter("type"))
    full_dir = os.path.dirname(path)
    if full_dir:
        os.makedirs(full_dir, exist_ok=True)
    output_path = f"{path}.pylint.json"
    with open(output_path, "w") as f:
        json.dump(warns, f, indent=4)