from aoc.utils import Board, load_board_of_ints


def step(board: Board):
    for cell in board.cells_flat:
        cell.value += 1
    flashes_to_do = set()
    for cell in board.cells_flat:
        if cell.value > 9:
            flashes_to_do.add(cell)
    flashed = set()
    while flashes_to_do:
        cell = flashes_to_do.pop()
        flashed.add(cell)
        for neighbor in cell.get_neighbors(diagonal=True):
            neighbor.value += 1
            if neighbor.value > 9 and neighbor not in flashed:
                flashes_to_do.add(neighbor)
    for neighbor in flashed:
        neighbor.value = 0
    return flashed


def part1():
    board = Board(load_board_of_ints())
    total_flashed = 0
    for _ in range(100):
        flashed = step(board)
        total_flashed += len(flashed)
    return total_flashed


def part2():
    board = Board(load_board_of_ints())
    for i in range(1000):
        flashed = step(board)
        if len(flashed) == board.num_cells:
            return i + 1
    raise AssertionError("shouldn't reach here")


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
