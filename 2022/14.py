from enum import Enum
import itertools
from pathlib import Path
from pprint import pprint
import sys

from aoc import lines, V, positive_g


def group(g, n, allow_partial=False):
    """Groups elements yielded by a generator into lists of n elements

    gr = group(g=[1, 2, 3, 4], n=2)
    list(gr) -> [[1, 2], [3, 4]]
    """
    # TODO: allow yielding remaining < n when last group is not full by flipping allow_partial
    while True:
        try:
            # NOTE: When
            result = list(itertools.islice(g, n))
            # if not allow_partial and 0 < len(result) < n:
            if not result:
                # Empty result, so slicing exhausted
                return
            yield result
        except StopIteration:
            return


AIR = ' '
WALL = '█'
SAND = 'o'
X = 'X'
SOURCE = '+'


def set_tile(world, p: V, tile):
    world[p] = tile


def get_tile(world, p, max_y):
    # p = V(x, y)
    if p in world:
        return world[p]
    elif p.y == max_y:
        return WALL
    else:
        return AIR


def world_boundaries(world):
    min_x = min(v.x for v in world.keys())
    min_y = min(v.y for v in world.keys())
    max_x = max(v.x for v in world.keys())
    max_y = max(v.y for v in world.keys())
    return min_x, min_y, max_x, max_y


def world_to_grid(world, floor=False):
    min_x, min_y, max_x, max_y = world_boundaries(world)
    print(f'World spans from {min_x, min_y} to {max_x, max_y}')
    additional = 2 if floor else 0
    grid = [
        [
            get_tile(world, V(x, y), max_y)
            for x in range(min_x, max_x + 1)
        ]
        for y in range(min_y, max_y + 1 + additional)
    ]
    return grid


def print_world(world, floor=False):
    grid = world_to_grid(world, floor)
    for row in grid:
        print(''.join(row))



class Result(Enum):
    """Result for producing sand"""
    settled = 0
    abyss = 1
    blocked = 2


def produce_sand(world, origin: V, max_y) -> Result:
    """
    :returns: Whether sand fell into the Abyss, have settled, or blocked the source
    """
    unit_pos = origin
    # Try moving down, then down-left, then down-right
    candidates = [V(0, 1), V(-1, 1), V(1, 1)]
    cnt = 0
    while True:
        cnt += 1
        # print(f'\n[{cnt}] {unit_pos}')
        moved = False
        for c in candidates:
            if get_tile(world, unit_pos + c, max_y) == AIR:
                # print(f'{unit_pos + c} is AIR')
                # set_tile(world, unit_pos, X)
                # print_world(world, True)
                # set_tile(world, unit_pos, AIR)
                unit_pos += c

                moved = True
                # Sand fell into the Abyss
                # print(unit_pos, max_y)
                if unit_pos.y > max_y:
                    return Result.abyss
                break

        if not moved:
            if get_tile(world, unit_pos, max_y) == SOURCE:
                return Result.blocked
            set_tile(world, unit_pos, SAND)
            return Result.settled


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    world = {}  # V -> char?

    def from_to(start: V, goal: V):
        if start.x != goal.x:
            # Move by x
            sx, gx = min(start.x, goal.x), max(start.x, goal.x)
            for x in range(sx, gx + 1):
                set_tile(world, V(x, start.y), WALL)
        else:
            # Move by y
            sy, gy = min(start.y, goal.y), max(start.y, goal.y)
            for y in range(sy, gy + 1):
                set_tile(world, V(start.x, y), WALL)

    for line in lines(in_file):
        # print(line)
        prev = None
        ints = positive_g(line)
        for xy in group(ints, 2):
            p = V(xy[0], xy[1])
            if prev:
                # print(prev, '->', p)
                from_to(prev, p)
            prev = p

    # World is now constructed
    set_tile(world, V(500, 0), SOURCE)
    # print_world(world)

    _, _, _, max_y = world_boundaries(world)

    print('Start producing sand')
    sand_origin = V(500, 0)
    while True:
        result = produce_sand(world, sand_origin, max_y)
        if result == Result.abyss:
            print('Fell into the abyss...')
            break
        elif result == Result.settled:
            print('Settled')
            result_1 += 1
        else:
            raise ValueError(result)

    print_world(world)

    # Part 2
    # Clear world of sand
    world = {
        p: tile
        for p, tile in world.items()
        if tile != SAND
    }
    print_world(world, True)

    while True:
        result = produce_sand(world, sand_origin, max_y + 2)
        if result == Result.blocked:
            print('Blocked source...')
            break
        if result == Result.settled:
            print('Settled')
            result_2 += 1
        else:
            raise ValueError(result)

    print_world(world, True)



    return result_1, result_2


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
