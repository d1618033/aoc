from dataclasses import dataclass
from typing import List

from sympy.ntheory.modular import crt

from aoc.utils import load_input


@dataclass
class Bus:
    id: int
    index: int


@dataclass
class Data:
    arrival: int
    buses: List[Bus]


def load_data():
    data = load_input()
    arrival = int(data[0])
    buses = [
        Bus(id=int(bus), index=i)
        for i, bus in enumerate(data[1].split(","))
        if bus != "x"
    ]
    return Data(arrival=arrival, buses=buses)


def part1():
    data = load_data()

    def minutes_to_wait(bus):
        return bus.id - data.arrival % bus.id

    bus = min(data.buses, key=minutes_to_wait)
    return bus.id * minutes_to_wait(bus)


def part2():
    data = load_data()
    return crt(
        [bus.id for bus in data.buses],
        [bus.id - bus.index for bus in data.buses],
    )[0]


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
