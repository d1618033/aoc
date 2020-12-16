import pytest

from aoc.day16 import get_field_order, load_data, part1


def test_part1():
    assert part1() == 71


@pytest.mark.input_file("example_2")
def test_get_field_order():
    data = load_data()
    assert get_field_order(data) == ["row", "class", "seat"]
