from more_itertools import sliding_window

from aoc.utils import load_ints


def diff(data):
    return (next_ - prev for (prev, next_) in sliding_window(data, 2))


def part1():
    data = load_ints()
    return sum(num > 0 for num in diff(data))


def part2():
    data = load_ints()
    data = (sum(nums) for nums in sliding_window(data, 3))
    return sum(num > 0 for num in diff(data))


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
