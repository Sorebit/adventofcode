import itertools
from pathlib import Path
from pprint import pprint
import sys

from aoc import lines


def parse_in(filename: str | Path) -> list[int]:
    mul_lu = {
        'L': -1,
        'R': 1,
    }
    return [
        mul_lu[line[0]] * int(line[1:])
        # for line in parse_in("day1_example.in")
        for line in lines(filename)
    ]


mod = 100
check_for = 0
start = 50

def part_one(rotations):
    result = 0    
    current = start
    for rot in rotations:
        after = current + rot
        current = after % mod
        if current == check_for:
            result += 1
        print(current)

    return result

def check_crossings(current, rot):
    if rot == 0:
        raise ValueError("posint")
    print(f"{current=}, {rot=}")
    total_turns = abs(rot) // mod
    print(f"{total_turns=}")
    after = (current + rot) % mod
    if after == current:
        print(f"after == current -> -1")
        total_turns -= 1
    print(f"{after=}")
    last_crossing = 0
    if after == 0:
        print("after=0 -> +1")
        return total_turns + 1
    if current == 0:
        return total_turns
    if rot > 0:  # czyli idziemy w prawo, czyli 60 -> 90 nie, ale 60 -> 59, 60 -> 60
        if after <= current:
            print("after <= current")
            last_crossing += 1
    elif rot < 0:
        # w lewo czyli 60 -> 30 ok, ale 60 -> 61
        if after >= current:
            print("after >= current")
            last_crossing += 1
    else:
        raise ValueError(f"{current=}, {rot=}")
    return total_turns + last_crossing


def brute_force(current, rot):
    dir = -1 if rot < 0 else 1
    abs_rot = abs(rot)
    total_crossings = 0
    while abs_rot > 0:
        current = (current + dir) % mod
        if current == 0:
            total_crossings += 1
        abs_rot -= 1
    return total_crossings, current


def test_suite():
    cases = [
        # dict(current=0, rot=0, expected_end=0, expected_crossings=1),
        dict(current=50, rot=10, expected_end=60, expected_crossings=0),
        dict(current=50, rot=50, expected_end=0, expected_crossings=1),
        dict(current=50, rot=60, expected_end=10, expected_crossings=1),
        dict(current=50, rot=150, expected_end=0, expected_crossings=2),
        dict(current=50, rot=160, expected_end=10, expected_crossings=2),
        dict(current=50, rot=100, expected_end=50, expected_crossings=1),
        dict(current=50, rot=200, expected_end=50, expected_crossings=2),
        dict(current=50, rot=300, expected_end=50, expected_crossings=3),
        dict(current=0, rot=99, expected_end=99, expected_crossings=0),
        dict(current=99, rot=102, expected_end=1, expected_crossings=2),
        dict(current=50, rot=1000, expected_end=50, expected_crossings=10),
        dict(current=50, rot=-10, expected_end=40, expected_crossings=0),
        dict(current=50, rot=-50, expected_end=0, expected_crossings=1),
        dict(current=50, rot=-51, expected_end=99, expected_crossings=1),
    ]

    for test_case in cases:
        test_check_crossings(test_case)


def test_check_crossings(test_case):
    current=test_case["current"]
    rot=test_case["rot"]
    expected_end = test_case["expected_end"]
    expected_crossings = test_case["expected_crossings"]
    brute_result, brute_end = brute_force(current, rot)
    assert expected_crossings == brute_result, f"BAD LUCK {expected_crossings=} != {brute_result=} for {test_case=}"
    assert expected_end == brute_end, f"BAD LUCK {expected_end=} != {brute_end=} for {test_case=}"
    
    result = check_crossings(current, rot)
    assert result == expected_crossings, f"{result} != {expected_crossings} for {test_case=}"
    print("")


def part_two(rotations):
    result = 0
    current = start
    for rot in rotations:
        crossings, end = brute_force(current, rot)
        # crossings = check_crossings(current, rot)
        after = (current + rot) % mod
        print(f"{current},{rot},{after},{crossings}")
        current = after
        # breakpoint()
        result += crossings
        # print(current)

    return result


test_check_crossings({'current': 0, 'rot': -79, 'expected_end': 21, 'expected_crossings': 0})


def gen_test_cases():
    for line in lines("testcases.in"):
        current, rot, excepted_end, expected_crossings = map(int, line.split(","))
        yield dict(current=current, rot=rot, expected_end=excepted_end, expected_crossings=expected_crossings)
    
for test_case in gen_test_cases():
    print(test_case)
    test_check_crossings(test_case)

rots = parse_in("day_1_p1.in")

# part_one_res = part_one(rots)
part_two_res = part_two(rots)

# print(f"Part 1: {part_one_res}")
print(f"Part 2: {part_two_res}")


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    for line in lines(in_file):
        print(line)

    return result_1, result_2


# if __name__ == '__main__':
#     # python {{nn}}.py in/{{nn}}/...
#     in_file = Path(sys.argv[1])
#     part_1, part_2 = solve(in_file)
#     print(part_1, part_2)