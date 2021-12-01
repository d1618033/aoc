import pytest

from aoc.year2020.day4 import AdvancedPassportModel, part1, part2, validate_passport


@pytest.mark.input_file("example_part1")
def test_part1():
    assert part1() == 2


@pytest.mark.input_file("example_part2")
def test_part2():
    assert part2() == 4


def test_hcl_exact_match():
    validation = validate_passport(
        AdvancedPassportModel,
        "iyr:2010 hgt:158cm hcl:#b6652aZ ecl:blu byr:1944 eyr:2021 pid:093154719",
    )
    assert validation is not None
    [error] = validation.errors()
    assert error["loc"] == ("hcl",)
