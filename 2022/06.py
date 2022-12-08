from pathlib import Path
import sys

from aoc import lines, VERBOSE

def find_n_distint_subopt(line, n):
    """Finds n consecutive distinct characters in string. Suboptimal O(len(line)*n)"""
    for i in range(len(line) - n + 1):
        sub = line[i:(i+n)]
        if VERBOSE:
            print(sub, set(sub))
        if len(set(sub)) == len(sub):
            return i + n
    # No solution
    return None


def find_n_distinct(line, n):
    """Finds n consecutive distinct characters in string. Optimal O(len(line))"""
    # Set of chars already present in the subword
    active = set()
    # Left-most character of current subword
    tail = 0
    # Try to make subword longer by adding only characters not already present in subword
    for head, c in enumerate(line):
        if VERBOSE:
            print(line[tail:head+1], tail, head, c, active)
        # To progress, c cannot be in the active set
        if c in active:  # Note: This if is left here purely for readability)
            # Move tail forward, until we throw out the needed character from set
            while c in active and tail < head:
                active.remove(line[tail])
                tail += 1
                if VERBOSE:
                    print(line[tail:head], '+', line[head])
        # Now it is possible to lengthen the subword
        active.add(c)
        if len(active) == n:
            return head + 1
    # No solution
    return None


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    for line in lines(in_file):
        result_1 = find_n_distinct(line, 4)
        result_2 = find_n_distinct(line, 14)

    return result_1, result_2


if __name__ == '__main__':
    # python 06.py in/06/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
