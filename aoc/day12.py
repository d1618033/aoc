# pylint: disable=no-value-for-parameter
from dataclasses import dataclass
from math import cos, pi, sin

from fn.func import curried

from aoc.utils import iadd, isub, load_input


@dataclass
class Location:
    x: float
    y: float

    @curried
    def move(self, direction, amount):
        self.x, self.y = (
            self.x + amount * direction.x,
            self.y + amount * direction.y,
        )

    @property
    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)


@dataclass
class Direction:
    x: float
    y: float

    def tilt(self, angle):
        rad = angle / 360 * 2 * pi
        self.x, self.y = (
            cos(rad) * self.x - sin(rad) * self.y,
            sin(rad) * self.x + cos(rad) * self.y,
        )

    left = tilt

    def right(self, angle):
        return self.tilt(-angle)


def part1():
    ship = Location(0, 0)
    direction = Direction(1, 0)

    op_to_method = {
        "N": ship.move(Direction(0, 1)),
        "S": ship.move(Direction(0, -1)),
        "E": ship.move(Direction(1, 0)),
        "W": ship.move(Direction(-1, 0)),
        "L": direction.left,
        "R": direction.right,
        "F": ship.move(direction),
    }
    run_commands_on_input(op_to_method)
    return ship.manhattan_distance


def run_commands_on_input(op_to_method):
    for line in load_input():
        op = line[0]
        arg = int(line[1:])
        op_to_method[op](arg)


def part2():
    ship = Location(0, 0)
    waypoint = Direction(10, 1)

    op_to_method = {
        "N": iadd(waypoint, "y"),
        "S": isub(waypoint, "y"),
        "E": iadd(waypoint, "x"),
        "W": isub(waypoint, "x"),
        "L": waypoint.left,
        "R": waypoint.right,
        "F": ship.move(waypoint),
    }
    run_commands_on_input(op_to_method)
    return ship.manhattan_distance


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
