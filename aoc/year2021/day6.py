import collections

from aoc.utils import load_input


def part1():
    return get_num_fishes(80)


class Fishes:
    def __init__(self, numbers):
        self.fishes = collections.Counter(numbers)

    def next(self):
        new_fishes = collections.defaultdict(int)
        for number, count in self.fishes.items():
            if number == 0:
                new_fishes[8] += count
                new_fishes[6] += count
            else:
                new_fishes[number - 1] += count
        self.fishes = new_fishes
        return self

    def __len__(self):
        return sum(self.fishes.values())

    @property
    def all_numbers(self):
        output = []
        for number, count in self.fishes.items():
            output.extend([number] * count)
        return output

    def __str__(self):
        return ",".join(map(str, self.all_numbers))

    def __repr__(self):
        return f"Fishes({self})"


def parse_data():
    return list(map(int, load_input()[0].split(",")))


def get_num_fishes(days):
    fishes = Fishes(parse_data())
    for _day in range(days):
        fishes.next()
    return len(fishes)


def part2():
    return get_num_fishes(256)


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
