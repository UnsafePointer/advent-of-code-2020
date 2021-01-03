from typing import Dict, Tuple, List, Set
from copy import deepcopy


def transition_state(
    initial_state: Set[Tuple[float, float]]
) -> Set[Tuple[float, float]]:
    new_state = deepcopy(initial_state)
    for tile_id in initial_state:
        number_of_black_tile_neighbors = get_number_of_black_tile_neighbors(
            initial_state, tile_id
        )
        if number_of_black_tile_neighbors == 0 or number_of_black_tile_neighbors > 2:
            new_state.remove(tile_id)
        neighbors = get_neighbors_for_tile_id(tile_id)
        for neighbor in neighbors:
            if neighbor not in initial_state:
                number_of_black_tile_neighbors_for_neighbor = (
                    get_number_of_black_tile_neighbors(initial_state, neighbor)
                )
                if number_of_black_tile_neighbors_for_neighbor == 2:
                    new_state.add(neighbor)
    return new_state


def get_number_of_black_tile_neighbors(
    state: Set[Tuple[float, float]], tile_id: Tuple[float, float]
) -> int:
    adjacent_tile_ids = get_neighbors_for_tile_id(tile_id)
    number_of_black_tiles = 0
    for adjacent_tile_id in adjacent_tile_ids:
        if adjacent_tile_id in state:
            number_of_black_tiles += 1
    return number_of_black_tiles


def get_neighbors_for_tile_id(
    tile_id: Tuple[float, float]
) -> List[Tuple[float, float]]:
    (e_w_counter, n_s_counter) = tile_id
    return [
        move_counters_to_direction((e_w_counter, n_s_counter), "ne"),
        move_counters_to_direction((e_w_counter, n_s_counter), "e"),
        move_counters_to_direction((e_w_counter, n_s_counter), "se"),
        move_counters_to_direction((e_w_counter, n_s_counter), "sw"),
        move_counters_to_direction((e_w_counter, n_s_counter), "w"),
        move_counters_to_direction((e_w_counter, n_s_counter), "nw"),
    ]


def move_counters_to_direction(
    counters: Tuple[float, float], direction: str
) -> Tuple[float, float]:
    (e_w_counter, n_s_counter) = counters
    if direction == "ne":
        n_s_counter += 1
        e_w_counter += 0.5
    elif direction == "sw":
        n_s_counter -= 1
        e_w_counter -= 0.5
    elif direction == "se":
        n_s_counter -= 1
        e_w_counter += 0.5
    elif direction == "nw":
        n_s_counter += 1
        e_w_counter -= 0.5
    elif direction == "e":
        e_w_counter += 1
    else:  # direction == "w":
        e_w_counter -= 1
    return (e_w_counter, n_s_counter)


def solve() -> str:
    file = open("input.txt", "r")
    temporal_character = ""
    e_w_counter = 0.0
    n_s_counter = 0.0
    tiles: Set[Tuple[float, float]] = set()
    for line in file:
        characters = list(line[:-1])
        while characters:
            character = characters.pop(0)
            if not temporal_character and character in ["n", "s"]:
                temporal_character += character
            elif temporal_character:
                temporal_character += character
                (e_w_counter, n_s_counter) = move_counters_to_direction(
                    (e_w_counter, n_s_counter), temporal_character
                )
                temporal_character = ""
            else:
                (e_w_counter, n_s_counter) = move_counters_to_direction(
                    (e_w_counter, n_s_counter), character
                )
        tile_id = (e_w_counter, n_s_counter)
        if tile_id in tiles:
            tiles.remove(tile_id)
        else:
            tiles.add(tile_id)
        e_w_counter = 0.0
        n_s_counter = 0.0

    for _ in range(0, 100):
        tiles = transition_state(tiles)

    return str(len(tiles))


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
