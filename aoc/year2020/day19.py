import itertools
from typing import Callable, Dict, List, Tuple, Union

from arpeggio import (
    EOF,
    ArpeggioError,
    NoMatch,
    OneOrMore,
    ParserPython,
    PTNodeVisitor,
    RegExMatch,
    ZeroOrMore,
    visit_parse_tree,
)

from aoc.utils import load_input, logger


def rule_definition_grammar():
    def rule_id():
        return RegExMatch(r"\d+")

    def rule_sequence():
        return OneOrMore(rule_id)

    def character():
        return RegExMatch('"[a-z]"')

    def one_of_rule_sequences():
        return rule_sequence, ZeroOrMore("|", rule_sequence)

    def rule_definition():
        return rule_id, ":", [one_of_rule_sequences, character]

    return OneOrMore(rule_definition), EOF


class RuleDefinitionVisitor(PTNodeVisitor):
    _internal_rules: Dict[str, Union[str, Callable, Tuple, List]] = {}
    rules: Dict[str, Callable] = {}

    def generate_rule(self, i):
        def rule(rule_number=i):
            return self._internal_rules[f"rule_{rule_number}"]

        rule.__name__ = f"rule_{i}"
        self.rules[rule.__name__] = rule

    def visit_rule_id(self, node, _):
        rule = int(node.value)
        if rule not in self.rules:
            self.generate_rule(rule)
        return self.rules[f"rule_{node.value}"]

    def visit_rule_sequence(self, _, children):
        return tuple(children)

    def visit_character(self, node, _):
        return node.value.replace('"', "")

    def visit_one_of_rule_sequences(self, _, children):
        return list(children)

    def visit_rule_definition(self, _, children):
        self._internal_rules[children[0].__name__] = children[1]


def part1():
    rules, messages = load_input(delim="\n\n")
    rule = get_root_rule(rules.splitlines())
    return get_num_valid(messages, rule)


def get_num_valid(messages, rule):
    parser = ParserPython(rule)
    num_valid = 0
    for message in messages.splitlines():
        try:
            pt = parser.parse(message)
        except (ArpeggioError, NoMatch) as e:
            logger.error(f"failed to parse {message}: {e}")
            continue
        logger.info(f"successfully parsed {message}: {pt.tree_str()}")
        num_valid += 1
    return num_valid


def get_root_rule(rules):
    visitor = parse_rules(rules)

    def root_rule():
        return visitor.rules["rule_0"], EOF

    return root_rule


def parse_rules(rules):
    parser = ParserPython(rule_definition_grammar)
    visitor = RuleDefinitionVisitor()
    for line in rules:
        if not line.strip():
            continue
        parse_tree = parser.parse(line.strip())
        visit_parse_tree(parse_tree, visitor)
    return visitor


def part2():
    rules, messages = load_input(delim="\n\n")
    visitor = parse_rules(rules.splitlines())
    all_possible_42 = set(generate_all_possible(visitor.rules["rule_42"]))
    all_possible_31 = set(generate_all_possible(visitor.rules["rule_31"]))
    num_valid = 0

    def is_valid_rule_11(message):
        if len(message) == 0:
            return True
        for possible_31 in all_possible_31:
            if message.endswith(possible_31):
                cut_message = message[: -len(possible_31)]
                for possible_42 in all_possible_42:
                    if cut_message.startswith(possible_42):
                        if is_valid_rule_11(cut_message[len(possible_42) :]):
                            return True
        return False

    def is_valid_rule_8_and_11(message):
        if len(message) == 0:
            return False
        for possible in all_possible_42:
            if message.startswith(possible) and len(message) > len(possible):
                if is_valid_rule_11(message[len(possible) :]):
                    return True
                if is_valid_rule_8_and_11(message[len(possible) :]):
                    return True
        return False

    for message in messages.splitlines():
        if is_valid_rule_8_and_11(message):
            num_valid += 1

    return num_valid


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()


def generate_all_possible(rule, prefix=""):
    if callable(rule):
        rule = rule()
    if isinstance(rule, list):
        for sub_rule in rule:
            yield from generate_all_possible(sub_rule, prefix)
    elif isinstance(rule, tuple):
        for possibles in itertools.product(
            *[generate_all_possible(sub_rule, prefix) for sub_rule in rule]
        ):
            yield "".join(possibles)
    elif isinstance(rule, str):
        yield prefix + rule


def generate_all_possible_from_rule_name(rule_name):
    rules = load_input(delim="\n\n")[0]
    visitor = parse_rules(rules.splitlines())
    yield from generate_all_possible(visitor.rules[rule_name])
