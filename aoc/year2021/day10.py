from aoc.utils import load_input


class InvalidSyntax(Exception):
    pass


class InvalidParenthesis(InvalidSyntax):
    def __init__(self, line, invalid_char, expected_char, index):
        self.line = line
        self.invalid_char = invalid_char
        self.expected_char = expected_char
        self.index = index
        super().__init__(
            f"Invalid paranthesis in line {line} at index {index}."
            f" Expected {expected_char} got {invalid_char} instead"
        )


class IncompleteExpression(InvalidSyntax):
    def __init__(self, line, expected):
        self.line = line
        self.expected = expected
        super().__init__(
            f"Incomplete line {line}."
            f" Expected closing parenthesis: {' '.join(expected)}"
        )


def assert_validity(line):
    stack = []
    parens = {
        "(": ")",
        "[": "]",
        "<": ">",
        "{": "}",
    }
    for index, char in enumerate(line):
        if char in parens:
            stack.append(char)
        elif char in parens.values():
            expected_char = parens[stack.pop()]
            if expected_char != char:
                raise InvalidParenthesis(
                    line=line,
                    invalid_char=char,
                    expected_char=expected_char,
                    index=index,
                )
    if stack:
        raise IncompleteExpression(
            line=line, expected=[parens[char] for char in stack[::-1]]
        )


def part1():
    score_map = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    score = 0
    for line in load_input():
        try:
            assert_validity(line)
        except IncompleteExpression:
            pass
        except InvalidParenthesis as e:
            score += score_map[e.invalid_char]
    return score


def calc_score_part2(expected_parens):
    score_map = {")": 1, "]": 2, "}": 3, ">": 4}
    score = 0
    for parens in expected_parens:
        score = 5 * score + score_map[parens]
    return score


def part2():
    scores = []
    for line in load_input():
        try:
            assert_validity(line)
        except InvalidParenthesis:
            pass
        except IncompleteExpression as e:
            scores.append(calc_score_part2(e.expected))
    return sorted(scores)[len(scores) // 2]


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
