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

inverse = {
    operator.add: operator.sub,
    operator.sub: operator.add,
    operator.mul: operator.floordiv,
    operator.floordiv: operator.mul,
}
"""Inverse operation from operation"""


@dataclass
class Node:
    name: str
    value: int | None
    operator: any
    left: any  # Self | None
    right: any  # Self | None

    def eval_1(self):
        """Just evaluate the expression, treating humn as its supplied value"""
        if self.value is None:
            # self.value = self.operator(
            return self.operator(
                self.left.eval_1(),
                self.right.eval_1()
            )

        return self.value

    def expr(self):
        """String representation of expression at node"""
        if self.name == 'humn':
            return self.name

        if self.value is not None:
            return self.value

        o = s[self.operator] if self.name != 'root' else '='
        return f'({self.left.expr()} {o} {self.right.expr()})'

    def eval_2(self):
        """Simplify expression by evaluating where possible. Updates values along.

        The only scenario when eval is not possible is if subtree has `humn`
        in it. In such case return expression as string.
        """
        if self.name == 'humn':
            return 'humn'

        if self.value is not None:
            return self.value

        left_val = self.left.eval_2()
        right_val = self.right.eval_2()
        if type(left_val) == int and type(right_val) == int:
            self.value = self.operator(
                left_val,
                right_val,
            )
            return self.value
        # One of them is not an int, but an expression
        o = s[self.operator] if self.name != 'root' else '='
        return f'({left_val} {o} {right_val})'


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
        inv_op = inverse[current.operator]
        if current.right.value:
            # ? + 4 = 150  -> ? = 150 - 4
            # ? - 4 = 150  -> ? = 150 + 4
            # ? * 4 = 150  -> ? = 150 / 4
            # ? / 4 = 150  -> ? = 150 * 4
            result = inv_op(result, current.right.value)
            current = current.left
        else:
            if current.operator in (operator.add, operator.mul):
                # 4 * ? = 150  ->  ? = 150 / 4
                # 4 + ? = 150  ->  ? = 150 - 4
                result = inv_op(result, current.left.value)
            else:
                # 4 / ? = 150  ->  ? = 4 / 150
                # 4 - ? = 150  ->  -? = 150 - 4,  ? = 4 - 150
                result = current.operator(current.left.value, result)

            current = current.right

    return result


def solve(in_file: Path):
    result_1, result_2 = 0, 0

    monkeys: dict[str, Node] = dict()

    for line in lines(in_file):
        words = line.split()
        name, args = words[0][:-1], words[1:]
        if len(args) == 1:
            m = Node(name, int(args[0]), None, None, None)
        else:
            m = Node(name, None, op[args[1]], args[0], args[2])
        monkeys[name] = m
        # print(name, m)

    for monkey in monkeys.values():
        if monkey.value is None:
            left_name = monkey.left
            right_name = monkey.right
            monkey.left = monkeys[left_name]
            monkey.right = monkeys[right_name]

    result_1 = monkeys['root'].eval_1()

    # Part 2
    monkeys['root'].left.eval_2()
    monkeys['root'].right.eval_2()

    print(monkeys['root'].expr())

    result_2 = untangle(monkeys['root'])

    return result_1, result_2


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
