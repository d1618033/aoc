from functools import partial
from math import cos, pi, sin
from turtle import Turtle

from aoc.utils import load_input


def part1():
    turtle = Turtle()

    def move_in_direction(angle, amount):
        heading = turtle.heading()
        turtle.setheading(angle)
        turtle.forward(amount)
        turtle.setheading(heading)

    op_to_method = {
        "N": partial(move_in_direction, 90),
        "S": partial(move_in_direction, 270),
        "E": partial(move_in_direction, 0),
        "W": partial(move_in_direction, 180),
        "L": turtle.left,
        "R": turtle.right,
        "F": turtle.forward,
    }
    turtle.speed(0)
    turtle.setheading(0)
    for line in load_input():
        op = line[0]
        arg = int(line[1:])
        op_to_method[op](arg)
        print(turtle.pos())
    return sum(map(abs, turtle.pos()))


def part2():
    turtle = Turtle()
    waypoint = Turtle()
    turtle.getscreen().tracer(10000)
    waypoint.getscreen().tracer(10000)

    def move_in_direction_of_waypoint(amount):
        pos = turtle.pos()
        waypoint_pos = waypoint.pos()
        new_pos = (pos[0] + waypoint_pos[0] * amount, pos[1] + waypoint_pos[1] * amount)
        turtle.setpos(new_pos)

    def move_waypoint_in_direction(angle, amount):
        heading = waypoint.heading()
        waypoint.setheading(angle)
        waypoint.forward(amount)
        waypoint.setheading(heading)

    def tilt_waypoint(angle):
        rad = angle / 360 * 2 * pi
        print(angle, rad, sin(rad), cos(rad), waypoint.pos())
        waypoint.setpos(
            (
                cos(rad) * waypoint.xcor() - sin(rad) * waypoint.ycor(),
                sin(rad) * waypoint.xcor() + cos(rad) * waypoint.ycor(),
            )
        )

    op_to_method = {
        "N": partial(move_waypoint_in_direction, 90),
        "S": partial(move_waypoint_in_direction, 270),
        "E": partial(move_waypoint_in_direction, 0),
        "W": partial(move_waypoint_in_direction, 180),
        "L": tilt_waypoint,
        "R": lambda angle: tilt_waypoint(-angle),
        "F": move_in_direction_of_waypoint,
    }
    turtle.speed(0)
    turtle.setheading(0)
    waypoint.setheading(waypoint.towards((10, 1)))
    waypoint.setpos((10, 1))
    for line in load_input():
        op = line[0]
        arg = int(line[1:])
        op_to_method[op](arg)
        print(line, turtle.pos(), waypoint.pos())
    return sum(map(abs, turtle.pos()))


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
