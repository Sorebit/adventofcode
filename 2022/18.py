import itertools
from pathlib import Path
from pprint import pprint
import sys

from aoc import lines, find_all_ints, pm3d, vec_sum

sys.setrecursionlimit(100000)


water = set()
blocks = set()

result_2 = 0


def dfs(xyz):
    global result_2
    if xyz in blocks:
        result_2 += 1
        return
    x, y, z = xyz
    if x > 22 or y > 22 or z > 22:
        return
    if x < -1 or y < -1 or z < -1:
        return
    water.add(xyz)
    # print(xyz)
    for v in pm3d():
        d = vec_sum(xyz, v)
        if d not in water:
            dfs(d)


def solve(in_file: Path):
    result_1 = 0

    max_x, max_y, max_z = None, None, None

    for line in lines(in_file):
        xyz = tuple(find_all_ints(line))

        x, y, z = xyz
        max_x = max(max_x, x) if max_x is not None else x
        max_y = max(max_y, y) if max_y is not None else y
        max_z = max(max_z, z) if max_z is not None else z
        blocks.add(xyz)

    print(max_x, max_y, max_z)

    result_1 = 6 * len(blocks)

    for xyz in blocks:
        for v in pm3d():
            if vec_sum(xyz, v) in blocks:
                result_1 -= 1

    # Part 2
    # Any starting point outside of the lava ball would do
    assert (0, 0, 0) not in blocks
    dfs((0, 0, 0))

    return result_1, result_2


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
