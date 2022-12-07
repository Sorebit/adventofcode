# https://adventofcode.com/2019/day/7

import sys
import itertools
import math

sys.path.append("../")
from modules.utils import check

from modules.intcode import Program


def solve(raw_intcode, phases):
    current_input = 0
    amp = None
    for i in range(5):
        amp = Program(raw_intcode)
        # print(f"Starting {i} | phase: {phases[i]} | input: {current_input}")
        amp.set_input([phases[i], current_input])
        amp.mute_output = True

        amp.process(verbose=False)

        current_input = amp.last_output

    return amp.last_output


def test(path, expected_path=None):
    data = None
    print("File:", path)
    with open(path, "r") as file:
        data = [line for line in file.readlines()]

    expected = None
    if expected_path:
        with open(expected_path, "r") as file:
            expected = [int(line) for line in file.readlines()]

    part_1, part_2 = solve(data)

    if expected:
        print("Part 1:", check(part_1, expected[0]))
        print("Part 2:", check(part_2, expected[1]))
    else:
        print("Part 1:", part_1)
        print("Part 2:", part_2)
    print("")


def main():
    # test("input.txt")
    # test("tests/1.in", "tests/1.out")

    raw_intcode = None
    # Open input intcodes and solve
    with open("input.txt", "r") as file:
        raw_intcode = [int(ins) for ins in file.readline().split(",")]

    # Solve part 1
    print("Part 1")

    phases = list(range(5))
    permutations = list(itertools.permutations(phases))
    best = -math.inf

    for p in permutations:
        output = solve(raw_intcode, p)
        best = max(best, output)

    print(best)


if __name__ == "__main__":
    main()
