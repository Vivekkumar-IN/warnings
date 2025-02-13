import asyncio
import shutil
import json
import os
from os import path

CURRENT_REPO_DIR = os.getcwd()
warnings_json = path.join(CURRENT_REPO_DIR, "warnings.json")
EXCLUDED_FILES = {
    path.join(CURRENT_REPO_DIR, ".gitignore"),
    path.join(CURRENT_REPO_DIR, "LICENSE"),
    path.join(CURRENT_REPO_DIR, "README.md"),
    path.join(CURRENT_REPO_DIR, "script.py"),
    path.join(CURRENT_REPO_DIR, ".github", "workflows", "pylint.yml"),
    path.join(CURRENT_REPO_DIR, "warnings.json"),
}

for root, dirs, files in os.walk(CURRENT_REPO_DIR, topdown=False):

    for file in files:
        file_path = path.join(root, file)
        if file_path not in EXCLUDED_FILES:
            os.remove(file_path)

    for dir_name in dirs:
        dir_path = path.join(root, dir_name)
        if dir_path not in [os.path.dirname(p) for p in EXCLUDED_FILES]:
            shutil.rmtree(dir_path, ignore_errors=True)
            
if not path.exists(warnings_json):
    print(f"Error: {warnings_json} not found")
    exit(1)

async def write_warnings(file_path, warnings):
    file_path = path.join(CURRENT_REPO_DIR, f"{path.splitext(file_path)[0]}.json")

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
    await parse_and_write_warnings()
    if path.exists(warnings_json):
        os.remove(warnings_json)

if __name__ == "__main__":
    asyncio.run(main())
