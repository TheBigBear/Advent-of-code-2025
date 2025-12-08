
#!/usr/bin/env python3
import sys

def solve(lines):
    pos = 50  # starting position per puzzle
    part1 = 0
    part2 = 0

    for ln in lines:
        ln = ln.strip()
        if not ln: 
            continue
        dirc, val = ln[0].upper(), int(ln[1:])
        m = val if dirc == 'R' else -val

        # Part 2: count zero passes/landings during the move
        if m >= 0:
            part2 += (pos + m) // 100
        else:
            part2 += ((pos - 1) // 100) - ((pos + m - 1) // 100)

        # Update position with wrap-around (Python's % already non-negative)
        pos = (pos + m) % 100

        # Part 1: count moves that end on zero
        if pos == 0:
            part1 += 1

    return part1, part2

if __name__ == "__main__":
    lines = sys.stdin.read().splitlines()
    p1, p2 = solve(lines)
    print(f"Part 1 (actual password): {p1}")
