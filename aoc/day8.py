from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Set, Tuple

from aoc.utils import load_input


def part1():
    data = load_input()
    return run_program(data).value


class ProgramStatus(Enum):
    infinite_loop = "infinite_loop"
    exit = "exit"


@dataclass
class ProgramResult:
    status: ProgramStatus
    value: int


def run_program(data):
    data = [line for line in data if line.strip()]
    value = 0
    current_instruction = 0
    seen_instructions = set()
    while current_instruction < len(data):
        if current_instruction in seen_instructions:
            print(f"{current_instruction} already seen")
            return ProgramResult(ProgramStatus.infinite_loop, value)
        seen_instructions.add(current_instruction)
        instruction = data[current_instruction].strip()
        op, arg = instruction.split(" ")
        op = op.strip()
        arg = int(arg.strip())
        if op == "nop":
            current_instruction += 1
            continue
        if op == "acc":
            value += arg
            current_instruction += 1
        elif op == "jmp":
            current_instruction += arg
    return ProgramResult(ProgramStatus.exit, value)


def part2():
    data = load_input()
    for i, instruction in enumerate(data):
        if "nop" in instruction or "jmp" in instruction:
            new_data = data.copy()
            if "nop" in instruction:
                new_data[i] = instruction.replace("nop", "jmp")
            elif "jmp" in instruction:
                new_data[i] = instruction.replace("jmp", "nop")
            result = run_program(new_data)
            if result.status == ProgramStatus.exit:
                return result.value


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
