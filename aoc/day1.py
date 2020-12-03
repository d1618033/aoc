from typing import Optional, Set

from aoc.utils import load_input

GOAL_NUMBER = 2020


def part1(numbers: Set[int], goal_number: int = GOAL_NUMBER) -> Optional[int]:
    for number in numbers:
        complement = goal_number - number
        if complement in numbers:
            return complement * number
    return None


def part2(numbers: Set[int], goal_number: int = GOAL_NUMBER) -> Optional[int]:
    for number1 in numbers:
        for number2 in numbers:
            number3 = goal_number - number1 - number2
            if number1 != number2 and number3 in numbers:
                return number1 * number2 * number3
    return None


def main():
    numbers = {int(line) for line in load_input()}
    print("part1", part1(numbers))
    print("part2", part2(numbers))


if __name__ == "__main__":
    main()
