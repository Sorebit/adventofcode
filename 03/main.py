# https://adventofcode.com/2019/day/3
#
# Complexity could be better for part 1.
# It doesn't matter since not that better complexity for part 2.

import math

class Wire(object):
    def __init__(self, lines):
        self.lines = lines
        self.visited = {} # self.visited[x][y] = step_count
        self.closest = math.inf
        self.shortest = math.inf
        self.step_counter = 0


    def _visit(self, x, y):
        if x not in self.visited:
            self.visited[x] = {}
        self.visited[x][y] = self.step_counter


    def _is_visited(self, x, y):
        return x in self.visited and y in self.visited[x]


    def traverse(self, other = None):
        lookup = {"U": [0, 1], "D": [0, -1], "L": [-1, 0], "R": [1, 0]}
        x, y = 0, 0
        for line in self.lines:
            # Calculate deltas used for traversing each field
            dx, dy = lookup[line[:1]]
            distance = int(line[1:])
            
            # Actually visit fields
            for _ in range(distance):
                self._visit(x, y)
                
                # Check for crossings if other Wire passed as param
                if other and (x, y) != (0, 0) and other._is_visited(x, y):
                    # We've got a crosssing
                    # Check if it's better than current for part 1
                    man = abs(x) + abs(y)
                    self.closest = min(self.closest, man)

                    # Check if it's better than current for part 2
                    crosss_step_count = self.visited[x][y] + other.visited[x][y]
                    self.shortest = min(self.shortest, crosss_step_count)


                # Step in line direction
                x, y = x + dx, y + dy
                self.step_counter += 1

            # Visit wire ending
            # There probably exists an edge case when two wires meet at the end
            # Luckily, not in the tests cases
            self._visit(x, y)

        return self.closest, self.shortest


def check(value, expected):
    if value == expected:
        return "OK %d" % value
    return "Expected %d, got %d" % (expected, value)


def solve(path, expected_path = None):
    lines = None
    print("File:", path)
    with open(path, "r") as file:
        lines = [line.split(",") for line in file.readlines()]

    expected = None
    if expected_path:
        with open(expected_path, "r") as file:
            expected = [int(line) for line in file.readlines()]

    one = Wire(lines[0])
    two = Wire(lines[1])

    one.traverse()
    part_1, part_2 = two.traverse(one)

    if expected:
        print("Part 1:", check(part_1, expected[0]))
        print("Part 2:", check(part_2, expected[1]))
    else:
        print("Part 1:", part_1)
        print("Part 2:", part_2)
    print("")


def main():
    solve("tests/1.txt", "tests/1_out.txt")
    solve("tests/2.txt", "tests/2_out.txt")
    solve("tests/3.txt", "tests/3_out.txt")
    solve("input.txt")
        

if __name__ == '__main__':
    main()
