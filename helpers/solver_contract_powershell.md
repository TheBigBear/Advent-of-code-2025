# AoC 2025 PowerShell Solver Contract

Dispatcher: run_day.ps1 will dot-source powershell/dayXX-code.ps1 and pass:

    -Lines [string[]]  # from inputs/dayXX.txt

Your solver must:
- Be pure (no file I/O).
- Define exactly:

    function Solve {
        param([string[]]$Lines)
        return @{ Part1 = <int>; Part2 = <int> }
    }

- No printing inside Solve.
- Use only core PowerShell (no external modules).
- Runtime should be efficient (O(N) or close).

Deliverable:
- Write code to: powershell/dayXX-code.ps1
- Include minimal comment-based help and inline comments.
- Optional: tiny internal test using official sample guarded with:
    if ($false) {
        # sample-driven self-check (never runs under dispatcher)
    }
  so it never runs under dispatcher.
