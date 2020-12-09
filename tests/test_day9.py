from aoc.day9 import part1, part2


def test_part1():
    assert part1(preamble_size=5) == 127


def test_part2():
    assert part2(preamble_size=5) == 62
