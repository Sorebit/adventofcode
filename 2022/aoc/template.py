import itertools
from pathlib import Path
from pprint import pprint
import sys

from aoc import lines


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    for line in lines(in_file):
        print(line)

    return result_1, result_2


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
