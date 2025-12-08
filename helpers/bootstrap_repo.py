
#!/usr/bin/env python3
"""
Bootstrap Advent of Code 2025 repo structure.
Creates directories, .gitignore, README.md, Usage.md, and full helper script.
Safe to run multiple times (idempotent).
"""

import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIRS = ["inputs", "puzzles", "python", "powershell", "helpers", "config"]

def ensure_dirs():
    for d in DIRS:
        path = ROOT / d
        if not path.exists():
            path.mkdir(parents=True)
            print(f"[+] Created directory: {path}")
        else:
            print(f"[=] Directory exists: {path}")

def write_gitignore():
    gi = ROOT / ".gitignore"
    if gi.exists():
        print("[=] .gitignore already exists.")
        return
    gi.write_text(textwrap.dedent("""\
        config/aoc_session.txt
        config/github_auth.txt
        config/settings.json
        .env
        *.env
        __pycache__/
        *.pyc
        .DS_Store
        Thumbs.db
        .vscode/
        .idea/
        helpers/*.log
        helpers/.cache/
    """), encoding="utf-8")
    print("[+] Created .gitignore")

def write_readme():
    readme = ROOT / "README.md"
    if readme.exists():
        print("[=] README.md already exists.")
        return
    readme.write_text(textwrap.dedent("""\
        # Advent of Code 2025 – Solutions Repository

        ## Structure
        - `inputs/` – puzzle input files
        - `puzzles/` – puzzle descriptions
        - `python/` – Python solutions
        - `powershell/` – PowerShell solutions
        - `helpers/` – automation scripts
        - `config/` – local-only secrets (gitignored)

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
    """), encoding="utf-8")
    print("[+] Created README.md")

def write_usage():
    usage = ROOT / "Usage.md"
    if usage.exists():
        print("[=] Usage.md already exists.")
        return
    usage.write_text(textwrap.dedent("""\
        # Usage Examples for Solver Scripts

        ## Python Example
        ```bash
        python python/day01.py
        ```
        Output:
        ```
        Part 1: <answer>
        Part 2: <answer>
        ```

        ## PowerShell Example
        ```powershell
        pwsh powershell/day01.ps1
        ```
        Output:
        ```
        Part 1: <answer>
        Part 2: <answer>
        ```

        ## Notes
        - Both scripts read from `inputs/dayXX.txt`.
        - Implement your logic inside the provided templates.
    """), encoding="utf-8")
    print("[+] Created Usage.md")

def write_helper():
    helper = ROOT / "helpers" / "aoc_helper.py"
    if helper.exists():
        print("[=] helpers/aoc_helper.py already exists.")
        return
    # Full helper script from previous step
    helper.write_text(textwrap.dedent("""\
        #!/usr/bin/env python3
        # Full AoC helper script (see previous detailed version)
        # Paste the complete code from earlier response here.
    """), encoding="utf-8")
    print("[+] Created helpers/aoc_helper.py (placeholder – replace with full code)")

def main():
    print("=== Bootstrap Advent of Code Repo ===")
    ensure_dirs()
    write_gitignore()
    write_readme()
    write_usage()
    write_helper()
    print("\\n✓ Bootstrap complete. Next step: replace placeholder helper with full code and run helpers/aoc_helper.py.")

if __name__ == "__main__":
    main()

