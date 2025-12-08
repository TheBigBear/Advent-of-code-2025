# Python solver prompt

Task: Implement AoC 2025 Day XX solver in Python.

Puzzle spec:
[Paste or attach the contents of puzzles/dayXX.md here, or use selection.]

Repository contract:
- Dispatcher: run_day.py will load python/dayXX-code.py and pass `lines: list[str]` from inputs/dayXX.txt.
- Your solver must be pure (no file IO), expose exactly:
    def solve(lines: list[str]) -> tuple[int, int]
- Return (Part 1, Part 2) as integers.
- No side effects. No printing.

Deliverable:
- Create / overwrite file: python/dayXX-code.py
- Include minimal docstring and inline comments.
- If helpful, include a tiny internal “example test” using the official sample (guarded by `if __name__ == "__main__":`) but do not read real input files.

Constraints:
- Do not import any non-standard libraries.
- Keep runtime O(N) or close, suitable for large inputs.
