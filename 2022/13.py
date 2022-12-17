from pathlib import Path
from pprint import pprint
import sys

from aoc import lines


def next_n(g, n):
    """Returns next n items from generator g"""
    return [next(g) for _ in range(n)]


def group_lines(in_file, n):
    gen = lines(in_file)
    # TODO: yield remaining < n when last group is not full
    while True:
        try:
            yield next_n(gen, n)
        except StopIteration:
            return


def compare_lists(left, right) -> bool | None:
    for i, left_item in enumerate(left):
        # Left list is longer, Out of order
        if i >= len(right):
            # print('OUT OF ORDER')
            return False

        right_item = right[i]
        # print('Compare', left_item, 'vs', right_item)

        if type(left_item) == int and type(right_item) == int:
            if left_item < right_item:
                return True
            if left_item > right_item:
                return False

        if type(left_item) == list and type(right_item) == list:
            result = compare_lists(left_item, right_item)
            if result is not None:
                return result

        if type(left_item) == list and type(right_item) == int:
            result = compare_lists(left_item, [right_item])
            if result is not None:
                return result

        if type(left_item) == int and type(right_item) == list:
            result = compare_lists([left_item], right_item)
            if result is not None:
                return result

    # Left is shorter and no item was OOO, in right order
    if len(left) < len(right):
        return True
    # This happens only inside recursion steps
    return None


class Packet:
    def __init__(self, s):
        self.s = s

    @classmethod
    def from_line(cls, line):
        return cls(eval(line))

    def __repr__(self) -> str:
        return repr(self.s)

    def __lt__(self, other):
        return compare_lists(self.s, other.s)


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    # Part 1
    for pair_i, group in enumerate(group_lines(in_file, 3)):
        left, right, _ = group
        left = eval(left)
        right = eval(right)

        result = compare_lists(left, right)
        # print(f'{pair_i + 1} -> {result}')
        if result:
            result_1 += pair_i + 1

    # Part 2
    SEP_1 = Packet([[2]])
    SEP_2 = Packet([[6]])
    packets = [SEP_1, SEP_2]
    for line in lines(in_file):
        if not line:
            continue
        packets.append(Packet.from_line(line))

    in_order = sorted(packets)
    result_2 = (in_order.index(SEP_1) + 1) * (in_order.index(SEP_2) + 1)

    return result_1, result_2


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
