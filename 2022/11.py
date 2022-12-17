from dataclasses import dataclass
import operator
from pathlib import Path
from pprint import pprint
import sys

from aoc import lines, find_all_ints

import pdb

modulus = 1

@dataclass
class Monkey:
    items: list[int]
    operation: any
    operand: int | None
    test: int
    throw: dict[bool, int]
    inspected: int

    def inspect(self, old):
        self.inspected += 1
        if self.operand is None:
            return self.operation(old, old) % modulus
            return self.operation(old, old) // 3
        else:
            return self.operation(old, self.operand) % modulus
            return self.operation(old, self.operand) // 3


def solve(in_file: Path):
    global modulus

    result_1, result_2 = 0, 0

    monkeys: dict[int, Monkey] = {}
    monkey_num = None

    for line in lines(in_file):
        if not line:
            continue
        words = line.split()

        if words[0] == 'Monkey':
            monkey_num = int(words[1][:-1])
            monkeys[monkey_num] = Monkey([], None, None, None, {}, 0)
        elif words[0] == 'Starting':
            monkeys[monkey_num].items = find_all_ints(line)
        elif words[0] == 'Operation:':
            op = words[4]
            op_map = {
                '*': operator.mul,
                '+': operator.add
            }
            op_callable = op_map[op]

            monkeys[monkey_num].operation = op_callable
            if words[5] == 'old':
                monkeys[monkey_num].operand = None
            else:
                monkeys[monkey_num].operand = int(words[5])
        elif words[0] == 'Test:':
            monkeys[monkey_num].test = find_all_ints(line)[0]
            modulus *= monkeys[monkey_num].test
        elif words[1] == 'true:':
            monkeys[monkey_num].throw[True] = find_all_ints(line)[0]
        elif words[1] == 'false:':
            monkeys[monkey_num].throw[False] = find_all_ints(line)[0]

    # Initial state is now constructed
    # for n, monkey in monkeys.items():
    #     print(n, monkey)

    for round in range(10000):
        print(f'[ROUND {round}]')
        for n, monkey in monkeys.items():
            # print(f'Monkey {n}')
            for item in monkey.items:
                new_worry = monkey.inspect(item)
                # print(f'Inpsecting {item} => {new_worry}')
                test_outcome = new_worry % monkey.test == 0
                # print(f'Test: {new_worry} div by {monkey.test} -> {test_outcome}')
                selected_monkey = monkey.throw[test_outcome]
                # print(f'Throw [{new_worry}] to Monkey {selected_monkey}')
                monkeys[selected_monkey].items.append(new_worry)

            # TODO: Use deque
            monkey.items = []

        # for n, monkey in monkeys.items():
        #     print(f'{n} ({monkey.inspected}):', monkey.items)

        # pdb.set_trace()
            # It throws away all the items, so
            # monkey.items = []

        top = reversed(sorted([m.inspected for m in monkeys.values()]))
        result_1 = next(top) * next(top)

    return result_1, result_2


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file)
    print(part_1, part_2)
