#!/usr/bin/env pwsh
<#
AoC 2025 dispatcher for PowerShell solvers.
Loads powershell/dayXX-code.ps1, reads inputs/dayXX.txt, and prints Part 1 & Part 2.
#>

param(
    [Parameter(Mandatory=$true)]
    [ValidateRange(1,25)]
    [int]$Day
)

$root      = $PSScriptRoot
$codePath  = Join-Path $root ("powershell/day{0}.ps1" -f $Day.ToString("00") + "-code").Replace(".ps1-code",".ps1")  # results in powershell/dayXX-code.ps1
$inputPath = Join-Path $root ("inputs/day{0}.txt" -f $Day.ToString("00"))

if (-not (Test-Path -LiteralPath $codePath)) {
    Write-Error "PowerShell solver not found: $codePath"
    exit 1
}
if (-not (Test-Path -LiteralPath $inputPath)) {
    Write-Error "Input not found: $inputPath"
    exit 1
}

# Dot-source the day-specific solver code file; it must define a function:
#   function Solve { param([string[]]$Lines) return @{Part1=...; Part2=...} }
. $codePath

if (-not (Get-Command -Name Solve -ErrorAction SilentlyContinue)) {
    Write-Error "The solver file '$codePath' must define a function: Solve([string[]]$Lines)"
    exit 1
}

$lines  = Get-Content -LiteralPath $inputPath
$result = Solve -Lines $lines

if (-not $result.ContainsKey("Part1") -or -not $result.ContainsKey("Part2")) {
    Write-Error "Solve() must return a hashtable with keys Part1 and Part2."
    exit 1
}

Write-Output ("Part 1: {0}" -f $result.Part1)
Write-Output ("Part 2: {0}" -f $result.Part2)
