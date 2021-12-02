from dataclasses import dataclass, field

from aoc.utils import load_input


@dataclass
class State:
    position: int = field(default=0)
    depth: int = field(default=0)


@dataclass
class StatePart2(State):
    aim: int = field(default=0)


def part1():
    data = load_input()
    state = State()
    for line in data:
        match line.split():
            case (op, arg):
                arg = int(arg)
                match op:
                    case "forward":
                        state.position += arg
                    case "up":
                        state.depth -= arg
                    case "down":
                        state.depth += arg
                    case _:
                        raise ValueError(f"Unknown op {op}")
            case _:
                raise ValueError(f"Can't parse line: {line}")
    return state.position * state.depth


def part2():
    data = load_input()
    state = StatePart2()
    for line in data:
        match line.split():
            case (op, arg):
                arg = int(arg)
                match op:
                    case "forward":
                        state.position += arg
                        state.depth += arg * state.aim
                    case "up":
                        state.aim -= arg
                    case "down":
                        state.aim += arg
                    case _:
                        raise ValueError(f"Unknown op {op}")
            case _:
                raise ValueError(f"Can't parse line: {line}")
    return state.position * state.depth


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
