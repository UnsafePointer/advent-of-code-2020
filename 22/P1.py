from typing import List
from os import linesep


def solve() -> str:
    file = open("input.txt", "r")
    player_1: List[int] = []
    player_2: List[int] = []
    player_1_done = False
    for line in file:
        if "Player" in line:
            continue
        elif line == linesep:
            player_1_done = True
        elif not player_1_done:
            player_1.append(int(line.strip()))
        else:
            player_2.append(int(line.strip()))

    while len(player_1) > 0 and len(player_2) > 0:
        player_1_card = player_1.pop(0)
        player_2_card = player_2.pop(0)
        if player_1_card > player_2_card:
            player_1.append(player_1_card)
            player_1.append(player_2_card)
        else:
            player_2.append(player_2_card)
            player_2.append(player_1_card)

    winner: List[int]
    if len(player_1) > len(player_2):
        winner = player_1
    else:
        winner = player_2

    score = 0
    iteration = 1
    while winner:
        bottom_card = winner.pop()
        score += bottom_card * iteration
        iteration += 1
    return str(score)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
