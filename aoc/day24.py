import re
from functools import lru_cache, reduce

from aoc.utils import load_input


def load_data(lines=None):
    if lines is None:
        lines = load_input()
    directions = []
    for line in lines:
        directions.append(re.findall("(?:se)|(?:sw)|(?:ne)|(?:nw)|e|w", line))
    return directions


direction_map = {
    "e": (1, -1, 0),
    "w": (-1, 1, 0),
    "nw": (0, 1, -1),
    "sw": (-1, 0, 1),
    "ne": (1, 0, -1),
    "se": (0, -1, 1),
}


def part1():
    return sum(build_tiles().values())


def add(x, y):
    return tuple(x_i + y_i for x_i, y_i in zip(x, y))


def build_tiles():
    initial = (0, 0, 0)
    black = {}

    for directions in load_data():
        current = initial
        for direction in directions:
            current = add(current, direction_map[direction])
        black[current] = not black.get(current, False)
    return black


class GameofLife:
    def __init__(self):
        self.tiles = set([tile for tile, is_black in build_tiles().items() if is_black])

    @lru_cache
    def get_adjacent(self, tile):
        return {add(tile, direction) for direction in direction_map.values()}

    def get_all(self):
        return set([tile for tile in self.tiles]) | reduce(
            set.union, (set(self.get_adjacent(tile)) for tile in self.tiles), set()
        )

    def evolve(self):
        self.tiles = {
            tile
            for tile in self.get_all()
            if sum([adj_tile in self.tiles for adj_tile in self.get_adjacent(tile)])
            in ([1, 2] if (tile in self.tiles) else [2])
        }


def part2():
    gol = GameofLife()
    for i in range(100):
        gol.evolve()
    return len(gol.tiles)


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
