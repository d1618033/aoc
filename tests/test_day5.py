from aoc.day5 import Direction, binary_search, part1


def test_binary_search():
    assert binary_search(list(map(Direction, "FBFBBFF"))) == 44


def test_part1():
    assert part1() == 820
