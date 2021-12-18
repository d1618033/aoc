import ast
import copy
import math
from dataclasses import dataclass, field
from typing import Optional

from aoc.utils import load_input


@dataclass
class Node:
    left: Optional["Node"]
    right: Optional["Node"]
    parent: Optional["Node"] = field(repr=False)
    value: Optional[int]

    @property
    def is_root(self):
        return self.parent is None

    @property
    def is_leaf(self):
        return self.left is None and self.right is None

    @property
    def depth(self):
        if self.is_root:
            return 0
        return self.parent.depth + 1

    @classmethod
    def from_list_of_lists(cls, data, parent=None):
        node = cls(left=None, right=None, value=None, parent=parent)
        if isinstance(data, int):
            node.value = data
            return node
        assert len(data) == 2
        node.left = cls.from_list_of_lists(data[0], parent=node)
        node.right = cls.from_list_of_lists(data[1], parent=node)
        return node

    def to_list_of_lists(self):
        if self.is_leaf:
            return self.value
        return [self.left.to_list_of_lists(), self.right.to_list_of_lists()]

    @property
    def first_leaf_child_to_left(self):
        if self.is_leaf:
            return self
        return self.left.first_leaf_child_to_left

    @property
    def first_leaf_child_to_right(self):
        if self.is_leaf:
            return self
        return self.right.first_leaf_child_to_right

    @property
    def first_relative_to_right(self):
        if self.is_root:
            return None
        if self.parent.left is self:
            return self.parent.right
        if self.parent.right is self:
            return self.parent.first_relative_to_right
        return None

    @property
    def first_relative_to_left(self):
        if self.is_root:
            return None
        if self.parent.right is self:
            return self.parent.left
        if self.parent.left is self:
            return self.parent.first_relative_to_left
        return None

    @property
    def first_leaf_relative_to_left(self):
        relative = self.first_relative_to_left
        if relative:
            return relative.first_leaf_child_to_right
        return None

    @property
    def first_leaf_relative_to_right(self):
        relative = self.first_relative_to_right
        if relative:
            return relative.first_leaf_child_to_left
        return None

    def explode(self):
        depth = self.depth
        if (
            depth == 4
            and self.left
            and self.left.is_leaf
            and self.right
            and self.right.is_leaf
        ):
            if (relative := self.first_leaf_relative_to_left) is not None:
                relative.value += self.left.value
            if (relative := self.first_leaf_relative_to_right) is not None:
                relative.value += self.right.value
            self.left = None
            self.right = None
            self.value = 0
            return True
        if depth < 4:
            if self.left is not None:
                if self.left.explode():
                    return True
            if self.right is not None:
                if self.right.explode():
                    return True
            return False
        return False

    def split(self):
        if self.is_leaf and self.value > 9:
            down = math.floor(self.value / 2)
            up = math.ceil(self.value / 2)
            self.left = Node(left=None, right=None, parent=self, value=down)
            self.right = Node(left=None, right=None, parent=self, value=up)
            self.value = None
            return True
        if self.left is not None:
            if self.left.split():
                return True
        if self.right is not None:
            if self.right.split():
                return True
        return False

    def reduce(self):
        for _ in range(1000):
            change = False
            change = change or self.explode()
            change = change or self.split()
            if not change:
                break
        else:
            raise RuntimeError("Ran too many reduces")

    def __add__(self, other):
        assert self.is_root
        assert other.is_root
        left = copy.deepcopy(self)
        right = copy.deepcopy(other)
        node = Node(left=left, right=right, parent=None, value=None)
        left.parent = node
        right.parent = node
        node.reduce()
        return node

    @property
    def magnitude(self):
        if self.is_leaf:
            return self.value
        return 3 * self.left.magnitude + 2 * self.right.magnitude


def part1():
    nodes = [Node.from_list_of_lists(ast.literal_eval(line)) for line in load_input()]
    current = nodes[0]
    for node in nodes[1:]:
        current = current + node
    return current.magnitude


def part2():
    nodes = [Node.from_list_of_lists(ast.literal_eval(line)) for line in load_input()]
    max_magnitude = 0
    for node1 in nodes:
        for node2 in nodes:
            if node1 is node2:
                continue
            magnitude = (node1 + node2).magnitude
            if magnitude > max_magnitude:
                max_magnitude = magnitude
    return max_magnitude


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
