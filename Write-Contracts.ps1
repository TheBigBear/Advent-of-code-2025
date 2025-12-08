
#!/usr/bin/env pwsh
<#
Write-Contracts.ps1
One-time script to create AoC solver contract files for Python and PowerShell
with checksum verification.

Creates:
  helpers/solver_contract_python.md
  helpers/solver_contract_powershell.md

Usage:
  pwsh ./Write-Contracts.ps1
  pwsh ./Write-Contracts.ps1 -Force   # overwrite if files exist
#>

[CmdletBinding()]
param(
  [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# --- Helpers dir ---
$root    = Split-Path -Parent $PSCommandPath
$helpers = Join-Path $root 'helpers'
if (-not (Test-Path -LiteralPath $helpers)) {
  New-Item -ItemType Directory -Path $helpers | Out-Null
}

# --- Contract contents ---
# NOTE: We avoid triple backticks inside payload to keep here-strings robust.
#       Use 4-space indented code blocks for Markdown code samples.

$pythonContract = @'
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
'@

$powershellContract = @'
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
'@

# --- Paths ---
$pyPath = Join-Path $helpers 'solver_contract_python.md'
$psPath = Join-Path $helpers 'solver_contract_powershell.md'

# --- Overwrite protection ---
foreach ($p in @($pyPath, $psPath)) {
  if ((Test-Path -LiteralPath $p) -and -not $Force) {
    Write-Error "File exists: $p. Use -Force to overwrite."
  }
}

# --- Write files (UTF-8 without BOM) ---
Set-Content -LiteralPath $pyPath -Value $pythonContract -Encoding UTF8
Set-Content -LiteralPath $psPath -Value $powershellContract -Encoding UTF8

# --- Hash helpers ---
function Get-StringHashHex {
  param(
    [Parameter(Mandatory)][string]$Text,
    [ValidateSet('SHA256','SHA1','MD5')][string]$Algorithm = 'SHA256'
  )
  $bytes  = [System.Text.Encoding]::UTF8.GetBytes($Text)
  $hasher = [System.Security.Cryptography.HashAlgorithm]::Create($Algorithm)
  $hash   = $hasher.ComputeHash($bytes)
  ($hash | ForEach-Object { $_.ToString('x2') }) -join ''
}

function Get-FileHashHex {
  param(
    [Parameter(Mandatory)][string]$Path,
    [ValidateSet('SHA256','SHA1','MD5')][string]$Algorithm = 'SHA256'
  )
  (Get-FileHash -LiteralPath $Path -Algorithm $Algorithm).Hash.ToLowerInvariant()
}

# --- Compute expected (from strings) and actual (from files) hashes ---
$expectedPySHA256 = Get-StringHashHex -Text $pythonContract -Algorithm 'SHA256'
$expectedPsSHA256 = Get-StringHashHex -Text $powershellContract -Algorithm 'SHA256'

$actualPySHA256   = Get-FileHashHex -Path $pyPath -Algorithm 'SHA256'
$actualPsSHA256   = Get-FileHashHex -Path $psPath -Algorithm 'SHA256'

# --- Simple length diagnostics, too ---
$pyLen = (Get-Content -LiteralPath $pyPath -Encoding UTF8 | Measure-Object -Line).Lines
$psLen = (Get-Content -LiteralPath $psPath -Encoding UTF8 | Measure-Object -Line).Lines

# --- Report ---
Write-Host "✓ Created:"
Write-Host "  $pyPath"
Write-Host "  $psPath"
Write-Host ""
Write-Host "Python contract:"
Write-Host "  SHA256 expected: $expectedPySHA256"
Write-Host "  SHA256 actual  : $actualPySHA256"
Write-Host "  Lines          : $pyLen"
Write-Host ""
Write-Host "PowerShell contract:"
Write-Host "  SHA256 expected: $expectedPsSHA256"
Write-Host "  SHA256 actual  : $actualPsSHA256"
Write-Host "  Lines          : $psLen"
Write-Host ""

# --- Verify ---
$ok = ($expectedPySHA256 -eq $actualPySHA256) -and ($expectedPsSHA256 -eq $actualPsSHA256)
if ($ok) {
  Write-Host "✅ Verification: hashes match. Files were written exactly as intended." -ForegroundColor Green
} else {
  Write-Host "❌ Verification: hash mismatch. Written files may not match intended content." -ForegroundColor Red
  Write-Host "   Please rerun with -Force, or check if any post-write tooling modified the files."
  exit 1
}
