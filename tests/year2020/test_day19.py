import pytest
from arpeggio import EOF, ParserPython

from aoc.utils import load_input
from aoc.year2020.day19 import generate_all_possible, parse_rules, part1, part2


@pytest.mark.input_file("example")
def test_part1():
    assert part1() == 2


@pytest.mark.input_file("example_2")
def test_part2():
    assert part2() == 12


@pytest.mark.input_file("example_2")
def test_rules_individually():
    rules = load_input(delim="\n\n")[0]
    visitor = parse_rules(rules.splitlines())
    for _, rule in visitor.rules.items():
        parser = ParserPython(rule, EOF)
        for possible in generate_all_possible(rule):
            parser.parse(possible)


@pytest.mark.input_file("example_2")
@pytest.mark.parametrize(
    "rule,all_possible",
    [
        ("rule_1", ["a"]),
        ("rule_4", ["aa"]),
        ("rule_18", ["aa", "ab", "ba", "bb"]),
        ("rule_25", ["aa", "ab"]),
        ("rule_23", ["aaa", "bbb", "aba"]),
    ],
)
def test_generate_all_possibles(rule, all_possible):
    rules = load_input(delim="\n\n")[0]
    visitor = parse_rules(rules.splitlines())
    assert sorted(generate_all_possible(visitor.rules[rule])) == sorted(all_possible)


@pytest.mark.input_file("input")
def test_part_1_different_way():
    rules, messages = load_input(delim="\n\n")
    visitor = parse_rules(rules.splitlines())
    all_possible = set(generate_all_possible(visitor.rules["rule_0"]))
    matches = [message for message in messages.splitlines() if message in all_possible]
    assert len(matches) == 102
