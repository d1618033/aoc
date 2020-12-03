import re
from typing import Callable

from pydantic.main import BaseModel

from aoc.utils import load_input, unwrap


class Policy(BaseModel):
    lower: int
    upper: int
    letter: str
    password: str


def parse_line(line: str) -> Policy:
    match = unwrap(
        re.match(
            r"(?P<lower>\d+)-(?P<upper>\d+)\s+(?P<letter>\w+):\s+(?P<password>\w+)",
            line,
        )
    ).groupdict()
    return Policy(**match)


def is_valid_part_1(line: str) -> bool:
    policy = parse_line(line)
    return policy.lower <= policy.password.count(policy.letter) <= policy.upper


def is_valid_part_2(line: str) -> bool:
    policy = parse_line(line)

    def letter_is_in_pos(position):
        return policy.password[position - 1] == policy.letter

    return letter_is_in_pos(policy.lower) ^ letter_is_in_pos(policy.upper)


def num_valid_in_file(validation_func: Callable[[str], bool]) -> int:
    return sum(validation_func(line) for line in load_input())


def main():
    print("part1", num_valid_in_file(is_valid_part_1))
    print("part2", num_valid_in_file(is_valid_part_2))


if __name__ == "__main__":
    main()
