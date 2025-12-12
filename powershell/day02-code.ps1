<#
.SYNOPSIS
Advent of Code 2025 - Day 2: Gift Shop
Find invalid product IDs (pattern: repeated sequence twice) in given ranges.

.DESCRIPTION
Part 1: Sum of all invalid IDs across ranges.
Part 2: Placeholder (extend if puzzle specifies additional logic).
#>

function Solve {
    param([string[]]$Lines)

    # Parse input: single line with comma-separated ranges
    $ranges = $Lines[0].Trim() -split ','

    function Is-Invalid($n) {
        $s = [string]$n
        # Must have even length for repeated pattern
        if ($s.Length % 2 -ne 0) { return $false }
        $half = $s.Length / 2
        return ($s.Substring(0, $half) -eq $s.Substring($half))
    }

    $part1 = 0
    foreach ($r in $ranges) {
        $parts = $r -split '-'
        $start = [int64]$parts[0]
        $end   = [int64]$parts[1]
        for ($num = $start; $num -le $end; $num++) {
            if (Is-Invalid $num) {
                $part1 += $num
            }
        }
    }

    $part2 = 0 # Placeholder for future logic
    return @{ Part1 = $part1; Part2 = $part2 }
}

# Optional internal test (never runs under dispatcher)
if ($false) {
    $sample = @("11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124")
    $result = Solve -Lines $sample
    Write-Host "Sample Result: $($result.Part1), $($result.Part2)" # Expected: 1227775554, 0
}

