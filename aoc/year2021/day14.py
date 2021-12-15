import collections

import more_itertools

from aoc.utils import load_input


def step(template, rules):
    new_template = collections.defaultdict(int)
    for pair, count in template.items():
        if pair not in rules:
            new_template[pair] = count
            continue
        insert = rules[pair]
        new_template[f"{pair[0]}{insert}"] += count
        new_template[f"{insert}{pair[1]}"] += count
    return new_template


def get_counts_of_pairs(line):
    return collections.Counter(f"{a}{b}" for a, b in more_itertools.windowed(line, 2))


def parse():
    lines = load_input()
    template = lines[0]
    rules = dict(line.split(" -> ") for line in lines[1:])
    return template, rules


def get_counts_from_counts_of_pairs(template):
    counts = collections.defaultdict(int)
    for pair, count in template.items():
        counts[pair[0]] += count
    return counts


def step_slow(template, rules):
    new_template = []
    for (a, b) in more_itertools.windowed(template, 2):
        new_template.append(a)
        key = f"{a}{b}"
        if key in rules:
            new_template.append(rules[key])
    new_template.append(template[-1])
    return "".join(new_template)


def run_steps_and_get_counts(template, rules, num_steps):
    template = get_counts_of_pairs(template)
    for _ in range(num_steps):
        template = step(template, rules)
    counts = get_counts_from_counts_of_pairs(template)
    return counts


def run_steps_and_get_counts_slow(template, rules, num_steps):
    for _ in range(num_steps):
        template = step_slow(template, rules)
    counts = collections.Counter(template)
    return counts


def subtract_most_common_from_least(counts):
    common = sorted(counts.items(), key=lambda x: x[1])
    return common[-1][1] - common[0][1]


def part1():
    template, rules = parse()
    counts = run_steps_and_get_counts_slow(template, rules, 10)
    return subtract_most_common_from_least(counts)


def part2():
    template, rules = parse()
    counts_fast = run_steps_and_get_counts(template, rules, 40)
    counts_fast[template[-1]] += 1
    return subtract_most_common_from_least(counts_fast)


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
