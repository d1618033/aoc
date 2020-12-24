from dataclasses import dataclass

from aoc.utils import load_input


@dataclass
class Cup:
    __slots__ = ["value", "next"]

    value: int
    next: "Cup"

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Cup({self.value}, next={self.next.value})"


class Circle:
    def __init__(self, cup_values):
        self._value_to_cup = {}
        self.head = Cup(cup_values[0], next=None)
        self._value_to_cup[self.head.value] = self.head
        self.tail = self.head
        for cup_value in cup_values[1:]:
            self.tail.next = Cup(value=cup_value, next=self.head)
            self.tail = self.tail.next
            self._value_to_cup[self.tail.value] = self.tail

    def iter_from(self, cup: Cup):
        current = cup
        while True:
            yield current
            current = current.next
            if current == cup:
                return

    def __iter__(self):
        return self.iter_from(self.head)

    def __contains__(self, item):
        for cup in self:
            if cup.value == item:
                return True
        return False

    def get(self, value):
        return self._value_to_cup[value]


def play(data, num_moves=10, verbose=False):
    cups = Circle(data)
    max_data = max(data)
    for move in range(num_moves):
        current_cup = cups.head
        if verbose:
            print(f"-- move {move + 1} --")
            print(
                f"cups: ",
                " ".join(
                    [str(cup) if cup != current_cup else f"({cup})" for cup in cups]
                ),
            )
        picked_up = []
        current_picked_up = current_cup
        for _ in range(3):
            current_picked_up = current_picked_up.next
            current_cup.next = current_picked_up.next
            picked_up.append(current_picked_up)
        if verbose:
            print(f"picked up:", ",".join(map(str, picked_up)))
            print(f"remaining: ", ",".join(map(str, cups.iter_from(current_cup.next))))
        destination_cup_value = current_cup.value - 1
        if destination_cup_value <= 0:
            destination_cup_value = max_data
        picked_up_values = {p.value for p in picked_up}
        while destination_cup_value in picked_up_values:
            destination_cup_value -= 1
            if destination_cup_value <= 0:
                destination_cup_value = max_data
        if verbose:
            print(f"destination: {destination_cup_value}")
        destination_cup = cups.get(destination_cup_value)
        destination_cup_next = destination_cup.next
        destination_cup.next = picked_up[0]
        picked_up[-1].next = destination_cup_next
        cups.head = current_cup.next
        if verbose:
            print()
    return cups


def part1():
    data = list(map(int, load_input()[0]))
    cups = play(num_moves=100, data=data, verbose=True)
    return "".join(list(map(str, cups.iter_from(cups.get(1))))[1:])


def part2():
    data = list(map(int, load_input()[0]))
    data.extend([num for num in range(max(data) + 1, 10 ** 6 + 1)])
    cups = play(num_moves=10 ** 7, data=data)
    cup_1 = cups.get(1)
    return cup_1.next.value * cup_1.next.next.value


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
