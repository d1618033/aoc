import collections
from dataclasses import dataclass

from aoc.utils import load_input, sign


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    @classmethod
    def from_str(cls, string):
        x, y = string.split(",")
        return cls(x=int(x), y=int(y))

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(frozen=True)
class Line:
    from_: Point
    to: Point

    @classmethod
    def from_str(cls, string):
        p1, p2 = string.split(" -> ")
        return cls(from_=Point.from_str(p1), to=Point.from_str(p2))

    @property
    def is_straight(self):
        return self.from_.x == self.to.x or self.from_.y == self.to.y

    @property
    def all_points(self):
        dx = sign(self.to.x - self.from_.x)
        dy = sign(self.to.y - self.from_.y)
        current = self.from_
        while current != self.to:
            yield current
            current = Point(x=current.x + dx, y=current.y + dy)
        yield self.to


def _print_board(board):
    max_x = max([point.x for point in board])
    max_y = max([point.y for point in board])
    to_print = []
    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            p = Point(x=x, y=y)
            count = board[p]
            if count == 0:
                row.append(".")
            else:
                row.append(str(count))
        to_print.append(row)
    print("\n")
    print("\n".join("\t".join(c for c in row) for row in to_print))


def part1():
    lines = [Line.from_str(line) for line in load_input()]
    board = collections.defaultdict(int)
    for line in lines:
        if not line.is_straight:
            continue
        for point in line.all_points:
            board[point] += 1

    return len([p for p, count in board.items() if count > 1])


def part2():
    lines = [Line.from_str(line) for line in load_input()]
    board = collections.defaultdict(int)
    for line in lines:
        for point in line.all_points:
            board[point] += 1

    return len([p for p, count in board.items() if count > 1])


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
