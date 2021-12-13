import numpy

from aoc.utils import load_input


def parse():

    data = []
    instructions = []
    for line in load_input():
        if "," in line:
            data.append(list(map(int, line.split(","))))
        elif "fold" in line:
            axis, num = line.split()[-1].split("=")
            instructions.append((axis, int(num)))
    max_x = max(row[0] for row in data)
    max_y = max(row[1] for row in data)
    array = numpy.ones((max_y + 1, max_x + 1)) * 0
    for row in data:
        array[row[1], row[0]] = 1
    return array, instructions


def fold(array, instruction):
    if instruction[0] == "x":
        left, right = array[:, : instruction[1]], array[:, instruction[1] + 1 :]
        right = numpy.flip(right, 1)
        combined = left
        combined[:, -right.shape[1] :] = combined[:, -right.shape[1] :] + right
    else:
        top, bottom = array[: instruction[1], :], array[instruction[1] + 1 :, :]
        bottom = numpy.flip(bottom, 0)
        combined = top
        combined[-bottom.shape[0] :, :] = combined[-bottom.shape[0] :, :] + bottom
    return combined


def part1():
    array, instructions = parse()
    array = fold(array, instructions[0])
    return (array >= 1).sum()


def part2():
    array, instructions = parse()
    for instruction in instructions:
        array = fold(array, instruction)
    printed = []
    for i in range(array.shape[0]):
        row = []
        for j in range(array.shape[1]):
            row.append("#" if array[i, j] >= 1 else ".")
        printed.append("".join(row))
    print("\n".join(printed))


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
