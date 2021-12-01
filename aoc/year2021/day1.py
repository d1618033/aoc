import functools
import itertools
import re
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple

from aoc.utils import load_input, print_


def part1():
    data = list(map(int, load_input()))
    return sum(next_ - prev > 0 for (prev, next_) in zip(data, data[1:]))


def part2():
    data = list(map(int, load_input()))
    data = [a + b + c for a, b, c in zip(data, data[1:], data[2:])]
    return sum(next_ - prev > 0 for (prev, next_) in zip(data, data[1:]))


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
