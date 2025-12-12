#!/usr/bin/env python3
"""
generate_day_prompts.py — Automate AoC day setup and prompt generation.

Features:
- Prepares resources (puzzle, input, solver stubs for both languages).
- Generates both sample and full prompts for Python and PowerShell.
- Saves prompts in the 'prompts' directory:
    - dayXX-prompt.md (sample/truncated input)
    - dayXX-prompt-full.md (full input)
"""

import subprocess
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[1]
HELPERS = ROOT / "helpers"
PROMPTS_DIR = ROOT / "prompts"

def run_command(cmd: list):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def main():
    ap = argparse.ArgumentParser(description="Generate AoC prompts for a specific day.")
    ap.add_argument("--day", type=int, required=True, help="Day number (1–25)")
    args = ap.parse_args()

    day = args.day
    PROMPTS_DIR.mkdir(exist_ok=True)

    # Step 1: Prepare resources
    run_command(["python", str(HELPERS / "aoc_helper.py"), "--day", str(day), "--lang", "both", "--force"])

    # Step 2: Generate prompts for Python
    run_command([
        "python", str(HELPERS / "make_prompt.py"),
        "--day", str(day), "--lang", "py",
        "--include-stub", "--example-output",
        "--output", str(PROMPTS_DIR / f"day{day:02d}-prompt.md")
    ])
    run_command([
        "python", str(HELPERS / "make_prompt.py"),
        "--day", str(day), "--lang", "py",
        "--full-input", "--include-stub", "--example-output",
        "--output", str(PROMPTS_DIR / f"day{day:02d}-prompt-full.md")
    ])

    # Step 3: Generate prompts for PowerShell
    run_command([
        "python", str(HELPERS / "make_prompt.py"),
        "--day", str(day), "--lang", "ps",
        "--include-stub", "--example-output",
        "--output", str(PROMPTS_DIR / f"day{day:02d}-prompt-ps.md")
    ])
    run_command([
        "python", str(HELPERS / "make_prompt.py"),
        "--day", str(day), "--lang", "ps",
        "--full-input", "--include-stub", "--example-output",
        "--output", str(PROMPTS_DIR / f"day{day:02d}-prompt-ps-full.md")
    ])

    print(f"\n✅ All prompts for Day {day} have been generated in {PROMPTS_DIR}")

if __name__ == "__main__":
    main()

