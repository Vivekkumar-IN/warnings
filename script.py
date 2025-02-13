import asyncio
import json
import os
from os import path

CURRENT_REPO_DIR = os.getcwd()
YUKKI_MUSIC_DIR = path.abspath(path.join(CURRENT_REPO_DIR, "../YukkiMusic/YukkiMusic"))
OUTPUT_FILE = path.join(CURRENT_REPO_DIR, "warnings.json")
OUTPUT_FILE = path.join(CURRENT_REPO_DIR, "warnings.json")
CHECK_DIR = [YUKKI_MUSIC_DIR]

if not path.exists(YUKKI_MUSIC_DIR):
    print(f"Error: {YUKKI_MUSIC_DIR} not found")
    exit(1)

async def run_pylint():
    cmd = [
        "pylint",
        "--exit-zero",
        "--output-format=json",
        "--indent-string=    ",
        "--reports=no",
        *CHECK_DIR
    ]
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL
    )
    stdout, stderr = await process.communicate()

    if stderr:
        print("Pylint Error:", stderr.decode())
        
    if stdout:
        with open(OUTPUT_FILE, "w") as f:
            f.write(stdout.decode())

async def write_warnings(file_path, warnings):
    file_path = path.join(CURRENT_REPO_DIR, f"{file_path}.pylint.json")
    os.makedirs(path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(warnings, f, indent=4)

async def parse_and_write_warnings():
    if not path.exists(OUTPUT_FILE):
        print(f"{OUTPUT_FILE} Not found")
        return

    with open(OUTPUT_FILE, "r") as f:
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

if __name__ == "__main__":
    asyncio.run(main())
