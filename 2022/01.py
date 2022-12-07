from os import getenv
from pathlib import Path
import sys

from aoc import lines, TopN, VERBOSE


def solve(in_file: Path, cap: int = 1):

    if VERBOSE:
        print(f'Running with input from {in_file}')

    top = TopN(cap)
    elf_calories = 0

    for line in lines(in_file):
        if VERBOSE:
            print(':', line)
        if line == '':
            top.add(elf_calories)
            if VERBOSE:
                print(f'Elf carries: {elf_calories}')
                print(f'Top {cap}: {top}')
            elf_calories = 0
        else:
            elf_calories += int(line)

    # If last line is not a blank
    if elf_calories != 0:
        top.add(elf_calories)
        if VERBOSE:
            print(f'Elf carries: {elf_calories}')
            print(f'Top {cap}: {top}')

    if VERBOSE:
        print(f'Sum of best {cap}: {top.sum()}')

    return top.sum()


if __name__ == '__main__':
    # python 01.py <input path>
    in_file = Path(sys.argv[1])
    part_1 = solve(in_file)
    part_2 = solve(in_file, cap=3)
    print(part_1, part_2)
    assert part_1 == 72478
    assert part_2 == 210367
