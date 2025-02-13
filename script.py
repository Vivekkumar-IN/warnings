import asyncio
import json
import os

CHECK_DIR = ["YukkiMusic"]
OUTPUT_FILE = "current_repo/warnings.json"

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
    stdout, _ = await process.communicate()

    if stdout:
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)  # Ensure directory exists
        with open(OUTPUT_FILE, "w") as f:
            f.write(stdout.decode())

async def write_warnings(file_path, warnings):
    warning_file = f"current_repo/{file_path}.pylint.json"
    os.makedirs(os.path.dirname(warning_file), exist_ok=True)

    with open(warning_file, "w") as f:
        json.dump(warnings, f, indent=4)

async def parse_and_write_warnings():
    if not os.path.exists(OUTPUT_FILE):
        return

    with open(OUTPUT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return

    warnings_by_path = {}
    for entry in data:
        path = entry["path"]
        warnings_by_path.setdefault(path, []).append(entry)

    await asyncio.gather(*(write_warnings(file_path, warnings) for file_path, warnings in warnings_by_path.items()))

async def main():
    await run_pylint()
    await parse_and_write_warnings()

if __name__ == "__main__":
    asyncio.run(main())
