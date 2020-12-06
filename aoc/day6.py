import re
from collections import defaultdict

from aoc.utils import load_input


def part1():
    count = 0
    for group in load_input(delim="\n\n"):
        group_answers = set()
        for person in group.split("\n"):
            answers = re.findall(r"\w", person)
            group_answers.update(answers)
        count += len(group_answers)
    return count


def part2():
    count = 0
    for group in load_input(delim="\n\n"):
        group_answers = defaultdict(int)
        people = group.split("\n")
        for person in people:
            assert len(person) > 0
            for answer in set(person.strip()):
                group_answers[answer] += 1
        same_answers = [
            answer
            for answer, answer_count in group_answers.items()
            if answer_count == len(people)
        ]
        num_same = len(same_answers)
        count += num_same
    return count


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
