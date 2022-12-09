from dataclasses import dataclass
from pathlib import Path
import pprint
import sys
# from typing import Self

from aoc import lines


@dataclass
class Node:
    name: str
    is_dir: bool
    children: dict | None # dict[str, Node] for Dirs or None for Files
    parent: any  # Node | None
    size: int | None = None

    def print(self, indent: int = 0):
        node_type = 'dir' if self.is_dir else 'file'
        print(f'{"  " * indent}- {self.name} ({node_type}, size={self.size})')

        if self.is_dir:
            for child in self.children.values():
                child.print(indent + 1)

    def sizes(self):
        """Updates sizes of self and all subdirectories"""
        if not self.is_dir:
            raise NotADirectoryError(self.name)

        total_size = 0
        for child in self.children.values():
            if child.is_dir:
                total_size += child.sizes()
            else:
                total_size += child.size

        self.size = total_size
        return self.size

    def find(self, predicate):
        """Treating self as root of tree, yield all nodes that satisfy predicate"""
        if predicate(self):
            yield self

        if self.is_dir:
            for child in self.children.values():
                yield from child.find(predicate)


current_node = None
root = Node(is_dir=True, name='/', children={}, parent=None)


def change_dir(name):
    global current_node

    if name == '/':
        current_node = root
    elif name == '..':
        current_node = current_node.parent
    else:
        current_node = current_node.children[name]


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    # Construct the tree
    for line in lines(in_file):
        # Command
        if line.startswith('$'):
            _, *command = line.split()
            if command[0] == 'cd':
                change_dir(command[1])
            continue

        # File or directory
        sz_or_dir, name = line.split()
        if sz_or_dir == 'dir':
            is_dir, children, size = True, {}, None
        else:
            is_dir, children, size = False, None, int(sz_or_dir)

        if name not in current_node.children:
            current_node.children[name] = Node(
                is_dir=is_dir, name=name, children=children, parent=current_node, size=size)

    # Part 1
    root.sizes()
    root.print()
    found = root.find(lambda n: n.is_dir and n.size <= 100000)
    result_1 = sum(n.size for n in found)

    # Part 2
    free = 70000000 - root.size
    at_least = 30000000 - free
    candidates = root.find(lambda n: n.is_dir and n.size >= at_least)
    result_2 = min(n.size for n in candidates)

    return result_1, result_2


if __name__ == '__main__':
    # python 07.py in/07/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
