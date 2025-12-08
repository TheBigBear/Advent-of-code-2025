#!/usr/bin/env python3
import sys
from pathlib import Path

DAY = 8
root = Path(__file__).resolve().parents[1]
in_path = root / "inputs" / f"day{DAY:02d}.txt"

def solve(lines):
    # TODO: implement Part 1 and Part 2 for Day 8
    # 'lines' is a list of strings read from inputs/day08.txt
    return None, None

if __name__ == "__main__":
    data = in_path.read_text(encoding="utf-8").splitlines()
    p1, p2 = solve(data)
    print(f"Part 1: {p1}")
    print(f"Part 2: {p2}")
