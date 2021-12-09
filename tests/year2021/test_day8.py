import pytest

from aoc.year2021.day8 import detect_mapping, is_mapping_valid, part1, part2


def test_part1():
    assert part1() == 26


def test_part2():
    assert part2() == 61229


@pytest.mark.parametrize(
    "patterns,mapping",
    [
        (
            "abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg".split(),
            {letter: letter.upper() for letter in "abcdefg"},
        )
    ],
)
def test_detect_mapping(patterns, mapping):
    actual = detect_mapping(patterns)
    assert actual == mapping


def test_is_mapping_valid():
    assert is_mapping_valid(
        "abcefg cf acdeg acdfg bcdf abdfg abdefg acf abcdefg abcdfg".split(),
        {letter: letter.upper() for letter in "abcdefg"},
    )
