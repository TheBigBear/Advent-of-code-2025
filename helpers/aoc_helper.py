#!/usr/bin/env python3
"""
Advent of Code 2025 helper:
- Validates AoC 'session' cookie (via /settings) then fetches day HTML + input
- Creates Python & PowerShell solver templates (read inputs/dayXX.txt)
- Auto-commits and pushes to your GitHub repo using PAT via a non-persistent header
- Supports --day argument for non-interactive runs
"""

import argparse
import base64
import getpass
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path

try:
    import requests
except ImportError:
    print("Missing 'requests'. Install it in your venv: pip install requests")
    sys.exit(1)

# --- Repo paths & AoC constants ---
ROOT     = Path(__file__).resolve().parents[1]
CONFIG   = ROOT / "config"
INPUTS   = ROOT / "inputs"
PUZZLES  = ROOT / "puzzles"
PYDIR    = ROOT / "python"
PSDIR    = ROOT / "powershell"
HELPERS  = ROOT / "helpers"

AOC_YEAR = 2025
AOC_BASE = "https://adventofcode.com"

# --- Utility: git runner ---
def run_git(args, check=True, capture=True):
    """Run git command in repo root."""
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        capture_output=capture,
        text=True
    )

# --- Ensure directory structure exists ---
def ensure_dirs():
    for p in (CONFIG, INPUTS, PUZZLES, PYDIR, PSDIR, HELPERS):
        p.mkdir(parents=True, exist_ok=True)

# --- Session & PAT readers (prompt if missing) ---
def read_or_prompt_aoc_session():
    """Read AoC cooke from config/aoc_session.txt or prompt once."""
    sess_file = CONFIG / "aoc_session.txt"
    if sess_file.exists():
        return sess_file.read_text(encoding="utf-8").strip()
    print("\nTo fetch AoC pages, paste your 'session' cookie value from adventofcode.com.")
    s = getpass.getpass("AoC session cookie: ").strip()
    sess_file.write_text(s, encoding="utf-8")
    try: os.chmod(sess_file, 0o600)
    except Exception: pass
    return s

def read_or_prompt_github_auth():
    """Read GitHub username+PAT from config/github_auth.txt or prompt once."""
    gh_file = CONFIG / "github_auth.txt"
    if gh_file.exists():
        lines = gh_file.read_text(encoding="utf-8").splitlines()
        kv = dict([l.split("=", 1) for l in lines if "=" in l])
        return kv.get("username", ""), kv.get("pat", "")
    print("\nGitHub auth (for auto-push to your public repo):")
    username = input("GitHub username: ").strip()
    pat = getpass.getpass("GitHub PAT (repo scope): ").strip()
    gh_file.write_text(f"username={username}\npat={pat}\n", encoding="utf-8")
    try: os.chmod(gh_file, 0o600)
    except Exception: pass
    return username, pat

# --- Hardened AoC cookie helpers ---
def _clean_session(raw: str) -> str:
    """
    Normalize the AoC session cookie value:
    - strip quotes/whitespace
    - remove accidental 'session=' prefix
    - basic length sanity check
    """
    s = raw.strip().strip('"').strip("'")
    if not s:
        raise ValueError("AoC session cookie is empty.")
    if "session=" in s:
        s = s.replace("session=", "").strip()
    if " " in s:
        s = s.replace(" ", "")
    if len(s) < 40:  # AoC sessions are long opaque strings
        raise ValueError("AoC session cookie looks too short; paste the exact value from your browser.")
    return s

def _headers(session_value: str) -> dict:
    return {
        "User-Agent": "TheBigBear AoC helper (https://github.com/TheBigBear/Advent-of-code-2025)",
        "Cookie": f"session={session_value}",
    }

