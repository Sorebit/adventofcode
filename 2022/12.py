from pathlib import Path
from pprint import pprint
import sys

from aoc import lines, V, PQFrontier
import pdb


def uplr(v: V):
    neighbors = [V(0, 1), V(0, -1), V(-1, 0), V(1, 0)]
    for n in neighbors:
        yield v + n


class NoSolution(Exception):
    pass


def height(c):
    """Height from input character"""
    return ord(c) - ord('a')


def shortest_path(heightmap, start, goal):
    """Finds shortest path from start to goal by climbing up"""
    max_x = len(heightmap[0])
    max_y = len(heightmap)

    # Begin search from starting node with cost 0
    visited = {}
    frontier = PQFrontier([(0, start)])

    while True:
        if frontier.empty():
            raise NoSolution
        # print('')
        # print(f'Processing next: {frontier.frontier}')
        # print(f'Nodes in frontier: {frontier.nodes}')
        cost, node = frontier.take()
        visited[node] = cost
        # print(f'Visited {node} with cost {cost}')
        # print(f'Remaining frontier: {frontier.frontier}')
        # pdb.set_trace()

        if node == goal:
            # Found the shortest path
            return cost, node

        node_height = heightmap[node.y][node.x]

        # Expand frontier
        for e in uplr(node):
            # If node is in frontier, it has the best cost already
            if frontier.contains(e):
                continue
            # Expand using only unvisited nodes
            if e in visited:
                continue
            # Expand using only nodes on the map
            if e.x not in range(max_x):
                continue
            if e.y not in range(max_y):
                continue
            # "at most one higher than the elevation of your current square"
            e_height = heightmap[e.y][e.x]
            if e_height > node_height + 1:
                continue
            # print(f'  Adding {e} to frontier with cost {cost + 1}')
            frontier.add(cost + 1, e)


def find_closest(heightmap, start, goal_height):
    """Finds closest node with given height (climbing in reverse)"""
    max_x = len(heightmap[0])
    max_y = len(heightmap)

    visited = {}
    # Begin search from starting node with cost 0
    frontier = PQFrontier([(0, start)])

    while not frontier.empty():
        cost, node = frontier.take()
        visited[node] = cost

        node_height = heightmap[node.y][node.x]

        if node_height == goal_height:
            # Found the shortest path to node with goal height
            return cost, node

        # Expand frontier
        for e in uplr(node):
            # If node is in frontier, it has the best cost already
            if frontier.contains(e):
                continue
            # Expand using only unvisited nodes
            if e in visited:
                continue
            # Expand using only nodes on the map
            if e.x not in range(max_x):
                continue
            if e.y not in range(max_y):
                continue
            # "at most one higher than the elevation of your current square"
            e_height = heightmap[e.y][e.x]
            if node_height > e_height + 1:
                continue
            frontier.add(cost + 1, e)


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    heightmap = []
    start = None
    goal = None

    for row, line in enumerate(lines(in_file)):
        height_line = []
        for col, tile in enumerate(line):
            if tile == 'S':
                start = V(x=col, y=row)
                h = height('a')
            elif tile == 'E':
                goal = V(x=col, y=row)
                h = height('z')
            else:
                h = height(tile)
            height_line.append(h)

        heightmap.append(height_line)

    # Heightmap is now constructed
    result_1, _ = shortest_path(heightmap, start, goal)
    result_2, _ = find_closest(heightmap, goal, 0)

    return result_1, result_2


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
