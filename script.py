import asyncio
import json
import os
from os import path

CURRENT_REPO_DIR = os.getcwd()
warnings_json = path.join(CURRENT_REPO_DIR, "warnings.json")

if not path.exists(warnings_json):
    print(f"Error: {warnings_json} not found")
    exit(1)

async def write_warnings(file_path, warnings):
    file_path = path.join(CURRENT_REPO_DIR, f"{file_path}.pylint.json")
    os.makedirs(path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(warnings, f, indent=4)

async def parse_and_write_warnings():
    if not path.exists(warnings_json):
        print(f"{warnings_json} Not found")
        return

    with open(warnings_json, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return

    warnings_by_path = {}
    for entry in data:
        file_path = entry["path"]
        warnings_by_path.setdefault(file_path, []).append(entry)

    await asyncio.gather(*(write_warnings(file_path, warnings) for file_path, warnings in warnings_by_path.items()))

async def main():
    await run_pylint()
    await parse_and_write_warnings()
    os.remove(warnings_json)

if __name__ == "__main__":
    asyncio.run(main())
