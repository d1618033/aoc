import pytest

from aoc.year2020.day5 import Direction, binary_search, part1, part2


def test_binary_search():
    assert binary_search(list(map(Direction, "FBFBBFF"))) == 44


def test_part1():
    assert part1() == 820


@pytest.mark.input_file("input")
def test_part2():
    assert part2() == 711
