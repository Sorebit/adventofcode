from pathlib import Path
from pprint import pprint as pp
import sys

from aoc import lines


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    cur_cycle = 0  # Currently ongoing cycle
    cycles = []
    reg = {'x': 1}  # A dict, so it's easily mutated from inside add.inner
    x_during = []
    screen = [''] * 6

    def noop():
        return

    def add(value):
        def inner():
            reg['x'] += value

        return inner


    for line in lines(in_file):
        # Get next command
        command, *args = line.split()

        # Add operation's cycles to buffer
        if command == 'addx':
            value = int(args[0])
            cycles += [noop, add(value)]
        elif command == 'noop':
            cycles += [noop]
        else:
            raise NotImplementedError

        for operation in cycles:
            # Start of cycle is just the end of the last one with next cycle number
            # During cycle
            x = reg['x']  # Just for readability
            x_during.append(x)
            print(f'[{cur_cycle + 1}] x={x}')
            # if the sprite's horizontal position puts its pixels where the CRT is
            # currently drawing, then those pixels will be drawn.
            if cur_cycle % 40 in [x-1, x, x+1]:
                screen[cur_cycle // 40] += '#'
            else:
                screen[cur_cycle // 40] += '.'
            # End of cycle
            operation()
            cur_cycle += 1

        # Clear buffer, since we've completed ops
        cycles = []

    # Part 1
    for c in range(19, cur_cycle, 40):
        result_1 += x_during[c] * (c+1)

    # Part 2
    pp(screen)

    return result_1, result_2


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
