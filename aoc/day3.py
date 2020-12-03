import math
from dataclasses import dataclass
from itertools import starmap
from typing import Callable, Iterator, List, Optional

from aoc.utils import StringEnum, load


class Square(StringEnum):
    tree = "#"
    open = "."


@dataclass
class Coordinate:
    row: int
    col: int


class Grid:
    def __init__(self, data: List[List[Square]]):
        self._data = data

    def __getitem__(self, coordinate: Coordinate) -> Square:
        row = self._data[coordinate.row]
        return row[coordinate.col % len(row)]

    def __contains__(self, coordinate: Coordinate) -> bool:
        return coordinate.row < len(self._data)

    @classmethod
    def from_file(cls, file_name: str) -> "Grid":
        return cls(
            [
                [Square(char) for char in list(line.strip())]
                for line in load(file_name, day=3)
                if line.strip()
            ]
        )

    def __str__(self):
        return "\n".join("".join([col.value for col in row]) for row in self._data)


Stepper = Callable[["Coordinate"], "Coordinate"]


def step_through_grid(
    stepper: Stepper, grid: "Grid", initial_coordinate: Optional[Coordinate] = None
) -> Iterator[Coordinate]:
    if initial_coordinate is None:
        initial_coordinate = Coordinate(row=0, col=0)
    current_coordinate = initial_coordinate
    while (current_coordinate := stepper(current_coordinate)) in grid:
        yield current_coordinate


def make_stepper(right: int, down: int) -> Stepper:
    def stepper(current_coordinate: Coordinate) -> Coordinate:
        return Coordinate(
            row=current_coordinate.row + down, col=current_coordinate.col + right
        )

    return stepper


def num_trees_encountered(stepper, grid):
    return sum(
        grid[coordinate] == Square.tree
        for coordinate in step_through_grid(stepper, grid)
    )


def part1(grid):
    return num_trees_encountered(make_stepper(3, 1), grid)


def part2(grid):
    steppers = starmap(
        make_stepper,
        [
            (1, 1),
            (3, 1),
            (5, 1),
            (7, 1),
            (1, 2),
        ],
    )
    return math.prod(num_trees_encountered(stepper, grid) for stepper in steppers)


def main():
    grid = Grid.from_file("input")
    print("part1", part1(grid))
    print("part2", part2(grid))


if __name__ == "__main__":
    main()
