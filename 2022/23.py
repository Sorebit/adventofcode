import itertools
from pathlib import Path
from pprint import pprint
import sys

from aoc import lines, V, eight2d


GROUND = '.'
ELF = '#'

eight = eight2d()
U, D, L, R, UL, UR, DL, DR = eight


def bounding_box(elves):
    min_x = min(e.x for e in elves)
    max_x = max(e.x for e in elves)
    min_y = min(e.y for e in elves)
    max_y = max(e.y for e in elves)

    return min_x, max_x, min_y, max_y


def print_map(elves, padding=0):
    min_x, max_x, min_y, max_y = bounding_box(elves)
    x_label_size = max(len(str(min_x - padding)), len(str(max_x + padding)))
    y_label_size = max(len(str(min_y - padding)), len(str(max_y + padding)))

    print(' '*y_label_size, end=' ')
    for x in range(min_x - padding, max_x + 1 + padding):
        print(str(x).zfill(x_label_size), end='')

    print('')
    for y in range(min_y - padding, max_y + 1 + padding):
        print(str(y).zfill(y_label_size), end=' ')

        for x in range(min_x - padding, max_x + 1 + padding):

            if V(x, y) in elves:
                print(ELF, end='')
            else:
                print(GROUND, end='')
        print('')


def round(elves: set[V], order):
    # Proposed position -> list of elves whodunit
    proposals: dict[V, list[V]] = dict()

    considered = 0

    for elf in elves:
        if not any(elf + delta in elves for delta in eight):
            # No elf around, do nothing
            continue

        # print(f'Consider {elf}')
        considered += 1

        for move, check in order:
            any_elf_in_direction = any(elf + check_delta in elves
                                       for check_delta in check)
            if not any_elf_in_direction:
                found_next_move = elf + move

                if found_next_move in proposals:
                    proposals[found_next_move].append(elf)
                else:
                    proposals[found_next_move] = [elf]

                # print(elf, 'propsed', found_next_move)
                break

    for new_elf, old_elves in proposals.items():
        if len(old_elves) == 1:
            elves.remove(old_elves[0])
            elves.add(new_elf)

    return considered == 0


def count_empty(elves):
    min_x, max_x, min_y, max_y = bounding_box(elves)
    result = 0

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if V(x, y) not in elves:
                result += 1

    return result

def solve(in_file: Path, rounds=None):
    result = 0

    elves = set()

    for y, line in enumerate(lines(in_file)):
        for x, tile in enumerate(line):
            if tile == ELF:
                elves.add(V(x, y))

    order = [
        # move, check
        (U, (UL, U, UR)),
        (D, (DL, D, DR)),
        (L, (UL, L, DL)),
        (R, (UR, R, DR)),
    ]

    i = 0
    while True:
        i += 1
        print(f'Round {i}')
        any_elf_moved = round(elves, order)
        # Part 1
        if rounds is not None and i == rounds:
            break
        # Part 2
        if rounds is None and any_elf_moved:
            break

        # print_map(elves, padding=1)
        # Move first to the end of list
        order = order[1:] + order[0:1]

    if rounds is not None:
        # Part 1
        return count_empty(elves)
    else:
        # Part 2
        return i


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1 = solve(in_file, rounds=10)
    part_2 = solve(in_file, rounds=None)
    print(part_1, part_2)
