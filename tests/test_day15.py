from itertools import islice

from aoc.day15 import number_game, part1


def test_number_game():
    assert list(islice(number_game([0, 3, 6]), 0, 10)) == [0, 3, 6, 0, 3, 3, 1, 0, 4, 0]


def test_part1():
    assert part1() == 436
