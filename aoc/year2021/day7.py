import numpy
import scipy.optimize

from aoc.utils import load_input


def parse():
    return numpy.array(list(map(int, load_input()[0].split(","))))


def part1():
    numbers = parse()
    return numpy.sum(numpy.abs(numbers - numpy.median(numbers)))


def part2():
    x = parse()

    def func(m):
        diffs = (numpy.abs(x - m) * (numpy.abs(x - m) + 1)) / 2
        return numpy.sum(diffs)

    result = scipy.optimize.minimize(func, (1 + 2 * numpy.mean(x)) / (2 * len(x)))
    m = numpy.round(result.x)
    return func(m)


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
