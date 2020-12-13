from dataclasses import dataclass
from math import cos, pi, sin

from aoc.utils import load_input


@dataclass
class Location:
    x: float
    y: float

    def move(self, direction: "Direction", amount: float):
        self.x, self.y = (
            self.x + amount * direction.x,
            self.y + amount * direction.y,
        )


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

    def increase(self, x=0, y=0):
        self.x, self.y = (
            self.x + x,
            self.y + y,
        )


def part1():
    ship = Location(0, 0)
    direction = Direction(1, 0)

    op_to_method = {
        "N": lambda arg: ship.move(Direction(0, 1), arg),
        "S": lambda arg: ship.move(Direction(0, -1), arg),
        "E": lambda arg: ship.move(Direction(1, 0), arg),
        "W": lambda arg: ship.move(Direction(-1, 0), arg),
        "L": direction.tilt,
        "R": lambda angle: direction.tilt(-angle),
        "F": lambda arg: ship.move(direction, arg),
    }
    for line in load_input():
        op = line[0]
        arg = int(line[1:])
        op_to_method[op](arg)
    return sum(map(abs, [ship.x, ship.y]))


def part2():
    ship = Location(0, 0)
    waypoint = Direction(10, 1)

    op_to_method = {
        "N": lambda arg: waypoint.increase(y=arg),
        "S": lambda arg: waypoint.increase(y=-arg),
        "E": lambda arg: waypoint.increase(x=arg),
        "W": lambda arg: waypoint.increase(x=-arg),
        "L": waypoint.tilt,
        "R": lambda angle: waypoint.tilt(-angle),
        "F": lambda arg: ship.move(waypoint, arg),
    }
    for line in load_input():
        op = line[0]
        arg = int(line[1:])
        op_to_method[op](arg)
    return sum(map(abs, [ship.x, ship.y]))


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
