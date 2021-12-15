import pytest

from aoc.year2021.day14 import get_counts_of_pairs, parse, part1, part2, step


@pytest.mark.parametrize(
    "num_steps,expected",
    [
        (0, "NNCB"),
        (1, "NCNBCHB"),
        (2, "NBCCNBBBCBHCB"),
        (3, "NBBBCNCCNBBNBNBBCHBHHBCHB"),
        (4, "NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB"),
    ],
)
def test_step(num_steps, expected):
    template, rules = parse()
    for _ in range(num_steps):
        template = step(template, rules)
    assert get_counts_of_pairs(expected) == template


def test_part1():
    assert part1() == 1588


def test_part2():
    assert part2() == 2188189693529
