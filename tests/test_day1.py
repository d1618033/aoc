from aoc.day1 import part1, part2


def test_part1():
    assert part1({1, 30, 1990}) == 1990 * 30


def test_part2():
    assert part2({10, 20, 30, 1990}) == 1990 * 10 * 20
