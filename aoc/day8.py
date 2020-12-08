from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import List

from aoc.utils import load_input, logger


class Operation(Enum):
    no_operation = "nop"
    jump = "jmp"
    accumulate = "acc"


@dataclass
class Instruction:
    operation: Operation
    arg: int


class ProgramStatus(Enum):
    infinite_loop = "infinite_loop"
    exit = "exit"


@dataclass
class ProgramResult:
    status: ProgramStatus
    value: int


def parse_line(line: str) -> Instruction:
    op, arg = line.split(" ")
    return Instruction(Operation(op.strip()), int(arg.strip()))


def parse_program(data: List[str]) -> List[Instruction]:
    return [parse_line(line) for line in data if line.strip()]


def run_program(program: List[Instruction]) -> ProgramResult:
    value = 0
    current_instruction = 0
    seen_instructions = set()
    while current_instruction < len(program):
        if current_instruction in seen_instructions:
            logger.debug(f"{current_instruction} already seen")
            return ProgramResult(ProgramStatus.infinite_loop, value)
        seen_instructions.add(current_instruction)
        instruction = program[current_instruction]
        if instruction.operation == Operation.no_operation:
            current_instruction += 1
            continue
        if instruction.operation == Operation.accumulate:
            value += instruction.arg
            current_instruction += 1
        elif instruction.operation == Operation.jump:
            current_instruction += instruction.arg
    return ProgramResult(ProgramStatus.exit, value)


def part1() -> int:
    program = parse_program(load_input())
    return run_program(program).value


def part2() -> int:
    program = parse_program(load_input())
    to_replace = {
        Operation.no_operation: Operation.jump,
        Operation.jump: Operation.no_operation,
    }
    for i, instruction in enumerate(program):
        if instruction.operation in to_replace:
            new_program = deepcopy(program)
            new_program[i].operation = to_replace[instruction.operation]
            logger.debug(
                f"Trying to replace {i}:{instruction.operation}"
                f" with {new_program[i].operation}"
            )
            result = run_program(new_program)
            if result.status == ProgramStatus.exit:
                return result.value
    raise AssertionError("One replacement should have fixed it")


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
