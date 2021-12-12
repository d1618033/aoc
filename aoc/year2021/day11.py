from aoc.utils import get_neighbors, load_board_of_ints


def step(board):
    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            board[i][j] += 1
    flashes_to_do = set()
    for i, row in enumerate(board):
        for j, _ in enumerate(row):
            if board[i][j] > 9:
                flashes_to_do.add((i, j))
    flashed = set()
    while flashes_to_do:
        (i, j) = flashes_to_do.pop()
        flashed.add((i, j))
        for (ni, nj) in get_neighbors(i, j, len(board), len(row), diagonal=True):
            board[ni][nj] += 1
            if board[ni][nj] > 9 and (ni, nj) not in flashed:
                flashes_to_do.add((ni, nj))
    for (i, j) in flashed:
        board[i][j] = 0
    return flashed


def part1():
    board = load_board_of_ints()
    total_flashed = 0
    for _ in range(100):
        flashed = step(board)
        total_flashed += len(flashed)
    return total_flashed


def part2():
    board = load_board_of_ints()
    for i in range(1000):
        flashed = step(board)
        if len(flashed) == len(board) * len(board[0]):
            return i + 1
    raise AssertionError("shouldn't reach here")


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
