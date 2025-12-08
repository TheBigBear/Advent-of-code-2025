"""
AoC 2025 Day 1: Secret Entrance (Python solver)

Contract:
- Expose exactly: solve(lines: list[str]) -> tuple[int, int]
- Pure function: no file I/O, no printing inside solve.
- Runtime: O(N), suitable for large inputs.
"""

from typing import List, Tuple


def solve(lines: List[str]) -> Tuple[int, int]:
    """
    Compute Part 1 and Part 2 for AoC 2025 Day 1.

    Input:
        lines: list of strings, each representing a rotation instruction like "L68" or "R14".

    Returns:
        (part1, part2)
        - Part 1: number of times the dial ends at 0 after a rotation.
        - Part 2: number of times the dial points at 0 during any click (including intermediate positions).
    """
    # Dial properties
    MOD = 100  # dial positions: 0..99
    pos = 50   # starting position

    part1 = 0
    part2 = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        direction = line[0]
        steps = int(line[1:])

        # For Part 2, count intermediate zeros
        # Compute how many times we cross 0 during this rotation
        if direction == "L":
            # Moving left: decreasing position
            # Each full cycle of 100 steps crosses 0 once
            full_cycles = steps // MOD
            part2 += full_cycles
            # Remaining steps
            rem = steps % MOD
            # If pos - rem < 0, we cross 0 once more
            if pos - rem < 0:
                part2 += 1
            pos = (pos - steps) % MOD
        else:  # direction == "R"
            full_cycles = steps // MOD
            part2 += full_cycles
            rem = steps % MOD
            # If pos + rem >= 100, we cross 0 once more
            if pos + rem >= MOD:
                part2 += 1
            pos = (pos + steps) % MOD

        # For Part 1, check if we end at 0
        if pos == 0:
            part1 += 1

    return (part1, part2)


if __name__ == "__main__":
    # Example from puzzle description
    sample = [
        "L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"
    ]
    p1, p2 = solve(sample)
    # Expected: Part 1 = 3, Part 2 = 6
    assert p1 == 3, f"Expected 3, got {p1}"
    assert p2 == 6, f"Expected 6, got {p2}"
    print("Sample test passed:", p1, p2)
