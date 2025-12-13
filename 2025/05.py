import itertools
import sys
from pathlib import Path
from pprint import pprint
from typing import Iterable

from aoc import lmap, read_lines, vpprint, vprint


def parse_input(lines_iter: Iterable[str]):
    state = "RANGES"
    ranges = []
    queries = []
    for line in lines_iter:
        if not line:
            state = "QUERIES"
            continue
        if state == "RANGES":
            ranges.append(lmap(int, line.split("-")))
        else:
            queries.append(int(line))

    return ranges, queries


def prepare_ranges(ranges) -> list[list[int]]:
    all_ranges = list(sorted(ranges))
    vprint("Starting set")
    vpprint(all_ranges)
    flattened = []
    current_start = all_ranges[0][0]
    current_end = all_ranges[0][1]

    for i, r in enumerate(all_ranges):
        vprint("Working on", [current_start, current_end])
        start, end = r
        vprint(start, end)
        if start <= current_end:
            current_end = max(end, current_end)
            vprint("end :=", current_end)
        else:
            vprint("flattened <<", [current_start, current_end])
            flattened.append([current_start, current_end])
            current_start, current_end = start, end
            vprint("new", [current_start, current_end])
        # breakpoint()
        vprint()

    flattened.append([current_start, current_end])
    vprint("flattened <<", [current_start, current_end], "*last")
    # breakpoint()
    return flattened


def is_valid(ranges, query) -> bool:
    """Way suboptimal, since range trees exist, but this is 1d with ~100 ranges"""
    vprint("Q", query)
    for r in ranges:
        if query in range(r[0], r[1] + 1):
            print(r, "*")
            return True
    return False


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    ranges, queries = parse_input(read_lines(in_file))
    initial_len = len(ranges)
    ranges = prepare_ranges(ranges)
    vpprint(ranges)
    vprint(f"Went from {initial_len} to {len(ranges)} ranges")
    # part 1
    for query in queries:
        if is_valid(ranges, query):
            result_1 += 1

    # part 2
    for r in ranges:
        result_2 += len(range(r[0], r[1] + 1))
    return result_1, result_2


if __name__ == "__main__":
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
