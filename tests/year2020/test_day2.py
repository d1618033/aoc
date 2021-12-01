import pytest

from aoc.year2020.day2 import is_valid_part_1, is_valid_part_2

policies = [
    "1-3 a: abcde",
    "1-3 b: cdefg",
    "2-9 c: ccccccccc",
]


@pytest.mark.parametrize("policy,valid", zip(policies, (True, False, True)))
def test_is_valid_part_1(policy, valid):
    assert is_valid_part_1(policy) is valid


@pytest.mark.parametrize("policy,valid", zip(policies, (True, False, False)))
def test_is_valid_part_2(policy, valid):
    assert is_valid_part_2(policy) is valid
