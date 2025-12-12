#!/usr/bin/env python3
"""
aoc_helper.py — Prepare Advent of Code day resources.
Features:
- Download puzzle spec and input file for a given day.
- Create solver stub files for Python and PowerShell.
Options:
  --lang py | ps | both
  --force to overwrite existing stubs
"""

import argparse
from pathlib import Path
import requests
import sys

ROOT = Path(__file__).resolve().parents[1]
PUZZLES_DIR = ROOT / "puzzles"
INPUTS_DIR = ROOT / "inputs"
PYTHON_DIR = ROOT / "python"
POWERSHELL_DIR = ROOT / "powershell"

SESSION_FILE = ROOT / "config" / "aoc_session.txt"
BASE_URL = "https://adventofcode.com/2025/day/{day}"

PYTHON_STUB = """\
#!/usr/bin/env python3
from typing import List, Tuple

def solve(lines: List[str]) -> Tuple[int, int]:
    # TODO: Implement Part 1 and Part 2 logic
    part1 = 0
    part2 = 0
    return part1, part2
"""

POWERSHELL_STUB = """\
<#
.SYNOPSIS
AoC 2025 Day {day} solver stub.
.DESCRIPTION
Implement Solve function to return a hashtable with Part1 and Part2.
#>
function Solve {
    param([string[]]$Lines)
    # TODO: Implement Part 1 and Part 2 logic
    $part1 = 0
    $part2 = 0
    return @{ Part1 = $part1; Part2 = $part2 }
}
"""

def read_session() -> str:
    if not SESSION_FILE.exists():
        sys.exit("Session file not found. Please create config/aoc_session.txt with your AoC session token.")
    return SESSION_FILE.read_text(encoding="utf-8").strip()

def download_puzzle(day: int) -> None:
    url = BASE_URL.format(day=day)
    puzzle_path = PUZZLES_DIR / f"day{day:02d}.md"
    if puzzle_path.exists():
        print(f"Puzzle already exists: {puzzle_path}")
        return
    print(f"Downloading puzzle for Day {day}...")
    resp = requests.get(url)
    resp.raise_for_status()
    puzzle_path.write_text(resp.text, encoding="utf-8")

def download_input(day: int) -> None:
    url = f"https://adventofcode.com/2025/day/{day}/input"
    input_path = INPUTS_DIR / f"day{day:02d}.txt"
    if input_path.exists():
        print(f"Input already exists: {input_path}")
        return
    print(f"Downloading input for Day {day}...")
    session = read_session()
    resp = requests.get(url, cookies={"session": session})
    resp.raise_for_status()
    input_path.write_text(resp.text.strip(), encoding="utf-8")

def create_stub(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        print(f"Stub already exists: {path}")
        return
    path.write_text(content, encoding="utf-8")
    print(f"Created stub: {path}")

def create_stubs(day: int, lang: str, force: bool) -> None:
    if lang in ("py", "both"):
        create_stub(PYTHON_DIR / f"day{day:02d}-code.py", PYTHON_STUB, force)
    if lang in ("ps", "both"):
        create_stub(POWERSHELL_DIR / f"day{day:02d}-code.ps1", POWERSHELL_STUB.format(day=day), force)

def main():
    ap = argparse.ArgumentParser(description="Prepare AoC day resources.")
    ap.add_argument("--day", type=int, required=True)
    ap.add_argument("--lang", choices=["py", "ps", "both"], default="both")
    ap.add_argument("--force", action="store_true", help="Overwrite existing stubs")
    args = ap.parse_args()

    PUZZLES_DIR.mkdir(exist_ok=True)
    INPUTS_DIR.mkdir(exist_ok=True)
    PYTHON_DIR.mkdir(exist_ok=True)
    POWERSHELL_DIR.mkdir(exist_ok=True)

    download_puzzle(args.day)
    download_input(args.day)
    create_stubs(args.day, args.lang, args.force)

if __name__ == "__main__":
    main()

