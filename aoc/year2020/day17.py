import functools
import itertools
import operator
from typing import Tuple

from aoc.utils import load_input

Location = Tuple[int, ...]


class InfiniteGameOfLifeBoard:
    def __init__(self, dimensions=3):
        self._dimensions = dimensions
        self._active = set()
        self._num_neighbors_to_activate = {False: [3], True: [2, 3]}

    def set_active(self, location: Location, value: bool):
        if value:
            self._active.add(location)
        else:
            self._active.discard(location)

    def is_active(self, location: Location):
        return location in self._active

    @functools.lru_cache
    def get_neighbors(self, location: Location):
        neighbors = set()
        for diff in itertools.product([-1, 0, 1], repeat=self._dimensions):
            if all(d == 0 for d in diff):
                continue
            neighbors.add(tuple(map(operator.add, location, diff)))
        return neighbors

    def iter_locations(self):
        return self._active | set(
            neighbor
            for location in self._active
            for neighbor in self.get_neighbors(location)
        )

    def num_active_neighbors(self, location):
        return len(self.get_neighbors(location) & self._active)

    def activate(self, location):
        return (
            self.num_active_neighbors(location)
            in self._num_neighbors_to_activate[location in self._active]
        )

    def step(self):
        self._active = {
            location for location in self.iter_locations() if self.activate(location)
        }

    @property
    def total_active(self):
        return len(self._active)

    @property
    def active(self):
        return self._active


def get_num_active_after_steps(dimensions, num_steps):
    board = load_board(dimensions=dimensions)
    for _ in range(num_steps):
        board.step()
    return board.total_active


def part1():
    return get_num_active_after_steps(dimensions=3, num_steps=6)


def load_board(dimensions=3):
    board = InfiniteGameOfLifeBoard(dimensions=dimensions)
    for x, line in enumerate(load_input()):
        for y, value in enumerate(line):
            board.set_active(
                (x, y) + tuple(0 for _ in range(dimensions - 2)), value == "#"
            )
    return board


def part2():
    return get_num_active_after_steps(dimensions=4, num_steps=6)


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
