from dataclasses import dataclass, field

from pydantic import BaseModel

from aoc.utils import load_input


class Command(BaseModel):
    op: str
    arg: int


def parse(data):
    commands = []
    for row in data:
        match row.split():
            case (op, arg):
                commands.append(Command(op=op, arg=arg))
            case _:
                raise ValueError(f"Can't parse line: {row}")
    return commands


@dataclass
class State:
    position: int = field(default=0)
    depth: int = field(default=0)


@dataclass
class StatePart2(State):
    aim: int = field(default=0)


def part1():
    data = parse(load_input())
    state = State()
    for cmd in data:
        match cmd:
            case Command(op="forward", arg=arg):
                state.position += arg
            case Command(op="up", arg=arg):
                state.depth -= arg
            case Command(op="down", arg=arg):
                state.depth += arg
            case _:
                raise ValueError(f"Unknown op {op}")
    return state.position * state.depth


def part2():
    data = parse(load_input())
    state = StatePart2()
    for cmd in data:
        match cmd:
            case Command(op="forward", arg=arg):
                state.position += arg
                state.depth += state.aim * arg
            case Command(op="up", arg=arg):
                state.aim -= arg
            case Command(op="down", arg=arg):
                state.aim += arg
            case _:
                raise ValueError(f"Unknown op {op}")
    return state.position * state.depth


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
