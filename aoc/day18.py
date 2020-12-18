import operator

from arpeggio import (
    EOF,
    OneOrMore,
    Optional,
    ParserPython,
    PTNodeVisitor,
    RegExMatch,
    ZeroOrMore,
    visit_parse_tree,
)

from aoc.utils import load_input


def calc_part_1():
    def expression():
        return factor, ZeroOrMore(["+", "-", "*", "/"], factor)

    def factor():
        return Optional(["+", "-"]), [number, ("(", expression, ")")]

    def number():
        return RegExMatch(r"\d*\.\d*|\d+")

    return OneOrMore(expression), EOF


def calc_part_2():
    def number():
        return RegExMatch(r"\d*\.\d*|\d+")

    def factor():
        return Optional(["+", "-"]), [number, ("(", expression, ")")]

    def term():
        return factor, ZeroOrMore(["+", "-"], factor)

    def expression():
        return term, ZeroOrMore(["*", "/"], term)

    return OneOrMore(expression), EOF


class CalcVisitorPart1(PTNodeVisitor):
    def visit_number(self, node, _):
        return float(node.value)

    def visit_factor(self, _, children):
        if len(children) == 1:
            return children[0]
        sign = -1 if children[0] == "-" else 1
        return sign * children[-1]

    def visit_expression(self, _, children):
        expr = children[0]
        operators = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
        }
        for i in range(2, len(children), 2):
            expr = operators[children[i - 1]](expr, children[i])
        return expr


class CalcVisitorPart2(CalcVisitorPart1):
    def visit_term(self, node, children):
        return super().visit_expression(node, children)


def evaluate_part_1(line):
    parser = ParserPython(calc_part_1)
    return visit_parse_tree(parser.parse(line), CalcVisitorPart1())


def evaluate_part_2(line):
    parser = ParserPython(calc_part_2)
    return visit_parse_tree(parser.parse(line), CalcVisitorPart2())


def part1():
    return sum(evaluate_part_1(line) for line in load_input())


def part2():
    return sum(evaluate_part_2(line) for line in load_input())


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
