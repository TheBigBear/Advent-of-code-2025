#!/usr/bin/env pwsh
<#
Write-Contracts-Pretty.ps1
One-time script to create AoC solver contract files for Python and PowerShell
with perfect Markdown formatting (blank lines, fenced code blocks).

Usage:
  pwsh ./Write-Contracts-Pretty.ps1
  pwsh ./Write-Contracts-Pretty.ps1 -Force   # overwrite if files exist
#>

[CmdletBinding()]
param(
  [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root    = Split-Path -Parent $PSCommandPath
$helpers = Join-Path $root 'helpers'
if (-not (Test-Path -LiteralPath $helpers)) {
  New-Item -ItemType Directory -Path $helpers | Out-Null
}

$pythonContract = @"
# AoC 2025 Python Solver Contract

Dispatcher: `run_day.py` will dynamically load `python/dayXX-code.py` and pass:

```python
lines: list[str]  # from inputs/dayXX.txt
