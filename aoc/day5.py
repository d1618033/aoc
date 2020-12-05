from dataclasses import dataclass

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


@dataclass
class Seat:
    row: int
    col: int

    @property
    def id(self):
        return 8 * self.row + self.col


def get_seat(directions):
    return Seat(row=binary_search(directions[:7]), col=binary_search(directions[7:]))


def get_seats():
    for row in load_input():
        yield get_seat(list(map(Direction, row)))


def part1():
    return max(seat.id for seat in get_seats())


def part2():
    all_seats = [[Seat(row, col) for col in range(8)] for row in range(2 ** 7)]
    for seat in get_seats():
        all_seats[seat.row][seat.col] = None
    for row in all_seats[1:-1]:
        for seat in row:
            if seat is not None:
                return seat.id
    return None


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
