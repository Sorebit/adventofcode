from pathlib import Path
import sys

from aoc import lines


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    reg = {'x': 1}  # A dict, so it's easily mutated from inside add.inner
    x_during = []
    crt = [''] * 6

    def noop():
        return

    def add(value):
        def inner():
            reg['x'] += value

        return inner

    for line in lines(in_file):
        # Get next command
        command, *args = line.split()

        # We're gonna complete all cycles for this command before moving on
        cycles = []

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
            x_during.append(reg['x'])
            # End of cycle
            operation()

    # Part 1
    for c in range(19, len(x_during), 40):
        result_1 += x_during[c] * (c+1)

    # Part 2
    for c, x in enumerate(x_during):
        # if the sprite's horizontal position puts its pixels where the CRT is
        # currently drawing, then those pixels will be drawn.
        if c % 40 in [x-1, x, x+1]:
            crt[c // 40] += '█'
        else:
            crt[c // 40] += ' '
        print(f'[{c + 1}] x={x}')

    for line in crt:
        print(line)

    return result_1, result_2


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
