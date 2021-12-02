from dataclasses import dataclass, field

from pydantic import BaseModel

from aoc.utils import iadd, isub, load_input


@dataclass
class State:
    position: int = field(default=0)
    depth: int = field(default=0)


@dataclass
class StatePart2(State):
    aim: int = field(default=0)


class Command(BaseModel):
    op: str
    arg: int


def run_commands(commands, op_to_func):
    for cmd in commands:
        op_to_func[cmd.op](cmd.arg)


def parse(data):
    commands = []
    for row in data:
        match row.split():
            case (op, arg):
                commands.append(Command(op=op, arg=arg))
            case _:
                raise ValueError(f"Can't parse line: {row}")
    return commands


def part1():
    state = State()
    op_to_func = {
        "forward": iadd(state, "position"),
        "up": isub(state, "depth"),
        "down": iadd(state, "depth"),
    }
    run_commands(parse(load_input()), op_to_func)
    return state.position * state.depth


def part2():
    state = StatePart2()

    def forward(v):
        state.position += v
        state.depth += v * state.aim

    op_to_func = {
        "forward": forward,
        "up": isub(state, "aim"),
        "down": iadd(state, "aim"),
    }
    run_commands(parse(load_input()), op_to_func)
    return state.position * state.depth


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
