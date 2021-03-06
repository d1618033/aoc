from aoc.utils import load_input


def handshake(subject):
    value = 1
    while True:
        value *= subject
        value %= 20201227
        yield value


def get_pool_size(public_key):
    for i, value in enumerate(handshake(7)):
        if value == public_key:
            return i + 1
    return None


def get_encryption(pub_1, pub_2):
    pool_2 = get_pool_size(pub_2)
    v = None
    for v, _ in zip(handshake(pub_1), range(pool_2)):
        pass
    return v


def part1():
    return get_encryption(*list(map(int, load_input())))


def part2():
    ...


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
