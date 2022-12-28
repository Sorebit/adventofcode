from dataclasses import dataclass
import itertools
import operator
from pathlib import Path
from pprint import pprint
import sys

from aoc import lines, swap_kv


op = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.floordiv  # floordiv?
}
"""Operator from string"""

s = swap_kv(op)
"""String from operator (just for printing)"""


@dataclass
class Node:
    name: str
    value: int | None
    operator: any
    left: any  # Self | None
    right: any  # Self | None

    def expr(self, humn_is_value: bool = False):
        """String representation of expression at node"""
        if self.name == 'humn':
            if humn_is_value:
                return self.value
            else:
                return self.name

        if self.value is not None:
            return self.value

        left_val = self.left.expr(humn_is_value)
        right_val = self.right.expr(humn_is_value)

        o = s[self.operator] if self.name != 'root' else '='
        return f'({left_val} {o} {right_val})'

    def eval(self, find_humn=False):
        """Simplify expression by evaluating where possible. Updates values along.

        The only scenario when eval is not possible is if subtree has `humn`
        in it. In such case return expression as string.
        """
        if self.name == 'humn':
            if find_humn:
                return self.name
            else:
                # Just evaluate the expression, treating humn as its supplied value
                return self.value

        if self.value is not None:
            return self.value

        left_val = self.left.eval(find_humn)
        right_val = self.right.eval(find_humn)
        if type(left_val) == type(right_val) == int:
            # Evaluate the node
            self.value = self.operator(left_val, right_val)
            # Children have already been evalueated and are no longer needed
            self.left, self.right = None, None
            return self.value

        # One child is not an int. Treat it as an expression
        o = s[self.operator] if self.name != 'root' else '='
        return f'({left_val} {o} {right_val})'

    @property
    def inverse_operator(self):
        inverse = {
            operator.add: operator.sub,
            operator.sub: operator.add,
            operator.mul: operator.floordiv,
            operator.floordiv: operator.mul,
        }

        return inverse[self.operator]


def untangle(root: Node):
    """After simplifying, the remaining tree is just a path from root to humn
    with additional value nodes along the path.

    Example input after simplification:
                (root)
               /      \
            (/)        (150)
           /   \
        (+)     (4)
       /   \
    (4)     (*)
           /   \
        (2)    (-)
              /   \
        (humn)     (3)
    """
    if root.left.value:
        result = root.left.value
        current = root.right
    else:
        result = root.right.value
        current = root.left

    while True:
        if current.name == 'humn':
            break

        if current.right.value:
            # ? + 4 = 150  -> ? = 150 - 4
            # ? - 4 = 150  -> ? = 150 + 4
            # ? * 4 = 150  -> ? = 150 / 4
            # ? / 4 = 150  -> ? = 150 * 4
            result = current.inverse_operator(result, current.right.value)
            current = current.left
        else:
            if current.operator in (operator.add, operator.mul):
                # 4 * ? = 150  ->  ? = 150 / 4
                # 4 + ? = 150  ->  ? = 150 - 4
                result = current.inverse_operator(result, current.left.value)
            else:
                # 4 / ? = 150  ->  ? = 4 / 150
                # 4 - ? = 150  ->  -? = 150 - 4,  ? = 4 - 150
                result = current.operator(current.left.value, result)

            current = current.right

    return result


def solve(in_file: Path, part: int):
    monkeys: dict[str, Node] = dict()  # Nodes by name

    for line in lines(in_file):
        words = line.split()
        name, args = words[0][:-1], words[1:]
        if len(args) == 1:
            # name: value
            m = Node(name, int(args[0]), None, None, None)
        else:
            # name: left operator right
            m = Node(name, None, op[args[1]], args[0], args[2])
        monkeys[name] = m

    for monkey in monkeys.values():
        if monkey.value is None:
            left_name = monkey.left
            right_name = monkey.right
            monkey.left = monkeys[left_name]
            monkey.right = monkeys[right_name]

    # Tree is now created
    root = monkeys['root']
    if part == 1:
        # Part 1
        return root.eval()

    # Part 2
    root.left.eval(find_humn=True)
    root.right.eval(find_humn=True)

    print(root.expr(humn_is_value=False))

    return untangle(root)


if __name__ == '__main__':
    # python 21.py in/21/...
    in_file = Path(sys.argv[1])
    part_1 = solve(in_file, 1)
    part_2 = solve(in_file, 2)
    print(part_1, part_2)
