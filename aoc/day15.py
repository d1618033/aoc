from collections import defaultdict, deque
from dataclasses import dataclass
from functools import partial
from itertools import count, islice
from typing import Optional, List, Set, Tuple

from aoc.utils import load_input, load_ints


def number_game(starting_numbers):
    yield from iter(starting_numbers)
    deque_2 = partial(deque, maxlen=2)
    last_seen = defaultdict(deque_2, {number: deque_2([i]) for i, number in enumerate(starting_numbers)})
    current_number = starting_numbers[-1]
    for turn in count(len(starting_numbers)):
        last_seen_indices = last_seen[current_number]
        if len(last_seen_indices) <= 1:
            current_number = 0
        else:
            current_number = last_seen_indices[-1] - last_seen_indices[-2]
        last_seen[current_number].append(turn)
        yield current_number


def part1():
    starting_numbers = load_ints(delim=",")
    return next(islice(number_game(starting_numbers), 2020-1, 2020))


def part2():
    starting_numbers = load_ints(delim=",")
    return next(islice(number_game(starting_numbers), 30000000-1, 30000000))


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
