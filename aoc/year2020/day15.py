from collections import defaultdict, deque
from functools import partial
from itertools import count, islice

from aoc.utils import load_ints


def number_game(starting_numbers):
    yield from iter(starting_numbers)
    deque_2 = partial(deque, maxlen=2)
    last_seen = defaultdict(
        deque_2, {number: deque_2([i]) for i, number in enumerate(starting_numbers)}
    )
    current_number = starting_numbers[-1]
    for turn in count(len(starting_numbers)):
        last_seen_indices = last_seen[current_number]
        if len(last_seen_indices) <= 1:
            current_number = 0
        else:
            current_number = last_seen_indices[-1] - last_seen_indices[-2]
        last_seen[current_number].append(turn)
        yield current_number


def get_number_at(index):
    starting_numbers = load_ints(delim=",")
    return next(islice(number_game(starting_numbers), index - 1, index))


def part1():
    return get_number_at(2020)


def part2():
    return get_number_at(30000000)


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
