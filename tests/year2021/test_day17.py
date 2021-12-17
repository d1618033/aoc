import pytest

from aoc.year2021.day17 import (
    Point,
    Probe,
    Target,
    Velocity,
    part1,
    part2,
    step_until_in_or_over_target,
)


def test_part1():
    assert part1() == 45


def test_part2():
    assert part2() == 112


def test_point():
    point = Point(x=3, y=5)
    velocity = Velocity(x=5, y=6)
    point.increase_by_velocity(velocity)
    assert point.x == 8
    assert point.y == 11
    assert point.higher_than(Point(x=8, y=10))


def test_velocity():
    velocity = Velocity(x=1, y=6)
    velocity.drag_and_gravity()
    assert velocity.x == 0
    assert velocity.y == 5
    velocity = Velocity(x=-2, y=4)
    velocity.drag_and_gravity()
    assert velocity.x == -1
    assert velocity.y == 3
    velocity = Velocity(x=0, y=4)
    velocity.drag_and_gravity()
    assert velocity.x == 0
    assert velocity.y == 3


def test_step_until_in_or_over_target():
    position = Point(x=0, y=0)
    velocity = Velocity(x=6, y=9)
    probe = Probe(position=position, velocity=velocity)
    target = Target.from_str("target area: x=20..30, y=-10..-5")
    result = step_until_in_or_over_target(probe, target)
    assert result.success
    assert result.highest_position == 45


@pytest.mark.parametrize(
    "x,y",
    [
        (10, -1),
        (10, -2),
        (11, -1),
        (11, -2),
        (11, -3),
        (11, -4),
        (12, -2),
        (12, -3),
        (12, -4),
        (13, -2),
        (13, -3),
        (13, -4),
        (14, -2),
        (14, -3),
        (14, -4),
        (15, -2),
        (15, -3),
        (15, -4),
        (20, -10),
        (20, -5),
        (20, -6),
        (20, -7),
        (20, -8),
        (20, -9),
        (21, -10),
        (21, -5),
        (21, -6),
        (21, -7),
        (21, -8),
        (21, -9),
        (22, -10),
        (22, -5),
        (22, -6),
        (22, -7),
        (22, -8),
        (22, -9),
        (23, -10),
        (23, -5),
        (23, -6),
        (23, -7),
        (23, -8),
        (23, -9),
        (24, -10),
        (24, -5),
        (24, -6),
        (24, -7),
        (24, -8),
        (24, -9),
        (25, -10),
        (25, -5),
        (25, -6),
        (25, -7),
        (25, -8),
        (25, -9),
        (26, -10),
        (26, -5),
        (26, -6),
        (26, -7),
        (26, -8),
        (26, -9),
        (27, -10),
        (27, -5),
        (27, -6),
        (27, -7),
        (27, -8),
        (27, -9),
        (28, -10),
        (28, -5),
        (28, -6),
        (28, -7),
        (28, -8),
        (28, -9),
        (29, -10),
        (29, -5),
        (29, -6),
        (29, -7),
        (29, -8),
        (29, -9),
        (30, -10),
        (30, -5),
        (30, -6),
        (30, -7),
        (30, -8),
        (30, -9),
        (6, 0),
        (6, 1),
        (6, 2),
        (6, 3),
        (6, 4),
        (6, 5),
        (6, 6),
        (6, 7),
        (6, 8),
        (6, 9),
        (7, -1),
        (7, 0),
        (7, 1),
        (7, 2),
        (7, 3),
        (7, 4),
        (7, 5),
        (7, 6),
        (7, 7),
        (7, 8),
        (7, 9),
        (8, -1),
        (8, -2),
        (8, 0),
        (8, 1),
        (9, -1),
        (9, -2),
        (9, 0),
    ],
)
def test_step_until_in_or_over_target_success(x, y):
    position = Point(x=0, y=0)
    velocity = Velocity(x=x, y=y)
    probe = Probe(position=position, velocity=velocity)
    target = Target.from_str("target area: x=20..30, y=-10..-5")
    result = step_until_in_or_over_target(probe, target)
    assert result.success
