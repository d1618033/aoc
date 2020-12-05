from dataclasses import dataclass
from enum import Enum

from aoc.utils import load_input


class Direction(Enum):
    higher = "higher"
    lower = "lower"

    @classmethod
    def from_string(cls, string):
        string = string.strip()
        if string in ["F", "L"]:
            return cls.lower
        if string in ["B", "R"]:
            return cls.higher
        raise ValueError(string)


def binary_search(directions):
    low = 0
    high = 2 ** len(directions)
    for direction in directions:
        current = (low + high) // 2
        if direction == Direction.higher:
            low = current
        else:
            high = current
    return (low + high) // 2


@dataclass
class Seat:
    row: int
    col: int


def get_seat(directions):
    return Seat(row=binary_search(directions[:7]), col=binary_search(directions[7:]))


def get_seat_id(seat):
    return 8 * seat.row + seat.col


def get_seats():
    for row in load_input():
        yield get_seat(list(map(Direction.from_string, row)))


def part1():
    return max(get_seat_id(seat) for seat in get_seats())


def part2():
    all_seats = [[Seat(row, col) for col in range(8)] for row in range(2 ** 7)]
    for seat in get_seats():
        all_seats[seat.row][seat.col] = None
    for row in all_seats[1:-1]:
        for seat in row:
            if seat is not None:
                return get_seat_id(seat)
    return None


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
