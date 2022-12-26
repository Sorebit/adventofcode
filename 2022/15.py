import itertools
import math
from pathlib import Path
from pprint import pprint
import sys

from aoc import lines, find_all_ints, V, manhattan


def solve_for_y(M, target_y):
    result = 0
    ranges = []

    for sensor in M:
        fuel = M[sensor]
        dist_to_test_y = manhattan(sensor, V(sensor.x, target_y))
        left = fuel - dist_to_test_y
        # print(f'{sensor} wit {fuel} fuel | {left} left')
        # print(f'  to test: {dist_to_test_y}')
        # print(f'     left: {max(0, fuel - dist_to_test_y)}')
        if left >= 0:
            r = range(sensor.x - left, sensor.x + left)
            # print(f'  -> Mark {r}')
            ranges.append(r)

    # We'd like to merge the ranges, so that no number is counted twice
    ranges.sort(key=lambda r: r.start)
    # Start with the left-most range
    start = ranges[0].start
    stop = ranges[0].stop
    # print(f'\nStart with {start}, {stop}')
    for r in ranges[1:]:
        # print(r)
        if r.start <= stop:
            # Jeśli kolejny przedział zaczyna się w środku aktualnego, to
            # możemy wydłużyć aktualny (jeśli ten nowy sięga dalej)
            stop = max(r.stop, stop)
            # print(f'r is now {start}, {stop}')
        else:
            # Jeśli kolejny jest rozłączny (zaczyna się po stopie aktualnego)
            # To możemy dodać aktualny do wyniku, bo się już nic z nim nie
            # zdubluje
            print(f'Add {start}, {stop} = {stop - start + 1}')
            result += (stop - start + 1)
            start = r.start
            stop = r.stop
            # print(f'New range is {start}, {stop}')
    # Na koniec dodajemy to co zostało
    # print(f'Add {start}, {stop} = {stop - start + 1}')
    result += (stop - start + 1)

    found = start != ranges[0].start
    return result, ranges, found


def solve(in_file: Path, test_y):
    M = dict()
    yh = set()

    for line in lines(in_file):
        ints = find_all_ints(line)
        sensor = V(ints[0], ints[1])
        closest_beacon = V(ints[2], ints[3])
        dist = manhattan(sensor, closest_beacon)

        if closest_beacon.y == test_y:
            yh.add(closest_beacon)

        # Map sensor to distance (fuel)
        M[sensor] = dist
        # print(sensor, closest_beacon, '->', dist)

    # Apparently, Beacons are already acccounted for in first part
    res_1, _, _ = solve_for_y(M, test_y)
    result_1 = res_1 - len(yh)

    for y in range(4000000 + 1):
        print(y)
        _, ranges, found = solve_for_y(M, y)
        if found:
            print(f'Found for {y}')
            pprint(ranges)
            # Then I manually calculated the x*4000000 + y idgaf
            break

    result_2 = 0

    return result_1, result_2


if __name__ == '__main__':
    # python {{nn}}.py in/{{nn}}/...
    in_file = Path(sys.argv[1])
    part_1, part_2 = solve(in_file, 2000000)
    print(part_1, part_2)
