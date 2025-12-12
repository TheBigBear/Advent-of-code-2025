# Advent of Code 2025 — Quick Start Guide

## 1. Prepare Day Resources
Download puzzle, input, and create solver stubs:
```bash
python helpers/aoc_helper.py --day 3 --lang both --force
```

**Options:**
- `--lang py | ps | both`: Choose language(s) for stubs.
- `--force`: Overwrite existing stubs.

---

## 2. Generate Prompt for Copilot
Create a detailed prompt with full input, example output, and solver stub:

For **Python**:
```bash
python helpers/make_prompt.py --day 3 --lang py --full-input --include-stub --example-output --output prompts/day03-prompt-full.md
```

For **PowerShell**:
```bash
python helpers/make_prompt.py --day 3 --lang ps --full-input --include-stub --example-output --output prompts/day03-prompt-ps-full.md
```

**Options:**
- `--full-input`: Include entire input in prompt.
- `--include-stub`: Add sample solver stub.
- `--example-output`: Show expected output format.

---

## 3. Copy Prompt into Copilot Chat
Paste the generated prompt into Copilot Chat to get the solver code.

---

## 4. Run the Solution
Once Copilot returns the code:
```bash
python run_day.py --day 3
```
or
```powershell
./run_day.ps1 -Day 3
```

---

## 5. Automate All Actions for a Specific Day
Instead of running multiple commands manually, use the helper script `generate_day_prompts.py`:

```bash
python helpers/generate_day_prompts.py --day 5
```

This will:
- Download puzzle and input for Day 5.
- Create solver stubs for Python and PowerShell.
- Generate **4 prompt files** in `prompts/`:
  - `day05-prompt.md` (Python, sample input)
  - `day05-prompt-full.md` (Python, full input)
  - `day05-prompt-ps.md` (PowerShell, sample input)
  - `day05-prompt-ps-full.md` (PowerShell, full input)

Use this when you want **all actions done for one day in one go**.

