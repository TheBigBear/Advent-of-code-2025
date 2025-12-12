Advent of Code 2025 — Day 02 solver request (PowerShell)

Puzzle spec:
Day 2 - Advent of Code 2025
Advent of Code[About][Events][Shop][Settings][Log Out]TheBigBear 2*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/^2025$/[Calendar][AoC++][Sponsors][Leaderboards][Stats]
Our sponsors help make Advent of Code possible:Grist - The open-source spreadsheet-database that minds its business.
--- Day 2: Gift Shop ---You get inside and take the elevator to its only other stop: the gift shop. "Thank you for visiting the North Pole!" gleefully exclaims a nearby sign. You aren't sure who is even allowed to visit the North Pole, but you know you can access the lobby through here, and from there you can access the rest of the North Pole base.
As you make your way through the surprisingly extensive selection, one of the clerks recognizes you and asks for your help.
As it turns out, one of the younger Elves was playing on a gift shop computer and managed to add a whole bunch of invalid product IDs to their gift shop database! Surely, it would be no trouble for you to identify the invalid product IDs for them, right?
They've even checked most of the product ID ranges already; they only have a few product ID ranges (your puzzle input) that you'll need to check. For example:
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
(The ID ranges are wrapped here for legibility; in your input, they appear on a single long line.)
The ranges are separated by commas (,); each range gives its first ID and last ID separated by a dash (-).
Since the young Elf was just doing silly patterns, you can find the invalid IDs by looking for any ID which is made only of some sequence of digits repeated twice. So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice) would all be invalid IDs.
None of the numbers have leading zeroes; 0101 isn't an ID at all. (101 is a valid ID that you would ignore.)
Your job is to find all of the invalid IDs that appear in the given ranges. In the above example:
11-22 has two invalid IDs, 11 and 22.
95-115 has one invalid ID, 99.
998-1012 has one invalid ID, 1010.
1188511880-1188511890 has one invalid ID, 1188511885.
222220-222224 has one invalid ID, 222222.
1698522-1698528 contains no invalid IDs.
446443-446449 has one invalid ID, 446446.
38593856-38593862 has one invalid ID, 38593859.
The rest of the ranges contain no invalid IDs.
Adding up all the invalid IDs in this example produces 1227775554.
What do you get if you add up all of the invalid IDs?
To begin, get your puzzle input.
Answer:
You can also [Shareon
  Bluesky
  Twitter
  Mastodon] this puzzle.

Solver contract:
﻿# AoC 2025 PowerShell Solver Contract

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


Deliverable:
Implement in powershell/day02-code.ps1.

Sample input:
851786270-851907437,27-47,577-1044,1184-1872,28214317-28368250,47766-78575,17432-28112,2341-4099,28969-45843,5800356-5971672,6461919174-6461988558,653055-686893,76-117,2626223278-2626301305,54503501-54572133,990997-1015607,710615-802603,829001-953096,529504-621892,8645-12202,3273269-3402555,446265-471330,232-392,179532-201093,233310-439308,95134183-95359858,3232278502-3232401602,25116215-25199250,5489-8293,96654-135484,2-17


To run:
- Python: `python run_day.py --day 2`
- PowerShell: `./run_day.ps1 -Day 2`

Expected output format:
Part 1: <integer>
Part 2: <integer>

Sample solver stub:
function Solve {
    param([string[]]$Lines)
    # TODO: Implement Part 1 and Part 2 logic
    $part1 = 0
    $part2 = 0
    return @{ Part1 = $part1; Part2 = $part2 }
}

