# https://adventofcode.com/2019/day/1

def get_fuel(weight):
    return max(int(weight / 3) - 2, 0)

def get_add_fuel(weight):
    sum = 0;
    while weight > 0:
        sum += get_fuel(weight)
        weight = get_fuel(weight)
    return sum

def main():
    with open("input.txt", "r") as file:
        data = [int(line) for line in file]
        part1 = sum(get_fuel(m) for m in data)
        part2 = sum(get_add_fuel(m) for m in data)

        print("Advent of Code 2019 - Day 1")
        print("Part 1:", part1)
        print("Part 2:", part2)

if __name__ == '__main__':
    main()
