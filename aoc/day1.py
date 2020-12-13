import itertools
from math import prod
from typing import Final, Set, Tuple

from aoc.utils import compose, load_input

GOAL_NUMBER: Final = 2020


def find_numbers_that_sum_to_goal(
    numbers: Set[int], sample_size: int, goal_number: int = GOAL_NUMBER
) -> Tuple[int, ...]:
    for sample in itertools.combinations(numbers, r=sample_size - 1):
        complement = goal_number - sum(sample)
        if complement in numbers:
            return (complement,) + sample
    return tuple()


multiply_numbers_that_sum_to_goal = compose(prod, find_numbers_that_sum_to_goal)


def load_data():
    return {int(line) for line in load_input()}


def part1(numbers=None):
    if numbers is None:
        numbers = load_data()
    return multiply_numbers_that_sum_to_goal(numbers, sample_size=2)


def part2(numbers=None):
    if numbers is None:
        numbers = load_data()
    return multiply_numbers_that_sum_to_goal(numbers, sample_size=3)


def main():
    numbers = load_data()
    print("part1", part1(numbers))
    print("part2", part2(numbers))


if __name__ == "__main__":
    main()
