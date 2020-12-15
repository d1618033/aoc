from itertools import islice

from aoc.day15 import number_game, part1, part2


def test_number_game():
    assert list(islice(number_game([0, 3, 6]), 0, 10)) == [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]


def test_part1():
    assert part1() == 436


def test_part2():
    assert part2() is None
