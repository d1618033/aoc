from aoc.day24 import load_data, part1, part2


def test_part1():
    assert part1() == 10


def test_part2():
    assert part2() == 2208


def test_load_data():
    assert load_data(["nenwweswse"]) == [["ne", "nw", "w", "e", "sw", "se"]]
