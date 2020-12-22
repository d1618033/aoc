from dataclasses import dataclass
from typing import Optional, List, Set, Tuple

from aoc.utils import load_input
from collections import deque

def part1():
    player1, player2 = [deque(map(int, player.splitlines()[1:])) for player in load_input(delim="\n\n")]
    assert isinstance(player1, deque)
    assert isinstance(player2, deque)
    while player1 and player2:
        card1 = player1.popleft()
        card2 = player2.popleft()
        if card1 > card2:
            player1.extend([card1, card2])
        else:
            player2.extend([card2, card1])
    winner = player1 if player1 else player2
    return sum(card * score for card, score in zip(winner, range(len(winner), 0, -1)))


def part2():
    ...


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
