# Advent of Code 2025 – Solutions Repository

This repository is structured to help me organise and solve Advent of Code 2025 puzzles in **Python** and **PowerShell**, with automation for fetching puzzles and inputs, and pushing updates to my public GitHub repo.

---

## Structure
- `inputs/` – puzzle input files
- `puzzles/` – puzzle descriptions
- `python/` – Python solutions
- `powershell/` – PowerShell solutions
- `helpers/` – automation scripts
- `config/` – local-only secrets (gitignored)

---

## Quick Start
1. Clone your repo:
   ```bash
   git clone https://github.com/TheBigBear/Advent-of-code-2025.git
   cd Advent-of-code-2025
   ```
2. Run bootstrap:
   ```bash
   python bootstrap_repo.py
   ```
3. Fetch a puzzle:
   ```bash
   python helpers/aoc_helper.py
   ```
See `Usage.md` for detailed examples.

---

```markdown
Advent-of-code-2025/
│
├─ README.md
├─ .gitignore
│
├─ inputs/           # raw inputs (text) – one per day
│   └─ day01.txt
│
├─ puzzles/          # puzzle pages – stored locally for reference
│   ├─ day01.html    # raw HTML (verbatim from AoC)
│   └─ day01.md      # lightweight MD extraction (optional)
│
├─ python/           # your Python solutions; each reads inputs/dayXX.txt
│   └─ day01.py
│
├─ powershell/       # your PowerShell solutions; each reads inputs/dayXX.txt
│   └─ day01.ps1
│
└─ helpers/          # automation & prompts
    ├─ aoc_helper.py         # interactive helper (fetch + commit + push)
    ├─ solver_prompt.md      # reusable prompt for solution generation
    └─ utils/                # small helper modules, if needed later
        └─ __init__.py
```

