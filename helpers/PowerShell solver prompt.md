# PowerShell solver prompt

Task: Implement AoC 2025 Day XX solver in PowerShell.

Puzzle spec:
[Paste or attach the contents of puzzles/dayXX.md here, or use selection.]

Repository contract:
- Dispatcher: run_day.ps1 will dot-source powershell/dayXX-code.ps1 and pass `-Lines [string[]]` from inputs/dayXX.txt.
- Your solver must be pure (no file IO), define exactly:
    function Solve { param([string[]]$Lines) return @{ Part1 = <int>; Part2 = <int> } }
- No printing inside the solver; return only the hashtable.

Deliverable:
- Create / overwrite file: powershell/dayXX-code.ps1
- Include minimal comment-based help and inline comments.
- Optional: tiny internal “example test” using official sample guarded with `if ($false) { ... }` so it never runs under dispatcher.

Constraints:
- Use only core PowerShell (no external modules).
- Keep runtime O(N) or close.