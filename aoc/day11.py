from collections import Counter
from dataclasses import dataclass
from typing import List

from aoc.utils import StringEnum, load_input


class TileEnum(StringEnum):
    empty = "L"
    taken = "#"
    floor = "."


@dataclass
class Tile:
    row: int
    col: int
    tile_type: TileEnum


class Board:
    def __init__(self, tiles: List[List[TileEnum]]):
        self._tiles = [
            [
                Tile(row=row, col=col, tile_type=tile)
                for col, tile in enumerate(tiles_in_row)
            ]
            for row, tiles_in_row in enumerate(tiles)
        ]

    @staticmethod
    def _get_directions():
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                yield i, j

    def get_tile_neighbors(self, tile: "Tile", include_floor=True):
        for i, j in self._get_directions():
            for count in range(1, len(self._tiles)):
                new_row = tile.row + count * i
                new_col = tile.col + count * j
                neighbor = self.get_tile(new_row, new_col)
                if not neighbor:
                    break
                if include_floor or neighbor.tile_type != TileEnum.floor:
                    yield neighbor
                    break

    def __iter__(self):
        for row in self._tiles:
            for col in row:
                yield col

    def __str__(self):
        return "\n".join(
            ["".join([tile.tile_type.value for tile in row]) for row in self._tiles]
        )

    def get_tile(self, row, col):
        if 0 <= row < len(self._tiles):
            tiles_in_row = self._tiles[row]
            if 0 <= col < len(tiles_in_row):
                return tiles_in_row[col]
        return None

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)


def parse_data():
    return Board([[TileEnum(tile.strip()) for tile in line] for line in load_input()])


def run_game_of_life_until_steady_state(board, **kwargs):
    while run_game_of_life_step(board, **kwargs):
        pass


def part1():
    board = parse_data()
    run_game_of_life_until_steady_state(board)
    return sum(tile.tile_type == TileEnum.taken for tile in board)


def run_game_of_life_step(board, include_floor=True, num_taken_threshold=4):
    changes = []
    for tile in board:
        if tile.tile_type == TileEnum.floor:
            continue
        counts = Counter(
            neighbor.tile_type
            for neighbor in board.get_tile_neighbors(tile, include_floor=include_floor)
        )
        if tile.tile_type == TileEnum.empty and counts[TileEnum.taken] == 0:
            changes.append((tile, TileEnum.taken))
        elif (
            tile.tile_type == TileEnum.taken
            and counts[TileEnum.taken] >= num_taken_threshold
        ):
            changes.append((tile, TileEnum.empty))
    for tile, new_tile_type in changes:
        tile.tile_type = new_tile_type
    return len(changes) > 0


def part2():
    board = parse_data()
    run_game_of_life_until_steady_state(
        board, include_floor=False, num_taken_threshold=5
    )
    return sum(tile.tile_type == TileEnum.taken for tile in board)


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
