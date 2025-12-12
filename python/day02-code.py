
from typing import List, Tupledef solve(lines: List[str]) -> Tuple[int, int]:
    """
    Advent of Code 2025 - Day 2: Gift Shop
    Part 1: Sum of invalid IDs (pattern: repeated sequence twice) in given ranges.
    Part 2: (Assuming same logic unless puzzle specifies otherwise; placeholder for extension.)
    """
    # Parse input: single line with comma-separated ranges
    ranges = lines[0].strip().split(',')
    
    def is_invalid(n: int) -> bool:
        s = str(n)
        # Length must be even for repeated pattern
        if len(s) % 2 != 0:
            return False
        half = len(s) // 2
        return s[:half] == s[half:]
    
    part1_sum = 0
    for r in ranges:
        start, end = map(int, r.split('-'))
        for num in range(start, end + 1):
            if is_invalid(num):
                part1_sum += num
    
    # For now, Part 2 is unspecified; return 0 or same as Part 1 if needed
    part2_sum = 0  # Adjust if puzzle adds extra rule
    
    return part1_sum, part2_sum

# Optional internal test using example from description
if __name__ == "__main__":
    sample = ["11-22,95-115,998-1012,1188511880-1188511890,222220-222224,"
              "1698522-1698528,446443-446449,38593856-38593862,"
              "565653-565659,824824821-824824827,2121212118-2121212124"]
    print(solve(sample))  # Expected: (1227775554, 0)



