# https://adventofcode.com/2019/day/4

def check_double(num):
    for i in range(len(num) - 1):
        if num[i] == num[i + 1]:
            return True
    return False


def check_part_2(num):
    for i in range(1, 10):
        if str(i) * 2 in num and not str(i) * 3 in num:
            return True
    return False


def main():
    input_range = range(168630, 718098)

    part_1 = 0
    part_2 = 0
    for num in input_range:
        num = str(num)
        # Check if ascending numbers
        if ''.join(sorted(num)) != num:
            continue
        if check_double(num):
            part_1 += 1
        if check_part_2(num):
            part_2 += 1

    print("Part 1:", part_1)
    print("Part 2:", part_2)


if __name__ == '__main__':
    main()
