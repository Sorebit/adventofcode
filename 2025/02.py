import itertools
import sys
from pathlib import Path
from pprint import pprint

from aoc import lmap, read_lines, vprint


def split_parts(s: str, n: int) -> list[str]:
    """Split string into n parts of equal length"""
    if len(s) % n != 0:
        raise ValueError(f"len of {s} is not divisible by {n}")
    gen = itertools.batched(s, n)
    return lmap(lambda x: "".join(x), gen)


def left_right(s: str):
    l = len(s)
    if l % 2 != 0:
        raise ValueError(f"len of {s} is not even")
    return split_parts(s, l // 2)


def is_id_valid(product_id: str, n: int = 2) -> bool:
    l = len(product_id)
    if l % n != 0:
        return True
    left, right = left_right(product_id)
    return left != right


def next_parzystokopytny(r: str):
    """Next (tylko jak trzeba) liczba która ma parzystą długość. Basically 100..."""
    if len(r) % 2 == 0:
        return r
    return "1" + "0" * len(r)


def prev_parzystokopytny(r: str):
    """Prev (tylko jak trzeba) liczba która ma parzystą długość. Basically 999..."""
    if len(r) % 2 == 0:
        return r
    if len(r) <= 2:
        return 0
    return "9" * (len(r) - 1)


def next_invalid(r: str) -> str:
    """
    Z załozenia r jest juz parzystej długości.
    Czy moze byc tak ze przekroczymy zbior i trzeba wziac kolejna dlugosc? No chyba wlasnie nie
    bo jak jest 9999, to jest invalid, a to nas interesuje i 9999 mapuje sie na 9999
    """
    left, right = left_right(r)
    if left == right:
        # np 23,23
        return r
    elif int(left) > int(right):
        # 23,00 -> 23,23 -- czyli jak left > right, to left,left
        return left + left
    else:
        # ale 23,25 -> 24,24 -- a jak right > left, to left+1,left+1
        next_left = str(int(left) + 1)
        return next_left + next_left


def prev_invalid(r: str):
    """Z załozenia r jest juz parzystej długości.
    Czy prev moze zmienic dlugosc? Jak mamy 1000, to wskoczymy w mniejsza w sumie, bo 99
    Ale w naszym wypadku to musialoby byc cos w stylu 1000-1001
    """
    left, right = left_right(r)
    if left == right:
        # np 23, 23
        return r
    elif int(left) < int(right):
        # no to jest mamy 23,25 -> 2323
        return left + left
    else:
        # a jak 23,21 -> 2222
        # ale jak mamy 10,09
        # to samo sie naprawia intem :o
        # left-1, left-1
        prev_left = str(int(left) - 1)
        return prev_left + prev_left


def prepare_range(r_start: str, r_end: str) -> list[tuple[str, str]]:
    vprint("\n:::", (r_start, r_end))
    fixed_start = next_parzystokopytny(r_start)
    truly_fixed_start = next_invalid(fixed_start)
    vprint("L:", r_start, ">", fixed_start, ">", truly_fixed_start, "\n")

    fixed_end = prev_parzystokopytny(r_end)
    truly_fixed_end = prev_invalid(fixed_end)
    vprint("R:", r_end, ">", fixed_end, ">", truly_fixed_end, "\n")

    if int(truly_fixed_start) > int(truly_fixed_end):
        vprint("-> []")
        return []
    vprint("->", (truly_fixed_start, truly_fixed_end))

    # is_id_valid(r_start)
    # is_id_valid(r_end)

    if len(truly_fixed_start) == len(truly_fixed_end):
        # simplest case I think?
        pass
    else:
        raise ValueError(truly_fixed_start, truly_fixed_end)
        # lol wychodzi na to ze sie nie przejmuje tym przadkiem w ogole?
        pass
    return [(truly_fixed_start, truly_fixed_end)]


def prepare(ranges):
    prepared_ranges = []
    for range in ranges:
        pr = prepare_range(*range.split("-"))
        prepared_ranges.extend(pr)

    # Looks like generally the input ranges don't overlap
    # for first, second in zip(prepared_ranges[:-1], prepared_ranges[1:]):
    # if int(first[1]) > int(second[0]):
    # raise ValueError(first, second)
    return sorted(prepared_ranges, key=lambda pr: int(pr[0]))


def sum_range(fixed_start, fixed_end):
    total = 0
    start, _ = left_right(fixed_start)
    # z zalozenia (lol) wiemy ze maja tą samą długość
    l = len(start)
    mult = 10**l

    start = int(start)

    end, _ = left_right(fixed_end)
    end = int(end)
    vprint(": ", start, ",", end)
    vprint("*", mult)
    # nie bede tu świrować, więc
    total = sum(range(start, end + 1))
    vprint("+=", total)
    vprint(". ", total * (mult + 1))
    return total * (mult + 1)


def solve(in_file: Path):
    result_1, result_2 = 0, 0
    ranges = next(read_lines(in_file)).split(",")

    prepared_ranges = prepare(ranges)
    pprint(prepared_ranges)

    for fixed_start, fixed_end in prepared_ranges:
        vprint(fixed_start, fixed_end)

        if fixed_start == fixed_end:
            result_1 += int(fixed_start)
        else:
            result_1 += sum_range(fixed_start, fixed_end)

    return result_1, result_2


if __name__ == "__main__":
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
