from dataclasses import dataclass
from functools import total_ordering

from aenum import MultiValueEnum

from aoc.utils import load_input


class Direction(MultiValueEnum):
    lower = "L", "F"
    higher = "R", "B"


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


@total_ordering
@dataclass(frozen=True, eq=True)
class Seat:
    row: int
    col: int

    @property
    def id(self):
        return 8 * self.row + self.col

    def __gt__(self, other):
        return self.id > other.id


def get_seat(directions):
    return Seat(row=binary_search(directions[:7]), col=binary_search(directions[7:]))


def get_seats():
    for row in load_input():
        yield get_seat(list(map(Direction, row)))


def part1():
    return max(seat.id for seat in get_seats())


def part2():
    taken_seats = set(get_seats())
    min_seat = min(taken_seats)
    max_seat = max(taken_seats)
    possible_seats = {
        seat
        for row in range(1, 2 ** 7 - 1)
        for col in range(8)
        if (seat := Seat(row=row, col=col)) >= min_seat and seat <= max_seat
    }
    [your_seat] = possible_seats - taken_seats
    return your_seat.id


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
