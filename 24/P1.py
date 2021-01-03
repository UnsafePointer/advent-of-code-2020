from typing import Dict, Tuple


def solve() -> str:
    file = open("input.txt", "r")
    temporal_character = ""
    e_w_counter = 0.0
    n_s_counter = 0.0
    tiles: Dict[Tuple[float, float], int] = {}
    for line in file:
        characters = list(line[:-1])
        while characters:
            character = characters.pop(0)
            if not temporal_character and character in ["n", "s"]:
                temporal_character += character
            elif temporal_character:
                temporal_character += character
                if temporal_character == "ne":
                    n_s_counter += 1
                    e_w_counter += 0.5
                elif temporal_character == "sw":
                    n_s_counter -= 1
                    e_w_counter -= 0.5
                elif temporal_character == "se":
                    n_s_counter -= 1
                    e_w_counter += 0.5
                elif temporal_character == "nw":
                    n_s_counter += 1
                    e_w_counter -= 0.5
                temporal_character = ""
            else:
                if character == "e":
                    e_w_counter += 1
                elif character == "w":
                    e_w_counter -= 1
        tile_id = (e_w_counter, n_s_counter)
        tile_counter = tiles.get(tile_id, 0)
        tile_counter += 1
        tiles[tile_id] = tile_counter
        e_w_counter = 0.0
        n_s_counter = 0.0
    black_tiles = 0
    for tile_id in tiles:
        tile_counter = tiles[tile_id]
        if tile_counter % 2 == 1:
            black_tiles += 1
    return str(black_tiles)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
