
#!/usr/bin/env python3
"""
AoC 2025 dispatcher for Python solvers.
Loads python/dayXX-code.py, reads inputs/dayXX.txt, and prints Part 1 & Part 2.
"""

import argparse
import importlib.util
from pathlib import Path
from typing import Tuple, List

ROOT = Path(__file__).resolve().parent
PYCODE_DIR = ROOT / "python"
INPUTS_DIR = ROOT / "inputs"

def load_solver_module(day: int):
    code_path = PYCODE_DIR / f"day{day:02d}-code.py"
    if not code_path.exists():
        raise FileNotFoundError(f"Python solver not found: {code_path}")
    spec = importlib.util.spec_from_file_location(f"day{day:02d}_code", code_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    if not hasattr(mod, "solve"):
        raise AttributeError(f"{code_path} must define a function solve(lines: List[str]) -> Tuple[int,int]")
    return mod

def read_input(day: int) -> List[str]:
    in_path = INPUTS_DIR / f"day{day:02d}.txt"
    if not in_path.exists():
        raise FileNotFoundError(f"Input not found: {in_path}")
    return in_path.read_text(encoding="utf-8").splitlines()

def main():
    ap = argparse.ArgumentParser(description="Run AoC 2025 Python solution for a given day.")
    ap.add_argument("--day", type=int, required=True, help="Day number (1–25)")
    args = ap.parse_args()
    if not (1 <= args.day <= 25):
        raise ValueError("Day must be between 1 and 25.")

    lines = read_input(args.day)
    mod = load_solver_module(args.day)
    res = mod.solve(lines)
    if (not isinstance(res, tuple)) or len(res) != 2:
        raise TypeError("solve(lines) must return a tuple (part1:int, part2:int)")
    part1, part2 = res
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

if __name__ == "__main__":
    main()
