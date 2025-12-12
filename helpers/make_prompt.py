#!/usr/bin/env python3
"""
make_prompt.py — Build AoC solver prompt.
Options:
--full-input: Include entire input file
--include-stub: Include sample solver stub
--example-output: Include expected output format
"""

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUZZLES = ROOT / "puzzles"
HELPERS = ROOT / "helpers"
INPUTS = ROOT / "inputs"

CONTRACTS = {
    "py": HELPERS / "solver_contract_python.md",
    "ps": HELPERS / "solver_contract_powershell.md",
}

DELIVERABLES = {
    "py": "python/day{day:02d}-code.py",
    "ps": "powershell/day{day:02d}-code.ps1",
}

STUBS = {
    "py": """\
from typing import List, Tuple

def solve(lines: List[str]) -> Tuple[int, int]:
    # TODO: Implement Part 1 and Part 2 logic
    part1 = 0
    part2 = 0
    return part1, part2
""",
    "ps": """\
function Solve {
    param([string[]]$Lines)
    # TODO: Implement Part 1 and Part 2 logic
    $part1 = 0
    $part2 = 0
    return @{ Part1 = $part1; Part2 = $part2 }
}
"""
}

def read_text(path: Path, label: str) -> str:
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")
    return path.read_text(encoding="utf-8")

def build_prompt(day: int, lang: str, full_input: bool, include_stub: bool, example_output: bool) -> str:
    puzzle_md = read_text(PUZZLES / f"day{day:02d}.md", "Puzzle markdown")
    contract_md = read_text(CONTRACTS[lang], "Solver contract")
    input_content = read_text(INPUTS / f"day{day:02d}.txt", "Input file")
    sample_input = input_content if full_input else input_content[:500] + "\n...[truncated]"
    deliverable = DELIVERABLES[lang].format(day=day)

    header = f"Advent of Code 2025 — Day {day:02d} solver request ({'Python' if lang=='py' else 'PowerShell'})"
    run_instructions = f"To run:\n- Python: `python run_day.py --day {day}`\n- PowerShell: `./run_day.ps1 -Day {day}`\n"
    output_format = "Expected output format:\nPart 1: <integer>\nPart 2: <integer>\n" if example_output else ""
    stub_section = f"Sample solver stub:\n{STUBS[lang]}" if include_stub else ""

    return f"""{header}

Puzzle spec:
{puzzle_md}

Solver contract:
{contract_md}

Deliverable:
Implement in {deliverable}.

Sample input:
{sample_input}

{run_instructions}
{output_format}
{stub_section}
"""

def main():
    ap = argparse.ArgumentParser(description="Build AoC solver prompt.")
    ap.add_argument("--day", type=int, required=True)
    ap.add_argument("--lang", choices=["py", "ps"], required=True)
    ap.add_argument("--output", type=str)
    ap.add_argument("--full-input", action="store_true")
    ap.add_argument("--include-stub", action="store_true")
    ap.add_argument("--example-output", action="store_true")
    args = ap.parse_args()

    prompt = build_prompt(args.day, args.lang, args.full_input, args.include_stub, args.example_output)
    if args.output:
        Path(args.output).write_text(prompt, encoding="utf-8")
    else:
        print(prompt)

if __name__ == "__main__":
    main()

