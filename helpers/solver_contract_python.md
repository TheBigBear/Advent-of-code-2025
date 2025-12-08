# AoC 2025 Python Solver Contract

Dispatcher: run_day.py will dynamically load python/dayXX-code.py and pass:

    lines: list[str]  # from inputs/dayXX.txt

Your solver must:
- Be pure (no file I/O).
- Define exactly:

    def solve(lines: list[str]) -> tuple[int, int]:
        """
        Return (Part 1, Part 2) as integers.
        """

- No printing inside solve().
- No external libraries (only Python standard library).
- Runtime should be efficient (O(N) or close).

Deliverable:
- Write code to: python/dayXX-code.py
- Include minimal docstring and inline comments.
- Optional: tiny internal test using official sample (guarded by if __name__ == "__main__":)
  but do not read real input files.
