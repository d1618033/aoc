from sympy.ntheory.modular import crt

from aoc.utils import load_input


def part1():
    data = load_input()
    arrival = int(data[0])
    buses = [int(bus) for bus in data[1].split(",") if bus != "x"]

    def minutes_to_wait(bus):
        return bus - arrival % bus

    bus = min(buses, key=minutes_to_wait)
    return bus * minutes_to_wait(bus)


def part2():
    buses = [
        (int(bus), i) for i, bus in enumerate(load_input()[1].split(",")) if bus != "x"
    ]
    return crt(
        [bus[0] for bus in buses],
        [bus[0] - bus[1] for bus in buses],
    )[0]


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
