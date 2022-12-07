from os import getenv
from pathlib import Path
import sys

from ..aoc import lines, TopN


VERBOSE = getenv('VERBOSE')


def run(in_file: Path, cap: int = 1):

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


print(sys.argv)
p = Path(sys.argv[1])
part_1 = run(p)
part_2 = run(p, cap=3)

print(f'Part 1: {part_1}')
print(f'Part 2: {part_2}')