def _get(url: str, headers: dict, expect_text: bool = True):
    """
    GET with small retry loop and clearer errors on 400.
    Returns response text (default) or bytes if expect_text=False.
    """
    import time

    last_err = None
    for attempt in range(1, 4):
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 400:
                raise requests.HTTPError(
                    f"400 from {url} — Advent of Code rejected the session cookie. "
                    "Paste a fresh cookie (log in to AoC, copy exact 'session' value)."
                )
            r.raise_for_status()
            return r.text if expect_text else r.content
        except requests.HTTPError as e:
            if hasattr(r, "status_code") and r.status_code in (500, 502, 503, 504):
                last_err = e
                time.sleep(1.2)
                continue
            raise
        except Exception as e:
            last_err = e
            time.sleep(0.8)
    if last_err:
        raise last_err

def prompt_and_store_session():
    """Ask the user for a fresh session, store it, return normalized value."""
    fresh = getpass.getpass("Paste fresh AoC 'session' value: ").strip()
    fresh = _clean_session(fresh)
    sess_path = CONFIG / "aoc_session.txt"
    sess_path.write_text(fresh, encoding="utf-8")
    try: os.chmod(sess_path, 0o600)
    except Exception: pass
    return fresh

# --- AoC fetch main ---
def fetch_aoc(day: int, session_raw: str):
    """
    Validates the session by visiting /settings, then fetches:
      - day HTML      -> puzzles/dayXX.html
      - optional MD   -> puzzles/dayXX.md
      - input         -> inputs/dayXX.txt   (skips if already present)
    """
    # Normalize cookie value
    try:
        session = _clean_session(session_raw)
    except ValueError as e:
        print(f"[AoC] Session value invalid: {e}")
        print("[AoC] Prompting for a fresh cookie...")
        session = prompt_and_store_session()

    h = _headers(session)

    # 1) Validate session by visiting settings page
    print("[AoC] Validating session...")
    settings_html = _get(f"{AOC_BASE}/settings", h)
    if "Log In" in settings_html or "login" in settings_html.lower():
        print("[AoC] You appear to be logged out. Let's refresh your cookie.")
        session = prompt_and_store_session()
        h = _headers(session)
        settings_html = _get(f"{AOC_BASE}/settings", h)
        if "Log In" in settings_html or "login" in settings_html.lower():
            raise RuntimeError(
                "AoC still indicates you're not logged in. Verify the session cookie from your browser."
            )

    # 2) Fetch puzzle HTML
    print(f"[AoC] Fetching day {day} HTML ...")
    html = _get(f"{AOC_BASE}/{AOC_YEAR}/day/{day}", h)
    (PUZZLES / f"day{day:02d}.html").write_text(html, encoding="utf-8")

    # Optional MD extraction (simple tag stripping)
    md = re.sub(r"<(script|style)[\s\S]*?</\1>", "", html, flags=re.I)
    md = re.sub(r"<[^>]+>", "", md)
    md = re.sub(r"\s+\n", "\n", md)
    (PUZZLES / f"day{day:02d}.md").write_text(md.strip(), encoding="utf-8")

    # 3) Fetch input (skip if already present)
    in_file = INPUTS / f"day{day:02d}.txt"
    if in_file.exists():
        print(f"[AoC] Input already present: {in_file} (skipping fetch)")
    else:
        print(f"[AoC] Fetching day {day} input ...")
        input_text = _get(f"{AOC_BASE}/{AOC_YEAR}/day/{day}/input", h)
        in_file.write_text(input_text, encoding="utf-8")

