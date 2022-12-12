from pathlib import Path
from pprint import pprint
import sys

import numpy as np

from aoc import lines, lrev


def solve_for_single_row(row):
    """For each tree in given row, returns whether it is visible from the left"""
    dp = np.zeros_like(row)
    out = np.zeros_like(row)

    # row : 3 0 3 7 3
    #  dp: -1 3 3 3 7
    # out:  1 0 0 1 0
    dp[0] = -1
    out[0] = 1
    for i, tree in enumerate(row):
        if i == 0:
            continue
        # For each tree calc the max height of all the trees to the left
        dp[i] = max(dp[i-1], row[i-1])
        # A tree is visible from left side if its higher than all its predecessors
        # out[i] = tree > dp[i]
        out[i] = 1 if tree > dp[i] else 0

    return out


def solve_part_1(trees):
    # Final visibility matrix
    visible = np.zeros_like(trees)

    # From left to right
    print('LTR')
    for i, row in enumerate(trees):
        result = solve_for_single_row(row)
        # Start final visibility with the LTR results.
        # For next ones, we're gonna need their logical 'or' since a tree is visible
        # when it is visible from *any* side
        visible[i] = result

    pprint(visible)

    print('RTL')
    # From right to left (just reverse a row and the result)
    for i, row in enumerate(trees):
        result = lrev(
            solve_for_single_row(lrev(row))
        )
        visible[i] |= result

    pprint(visible)

    # Rotate 90 degrees counter-clockwise (left side is now top)
    rot_trees = np.rot90(trees)
    rot_visible = np.rot90(visible)
    print('Rotated 90 deg counter-clockwise')
    pprint(rot_trees)

    # From top to bottom
    print('TTB')
    for i, row in enumerate(rot_trees):
        result = solve_for_single_row(row)
        # It's really nice that rot_visible is a rotated view into visible
        rot_visible[i] |= result

    pprint(rot_visible)

    # From bottom to top
    print('BTT')
    for i, row in enumerate(rot_trees):
        result = lrev(
            solve_for_single_row(lrev(row))
        )
        rot_visible[i] |= result

    pprint(rot_visible)

    print('Final (un-rotated) view')
    pprint(trees)
    pprint(visible)

    return np.count_nonzero(visible)

def ray(u, t, default):
    """u - iterable of trees, t - rozpatrywane tree, default - result if oob"""
    return next((
        # (i+1, other)
        i+1
        for i, other in enumerate(u)
        if other >= t
    # ), (default, None))
    ), default,)


def solve_part_2(trees):
    grove_side = len(trees)

    def scenic_score(sx, sy, t):
        """sx,sy - starting pos. t - height of rozpatrywane tree"""
        print(f'({t})', sx, sy)

        u = [trees[y][sx] for y in range(sy-1, -1, -1)]
        # Jak idę w górę i dojdę do końca to zobaczę y drzew po drodze
        score_u = ray(u, t, default=y)
        print('  U', u, score_u)

        # Jak idę w dół i dojdę do końca to zobaczę len - y - 1 (bo 0-indexed)
        d = [trees[y][sx] for y in range(sy+1, grove_side)]
        score_d = ray(d, t, default=grove_side-y-1)
        print('  D', d, score_d)

        l = [trees[sy][x] for x in range(sx-1, -1, -1)]
        score_l = ray(l, t, default=x)
        print('  L', l, score_l)

        r = [trees[sy][x] for x in range(sx+1, grove_side)]
        score_r = ray(r, t, default=grove_side-x-1)
        print('  R', r, score_r)
        return score_u * score_d * score_l * score_r

    max_visible_trees = 0
    for y, row in enumerate(trees):
        for x, t in enumerate(row):
            candidate = scenic_score(x, y, t)
            max_visible_trees = max(max_visible_trees, candidate)

        print('')

    return max_visible_trees


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    trees = np.array([
        [int(tree) for tree in line]
        for line in lines(in_file)
    ])
    pprint(trees)

    result_1 = solve_part_1(trees)
    result_2 = solve_part_2(trees)

    return result_1, result_2


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
