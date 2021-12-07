import pytest

from aoc.year2021.day5 import Line, Point, part1, part2


def test_part1():
    assert part1() == 5


def test_part2():
    assert part2() == 12


@pytest.mark.parametrize(
    "line, expected",
    [
        ("2,2 -> 2,1", ["2,2", "2,1"]),
        ("0,9 -> 5,9", ["0,9", "1,9", "2,9", "3,9", "4,9", "5,9"]),
        ("1,0 -> 1,3", ["1,0", "1,1", "1,2", "1,3"]),
        ("1,2 -> 1,0", ["1,2", "1,1", "1,0"]),
        ("9,7 -> 7,9", ["9,7", "8,8", "7,9"]),
    ],
)
def test_line(line, expected):
    assert list(Line.from_str(line).all_points) == list(map(Point.from_str, expected))
