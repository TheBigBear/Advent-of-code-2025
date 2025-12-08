"""
AoC 2025 Day 2: Gift Shop (Python solver)

Repository contract:
- Expose exactly: solve(lines: list[str]) -> tuple[int, int]
- Pure function: no file I/O and no printing inside solve.
- Runtime: near O(N) — avoids per-ID scanning via closed-form summation.
"""
from typing import List, Tuple


def _sum_integers(a: int, b: int) -> int:
    """Sum of consecutive integers from a to b inclusive.
    Returns 0 if b < a. Works with Python big ints exactly.
    """
    if b < a:
        return 0
    count = b - a + 1
    # Use parity to avoid fractional intermediate
    if (count % 2) == 0:
        return (count // 2) * (a + b)
    else:
        return ((a + b) // 2) * count


def _pow10(n: int) -> int:
    """Exact integer 10**n (explicit helper for clarity)."""
    return 10 ** n


def _sum_invalid_in_range(lo: int, hi: int) -> int:
    """Closed-form sum of all invalid IDs n in [lo, hi],
    where invalid means n = x * (10**m + 1) with x being m-digit (no leading zeros).

    We iterate over m (half-length of the ID), translate bounds on n into bounds on x,
    intersect with the m-digit window, and sum via arithmetic series.
    """
    if hi < lo:
        lo, hi = hi, lo
    if hi < 1:
        return 0
    if lo < 1:
        lo = 1

    total = 0

    digits_end = len(str(hi))  # robust digit count
    for m in range(1, (digits_end // 2) + 1):
        pow10_m = _pow10(m)
        pow10_m_1 = _pow10(m - 1)
        factor = pow10_m + 1  # n = x * (10^m + 1)

        # x must be m-digit: x in [10^(m-1), 10^m - 1]
        x_min_mdigit = pow10_m_1
        x_max_mdigit = pow10_m - 1

        # Translate n-range to x-range via division.
        # ceil(lo / factor), floor(hi / factor) — factor > 0 always.
        x_min = (lo + factor - 1) // factor
        x_max = hi // factor

        # Intersect with the m-digit window.
        if x_min < x_min_mdigit:
            x_min = x_min_mdigit
        if x_max > x_max_mdigit:
            x_max = x_max_mdigit

        if x_max < x_min:
            continue

        sum_x = _sum_integers(x_min, x_max)
        total += factor * sum_x

    return total


def solve(lines: List[str]) -> Tuple[int, int]:
    """Compute Part 1 and Part 2 for AoC 2025 Day 2: Gift Shop.

    Input format: one long line (possibly wrapped in the file) of comma-separated ranges
    of the form "start-end", e.g., "11-22,95-115,...".

    Returns:
        (part1, part2)
        - Part 1: sum of all invalid IDs across all ranges.
        - Part 2: 0 (not specified in the provided puzzle spec).
    """
    # Join lines to handle wrapping; then split by commas and trim parts.
    text = ''.join(lines)
    parts = [p.strip() for p in text.split(',') if p.strip()]

    part1 = 0
    for spec in parts:
        ab = [s.strip() for s in spec.split('-')]
        if len(ab) != 2:
            continue
        a = int(ab[0])
        b = int(ab[1])
        part1 += _sum_invalid_in_range(a, b)

    part2 = 0  # Not specified in given spec
    return (part1, part2)


if __name__ == "__main__":
    # Tiny internal example test using the official sample; no file I/O.
    sample = [
        '11-22,95-115,998-1012,1188511880-1188511890,222220-222224,',
        '1698522-1698528,446443-446449,38593856-38593862,565653-565659,',
        '824824821-824824827,2121212118-2121212124'
    ]
    p1, p2 = solve(sample)
    # Expected Part1: 1227775554; Part2: 0
    assert p1 == 1227775554, (p1, p2)
