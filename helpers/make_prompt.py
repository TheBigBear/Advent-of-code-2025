
#!/usr/bin/env python3
"""
make_prompt.py — Combine AoC puzzle + solver contract into a single prompt
Usage:
  python helpers/make_prompt.py --day 1 --lang py
  python helpers/make_prompt.py --day 3 --lang ps
  python helpers/make_prompt.py --day 7 --lang py --output /tmp/day07-py-prompt.txt

This prints (or writes) a prompt with:
- Puzzle spec from puzzles/dayXX.md
- Solver contract from helpers/solver_contract_python.md or helpers/solver_contract_powershell.md
- Clear deliverable instructions pointing to python/dayXX-code.py or powershell/dayXX-code.ps1

No editor needed—just copy the printed prompt into Copilot Chat.
"""

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PUZZLES = ROOT / "puzzles"
HELPERS = ROOT / "helpers"

CONTRACTS = {
    "py": HELPERS / "solver_contract_python.md",
    "ps": HELPERS / "solver_contract_powershell.md",
}

DELIVERABLES = {
    "py": "python/day{day:02d}-code.py",
    "ps": "powershell/day{day:02d}-code.ps1",
}

def read_text(path: Path, label: str) -> str:
    if not path.exists():
        raise FileNotFoundError(f"{label} not found: {path}")
    return path.read_text(encoding="utf-8")

def build_prompt(day: int, lang: str) -> str:
    if lang not in CONTRACTS:
        raise ValueError("lang must be 'py' or 'ps'.")

    puzzle_path = PUZZLES / f"day{day:02d}.md"
    contract_path = CONTRACTS[lang]
    deliverable = DELIVERABLES[lang].format(day=day)

    puzzle_md = read_text(puzzle_path, "Puzzle markdown")
    contract_md = read_text(contract_path, "Solver contract")

    header = f"Advent of Code 2025 — Day {day:02d} solver request ({'Python' if lang=='py' else 'PowerShell'})"
    prompt = f"""\
{header}

Puzzle spec (from puzzles/day{day:02d}.md):
