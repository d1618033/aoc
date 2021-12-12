import pytest

from aoc.year2021.day12 import part1, part2


def test_part1():
    assert part1() == 10


@pytest.mark.input_file("example_2")
def test_part1_example2():
    assert part1() == 19


@pytest.mark.input_file("example_3")
def test_part1_example_3():
    assert part1() == 226


def test_part2():
    assert part2() == 36


@pytest.mark.input_file("example_2")
def test_part2_example2():
    assert part2() == 103


@pytest.mark.input_file("example_3")
def test_part2_example_3():
    assert part2() == 3509
