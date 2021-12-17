from dataclasses import dataclass

from aoc.utils import load_input


@dataclass
class Point:
    x: int
    y: int

    def increase_by_velocity(self, velocity: "Velocity"):
        self.x += velocity.x
        self.y += velocity.y

    def higher_than(self, other):
        return self.y > other.y


@dataclass
class Velocity:
    x: int
    y: int

    def drag_and_gravity(self):
        if self.x > 0:
            self.x -= 1
        elif self.x < 0:
            self.x += 1
        self.y -= 1


@dataclass
class Range:
    from_: int
    to: int

    def contains(self, x: int):
        return self.from_ <= x <= self.to

    @classmethod
    def from_str(cls, string):
        from_, to = map(int, string.strip().split(".."))
        return cls(from_=from_, to=to)


@dataclass
class Target:
    x_range: Range
    y_range: Range

    def contains(self, point: Point):
        return self.x_range.contains(point.x) and self.y_range.contains(point.y)

    def over(self, point: Point):
        return self.x_range.to < point.x or self.y_range.from_ > point.y

    @classmethod
    def from_str(cls, string):
        x_range, y_range = map(
            lambda x: Range.from_str(x.split("=")[1].strip()),
            string.removeprefix("target area:").strip().split(","),
        )
        return cls(x_range=x_range, y_range=y_range)


@dataclass
class Probe:
    position: Point
    velocity: Velocity

    def step(self):
        self.position.increase_by_velocity(self.velocity)
        self.velocity.drag_and_gravity()


@dataclass
class ExperimentResult:
    success: bool
    highest_position: int


def step_until_in_or_over_target(probe: Probe, target: Target):
    highest_position = probe.position.y
    for _ in range(1000):
        probe.step()
        if probe.position.y >= highest_position:
            highest_position = probe.position.y
        if target.contains(probe.position) or target.over(probe.position):
            break
    else:
        raise RuntimeError(f"Failed to get to target or over target {probe}")
    return ExperimentResult(
        success=target.contains(probe.position), highest_position=highest_position
    )


def part1():
    target = Target.from_str(load_input()[0])
    highest_position = 0
    xs_to_check = []
    for x in range(0, target.x_range.to):
        if target.x_range.from_ <= x * (x + 1) / 2 <= target.x_range.to:
            xs_to_check.append(x)

    for x in xs_to_check:
        for y in range(200, -1, -1):
            velocity = Velocity(x=x, y=y)
            initial_position = Point(x=0, y=0)
            probe = Probe(position=initial_position, velocity=velocity)
            result = step_until_in_or_over_target(probe, target)
            if result.success:
                if result.highest_position > highest_position:
                    highest_position = result.highest_position
                break
    return highest_position


def part2():
    target = Target.from_str(load_input()[0])
    num_positions = 0

    probe = Probe(position=Point(x=0, y=0), velocity=Velocity(x=0, y=0))
    for x in range(target.x_range.to + 1):
        for y in range(target.y_range.from_, 300):
            probe.velocity.x = x
            probe.velocity.y = y
            probe.position.x = 0
            probe.position.y = 0
            result = step_until_in_or_over_target(probe, target)
            if result.success:
                num_positions += 1
    return num_positions


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
