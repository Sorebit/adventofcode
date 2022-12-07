from pathlib import Path
import sys

import aoc


def fully_contains(first, second):
    """Whether first fully contains second"""
    return first[0] <= second[0] and first[1] >= second[1]


def overlaps(first, second):
    # First always starts first
    if first[0] > second[0]:
        first, second = second, first

    return not (
        # First is before second
        (first[0] < second[0] and first[1] < second[0]) or
        # First is after second
        (first[0] > second[1] and first[1] > second[1])
    )


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    for line in aoc.lines(in_file):
        a, b, c, d = aoc.find_all_positive(line)
        first = (a, b)
        second = (c, d)

        if fully_contains(first, second) or fully_contains(second, first):
            result_1 += 1
        if overlaps(first, second):
            result_2 += 1

    return result_1, result_2


if __name__ == '__main__':
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
