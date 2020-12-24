from collections import deque

from aoc.utils import load_input


def part1():
    player1, player2 = [
        deque(map(int, player.splitlines()[1:])) for player in load_input(delim="\n\n")
    ]
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
    return get_score(winner)


def get_score(winner):
    return sum(card * score for card, score in zip(winner, range(len(winner), 0, -1)))


def recurisve_combat(player1, player2, game=1):
    assert isinstance(player1, deque)
    assert isinstance(player2, deque)
    configurations = set()

    while player1 and player2:
        # print(f"Game {game}")
        # print(f"Player 1: {player1}")
        # print(f"Player 2: {player2}")
        key = (tuple(player1), tuple(player2))
        if key in configurations:
            return 1
        configurations.add(key)
        card1 = player1.popleft()
        card2 = player2.popleft()
        # print(f"Card1: {card1}, Card2: {card2}")
        if card1 <= len(player1) and card2 <= len(player2):
            winner = recurisve_combat(
                deque(list(player1)[:card1]),
                deque(list(player2)[:card2]),
                game=game + 1,
            )
        else:
            winner = 1 if card1 > card2 else 2
        if winner == 1:
            player1.extend([card1, card2])
        else:
            player2.extend([card2, card1])
    winner = 1 if player1 else 2
    return winner


def part2():
    player1, player2 = [
        deque(map(int, player.splitlines()[1:])) for player in load_input(delim="\n\n")
    ]
    winner = recurisve_combat(player1, player2)
    return get_score(player1 if winner == 1 else player2)


def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
