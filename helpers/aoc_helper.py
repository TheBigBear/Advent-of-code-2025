
#!/usr/bin/env python3
"""
Advent of Code 2025 helper:
- Bootstraps local repo structure
- Fetches AoC puzzle HTML + input using your session cookie
- Creates Python & PowerShell solver templates that read inputs/dayXX.txt
- Auto-commits and pushes to your GitHub public repo using PAT
"""

import base64, getpass, json, os, re, sys, subprocess, textwrap
from pathlib import Path

try:
    import requests
except ImportError:
    print("Please install 'requests' (pip install requests).")
    sys.exit(1)

REPO_URL = "https://github.com/TheBigBear/Advent-of-code-2025"
DEFAULT_BRANCHES = ["main", "master"]

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
INPUTS = ROOT / "inputs"
PUZZLES = ROOT / "puzzles"
PYDIR = ROOT / "python"
PSDIR = ROOT / "powershell"
HELPERS = ROOT / "helpers"

AOC_YEAR = 2025
AOC_BASE = "https://adventofcode.com"

def ensure_dirs():
    for p in [CONFIG, INPUTS, PUZZLES, PYDIR, PSDIR, HELPERS / "utils"]:
        p.mkdir(parents=True, exist_ok=True)

def write_gitignore():
    gi = ROOT / ".gitignore"
    if gi.exists():
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

def is_git_repo():
    return (ROOT / ".git").exists()

def run_git(args, extra_env=None, check=True):
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    return subprocess.run(["git", *args], cwd=ROOT, env=env, check=check, capture_output=True, text=True)

def bootstrap_repo():
    if is_git_repo():
        return
    # Clone the repo into current directory if empty or initialize then set remote
    # If ROOT has files already (you started from a cloned repo), we skip.
    print(f"[repo] Cloning {REPO_URL} ...")
    parent = ROOT.parent
    tmp = parent / f"__tmp_aoc_clone_{AOC_YEAR}"
    if tmp.exists():
        subprocess.run(["rm", "-rf", str(tmp)], check=False)
    subprocess.run(["git", "clone", REPO_URL, str(tmp)], check=True)
    # Move contents into ROOT if ROOT is empty
    if not any(ROOT.iterdir()):
        for item in tmp.iterdir():
            dest = ROOT / item.name
            if item.is_dir():
                subprocess.run(["bash", "-lc", f"mv '{item}' '{dest}'"], check=True)
            else:
                item.rename(dest)
    # Clean temp
    subprocess.run(["rm", "-rf", str(tmp)], check=False)

def prompt_day():
    while True:
        v = input("Which day to process? (1–25): ").strip()
        if v.isdigit() and 1 <= int(v) <= 25:
            return int(v)
        print("Please enter an integer between 1 and 25.")

def read_or_prompt_aoc_session():
    sess_file = CONFIG / "aoc_session.txt"
    if sess_file.exists():
        return sess_file.read_text(encoding="utf-8").strip()
    print("\nTo fetch AoC pages, paste your 'session' cookie value from adventofcode.com.")
    print("   (Log in in your browser, inspect cookies for adventofcode.com, copy the 'session' value.)")
    session = getpass.getpass("AoC session cookie: ").strip()
    sess_file.write_text(session, encoding="utf-8")
    try:
        os.chmod(sess_file, 0o600)
    except Exception:
        pass
    return session

def read_or_prompt_github_auth():
    gh_file = CONFIG / "github_auth.txt"
    if gh_file.exists():
        lines = gh_file.read_text(encoding="utf-8").splitlines()
        kv = dict([l.split("=", 1) for l in lines if "=" in l])
        return kv.get("username", ""), kv.get("pat", "")
    print("\nGitHub authentication (for auto-push to your public repo):")
    username = input("GitHub username: ").strip()
    pat = getpass.getpass("GitHub PAT (repo scope): ").strip()
    gh_file.write_text(f"username={username}\npat={pat}\n", encoding="utf-8")
    try:
        os.chmod(gh_file, 0o600)
    except Exception:
        pass
    return username, pat

