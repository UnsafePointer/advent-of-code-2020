from typing import List, Dict
from dataclasses import dataclass, field
from enum import Enum, auto
from os import linesep
from copy import deepcopy
from textwrap import dedent


class Direction(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


def opposite(direction: Direction) -> Direction:
    if direction == Direction.UP:
        return Direction.DOWN
    elif direction == Direction.RIGHT:
        return Direction.LEFT
    elif direction == Direction.DOWN:
        return Direction.UP
    else:  # elif direction == Direction.LEFT:
        return Direction.RIGHT


@dataclass
class Edge:
    edge_data: List[str]
    free: bool = field(default=True)


@dataclass
class Tile:
    tile_id: int
    tile_data: List[List[str]]
    edges: Dict[Direction, Edge] = field(init=False)

    def __post_init__(self) -> None:
        self.edges = make_edges(self)

    def __repr__(self) -> str:
        tile_repr = ""
        tile_repr += f"Tile: {self.tile_id}"
        tile_repr += linesep
        for row in self.tile_data:
            tile_repr += "".join(row)
            tile_repr += linesep
        return tile_repr


def make_edges(tile: Tile) -> Dict[Direction, Edge]:
    tile_data: List[List[str]] = tile.tile_data
    up_edge_data: List[str] = []
    for index in range(0, len(tile_data[0])):
        up_edge_data.append(tile_data[0][index])
    up_edge = Edge(up_edge_data)

    down_edge_data: List[str] = []
    for index in range(0, len(tile_data[len(tile_data) - 1])):
        down_edge_data.append(tile_data[len(tile_data) - 1][index])
    down_edge = Edge(down_edge_data)

    right_edge_data: List[str] = []
    for index in range(0, len(tile_data[len(tile_data) - 1])):
        right_edge_data.append(tile_data[index][len(tile_data) - 1])
    right_edge = Edge(right_edge_data)

    left_edge_data: List[str] = []
    for index in range(0, len(tile_data[len(tile_data) - 1])):
        left_edge_data.append(tile_data[index][0])
    left_edge = Edge(left_edge_data)
    return {
        Direction.UP: up_edge,
        Direction.RIGHT: right_edge,
        Direction.DOWN: down_edge,
        Direction.LEFT: left_edge,
    }


def flip_horizontal(tile: Tile) -> Tile:
    tile_data = deepcopy(tile.tile_data)
    for index in range(0, len(tile_data)):
        tile_data[index].reverse()
    return Tile(tile.tile_id, tile_data)


def flip_vertical(tile: Tile) -> Tile:
    tile_data = deepcopy(tile.tile_data)
    tile_data.reverse()
    return Tile(tile.tile_id, tile_data)


def rotate(tile: Tile) -> Tile:
    tile_data = deepcopy(tile.tile_data)
    list_of_tuples = zip(*tile_data[::-1])
    tile_data = [list(elem) for elem in list_of_tuples]
    return Tile(tile.tile_id, tile_data)


tile_variants_cache: Dict[int, List[Tile]] = {}


def make_tile_variants(tile: Tile) -> List[Tile]:
    if tile.tile_id in tile_variants_cache:
        return tile_variants_cache[tile.tile_id]

    tile_variants: List[Tile] = []
    base_variants: List[Tile] = []

    base_variants.append(tile)
    base_variants.append(flip_horizontal(tile))
    base_variants.append(flip_vertical(tile))

    for base_variant in base_variants:
        base_variant_rotated = base_variant
        for _ in range(0, 4):
            base_variant_rotated = rotate(base_variant_rotated)
            tile_variants.append(base_variant_rotated)

    duplicates: List[int] = []
    for tile_variant_index in range(0, len(tile_variants) - 1):
        for another_tile_variant_index in range(
            tile_variant_index + 1, len(tile_variants)
        ):
            if (
                tile_variants[tile_variant_index].tile_data
                == tile_variants[another_tile_variant_index].tile_data
            ):
                duplicates.append(another_tile_variant_index)

    tile_variants_without_dupes = [
        i for j, i in enumerate(tile_variants) if j not in duplicates
    ]
    tile_variants_cache[tile.tile_id] = tile_variants_without_dupes
    return tile_variants_without_dupes


def solve() -> str:
    file = open("input.txt", "r")
    tiles: List[Tile] = []
    tile_id: int
    tile_data: List[List[str]] = []
    while True:
        line = file.readline()
        if line == linesep or line == "":
            tile = Tile(tile_id, deepcopy(tile_data))
            tiles.append(tile)
            tile_data.clear()
            if line == "":
                break
        elif "Tile" in line:
            splitted = line.split(" ")
            tile_id = int(splitted[1].split(":")[0])
        else:
            tile_data.append(list(line.strip()))

    result = 1
    for tile in tiles:
        possible_appends = 0
        for tile_edge_direction in tile.edges:
            tile_edge = tile.edges[tile_edge_direction]
            for another_tile in tiles:
                if tile.tile_id == another_tile.tile_id:
                    continue
                for another_tile_variant in make_tile_variants(another_tile):
                    for (
                        another_tile_variant_edge_direction
                    ) in another_tile_variant.edges:
                        another_tile_variant_edge = another_tile_variant.edges[
                            another_tile_variant_edge_direction
                        ]
                        if (
                            opposite(tile_edge_direction)
                            == another_tile_variant_edge_direction
                            and tile_edge.edge_data
                            == another_tile_variant_edge.edge_data
                        ):
                            possible_appends += 1
        if possible_appends == 2:
            result *= tile.tile_id
    return str(result)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
