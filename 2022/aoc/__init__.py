"""Advent-of-Code-specific helpers"""
from enum import Enum, auto
import functools
import operator
from os import getenv
from pathlib import Path
import string
import re
import sys


def lines(p: Path, strip: bool = True):
    """Yields lines from file :param p: for processing them with or without storage. Opt-out withespace strip"""
    with open(p, 'r') as file:
        for line in file.readlines():
            if strip:
                yield line.strip()
            else:
                yield line


def find_all_positive(s: str):
    """Return all positive integers found in given string"""
    # finditer is a bit of an overkill, since the dataset is so small (4 ints per 1000 lines)
    # but I'm trying to force some good practices into my mind with this year's advent.
    # return [int(m) for m in re.findall(r'\d+', s)]
    return [int(m.group()) for m in re.finditer(r'\d+', s)]


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


VERBOSE = getenv('VERBOSE')
