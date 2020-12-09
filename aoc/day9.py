from aoc.day1 import find_numbers_that_sum_to_goal
from aoc.utils import load_input


def part1(preamble_size=25):
    data = [int(line) for line in load_input() if line]
    for i, number in enumerate(data):
        if i >= preamble_size:
            start = i - preamble_size
            end = i + 1
            numbers = find_numbers_that_sum_to_goal(
                set(data[start:end]), sample_size=2, goal_number=number
            )
            if len(set(numbers)) < 2:
                return number
    return None


def part2(preamble_size=25):
    invalid_number = part1(preamble_size)
    data = [int(line) for line in load_input() if line]
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if sum(data[i:j]) == invalid_number:
                return min(data[i:j]) + max(data[i:j])
    return None


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
