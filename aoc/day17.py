import functools
import itertools
from typing import Tuple

from aoc.utils import load_input

Location = Tuple[int, ...]


class InfiniteGameOfLifeBoard:
    def __init__(self, dimensions=3):
        self._dimensions = dimensions
        self._active = set()

    def set_active(self, location: Location, value: bool):
        if value:
            self._active.add(location)
        else:
            self._active.discard(location)

    def is_active(self, location: Location):
        return location in self._active

    @functools.lru_cache
    def get_neighbors(self, location: Location):
        neighbors = []
        for diff in itertools.product([-1, 0, 1], repeat=self._dimensions):
            if all(d == 0 for d in diff):
                continue
            neighbors.append(
                tuple(coordinate + d for coordinate, d in zip(location, diff))
            )
        return neighbors

    def iter_locations(self):
        return (
            self._active
            | set(
                neighbor
                for location in self._active
                for neighbor in self.get_neighbors(location)
            )
        )

    def step(self):
        changes = []
        for location in self.iter_locations():
            num_active_neighbors = len(set(self.get_neighbors(location)) & self._active)
            if location in self._active:
                changes.append((location, num_active_neighbors in [2, 3]))
            else:
                changes.append((location, num_active_neighbors == 3))
        self._active = (
            self._active | {location for location, activate in changes if activate}
        ) - {location for location, activate in changes if not activate}

    @property
    def total_active(self):
        return len(self._active)

    @property
    def active(self):
        return self._active


def get_num_activate_after_steps(dimensions, num_steps):
    board = load_board(dimensions=dimensions)
    for _ in range(num_steps):
        board.step()
    return board.total_active


def part1():
    return get_num_activate_after_steps(dimensions=3, num_steps=6)


def load_board(dimensions=3):
    board = InfiniteGameOfLifeBoard(dimensions=dimensions)
    for x, line in enumerate(load_input()):
        for y, value in enumerate(line):
            board.set_active(
                (x, y) + tuple(0 for _ in range(dimensions - 2)), value == "#"
            )
    return board


def part2():
    return get_num_activate_after_steps(dimensions=4, num_steps=6)


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
