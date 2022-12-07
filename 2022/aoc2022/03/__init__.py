from enum import Enum, auto
import functools
import operator
from os import getenv
from pathlib import Path
import string

class Reader:
    """_summary_
    """
    @classmethod
    def lines(cls, p: Path, strip: bool = True):
        """Yields lines from file :param p: for processing them with or without storage. Opt-out withespace strip"""
        with open(p, 'r') as file:
            for line in file.readlines():
                if strip:
                    yield line.strip()
                else:
                    yield line


VERBOSE = getenv('VERBOSE')




def find_bad_item(backpack: str) -> str:
    # Dokładnie jeden item type per plecak znajduje się w obu przegródkach?
    # Split line (backpack) in half (into two compartments)
    comp_size = int(len(backpack) / 2)
    # print(repr(line), comp_size)
    first, second = backpack[:comp_size], backpack[comp_size:]
    # print(first, second)
    # Only one item appears in both compartmentss
    bad_item = next(iter(
        set(first) & set(second)
    ))
    return bad_item


def find_common(group: list[str]) -> str:
    # More general
    # return next(iter(
    #     set(group[0]) & set(group[1]) & set(group[2])
    # ))
    # Return first element of output set
    return next(iter(
        # Get output set by chaining & operator on all items
        functools.reduce(
            operator.and_,
            # First turn string into set so we get only the item types
            map(set, group)
        )
    ))


def priority(item: str) -> int:
    item_types = string.ascii_letters
    # Find is O(n), so if the test case is big (M) we get O(M*n)
    # To turn this into O(M) we could prepare a letter -> priority hashmap
    priorities = { let: pri + 1 for pri, let in enumerate(string.ascii_letters) }
    # I'm not sure if this is a significant gain, since n=52 and hashing a string has some cost
    # What cost? Well, there's 52 letters, each is going to get hashed only once (CPython str property)
    # So we get basically M + n, where n=52, that's a significant gain.
    # Maybe i'll time it when im done with part 2 to see if i'm not mistaken
    # return priorities[item]
    return item_types.find(item) + 1


def run(in_file: Path):
    result_1 = 0
    
    elves_per_group = 3
    counter = 0
    group = []
    result_2 = 0
    
    for line in Reader.lines(in_file):
        bad_item = find_bad_item(line)
        # The result is the sum of priorities
        result_1 += priority(bad_item)
        
        # Part 2
        group.append(line)
        counter += 1
        if counter == elves_per_group:
            # find common item for whole group
            common_item = find_common(group)
            result_2 += priority(common_item)
            counter = 0
            group = []

    return result_1, result_2

        
part_1, part_2 = run(Path('./in/input'))
assert (part_1, part_2) == (8252, 2828)
print(part_1, part_2)