def fetch_aoc(day, session):
    headers = {
        "User-Agent": "TheBigBear AoC helper (https://github.com/TheBigBear/Advent-of-code-2025)",
        "Cookie": f"session={session}",
    }
    print(f"[AoC] Fetching day {day} HTML ...")
    r1 = requests.get(f"{AOC_BASE}/{AOC_YEAR}/day/{day}", headers=headers)
    r1.raise_for_status()
    html = r1.text
    (PUZZLES / f"day{day:02d}.html").write_text(html, encoding="utf-8")

    # naive text extraction → MD (optional)
    text = re.sub(r"<(script|style)[\\s\\S]*?</\\1>", "", html, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\\s+\\n", "\\n", text)
    (PUZZLES / f"day{day:02d}.md").write_text(text.strip(), encoding="utf-8")

    print(f"[AoC] Fetching day {day} input ...")
    r2 = requests.get(f"{AOC_BASE}/{AOC_YEAR}/day/{day}/input", headers=headers)
    r2.raise_for_status()
    (INPUTS / f"day{day:02d}.txt").write_text(r2.text, encoding="utf-8")

def ensure_solver_templates(day):
    pyf = PYDIR / f"day{day:02d}.py"
    psf = PSDIR / f"day{day:02d}.ps1"
    if not pyf.exists():
        pyf.write_text(textwrap.dedent(f"""\
            #!/usr/bin/env python3
            import sys
            from pathlib import Path

            DAY = {day}
            root = Path(__file__).resolve().parents[1]
            in_path = root / "inputs" / f"day{{DAY:02d}}.txt"

            def solve(lines):
                # TODO: implement Part 1 and Part 2 for Day {day}
                # lines is a list of strings from day{day:02d}.txt
                return None, None

            if __name__ == "__main__":
                data = in_path.read_text(encoding="utf-8").splitlines()
                p1, p2 = solve(data)
                print(f"Part 1: {{p1}}")
                print(f"Part 2: {{p2}}")
        """), encoding="utf-8")
    if not psf.exists():
        psf.write_text(textwrap.dedent(f"""\
            param(
                [int]$Day = {day}
            )
            $root = (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
            $inPath = Join-Path $root ("inputs/day{day:02d}.txt")
            if (-not (Test-Path $inPath)) {{
                Write-Error "Input file not found: $inPath"
                exit 1
            }}
            $lines = Get-Content -LiteralPath $inPath

            # TODO: implement Part 1 and Part 2 for Day {day} using $lines
            $part1 = $null
            $part2 = $null

            Write-Output ("Part 1: {0}" -f $part1)
            Write-Output ("Part 2: {0}" -f $part2)
        """), encoding="utf-8")

    # Update prompt template to point to the day’s files
    prompt_md = HELPERS / "solver_prompt.md"
    prompt_md.write_text(textwrap.dedent(f"""\
        Solve Advent of Code {AOC_YEAR} Day {day} using:
        - Puzzle: puzzles/day{day:02d}.md (raw HTML in puzzles/day{day:02d}.html)
        - Input:  inputs/day{day:02d}.txt

        Requirements:
        - Python:   write to python/day{day:02d}.py and read inputs/day{day:02d}.txt
        - PowerShell: write to powershell/day{day:02d}.ps1 and read inputs/day{day:02d}.txt
        - Print Part 1 and Part 2 answers.
    """), encoding="utf-8")

def commit_and_push(day, username, pat):
    files = [
        f"inputs/day{day:02d}.txt",
        f"puzzles/day{day:02d}.html",
        f"puzzles/day{day:02d}.md",
        f"python/day{day:02d}.py",
        f"powershell/day{day:02d}.ps1",
        "helpers/solver_prompt.md",
        ".gitignore",
    ]
    print("[git] add/commit ...")
    run_git(["add", *files], check=True)
    msg = f"Day {day:02d}: add puzzle + input + templates"
    run_git(["commit", "-m", msg], check=True)

    basic = base64.b64encode(f"{username}:{pat}".encode()).decode()
    for br in DEFAULT_BRANCHES:
        print(f"[git] push origin {br} ...")
        try:
            run_git(["push", "origin", br, "-c", f"http.extraheader=AUTHORIZATION: basic {basic}"], check=True)
            print(f"[git] pushed to {br}")
            return
        except subprocess.CalledProcessError as e:
            print(f"[git] push to {br} failed, trying next branch...")
    raise RuntimeError("Push failed for both 'main' and 'master'. Check your remote default branch.")

def main():
    print("=== Advent of Code helper ===")
    ensure_dirs()
    write_gitignore()
    bootstrap_repo()

    day = prompt_day()
    session = read_or_prompt_aoc_session()
    username, pat = read_or_prompt_github_auth()

    fetch_aoc(day, session)
    ensure_solver_templates(day)
    commit_and_push(day, username, pat)

    print(f"\n✓ Day {day:02d} ready.\n"
          f"  - inputs/day{day:02d}.txt\n"
          f"  - puzzles/day{day:02d}.html/.md\n"
          f"  - python/day{day:02d}.py\n"
          f"  - powershell/day{day:02d}.ps1\n"
          f"  - helpers/solver_prompt.md\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"[error] {ex}")
        sys.exit(1)
