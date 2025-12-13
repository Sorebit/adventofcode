import dataclasses
import itertools
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Self

from aoc import lmap, read_lines, vpprint, vprint

START = "S"
SPLITTER = "^"


def part_one(lines):
    result_1 = 0
    beams: set[int] = set()
    for level, line in enumerate(lines):
        beams, splits = process_line(line, beams, level)
        result_1 += splits
    return result_1


def process_line(line, beams: set[int], level: int) -> tuple[set[int], int]:
    splits = 0
    new_beams = beams.copy()
    for x, c in enumerate(line):
        if c == START:
            new_beams.add(x)
            print(START, end="")
        elif c == SPLITTER and x in beams:
            print("^", end="")
            new_beams.remove(x)
            new_beams |= {x - 1, x + 1}
            splits += 1
        elif x in beams:
            print("|", end="")
        else:
            print(".", end="")
    print()
    return new_beams, splits


def part_two_single_row(line, beams, level):
    beams_for_next_lv = defaultdict(set)
    for x, c in enumerate(line):
        if c == START:
            beams_for_next_lv[x] = set()  # w sensie ze root
            break  # assuming theres only one start

        if x in beams:
            if c == SPLITTER:
                beams_for_next_lv[x - 1].add(x)
                beams_for_next_lv[x + 1].add(x)
            else:
                beams_for_next_lv[x].add(x)

    return beams_for_next_lv


def part_two(lines):
    """
    I guess this could just be recursive and the counting would be post-order
    """
    beams: set[int] = set()
    beams_per_level = []
    for level, line in enumerate(lines):
        beams = part_two_single_row(level=level, beams=beams, line=line)
        beams_per_level.append(dict(beams))
        vprint(f"after lv={level}:")
        vpprint(dict(beams))
        vprint()

    counters_per_level = defaultdict(lambda: defaultdict(int))
    for node in beams_per_level[-1]:
        counters_per_level[len(beams_per_level) - 1][node] = 1

    for level in range(len(beams_per_level) - 1, -1, -1):
        beams = beams_per_level[level]
        vprint(level, beams)
        for node, parents in beams.items():
            ways_to_get_to_node = counters_per_level[level][node]
            for parent in parents:
                counters_per_level[level - 1][parent] += ways_to_get_to_node
            print(node, parents)

    vpprint(counters_per_level)
    return next(counter for counter in counters_per_level[0].values())


def solve(in_file: Path):
    result_1 = part_one(read_lines(in_file))
    result_2 = part_two(read_lines(in_file))

    return result_1, result_2


if __name__ == "__main__":
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
