import pytest

from aoc.year2020.day10 import part1, part2


def test_part1():
    assert part1() == 35


def test_part2():
    assert part2() == 8


@pytest.mark.input_file("example_2")
def test_part2_second_example():
    assert part2() == 19208