# --- Solver templates ---
def ensure_solver_templates(day: int):
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
                # 'lines' is a list of strings read from inputs/day{day:02d}.txt
                return None, None

            if __name__ == "__main__":
                data = in_path.read_text(encoding="utf-8").splitlines()
                p1, p2 = solve(data)
                print(f"Part 1: {{p1}}")
                print(f"Part 2: {{p2}}")
        """), encoding="utf-8")

    if not psf.exists():
        psf.write_text(textwrap.dedent(f"""\
            param([int]$Day = {day})
            $root   = (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
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

    # Update solver prompt (optional convenience)
    prompt_md = HELPERS / "solver_prompt.md"
    prompt_md.write_text(textwrap.dedent(f"""\
        Solve Advent of Code {AOC_YEAR} Day {day} using:
        - Puzzle: puzzles/day{day:02d}.md (raw HTML in puzzles/day{day:02d}.html)
        - Input:  inputs/day{day:02d}.txt

        Requirements:
        - Python:     write to python/day{day:02d}.py and read inputs/day{day:02d}.txt
        - PowerShell: write to powershell/day{day:02d}.ps1 and read inputs/day{day:02d}.txt
        - Print Part 1 and Part 2 answers.
    """), encoding="utf-8")

# --- Commit & push with non-persistent PAT header ---

def commit_and_push(day: int, username: str, pat: str):
    files = [
        f"inputs/day{day:02d}.txt",
        f"puzzles/day{day:02d}.html",
        f"puzzles/day{day:02d}.md",
        f"python/day{day:02d}.py",
        f"powershell/day{day:02d}.ps1",
        "helpers/solver_prompt.md",
    ]
    if (ROOT / ".gitignore").exists():
        files.append(".gitignore")

    print("[git] add/commit ...")
    try:
        run_git(["add", *files], check=True)
        msg = f"Day {day:02d}: add puzzle + input + templates"
        run_git(["commit", "-m", msg], check=True)
    except subprocess.CalledProcessError as e:
        # Proceed even if there's nothing to commit
        combined = (e.stderr or "") + (e.stdout or "")
        if "nothing to commit" in combined.lower() or "nothing added" in combined.lower():
            print("[git] Nothing new to commit, continuing to push.")
        else:
            print(combined)
            raise

    # Determine branch: current symbolic HEAD or remote HEAD
    branch = None
    try:
        r = run_git(["symbolic-ref", "--short", "HEAD"])
        branch = r.stdout.strip()
    except subprocess.CalledProcessError:
        try:
            r = run_git(["remote", "show", "origin"])
            m = re.search(r"HEAD branch:\s+(\S+)", r.stdout)
            branch = m.group(1) if m else None
        except subprocess.CalledProcessError:
            pass
    if not branch:
        branch = "main"

    # Build one-off Authorization header (non-persistent)
    basic = base64.b64encode(f"{username}:{pat}".encode()).decode()

    print(f"[git] push origin {branch} ...")
    try:
        # IMPORTANT: -c must precede the 'push' subcommand
        subprocess.run(
            ["git", "-c", f"http.extraheader=AUTHORIZATION: basic {basic}", "push", "origin", branch],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"[git] pushed to {branch}")
    except subprocess.CalledProcessError as e:
        print(e.stderr or e.stdout or "Push failed.")
        print("\nIf you see GH007 (email privacy), confirm your commit email is a GitHub noreply address and amend:")
        print("  git config user.email \"your_username@users.noreply.github.com\"")
        print("  git commit --amend --reset-author && git push -f")
        raise

# --- Arg parsing + main ---
def parse_args():
    p = argparse.ArgumentParser(description="AoC 2025 helper (fetch + scaffold + commit/push)")
    p.add_argument("--day", type=int, help="Day number (1–25). If omitted, you will be prompted.")
    return p.parse_args()

def prompt_day():
    while True:
        v = input("Which day to process? (1–25): ").strip()
        if v.isdigit() and 1 <= int(v) <= 25:
            return int(v)
        print("Please enter an integer between 1 and 25.")

def main():
    print("=== Advent of Code helper ===")
    ensure_dirs()

    # args / day
    args = parse_args()
    day = args.day if (args.day and 1 <= args.day <= 25) else prompt_day()

    # creds
    session_raw = read_or_prompt_aoc_session()
    username, pat = read_or_prompt_github_auth()

    # fetch + scaffold
    fetch_aoc(day, session_raw)
    ensure_solver_templates(day)

    # commit + push
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
