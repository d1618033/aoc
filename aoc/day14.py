import re

from aoc.utils import load_input


class Program:
    def __init__(self):
        self._memory = {}
        self._mask = ""

    def set_mask(self, mask):
        self._mask = mask

    def write(self, location, value):
        value_binary = self.pad(value)
        mask = self._mask
        for i, mask_value in enumerate(mask):
            if mask_value != "X":
                value_binary[i] = mask_value
        new_value = int("".join(value_binary), base=2)
        self._memory[location] = new_value

    def pad(self, value):
        value_binary_list = list(bin(int(value)))[2:]
        value_binary = ["0"] * (
            len(self._mask) - len(value_binary_list)
        ) + value_binary_list
        return value_binary

    @property
    def sum(self):
        return sum(self._memory.values())


class ProgramVersion2(Program):
    def write(self, location, value):
        location_binary = self.pad(location)
        mask = self._mask
        for i, mask_i in enumerate(mask):
            if mask_i == "1":
                location_binary[i] = "1"

        for possible_location in self.gen_all_values(location_binary, 0):
            new_location = int("".join(possible_location), base=2)
            self._memory[new_location] = int(value)

    def gen_all_values(self, location_binary, index):
        if index >= len(self._mask) or "X" not in self._mask:
            yield location_binary
            return
        mask_i = self._mask[index]
        if mask_i == "X":
            for bit in range(2):
                new_location_binary = location_binary.copy()
                new_location_binary[index] = str(bit)
                yield from self.gen_all_values(new_location_binary, index + 1)
        else:
            yield from self.gen_all_values(location_binary, index + 1)


def run(program):
    lines = load_input()
    methods = {
        r"^mem\[(?P<location>\d+)\]\s*=\s*(?P<value>\d+)$": program.write,
        r"^mask\s+=\s+(?P<mask>[X01]+)$": program.set_mask,
    }
    for line in lines:
        for pattern, method in methods.items():
            if m := re.match(pattern, line):
                method(**m.groupdict())
    return program.sum


def part1():
    return run(Program())


def part2():
    return run(ProgramVersion2())


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
