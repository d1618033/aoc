from aoc.year2021.day9 import Board, get_basin_size, parse, part1, part2


def test_part1():
    assert part1() == 15


def test_part2():
    assert part2() == 1134


def test_get_basin_size():
    board = Board([[2, 1, 4], [3, 9, 0], [0, 5, 1]])
    assert get_basin_size(board.get_cell(0, 0)) == 2
    assert get_basin_size(board.get_cell(0, 1)) == 4
    assert get_basin_size(board.get_cell(0, 2)) == 1
    assert get_basin_size(board.get_cell(1, 0)) == 1
    assert get_basin_size(board.get_cell(1, 1)) == 1
    assert get_basin_size(board.get_cell(1, 2)) == 4
    assert get_basin_size(board.get_cell(2, 0)) == 3
    assert get_basin_size(board.get_cell(2, 1)) == 1
    assert get_basin_size(board.get_cell(2, 2)) == 2


def test_get_basin_size_example():
    board = parse()
    assert get_basin_size(board.get_cell(0, 1)) == 3
    assert get_basin_size(board.get_cell(0, 9)) == 9
