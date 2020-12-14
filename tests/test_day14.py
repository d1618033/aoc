import pytest

from aoc.day14 import part1, part2


def test_part1():
    assert part1() == 165


@pytest.mark.input_file("example_2")
def test_part2():
    assert part2() == 208
