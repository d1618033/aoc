from dataclasses import dataclass
from typing import List

from aoc.utils import load_input


@dataclass
class Tile:
    number: int
    marked: bool = False

    def __str__(self):
        if self.marked:
            return f"*{self.number}*"
        return str(self.number)


@dataclass
class Board:
    tiles: List[List[Tile]]

    def __str__(self):
        output = []
        for row in self.tiles:
            output.append(" ".join(str(tile) for tile in row))
        output.append("= " * 10)
        return "\n".join(output)

    def get_column(self, i):
        return [row[i] for row in self.tiles]

    def get_row(self, i):
        return self.tiles[i]

    @property
    def columns(self):
        for i in range(len(self.tiles[0])):
            yield self.get_column(i)

    @property
    def rows(self):
        for i in range(len(self.tiles)):
            yield self.get_row(i)

    @property
    def won(self):
        for row in self.rows:
            if all(tile.marked for tile in row):
                return True
        for col in self.columns:
            if all(tile.marked for tile in col):
                return True
        return False

    def mark(self, number):
        for row in self.rows:
            for tile in row:
                if tile.number == number:
                    tile.marked = True
                    break

    @property
    def tiles_flat(self):
        for row in self.rows:
            for tile in row:
                yield tile

    @property
    def sum_unmarked(self):
        return sum(tile.number for tile in self.tiles_flat if not tile.marked)


def get_parsed_data():
    data = load_input(skip_empty=False)
    numbers = list(map(int, data[0].split(",")))
    boards = []
    current = Board(tiles=[])
    boards.append(current)
    for line in data[2:-1]:
        if line.strip() == "":
            current = Board(tiles=[])
            boards.append(current)
        else:
            current.tiles.append(
                list(map(lambda x: Tile(number=int(x)), line.strip().split()))
            )
    return boards, numbers


def part1():
    boards, numbers = get_parsed_data()
    for number in numbers:
        for board in boards:
            board.mark(number)
            if board.won:
                return board.sum_unmarked * number
    raise RuntimeError("No board won")


def part2():
    boards, numbers = get_parsed_data()
    winning_boards = []
    for number in numbers:
        for board in boards:
            if board in winning_boards:
                continue
            board.mark(number)
            if board.won:
                winning_boards.append(board)
            if len(winning_boards) == len(boards):
                return board.sum_unmarked * number
    raise RuntimeError("No board won")


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
