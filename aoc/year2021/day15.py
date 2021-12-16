import networkx
from networkx.algorithms.shortest_paths.generic import shortest_path

from aoc.utils import Board, load_board_of_ints


def get_shortest_path(board):
    g = networkx.DiGraph()
    for cell in board.cells_flat:
        for neighbor in cell.get_neighbors(diagonal=False):
            g.add_edge(cell, neighbor, weight=neighbor.value)
    path = shortest_path(
        g,
        source=board.get_cell(0, 0),
        target=board.get_cell(board.num_rows - 1, board.num_cols - 1),
        weight="weight",
        method="bellman-ford",
    )
    return sum(cell.value for cell in path[1:])

def part1():
    board = Board(load_board_of_ints())
    return get_shortest_path(board)


def loop_back(number):
    return (number - 1) % 9 + 1

def part2():
    board = load_board_of_ints()
    board_with_all_cols = []
    for row in board:
        new_row = [
            loop_back(cell + i)
            for i in range(5)
            for cell in row
        ]
        board_with_all_cols.append(new_row)
    new_board = [
        [
            loop_back(cell + i )
            for cell in row
        ]
        for i in range(5)
        for row in board_with_all_cols
    ]
    #  print("\n".join(["".join(str(cell) for cell in row) for row in new_board]))
    return get_shortest_path(Board(new_board))


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
