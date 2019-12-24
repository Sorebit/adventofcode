# https://adventofcode.com/2019/day/6

# Global, so should be cleared if you want to run solve again
neighbours = {}
values = {}
parents = {}
visited = {}

NODE_ROOT = "COM"

def dfs(node):
    if(node not in neighbours):
        return
    for n in neighbours[node]:
        dfs(n)
        values[node] += values[n] + 1


def count_orbits():
    dfs(NODE_ROOT)

    orbits = 0
    for n in values:
        orbits += values[n]

    return orbits


def find_path(node_a, node_b):
    # Traverse from node_a to root and store distance
    counter = 0
    while node_a != NODE_ROOT:
        node_a = parents[node_a]
        visited[node_a] = counter
        counter += 1

    # Traverse from node_b to path from node_a or to root
    # if not found (not really considered)
    counter = 0
    while node_b != NODE_ROOT:
        node_b = parents[node_b]
        if node_b in visited:
            return counter + visited[node_b]
        counter += 1


def solve(data):
    for edge in data:
        node_a, node_b = edge[:-1].split(')')

        # Part 1 preprocessing
        if node_a not in neighbours:
            neighbours[node_a] = []
        neighbours[node_a].append(node_b)

        values[node_a] = 0
        values[node_b] = 0

        # Part 2 preprocessing
        parents[node_b] = node_a


    part1 = count_orbits()
    part2 = find_path("YOU", "SAN")

    return part1, part2


def check(value, expected):
    if value == expected:
        return "OK %s" % str(value)
    return "Expected %s, got %s" % (str(expected), str(value))


def test(path, expected_path = None):
    data = None
    print("File:", path)
    with open(path, "r") as file:
        data = [line for line in file.readlines()]

    expected = None
    if expected_path:
        with open(expected_path, "r") as file:
            expected = [int(line) for line in file.readlines()]

    part_1, part_2 = solve(data)

    if expected:
        print("Part 1:", check(part_1, expected[0]))
        print("Part 2:", check(part_2, expected[1]))
    else:
        print("Part 1:", part_1)
        print("Part 2:", part_2)
    print("")


def main():
    test("input.txt")
    # test("tests/2.in", "tests/2.out")


if __name__ == '__main__':
    main()
