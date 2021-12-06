import pytest

from aoc.year2021.day6 import Fishes, get_num_fishes, part1, part2


def test_part1():
    assert part1() == 5934


def test_part2():
    assert part2() == 26984457539


def test_get_num_fishes():
    assert get_num_fishes(18) == 26
    assert get_num_fishes(80) == 5934


@pytest.mark.parametrize(
    "input_,expected",
    [
        ([2, 3, 2, 0, 1], [1, 1, 2, 8, 6, 0]),
        ([7, 7, 0], [6, 6, 6, 8]),
        ([0, 0], [6, 6, 8, 8]),
    ],
)
def test_next(input_, expected):
    assert sorted(Fishes(input_).next().all_numbers) == sorted(expected)


def test_len():
    assert len(Fishes([0, 1, 2, 2, 3, 4])) == 6


def test_example():
    fishes = Fishes(
        [3, 4, 3, 1, 2],
    )
    days = [
        [2, 3, 2, 0, 1],
        [1, 2, 1, 6, 0, 8],
        [0, 1, 0, 5, 6, 7, 8],
        [6, 0, 6, 4, 5, 6, 7, 8, 8],
        [5, 6, 5, 3, 4, 5, 6, 7, 7, 8],
        [4, 5, 4, 2, 3, 4, 5, 6, 6, 7],
        [3, 4, 3, 1, 2, 3, 4, 5, 5, 6],
        [2, 3, 2, 0, 1, 2, 3, 4, 4, 5],
        [1, 2, 1, 6, 0, 1, 2, 3, 3, 4, 8],
        [0, 1, 0, 5, 6, 0, 1, 2, 2, 3, 7, 8],
        [6, 0, 6, 4, 5, 6, 0, 1, 1, 2, 6, 7, 8, 8, 8],
        [5, 6, 5, 3, 4, 5, 6, 0, 0, 1, 5, 6, 7, 7, 7, 8, 8],
        [4, 5, 4, 2, 3, 4, 5, 6, 6, 0, 4, 5, 6, 6, 6, 7, 7, 8, 8],
        [3, 4, 3, 1, 2, 3, 4, 5, 5, 6, 3, 4, 5, 5, 5, 6, 6, 7, 7, 8],
        [2, 3, 2, 0, 1, 2, 3, 4, 4, 5, 2, 3, 4, 4, 4, 5, 5, 6, 6, 7],
        [1, 2, 1, 6, 0, 1, 2, 3, 3, 4, 1, 2, 3, 3, 3, 4, 4, 5, 5, 6, 8],
        [0, 1, 0, 5, 6, 0, 1, 2, 2, 3, 0, 1, 2, 2, 2, 3, 3, 4, 4, 5, 7, 8],
        [6, 0, 6, 4, 5, 6, 0, 1, 1, 2, 6, 0, 1, 1, 1, 2, 2, 3, 3, 4, 6, 7, 8, 8, 8, 8],
    ]
    for i, day in enumerate(days):
        fishes.next()
        assert sorted(fishes.all_numbers) == sorted(day)
        assert len(fishes) == len(day)
