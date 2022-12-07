from pathlib import Path
import sys

from aoc import lines, find_all_positive, VERBOSE


def show_stacks(stacks):
    for i, c in enumerate(stacks):
        print(i, c)


def solve(in_file: Path, new_model=False):
    stacks = [
        # stack num - 1  -> stack content: str (bottom 'MCD' top)
    ]

    for line in lines(in_file, strip=False):

        stripped = line.strip()

        if stripped.startswith('['):
            # A create is either a '[_] ' or '    '
            # Last crate is missing a single space, but that's alright since we're
            # taking only the second char
            crates_in_line = len(line) // 4
            if not stacks:
                # Now that we know how many stacks there are, initialize the list
                stacks = [''] * crates_in_line

            for i in range(crates_in_line):
                letter_pos = i*4 + 1
                content = line[letter_pos]
                if content.strip():
                    # If the content is not empty, add it to the bottom of the stack
                    stacks[i] = content + stacks[i]

        elif line.startswith('move'):
            # Assume stacks are already set up
            how_many, c_from, c_to = find_all_positive(line)
            c_from -= 1
            c_to -= 1
            if VERBOSE:
                print('Move', how_many, 'from', c_from, 'to', c_to )

            # Take crates from the top of source stack
            take = stacks[c_from][-how_many:]
            stacks[c_from] = stacks[c_from][:-how_many]
            # Place taken crates on target stack
            if not new_model:
                # One by one (reversed)
                stacks[c_to] += take[::-1]
            else:
                # All at once, it's the NEW model
                stacks[c_to] += take

            if VERBOSE:
                show_stacks(stacks)
        else:
            # Empty lines and crate numbers aren't useful
            continue

    # Join together all top crates from each stack, starting from left
    result_1 = ''.join(s[-1] for s in stacks)

    return result_1


if __name__ == '__main__':
    # python 05.py in/05/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file), solve(in_file, new_model=True)
    print(part_1, part_2)
    assert part_1 == 'JCMHLVGMG'
    assert part_2 == 'LVMRWSSPZ'
