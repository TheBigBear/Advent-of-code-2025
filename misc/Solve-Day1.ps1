
param(
    [Parameter(ValueFromPipeline=$true)]
    [string[]]$InputLines
)

begin {
    $pos   = 50
    $part1 = 0
    $part2 = 0
}
process {
    foreach ($line in $InputLines) {
        $line = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($line)) { continue }

        $dir = $line.Substring(0,1).ToUpper()
        $val = [int]$line.Substring(1)
        $m   = if ($dir -eq 'R') { $val } else { -$val }

        # Part 2: count zero passes/landings during the move
        if ($m -ge 0) {
            $part2 += [math]::Floor( ($pos + $m) / 100 )
        } else {
            $part2 += [math]::Floor( ($pos - 1) / 100 ) - [math]::Floor( ($pos + $m - 1) / 100 )
        }

        # Update position with wrap-around; PowerShell '%' can be negative, so fix it
        $pos = ($pos + $m) % 100
        if ($pos -lt 0) { $pos += 100 }

        # Part 1: if we end on zero, count one
        if ($pos -eq 0) { $part1++ }
    }
}
end {
    Write-Output ("Part 1 (actual password): {0}" -f $part1)
    Write-Output ("Part 2 (zero passes-or-landings): {0}" -f $part2)
}
