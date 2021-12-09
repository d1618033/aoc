import itertools

from aoc.utils import load_input


def part1():
    count = 0
    for line in load_input():
        numbers = line.strip().split("|")[1].strip()
        for number in numbers.split():
            if len(number) in [2, 3, 4, 7]:
                count += 1
    return count


configs = [
    {"A", "B", "C", "E", "F", "G"},
    {"C", "F"},
    {"A", "C", "D", "E", "G"},
    {"A", "C", "D", "F", "G"},
    {"B", "C", "D", "F"},
    {"A", "B", "D", "F", "G"},
    {"A", "B", "D", "E", "F", "G"},
    {"A", "C", "F"},
    {"A", "B", "C", "D", "E", "F", "G"},
    {"A", "B", "C", "D", "F", "G"},
]


def is_mapping_valid(patterns, letter_mapping):
    numbers = []
    for pattern in patterns:
        mapped = {letter_mapping[letter] for letter in pattern}
        possible = [number for number, config in enumerate(configs) if config == mapped]
        if len(possible) != 1:
            return False
        numbers.append(possible[0])
    if sorted(numbers) != list(range(10)):
        return False
    return True


def detect_mapping(patterns):
    for permutation in itertools.permutations("abcdefg"):
        mapping = dict(zip(permutation, "ABCDEFG"))
        if numbers := is_mapping_valid(patterns, mapping):
            return mapping


def part2():
    sum_ = 0
    for line in load_input():
        patterns, digits = line.strip().split("|")
        patterns = patterns.strip().split()
        digits = digits.strip().split()
        mapping = detect_mapping(patterns)
        numbers = []
        for digit in digits:
            mapped = {mapping[char] for char in digit}
            [number] = [
                number for number, config in enumerate(configs) if config == mapped
            ]
            numbers.append(str(number))
        number = int("".join(numbers))
        sum_ += number
    return sum_


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
