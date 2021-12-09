from dataclasses import dataclass
from math import prod

from aoc.utils import load_input


@dataclass(frozen=True)
class Cell:
    row_number: int
    col_number: int
    value: int
    board: "Board"

    def get_neighbors(self):
        for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if (
                0 <= self.row_number + drow < self.board.num_rows
                and 0 <= self.col_number + dcol < self.board.num_cols
            ):
                yield self.board.get_cell(
                    self.row_number + drow, self.col_number + dcol
                )

    def __hash__(self):
        return hash((self.row_number, self.col_number))


class Board:
    def __init__(self, data):
        self.cells = [
            [
                Cell(row_number=i, col_number=j, board=self, value=col)
                for j, col in enumerate(row)
            ]
            for i, row in enumerate(data)
        ]

    def get_cell(self, row_number, col_number) -> Cell:
        return self.cells[row_number][col_number]

    @property
    def num_rows(self):
        return len(self.cells)

    @property
    def num_cols(self):
        return len(self.cells[0])

    @property
    def cells_flat(self):
        for row in self.cells:
            for cell in row:
                yield cell


def parse():
    return Board([list(map(int, line)) for line in load_input()])


def part1():
    board = parse()
    sum_risk = 0
    for cell in board.cells_flat:
        if all(neighbor.value > cell.value for neighbor in cell.get_neighbors()):
            sum_risk += cell.value + 1
    return sum_risk


def get_basin_size(cell, checked_cells=None):
    if checked_cells is None:
        checked_cells = set()
    size = 1
    for neighbor in cell.get_neighbors():
        if neighbor in checked_cells:
            continue
        if neighbor.value > cell.value and neighbor.value != 9:
            checked_cells.add(neighbor)
            size += get_basin_size(neighbor, checked_cells=checked_cells)
    return size


def part2():
    board = parse()
    basin_sizes = []
    checked_cells = set()
    for cell in board.cells_flat:
        if all(neighbor.value > cell.value for neighbor in cell.get_neighbors()):
            basin_sizes.append(get_basin_size(cell, checked_cells=checked_cells))
    return prod(sorted(basin_sizes)[-3:])


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
