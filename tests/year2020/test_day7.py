import pytest

from aoc.year2020.day7 import part1, part2


def test_part1():
    assert part1() == 4


def test_part2_example1():
    assert part2() == 32


@pytest.mark.input_file("example_2")
def test_part2_example2():
    assert part2() == 126
