<#
.SYNOPSIS
AoC 2025 Day 2 - Gift Shop solver.

.DESCRIPTION
Part 1: Sum all IDs across input ranges which are "double patterns":
         any number that is made of a sequence of digits repeated twice (e.g., 55, 6464, 123123).
No leading zeroes are allowed (implicitly satisfied by construction).

Part 2: Not specified in provided puzzle spec; returns 0.

.PARAMETER Lines
String array of input lines; the input is one long CSV line with ranges "start-end" separated by commas.

.RETURNS
Hashtable: @{ Part1 = [int]; Part2 = [int] }

.NOTES
- Pure function: no file I/O and no printing inside Solve.
- Performance: near O(R * log10(maxID)), avoids per-ID scanning by closed-form summation
  of values n = x * (10^m + 1) with x in [10^(m-1) .. 10^m-1] intersected with range bounds.
#>

function Solve {
    param([string[]]$Lines)

    # ---- Local helpers (scoped to Solve) ----

    # Exact integer power of 10 for small exponents (avoids double rounding).
    function _Pow10([int]$n) {
        [long]$p = 1
        for ($i = 0; $i -lt $n; $i++) { $p *= 10 }
        return $p
    }

    # Sum of consecutive integers from a to b inclusive, in exact integer arithmetic.
    function _SumIntegers([long]$a, [long]$b) {
        if ($b -lt $a) { return 0L }
        [long]$count = $b - $a + 1
        # Use parity to avoid fractional intermediate.
        if (($count % 2) -eq 0) {
            return ($count / 2) * ($a + $b)
        } else {
            # When count is odd, (a + b) is even.
            return (($a + $b) / 2) * $count
        }
    }

    # Sum of all "double-pattern" IDs within [start, end].
    function _SumInvalidInRange([long]$start, [long]$end) {
        if ($end -lt $start) {
            $tmp = $start; $start = $end; $end = $tmp
        }
        if ($end -lt 1) { return 0L } # IDs are positive; nothing to sum below 1
        if ($start -lt 1) { $start = 1 }

        [long]$total = 0

        # Determine the number of digits of 'end' safely.
        # For end >= 1, digits = floor(log10(end)) + 1; for end < 10 -> 1 digit, etc.
        # Avoid relying on double Log10 for control flow; cap m by 9 (since 2m <= 18 within int64).
        # This is safe for typical AoC ranges <= 18 digits. Adjust here if your input goes beyond int64.
        # Compute digits via string to be robust:
        [int]$digitsEnd = ([string]$end).Length

        # m is half the digit length (only even-length numbers can be X·X)
        for ([int]$m = 1; $m -le [math]::Floor($digitsEnd / 2); $m++) {

            # Precompute bounds and factor
            [long]$pow10m      = _Pow10 $m                 # 10^m
            [long]$pow10m_1    = _Pow10 ($m - 1)           # 10^(m-1)
            [long]$factor      = $pow10m + 1               # n = x * (10^m + 1)
            [long]$min2mDigits = _Pow10 (2 * $m - 1)       # smallest 2m-digit number
            [long]$max2mDigits = (_Pow10 (2 * $m)) - 1     # largest 2m-digit number

            # Restrict the range to IDs with exactly 2m digits
            [long]$lowN  = [math]::Max($start, $min2mDigits)
            [long]$highN = [math]::Min($end,   $max2mDigits)
            if ($highN -lt $lowN) { continue }

            # Translate N bounds to X bounds via n = x * (10^m + 1)
            # X must also be m-digit: x ∈ [10^(m-1) .. 10^m - 1]
            # x_min = ceil(lowN / factor), x_max = floor(highN / factor)
            [long]$xMin = [long][math]::Ceiling([double]$lowN  / [double]$factor)
            [long]$xMax = [long][math]::Floor  ([double]$highN / [double]$factor)

            # Intersect with m-digit window
            if ($xMin -lt $pow10m_1) { $xMin = $pow10m_1 }
            if ($xMax -gt ($pow10m - 1)) { $xMax = $pow10m - 1 }

            if ($xMax -lt $xMin) { continue }

            # Sum of n over x in [xMin..xMax]: sum(n) = (10^m + 1) * sum(x)
            [long]$sumX = _SumIntegers $xMin $xMax
            $total += $factor * $sumX
        }

        return $total
    }

    # ---- Parse input ----
    # Input is a single long line with comma-separated ranges "a-b".
    # We join in case the file was wrapped; remove empty parts caused by trailing commas.
    $text = ($Lines -join '')
    $rangeSpecs = $text -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' }

    [long]$part1 = 0

    foreach ($spec in $rangeSpecs) {
        $ab = $spec -split '-'
        if ($ab.Count -ne 2) { continue }
        [long]$a = [long]$ab[0]
        [long]$b = [long]$ab[1]
        $part1 += _SumInvalidInRange $a $b
    }

    # Part 2 not specified in provided spec; return 0 to satisfy contract.
    [long]$part2 = 0

    return @{ Part1 = $part1; Part2 = $part2 }
}

# --- Optional sample check (never runs under dispatcher) ---
if ($false) {
    $sample = @(
        '11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124'
    )
    $res = Solve -Lines $sample
    # Expected Part1: 1227775554
    $res
}
