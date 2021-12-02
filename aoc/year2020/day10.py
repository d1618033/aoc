import functools
from collections import Counter

from aoc.utils import load_ints


def diff(data):
    return [next_ - current for current, next_ in zip(data, data[1:])]


def part1():
    adapters = get_adapters()
    counts = Counter(diff(adapters))
    return counts[1] * counts[3]


def get_adapters():
    adapters = sorted(load_ints())
    adapters += [adapters[-1] + 3]
    adapters = [0] + adapters
    return adapters


@functools.lru_cache()
def get_arrangements(adapters):
    if not adapters:
        return 1
    count = 0
    for i, adapter in enumerate(adapters):
        if 0 <= adapter <= 3:
            count += get_arrangements(
                tuple(adapter_ - adapter for adapter_ in adapters[i + 1 :])
            )
        else:
            break
    return count


def part2():
    adapters = get_adapters()
    return get_arrangements(tuple(adapters[1:]))


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
