import pytest

from aoc.year2020.day18 import evaluate_part_1, evaluate_part_2


@pytest.mark.parametrize(
    "line,expected_part_1,expected_part_2",
    [
        ("2 * 3 + (4 * 5)", 26, 46),
        ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437, 1445),
        ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240, 669060),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632, 23340),
    ],
)
def test_evaluate(line, expected_part_1, expected_part_2):
    assert evaluate_part_1(line) == expected_part_1
    assert evaluate_part_2(line) == expected_part_2
