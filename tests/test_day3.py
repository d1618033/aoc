import pytest

from aoc.day3 import Grid, part1, part2


@pytest.fixture
def grid():
    return Grid.from_file("example")


def test_part1(grid):
    assert part1(grid) == 7


def test_part2(grid):
    assert part2(grid) == 336
