from functools import reduce

from aoc.utils import load_input


def part1():
    data = load_input()
    arrival = int(data[0])
    buses = [int(bus) for bus in data[1].split(",") if bus != "x"]

    def minutes_to_wait(bus):
        return bus - arrival % bus

    bus = min(buses, key=minutes_to_wait)
    return bus * minutes_to_wait(bus)


def chinese_remainder(n, a):
    sum_ = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum_ += a_i * mul_inv(p, n_i) * p
    return sum_ % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def part2():
    buses = [
        (int(bus), i) for i, bus in enumerate(load_input()[1].split(",")) if bus != "x"
    ]
    return chinese_remainder(
        n=[bus[0] for bus in buses],
        a=[bus[0] - bus[1] for bus in buses],
    )


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
