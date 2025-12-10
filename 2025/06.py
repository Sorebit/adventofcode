import itertools
from pathlib import Path
import sys
from typing import Any, Iterable
import re
from aoc import ints_g, lines, vprint, vpprint, lmap
import math

NONEMPTY_NOT_WS = r"[^\s]"

def find_all_symbols(s: str):
    for m in re.finditer(NONEMPTY_NOT_WS, s):
        yield m.group()

def apply_operation(symbol: str, nums: list[int]):
    if symbol == "+":
        return sum(nums)
    elif symbol == "*":
        return math.prod(nums)


def part_one(all_lines: list[str]):
    result_1 = 0
    gen_nums = [
        ints_g(line)
        for line in all_lines[:-1]
    ]
    gen_symbols = find_all_symbols(all_lines[-1])
    
    for symbol, *nums in zip(gen_symbols, *gen_nums):
        print(symbol, nums)
        result_1 += apply_operation(symbol, nums)
    return result_1

WHITESPACE = [" ", "\n"]

def next_numbers(gen_nums):
    buffers = None
    for col in zip(*gen_nums):
        # print(col)
        if not buffers:
            buffers = [""] * len(col)
        # print(buffers, end="\n\n")

        if all(c in WHITESPACE for c in col):
            vertical = ["".join(args).strip() for args in zip(*buffers)]
            yield lmap(int, vertical)
            buffers = None
            continue
        
        for i, c in enumerate(col):
            buffers[i] += c if c not in WHITESPACE else " "
        pass


def part_two(all_lines: list[str]):
    result_2 = 0
    print("p2")
    gen_nums = [
        iter(line)
        for line in all_lines[:-1]
    ]
    gen_symbols = find_all_symbols(all_lines[-1])
    for symbol, nums in zip(gen_symbols, next_numbers(gen_nums)):
        print(symbol, nums)
        result_2 += apply_operation(symbol, nums)
    return result_2

def solve(in_file: Path):
    result_1, result_2 = 0, 0

    all_lines = list(lines(in_file, strip=False))
    result_1 = part_one(all_lines)
    result_2 = part_two(all_lines)

    return result_1, result_2


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
