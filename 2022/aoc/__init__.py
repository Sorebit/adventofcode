"""Advent-of-Code-specific helpers"""
from dataclasses import dataclass
from os import getenv
from pathlib import Path
import math
import re


# Input parsing helpers

def find_all_positive(s: str):
    """Return all positive integers found in given string"""
    # finditer is a bit of an overkill, since the dataset is so small (4 ints per 1000 lines)
    # but I'm trying to force some good practices into my mind with this year's advent.
    # return [int(m) for m in re.findall(r'\d+', s)]
    return [int(m.group()) for m in re.finditer(r'\d+', s)]


def find_all_ints(s: str) -> list[int]:
    """Return all integers found in given string"""
    return [int(m.group()) for m in re.finditer(r'-?\d+', s)]


def lines(p: Path, strip: bool = True):
    """Yields lines from file :param p: for processing them with or without storage. Opt-out withespace strip"""
    with open(p, 'r') as file:
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
            self._stack = self._stack[-self._cap:]

    def sum(self):
        return sum(self._stack)

    def __str__(self) -> str:
        return str(self._stack)


# TODO: Logger with verbosity set by env vars
#       to get rid of the nasty if VERBOSE: print(...)
VERBOSE = getenv('VERBOSE')


import numpy as np


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
        return V(x=self.x+other.x, y=self.y+other.y)

    def __sub__(self, other):
        return V(x=self.x-other.x, y=self.y-other.y)

    @classmethod
    def from_direction(cls, direction):
        """Up, down, left, or right unit vector."""
        choices = {
            'U': V(x=0, y=1),
            'D': V(x=0, y=-1),
            'L': V(x=-1, y=0),
            'R': V(x=1, y=0),
        }
        return choices[direction]

    def __repr__(self) -> str:
        return f'V({self.x}, {self.y})'

    def chebyshev_unit(self):
        """A 2D vector of length=1 in Chebyshev metric.

        (A diagonal move is a unit vector on a chess board)
        """
        x = self.x // abs(self.x) if self.x != 0 else 0
        y = self.y // abs(self.y) if self.y != 0 else 0
        return V(x=x, y=y)
