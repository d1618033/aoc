import collections

import networkx

from aoc.utils import load_input


def get_num_paths(graph, starting_node, end_node, visited):
    if starting_node == end_node:
        return 1
    num_paths = 0
    for child in graph.neighbors(starting_node):
        if child in visited:
            continue
        if child == child.lower():
            visited.add(child)
        num_paths += get_num_paths(graph, child, end_node, visited)
        if child in visited:
            visited.remove(child)
    return num_paths


def parse():
    graph = networkx.Graph()
    for line in load_input():
        graph.add_edge(*line.split("-"))
    return graph


def part1():
    graph = parse()
    return get_num_paths(graph, "start", "end", {"start"})


def get_num_paths_part2(graph, starting_node, end_node, visited):
    if starting_node == end_node:
        return 1
    num_paths = 0
    for child in graph.neighbors(starting_node):
        if child == "start":
            continue
        if any(count > 1 for count in visited.values()):
            if visited[child] >= 1:
                continue
        else:
            if visited[child] >= 2:
                continue
        if child == child.lower():
            visited[child] += 1
        num_paths += get_num_paths_part2(graph, child, end_node, visited)
        if child in visited:
            visited[child] -= 1
    return num_paths


def part2():
    graph = parse()
    visited = collections.defaultdict(int)
    return get_num_paths_part2(graph, "start", "end", visited)


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
