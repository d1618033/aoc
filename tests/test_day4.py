import pytest
from pydantic import ValidationError

from aoc.day4 import (
    AdvancedPassportModel,
    EyeColor,
    SimplePassportModel,
    parse_input,
    parse_single_passport,
    part1,
    part2,
)


@pytest.mark.input_file("example_part1")
def test_part1():
    assert part1() == 2


@pytest.mark.input_file("example_part1")
def test_parse_input_simple_model():
    assert parse_input(SimplePassportModel) == [
        SimplePassportModel(
            byr=1937,
            iyr=2017,
            eyr=2020,
            hgt="183cm",
            hcl="#fffffd",
            ecl="gry",
            pid="860033327",
            cid="147",
        ),
        None,
        SimplePassportModel(
            byr=1931,
            iyr=2013,
            eyr=2024,
            hgt="179cm",
            hcl="#ae17e1",
            ecl="brn",
            pid="760753108",
            cid=None,
        ),
        None,
    ]


@pytest.mark.input_file("example_part2")
def test_parse_input_advanced_model():
    assert parse_input(AdvancedPassportModel) == [
        None,
        None,
        None,
        None,
        AdvancedPassportModel(
            byr=1980,
            iyr=2012,
            eyr=2030,
            hgt="74in",
            hcl="#623a2f",
            ecl="grn",
            pid="087499704",
            cid=None,
        ),
        AdvancedPassportModel(
            byr=1989,
            iyr=2014,
            eyr=2029,
            hgt="165cm",
            hcl="#a97842",
            ecl="blu",
            pid="896056539",
            cid="129",
        ),
        AdvancedPassportModel(
            byr=2001,
            iyr=2015,
            eyr=2022,
            hgt="164cm",
            hcl="#888785",
            ecl="hzl",
            pid="545766238",
            cid="88",
        ),
        AdvancedPassportModel(
            byr=1944,
            iyr=2010,
            eyr=2021,
            hgt="158cm",
            hcl="#b6652a",
            ecl="blu",
            pid="093154719",
            cid=None,
        ),
    ]


@pytest.mark.input_file("example_part2")
def test_part2():
    assert part2() == 4


def test_hcl_exact_match():
    with pytest.raises(ValidationError):
        parse_single_passport(
            "iyr:2010 hgt:158cm hcl:#b6652aZ ecl:blu byr:1944 eyr:2021 pid:093154719",
            AdvancedPassportModel,
        )
