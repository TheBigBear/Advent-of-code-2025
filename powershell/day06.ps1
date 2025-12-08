param([int]$Day = 6)
$root   = (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
$inPath = Join-Path $root ("inputs/day06.txt")
if (-not (Test-Path $inPath)) {
    Write-Error "Input file not found: $inPath"
    exit 1
}
$lines = Get-Content -LiteralPath $inPath

# TODO: implement Part 1 and Part 2 for Day 6 using $lines
$part1 = $null
$part2 = $null

Write-Output ("Part 1: 0" -f $part1)
Write-Output ("Part 2: 0" -f $part2)
