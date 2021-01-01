from typing import List, Tuple, Set, Dict
from os import linesep
from copy import copy
from enum import Enum, auto
from uuid import uuid4


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

    player_1_decks: List[List[int]] = []
    player_1_decks.append(player_1)
    player_2_decks: List[List[int]] = []
    player_2_decks.append(player_2)

    cards_stack: List[Tuple[int, int, str]] = []

    caches: Dict[str, Set[Tuple[Tuple[int, ...], Tuple[int, ...]]]] = {}
    current_game_id = str(uuid4())

    while True:
        player_1_deck = player_1_decks[-1]
        player_2_deck = player_2_decks[-1]

        cache = caches.get(current_game_id, set())
        cache_key = (tuple(player_1_deck), tuple(player_2_deck))
        if cache_key in cache:
            player_2_deck.clear()
        cache.add(cache_key)
        caches[current_game_id] = cache

        if not player_1_deck:
            if len(player_1_decks) == 1 or len(player_2_decks) == 1:
                break
            player_1_decks.pop()
            player_2_decks.pop()
            player_2_deck = player_2_decks[-1]
            caches.pop(current_game_id)
            (player_1_card, player_2_card, previous_game_id) = cards_stack.pop(0)
            player_2_deck.append(player_2_card)
            player_2_deck.append(player_1_card)
            current_game_id = previous_game_id
            continue
        if not player_2_deck:
            if len(player_1_decks) == 1 or len(player_2_decks) == 1:
                break
            player_1_decks.pop()
            player_2_decks.pop()
            player_1_deck = player_1_decks[-1]
            caches.pop(current_game_id)
            (player_1_card, player_2_card, previous_game_id) = cards_stack.pop(0)
            player_1_deck.append(player_1_card)
            player_1_deck.append(player_2_card)
            current_game_id = previous_game_id
            continue

        player_1_card = player_1_deck.pop(0)
        player_2_card = player_2_deck.pop(0)

        if len(player_1_deck) >= player_1_card and len(player_2_deck) >= player_2_card:
            player_1_decks.append(copy(player_1_deck[0:player_1_card]))
            player_2_decks.append(copy(player_2_deck[0:player_2_card]))
            cards_stack.insert(0, (player_1_card, player_2_card, current_game_id))
            current_game_id = str(uuid4())
            if current_game_id in caches:
                break
        else:
            if player_1_card > player_2_card:
                player_1_deck.append(player_1_card)
                player_1_deck.append(player_2_card)
            else:
                player_2_deck.append(player_2_card)
                player_2_deck.append(player_1_card)

    winner: List[int] = []
    if len(player_1_decks[0]) > len(player_2_decks[0]):
        winner = player_1_decks[0]
    else:
        winner = player_2_decks[0]

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
