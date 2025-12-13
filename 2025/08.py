import dataclasses
import itertools
import sys
from collections import defaultdict
from pathlib import Path
from pprint import pprint
from typing import Any, Iterable

from aoc import V3, find_all_ints, lmap, read_lines, vpprint, vprint

points: list[V3] = []
Edge = tuple[int, int, float]
"""A idx, B idx, distance"""
by_distance = lambda d: d[2]

edges: list[Edge] = []


def add_point(pt: V3):
    pt_idx = len(points)
    for other_idx, other in enumerate(points):
        diff = pt - other
        vprint(diff)
        item = (pt_idx, other_idx, diff.euclidean())
        edges.append(item)
    points.append(pt)


unions = {}
current_union = 0
# connections_made = 0
grouped_by_union = [set()]


def make_union(a, b):
    global current_union
    vprint(f">> {a} ({points[a]}), {b} ({points[b]})")
    if a not in unions and b not in unions:
        vprint(a, b, "are not in any union, so go to", current_union)
        unions[a] = current_union
        unions[b] = current_union
        grouped_by_union[current_union] |= {a, b}
        current_union += 1
        grouped_by_union.append(set())
    elif a not in unions:
        vprint(a, "is not in any union, but", b, "is ->", unions[b])
        unions[a] = unions[b]
        grouped_by_union[unions[b]].add(a)
    elif b not in unions:
        vprint(b, "is not in any union, but", a, "is ->", unions[a])
        unions[b] = unions[a]
        grouped_by_union[unions[a]].add(b)
    elif unions[a] != unions[b]:
        vprint(a, b, "are already in some unions", unions[a], unions[b])
        vprint("moving all nods from union b:", unions[b], "to union a:", unions[a])
        # breakpoint()
        # merge_unions()
        vprint(unions)
        vprint(grouped_by_union)
        union_a, union_b = unions[a], unions[b]
        detached = grouped_by_union[union_b]
        for node_in_union_b in detached:
            unions[node_in_union_b] = union_a
        grouped_by_union[union_b] = set()
        grouped_by_union[union_a] |= detached
    else:
        vprint(a, b, "are already in the same union", unions[a], unions[b])
        # connections_made -= 1
    vprint(unions)
    vprint(grouped_by_union)


def union(edges, top_k):
    connections_made = 0
    for a, b, _ in sorted(edges, key=by_distance):
        make_union(a, b)
        connections_made += 1
        if connections_made >= top_k:
            break

    return unions, current_union, grouped_by_union


def part_one(edges, top_k):
    unions, num_of_unions, grouped = union(edges, top_k)
    pprint(grouped)

    result_1 = 1
    breakpoint()
    for u in sorted(grouped, key=lambda x: -len(x))[:3]:
        print(u)
        result_1 *= len(u)

    return result_1


def part_two(edges):
    for a, b, _ in sorted(edges, key=by_distance):
        make_union(a, b)
        if len(unions) >= len(points):
            print(a, points[a], b, points[b])
            breakpoint()
            return points[a].x * points[b].x
    return None


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    for line in read_lines(in_file):
        vprint(line)
        pt = V3(*find_all_ints(line))
        add_point(pt)
        vprint(edges)

    # pprint(edges)

    # result_1 = part_one(edges, top_k=1000)
    # its either 1 or 2, idc to make it clean
    result_2 = part_two(edges)

    return result_1, result_2


if __name__ == "__main__":
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
