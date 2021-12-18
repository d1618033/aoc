import pytest

from aoc.year2021.day18 import Node, part1, part2


def test_node_from_list_of_lists():
    root = Node.from_list_of_lists([1, [2, [[3, 4], 5]]])
    assert root.left.value == 1
    assert root.right.left.value == 2
    assert root.right.right.left.left.value == 3
    assert root.right.right.left.right.value == 4
    assert root.right.right.right.value == 5


def test_to_list_of_lists():
    list_of_lists = [1, [2, [[3, 4], 5]]]
    root = Node.from_list_of_lists(list_of_lists)
    assert root.to_list_of_lists() == list_of_lists


def test_first_leaf_child():
    root = Node.from_list_of_lists([1, [2, [[3, 4], 5]]])
    assert root.first_leaf_child_to_right.value == 5
    assert root.first_leaf_child_to_left.value == 1


def test_first_relative():
    root = Node.from_list_of_lists([1, [2, [[3, 4], 5]]])
    assert root.first_relative_to_right is None
    assert root.left.first_relative_to_right is root.right
    assert root.right.first_relative_to_right is None
    assert root.right.left.first_relative_to_right is root.right.right


def test_first_leaf_relative():
    root = Node.from_list_of_lists([[6, [5, [4, [3, 2]]]], 1])
    assert root.left.right.right.right.first_leaf_relative_to_right.value == 1


@pytest.mark.parametrize(
    "input_,output",
    [
        (10, [5, 5]),
        (11, [5, 6]),
        ([10, 11], [[5, 5], 11]),
        ([4, [10, 11]], [4, [[5, 5], 11]]),
    ],
)
def test_split(input_, output):
    root = Node.from_list_of_lists(input_)
    root.split()
    assert root.to_list_of_lists() == output


@pytest.mark.parametrize(
    "input_,output",
    [
        ([[[[[9, 8], 1], 2], 3], 4], [[[[0, 9], 2], 3], 4]),
        ([7, [6, [5, [4, [3, 2]]]]], [7, [6, [5, [7, 0]]]]),
        ([[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3]),
        (
            [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]],
            [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
        ),
        (
            [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
            [[3, [2, [8, 0]]], [9, [5, [7, 0]]]],
        ),
    ],
)
def test_explode(input_, output):
    root = Node.from_list_of_lists(input_)
    root.explode()
    assert root.to_list_of_lists() == output


@pytest.mark.parametrize(
    "input_,output",
    [
        (
            [[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]],
            [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]],
        )
    ],
)
def test_reduce(input_, output):
    root = Node.from_list_of_lists(input_)
    root.reduce()
    assert root.to_list_of_lists() == output


@pytest.mark.parametrize(
    "node1,node2,output",
    [
        (
            [[[[4, 3], 4], 4], [7, [[8, 4], 9]]],
            [1, 1],
            [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]],
        )
    ],
)
def test_add(node1, node2, output):
    node1 = Node.from_list_of_lists(node1)
    node2 = Node.from_list_of_lists(node2)
    node3 = node1 + node2
    assert node3.to_list_of_lists() == output


def test_part1():
    assert part1() == 4140


def test_part2():
    assert part2() == 3993
