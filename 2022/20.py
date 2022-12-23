from dataclasses import dataclass
import functools
import itertools
from pathlib import Path
from pprint import pprint
import operator
import sys

from aoc import lines


@dataclass
class Node:
    """Double linked list node"""
    value: int
    prev: any
    next: any

    def __repr__(self):
        n = self.next.value if self.next else self.next
        p = self.prev.value if self.prev else self.prev
        return f'prev={p}, ({self.value}), next={n}'

    def swap_next(self):
        # Z -> A -> B -> C
        Z = self.prev
        B = self.next
        C = B.next

        Z.next = B
        B.next.prev = self

        # Z -> B -> A -> C
        self.next = C
        B.next = self

        self.prev = B
        B.prev = Z

    def swap_prev(self):
        # Z -> B -> A -> C
        B = self.prev
        C = self.next
        Z = B.prev

        Z.next = self
        B.prev = self

        B.next = C
        C.prev = B

        self.prev = Z
        self.next = B

    def print_rest(self):
        print(self.value, end='')
        it = self.next
        while it != self:
            print(f' -> {it.value}', end='')
            if not it.next:
                raise ValueError(it, it.next)
            it = it.next
        print('')

    def whole_list(self):
        """Yields each element of list once"""
        yield self
        it = self.next
        while it != self:
            yield it
            it = it.next

    def find_next(self, value):
        """Returns next node with given value, or None when no result"""
        try:
            return next(
                n
                for n in self.whole_list()
                if n.value == value
            )
        except StopIteration:
            return None


def solve(in_file: Path, dec_key=1, mix_rounds=1):
    result_1 = 0

    numbers = [int(line)*dec_key for line in lines(in_file)]

    original = [Node(num, None, None) for num in numbers]

    for a, b in zip(original[:-1], original[1:]):
        a.next = b
        b.prev = a

    original[0].prev = original[-1]
    original[-1].next = original[0]

    print('ORIGINAL ORDER')
    for o in original:
        print(o)

    original[0].print_rest()

    # original[0].swap_next()

    # print('\nAFTER SWAP [0] WITH NEXT')
    # print(original[1])
    # print(original[0])

    # for o in original[2:]:
    #     print(o)

    # original[1].print_rest()
    # # move(0, numbers)

    # original[0].swap_prev()
    # print('\nAFTER SWAP [0] WITH PREV')
    # print(original[0])
    # print(original[1])
    # for o in original[2:]:
    #     print(o)

    list_len = len(original)

    original[0].print_rest()

    print('\n')

    for r in range(mix_rounds):
        print(f'Round {r}')
        for o in original:
            swaps = o.value % (list_len - 1)
            for _ in range(swaps):
                o.swap_next()

        # original[0].print_rest(s)

    zero = original[0].find_next(0)
    final = list(zero.whole_list())
    for y in enumerate(final):
        print(y)
    result_1 = sum(
        final[c % len(final)].value
        for c in (1000, 2000, 3000)
    )

    for c in (1000, 2000, 3000):
        print(final[c % len(final)].value)

    return result_1


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1 = solve(in_file)
    part_2 = solve(in_file, dec_key=811589153, mix_rounds=10)
    print(part_1, part_2)
