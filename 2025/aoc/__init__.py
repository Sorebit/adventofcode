"""Advent-of-Code-specific helpers"""

import heapq
import math
import re
from dataclasses import dataclass
from os import getenv
from pathlib import Path
from pprint import pprint
from typing import Any, Literal

# Logging

VERBOSE = getenv("VERBOSE")


def vprint(
    *values: object,
    sep: str | None = " ",
    end: str | None = "\n",
    file: Any | None = None,
    flush: Literal[False] = False,
):
    if VERBOSE:
        print(*values, sep=sep, end=end, file=file, flush=flush)


def vpprint(*args, **kwargs):
    if VERBOSE:
        pprint(*args, *kwargs)


# Input parsing helpers


def positive_g(s: str):
    """Like find_all_positive but a generator"""
    for m in re.finditer(r"\d+", s):
        yield int(m.group())


def find_all_positive(s: str):
    """Return all positive integers found in given string"""
    # finditer is a bit of an overkill, since the dataset is so small (4 ints per 1000 lines)
    # but I'm trying to force some good practices into my mind with this year's advent.
    # return [int(m) for m in re.findall(r'\d+', s)]
    return list(positive_g(s))


def ints_g(s: str):
    """Like find_all_ints but a generator"""
    for m in re.finditer(r"-?\d+", s):
        yield int(m.group())


def find_all_ints(s: str) -> list[int]:
    """Return all integers found in given string"""
    return list(ints_g(s))


def read_lines(p: Path, strip: bool = True):
    """Yields lines from file :param p: for processing them with or without storage. Opt-out withespace strip"""
    with open(p, "r") as file:
        for line in file.readlines():
            if strip:
                yield line.strip()
            else:
                yield line


# Func. helpers


def lmap(func, *iterables):
    return list(map(func, *iterables))


def lrev(iterable):
    return list(reversed(iterable))


def first(sequence):
    """next(sequence?)"""
    return sequence[0]


def second(sequence):
    """next(sequence?)"""
    return sequence[1]


# Structures


class TopN:
    """A structure that keeps track of only the top N biggest items"""

    def __init__(self, cap: int):
        self._cap = cap
        self._stack = []

    def add(self, item):
        """For bigger caps, it might be reasonable to insert with a binary search instead of sorting after each insert. (Or use a proper priority queue)"""
        self._stack.append(item)
        self._stack.sort()
        if len(self._stack) > self._cap:
            # Keep only N biggest values
            print("-", self._stack[0])
            self._stack = self._stack[-self._cap :]

    def __len__(self):
        return len(self._stack)

    def sum(self):
        return sum(self._stack)

    def __str__(self) -> str:
        return str(self._stack)

    def __repr__(self):
        return str(self)


# import numpy as np


# class V:
#     def __init__(self, x, y) -> None:
#         self._ = np.array([x, y])

#     @property
#     def x(self):
#         return self._[0]

#     @property
#     def y(self):
#         return self._[1]


@dataclass(frozen=True)
class V:
    x: int
    y: int

    def __add__(self, other):
        return V(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return V(x=self.x - other.x, y=self.y - other.y)

    @classmethod
    def from_direction(cls, direction):
        """Up, down, left, or right unit vector."""
        choices = {
            "U": V(x=0, y=1),
            "D": V(x=0, y=-1),
            "L": V(x=-1, y=0),
            "R": V(x=1, y=0),
        }
        return choices[direction]

    def __repr__(self) -> str:
        return f"V({self.x}, {self.y})"

    def chebyshev_unit(self):
        """A 2D vector of length=1 in Chebyshev metric.

        (A diagonal move is a unit vector on a chess board)
        """
        x = self.x // abs(self.x) if self.x != 0 else 0
        y = self.y // abs(self.y) if self.y != 0 else 0
        return V(x=x, y=y)

    def __lt__(self, other) -> bool:
        """Anything to order these (x, then y)"""
        if self.x < other.x:
            return True
        return self.y < other.y


@dataclass(frozen=True)
class V3:
    x: int
    y: int
    z: int

    def __sub__(self, other: "V3") -> "V3":
        return V3(
            x=self.x - other.x,
            y=self.y - other.y,
            z=self.z - other.z,
        )

    def euclidean(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __repr__(self):
        return f"{self.x},{self.y},{self.z}"


def manhattan(a: V, b: V) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def pm2d():
    """U, D, L, R = pm2d()"""
    return (
        V(0, -1),
        V(0, 1),
        V(-1, 0),
        V(1, 0),
    )


def eight2d():
    """
    U, D, L, R, UL, UR, DL, DR = eight2d()
    """
    return pm2d() + (
        V(-1, -1),
        V(1, -1),
        V(-1, 1),
        V(1, 1),
    )


def pm3d():
    return (
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    )


def vec_sum(a, b):
    return tuple(a_i + b_i for a_i, b_i in zip(a, b))


class PQFrontier:
    def __init__(self, initial=None):
        """
        initial - Optional list of (priority, item) tuples
        """
        self.frontier = initial or []
        heapq.heapify(self.frontier)
        # Assume the same node will not be added twice
        self.nodes = set()
        for p, node in self.frontier:
            self.nodes.add(node)

    def add(self, priority, node):
        """Assumes the same node will not be added twice"""
        heapq.heappush(self.frontier, (priority, node))
        self.nodes.add(node)

    def take(self):
        p, node = heapq.heappop(self.frontier)
        self.nodes.remove(node)
        return (p, node)

    def empty(self):
        return len(self.frontier) == 0

    def contains(self, node):
        return node in self.nodes


def swap_kv(d: dict) -> dict:
    """Returns a dictionary where keys are swapped with values"""
    return {v: k for k, v in d.items()}
