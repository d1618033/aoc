from collections import Counter

from aoc.utils import load_input


def part1():
    data = load_input()
    counts = Counter((index, bit) for line in data for index, bit in enumerate(line))
    gamma = []
    epsilon = []
    for i in range(len(data[0])):
        if counts[(i, "1")] > counts[(i, "0")]:
            gamma.append("1")
            epsilon.append("0")
        else:
            gamma.append("0")
            epsilon.append("1")
    gamma_num = int("".join(gamma), 2)
    epsilon_num = int("".join(epsilon), 2)
    return gamma_num * epsilon_num


def get_num(data, get_num_to_use):
    possible = data
    index = 0
    while len(possible) > 1:
        counts = Counter([num[index] for num in possible])
        num_to_use = get_num_to_use(counts["0"], counts["1"])
        possible = [num for num in possible if num[index] == num_to_use]
        index += 1
    return int("".join(possible[0]), 2)


def part2():
    data = load_input()
    oxy = get_num(data, lambda a, b: "1" if b >= a else "0")
    co2 = get_num(data, lambda a, b: "0" if a <= b else "1")
    return oxy * co2


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
