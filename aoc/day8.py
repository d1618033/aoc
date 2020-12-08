from copy import deepcopy
from dataclasses import dataclass, field
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


@dataclass
class ProgramState:
    value: int = field(default=0)
    current_instruction_index: int = field(default=0)

    def next(self):
        self.current_instruction_index += 1


class ProgramVisitor:
    @staticmethod
    def visit_no_operation(program_state: ProgramState, **_):
        program_state.next()

    @staticmethod
    def visit_accumulate(program_state: ProgramState, arg: int):
        program_state.value += arg
        program_state.next()

    @staticmethod
    def visit_jump(program_state: ProgramState, arg: int):
        program_state.current_instruction_index += arg


def run_program(program: List[Instruction], visitor: ProgramVisitor) -> ProgramResult:
    state = ProgramState()
    seen_instructions = set()
    while state.current_instruction_index < len(program):
        if state.current_instruction_index in seen_instructions:
            logger.debug(f"{state.current_instruction_index} already seen")
            return ProgramResult(ProgramStatus.infinite_loop, state.value)
        seen_instructions.add(state.current_instruction_index)
        instruction = program[state.current_instruction_index]
        getattr(visitor, f"visit_{instruction.operation.name}")(
            program_state=state, arg=instruction.arg
        )
    return ProgramResult(ProgramStatus.exit, state.value)


def part1() -> int:
    program = parse_program(load_input())
    return run_program(program, ProgramVisitor()).value


def part2() -> int:
    program = parse_program(load_input())
    visitor = ProgramVisitor()
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
            result = run_program(new_program, visitor)
            if result.status == ProgramStatus.exit:
                return result.value
    raise AssertionError("One replacement should have fixed it")


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
