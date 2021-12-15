from math import prod

from aoc.utils import Board, load_board_of_ints


def parse():
    return Board(load_board_of_ints())


def part1():
    board = parse()
    sum_risk = 0
    for cell in board.cells_flat:
        if all(
            neighbor.value > cell.value
            for neighbor in cell.get_neighbors(diagonal=False)
        ):
            sum_risk += cell.value + 1
    return sum_risk


def get_basin_size(cell, checked_cells=None):
    if checked_cells is None:
        checked_cells = set()
    size = 1
    for neighbor in cell.get_neighbors(diagonal=False):
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
        if all(
            neighbor.value > cell.value
            for neighbor in cell.get_neighbors(diagonal=False)
        ):
            basin_sizes.append(get_basin_size(cell, checked_cells=checked_cells))
    return prod(sorted(basin_sizes)[-3:])


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
