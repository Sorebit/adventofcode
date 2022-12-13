from dataclasses import dataclass
from pathlib import Path
import sys

from aoc import lines


@dataclass(frozen=True)
class V:
    x: int
    y: int

    def __add__(self, other):
        return V(x=self.x+other.x, y=self.y+other.y)

    def __sub__(self, other):
        return V(x=self.x-other.x, y=self.y-other.y)

    @classmethod
    def from_input(cls, direction):
        choices = {
            'U': V(x=0, y=1),
            'D': V(x=0, y=-1),
            'L': V(x=-1, y=0),
            'R': V(x=1, y=0),
        }
        return choices[direction]

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'

    def unit(self):
        x = self.x // abs(self.x) if self.x != 0 else 0
        y = self.y // abs(self.y) if self.y != 0 else 0
        return V(x=x, y=y)


class Rope:
    def __init__(self, seg_count: int, start: V) -> None:
        self.segments: list[V] = [start] * seg_count
        self.visited: set[V] = {start}

    @property
    def head(self) -> V:
        return self.segments[0]

    @property
    def tail(self) -> V:
        return self.segments[-1]

    def move_head(self, m: V) -> None:
        """m - unit direction"""
        for i, _ in enumerate(self.segments):
            if i == 0:
                # Move head
                self.segments[i] += m
                continue

            diff = self.segments[i-1] - self.segments[i]
            if abs(diff.x) > 1 or abs(diff.y) > 1:
                # Not neighboring, move tail in head's general direction
                self.segments[i] += diff.unit()

        # Update tail visits
        self.visited.add(self.tail)


def solve(in_file: Path):
    short = Rope(2, V(x=0, y=0))
    long = Rope(10, V(x=0, y=0))

    for line in lines(in_file):
        direction, count = line.split()
        count = int(count)

        move = V.from_input(direction)
        for _ in range(count):
            short.move_head(move)
            long.move_head(move)

    return len(short.visited), len(long.visited)


if __name__ == '__main__':
    # python 09.py in/09/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
