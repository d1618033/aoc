from aoc.year2020.day17 import load_board, part1, part2


def test_part1():
    assert part1() == 112


def test_neighbors():
    board = load_board()
    assert board.is_active((0, 1, 0))
    neighbors = list(board.get_neighbors((0, 1, 0)))
    assert (1, 2, 0) in neighbors
    assert board.is_active((1, 2, 0))
    assert sum(map(board.is_active, neighbors)) == 1


def test_part2():
    assert part2() == 848
