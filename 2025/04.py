import itertools
import sys
from collections import defaultdict
from pathlib import Path
from pprint import pprint
from typing import Literal

from aoc import V, eight2d, read_lines, vpprint, vprint

FLOOR: str = "."
PAPER: str = "@"

directions = eight2d()


class Map:
    def __init__(self, rows):
        self.rows = [list(row) for row in rows]
        self.num_rows = len(rows)
        self.num_cols = len(rows[0])
        self.oob_default = FLOOR

    def _check_bounds(self, row, col):
        if row < 0 or col < 0:
            return False
        if row >= self.num_rows or col >= self.num_cols:
            return False
        return True

    def __getitem__(self, pos: tuple[int, int]):
        row, col = pos
        if not self._check_bounds(row, col):
            return self.oob_default
        return self.rows[row][col]

    def __setitem__(self, pos: tuple[int, int], value: str):
        row, col = pos
        if not self._check_bounds(row, col):
            raise ValueError(f"Out of bounds {row=}, {col=}")
        self.rows[row][col] = value

    def count_neighbours(self, row, col):
        result = defaultdict(int)
        pos = V(x=col, y=row)
        for delta in directions:
            target = pos + delta
            tile = self[target.y, target.x]

            result[tile] += 1

        return result


def find_removable(m: Map):
    """
    I'm aware this is very suboptimal since we're scanning all the time
    It would be better to keep a frontier of the neighbours of deleted tiles and test that.
    """
    total = 0
    to_remove = []
    for row in range(m.num_rows):
        for col in range(m.num_rows):
            tile = m[row, col]
            neighbours = m.count_neighbours(row, col)
            if tile == PAPER and neighbours[PAPER] < 4:
                total += 1
                to_remove.append((row, col))
                vprint("x", end="")
            else:
                vprint(m[row, col], end="")

        vprint()
    vprint()

    return total, to_remove


def remove_removable(m: Map, to_remove: list[tuple[int, int]]):
    for row, col in to_remove:
        m[row, col] = FLOOR
    return m


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    rows = [line for line in read_lines(in_file)]

    m = Map(rows)
    result_1, to_remove = find_removable(m)

    while True:
        how_many, to_remove = find_removable(m)
        remove_removable(m, to_remove)
        result_2 += how_many
        if not how_many:
            break

    return result_1, result_2


if __name__ == "__main__":
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
