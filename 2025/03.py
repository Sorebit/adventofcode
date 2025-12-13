import itertools
import sys
from pathlib import Path
from pprint import pprint

from aoc import TopN, first, lmap, lrev, read_lines, vpprint, vprint


def largest_to_date(iterable, compare_fn) -> list:
    best = None
    result = []
    for i, n in enumerate(iterable):
        if best is None or compare_fn(n, best):
            best = n
        result.append(best)
    return result


gt = lambda n, best: n > best


def solve_single(nums: str):
    nums = lmap(int, nums)

    largest_ltr = largest_to_date(map(int, nums), gt)
    largest_rtl = lrev(largest_to_date(map(int, reversed(nums)), gt))
    vpprint(nums)
    vpprint(largest_ltr)
    vpprint(largest_rtl)
    # czyli znajdujemy pierwsze wystąpienie przedostaniej wartości w ltr?
    looking_for = largest_ltr[-2]
    i = next(i for i, n in enumerate(largest_ltr[:-1]) if n == looking_for)
    r = largest_rtl[i + 1]
    vprint(f"[{i}]: {looking_for} -> [{i+1}]: {r} -> {looking_for}{r}")
    return int(f"{looking_for}{r}")


def from_top(top):
    els = sorted(top._stack, key=lambda el: el[2])
    return "".join(map(first, els))


def current_front(top):
    return from_top(top)[0]


def add_from_to(top, nums, old_head, new_head, largest_rtl):
    for i in range(old_head, new_head - 1, -1):
        el = (nums[i], -(len(nums) - i), i)
        if int(nums[i]) >= largest_rtl[i]:
            top.add(el)


def solve_single_part_2(nums: str, w_size: int = 12) -> str:
    # czyli tak naprawdę idziemy od prawej do lewej
    # zaczynamy od okna len=12
    # i trzymamy top liczb, ale wpuszczamy nową tylko wtedy kiedy jest większa od tej
    # najbardziej lewo
    largest_rtl = lrev(largest_to_date(map(int, reversed(nums)), gt))
    head = len(nums) - w_size

    # i jak znajdzie sie cos co jest wieksze niz head, to wyrzucamy najmniejsza z puli, ale najbardziej na lewo
    top = TopN(w_size)
    # for i in range(len(nums) - 1, head, -1):
    for i in range(len(nums) - 1, 0 - 1, -1):
        print(f"[{i}]", nums[i])
        el = (nums[i], -(len(nums) - i), i)
        if len(top) < w_size:
            top.add(el)
        elif current_front(top) <= nums[i]:
            print(f"{current_front(top)} <= {nums[i]}")
            # top = reconstruct(nums, w_size, i)
            print("t", lrev(top._stack))
            print(i, "<<", el)
            add_from_to(top, nums, old_head=head, new_head=i, largest_rtl=largest_rtl)
            head = i
            # top.add(el)
            # chyba bardziej reconstruct odtąd?
            print(lrev(top._stack))

        if len(top) == w_size:
            print(" " * i + from_top(top))
        # breakpoint()
        pass
    return from_top(top)


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    for line in read_lines(in_file):
        print(line)
        result_2 += int(solve_single_part_2(line))
        # result_1 += solve_single(line)
        print()

    return result_1, result_2


if __name__ == "__main__":
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
