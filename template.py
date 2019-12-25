# https://adventofcode.com/2019/day/

import sys
sys.path.append('../')
from modules.utils import check


def solve(data):
    return None, None


def test(path, expected_path = None):
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
    test("input.txt")
    # test("tests/1.in", "tests/1.out")


if __name__ == '__main__':
    main()
