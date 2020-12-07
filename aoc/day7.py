import re
from dataclasses import dataclass
from typing import Dict, List

import networkx
from networkx import ancestors

from aoc.utils import load_input, unwrap


@dataclass
class BagContained:
    amount: int
    bag: "Bag"


class Bag:
    def __new__(cls, color):
        if color in cls._bags:
            return cls._bags[color]
        obj = object.__new__(cls)
        cls._bags[color] = obj
        return obj

    def __init__(self, color: str):
        self.color = color
        self.contains: List[BagContained] = []

    def add_contained(self, bag_contained: BagContained):
        self.contains.append(bag_contained)

    @classmethod
    def get_all(cls):
        return sorted(cls._bags.values(), key=lambda x: x.color)

    _bags: Dict[str, "Bag"] = {}


def parse_input():
    for line in load_input():
        if not line:
            continue
        main_bag, contains = line.split("contain")
        main_bag_color = main_bag.replace("bags", "").strip()
        main_bag_color = Bag(main_bag_color)
        for bag in contains.replace(".", "").split(","):
            bag = re.sub("bags?", "", bag).strip()
            if bag == "no other":
                continue
            bag = unwrap(
                re.match(r"(?P<amount>\d+)\s+(?P<color>[a-zA-Z ]+)", bag), item=bag
            ).groupdict()
            main_bag_color.add_contained(
                BagContained(amount=int(bag["amount"]), bag=Bag(bag["color"]))
            )
    return Bag.get_all()


def create_network(bags: List[Bag]):
    graph = networkx.DiGraph()
    for bag in bags:
        graph.add_node(bag.color)
    for bag in bags:
        for contained in bag.contains:
            graph.add_edge(bag.color, contained.bag.color, amount=contained.amount)
    return graph


def part1():
    graph = create_network(parse_input())
    return len(ancestors(graph, "shiny gold"))


def total_bags(graph, node):
    total = 0
    for successor in graph.successors(node):
        weight = graph.get_edge_data(node, successor)["amount"]
        total += (1 + total_bags(graph, successor)) * weight
    return total


def part2():
    graph = create_network(parse_input())
    return total_bags(graph, "shiny gold")


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
