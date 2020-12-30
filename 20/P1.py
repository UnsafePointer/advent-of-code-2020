from os import linesep
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass, field
from copy import deepcopy, copy
from enum import Enum, auto


class EdgeDirection(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


def opposite(direction: EdgeDirection) -> EdgeDirection:
    if direction == EdgeDirection.UP:
        return EdgeDirection.DOWN
    elif direction == EdgeDirection.RIGHT:
        return EdgeDirection.LEFT
    elif direction == EdgeDirection.DOWN:
        return EdgeDirection.UP
    else:  # elif direction == EdgeDirection.LEFT:
        return EdgeDirection.RIGHT


@dataclass
class Edge:
    edge_data: List[int]
    free: bool = field(default=True)


@dataclass
class Tile:
    tile_id: int
    tile_data: List[List[int]]
    edges: Dict[EdgeDirection, Edge] = field(init=False)

    def __post_init__(self) -> None:
        self.edges = make_edges(self)

    def print_data(self) -> None:
        for data in self.tile_data:
            print(data)

    def number_of_free_edges_per_direction(self) -> Dict[EdgeDirection, int]:
        total: Dict[EdgeDirection, int] = {}
        for edge_direction in self.edges:
            edge = self.edges[edge_direction]
            if edge.free:
                total_for_direction = total.get(edge_direction, 0)
                total_for_direction += 1
                total[edge_direction] = total_for_direction
        return total

    def number_of_free_edges(self) -> int:
        total = 0
        for edge_direction in self.edges:
            edge = self.edges[edge_direction]
            if edge.free:
                total += 1
        return total


def make_edges(tile: Tile) -> Dict[EdgeDirection, Edge]:
    tile_data: List[List[int]] = tile.tile_data
    up_edge_data: List[int] = []
    for index in range(0, len(tile_data[0])):
        up_edge_data.append(tile_data[0][index])
    up_edge = Edge(up_edge_data)

    down_edge_data: List[int] = []
    for index in range(0, len(tile_data[len(tile_data) - 1])):
        down_edge_data.append(tile_data[len(tile_data) - 1][index])
    down_edge = Edge(down_edge_data)

    right_edge_data: List[int] = []
    for index in range(0, len(tile_data[len(tile_data) - 1])):
        right_edge_data.append(tile_data[index][len(tile_data) - 1])
    right_edge = Edge(right_edge_data)

    left_edge_data: List[int] = []
    for index in range(0, len(tile_data[len(tile_data) - 1])):
        left_edge_data.append(tile_data[index][0])
    left_edge = Edge(left_edge_data)
    return {
        EdgeDirection.UP: up_edge,
        EdgeDirection.RIGHT: right_edge,
        EdgeDirection.DOWN: down_edge,
        EdgeDirection.LEFT: left_edge,
    }


def make_position_for_direction_from_position(
    position: Tuple[int, int], direction: EdgeDirection
) -> Tuple[int, int]:
    if direction == EdgeDirection.UP:
        return (position[0], position[1] + 1)
    elif direction == EdgeDirection.RIGHT:
        return (position[0] + 1, position[1])
    elif direction == EdgeDirection.DOWN:
        return (position[0], position[1] - 1)
    else:  # elif direction == EdgeDirection.LEFT:
        return (position[0] - 1, position[1])


def make_adjacent_positions_by_directions(
    position: Tuple[int, int]
) -> Dict[EdgeDirection, Tuple[int, int]]:
    positions_by_direction: Dict[EdgeDirection, Tuple[int, int]] = {}
    for direction in EdgeDirection:
        positions_by_direction[direction] = make_position_for_direction_from_position(
            position, direction
        )
    return positions_by_direction


@dataclass
class Image:
    tiles: Dict[Tuple[int, int], Tile] = field(default_factory=lambda: {})

    def available_spots(self) -> List[Tuple[int, int]]:
        spots: List[Tuple[int, int]] = []
        for spot in self.tiles:
            tile = self.tiles[spot]
            for tile_edge_direction in tile.edges:
                tile_edge = tile.edges[tile_edge_direction]
                if tile_edge.free:
                    free_spot = make_position_for_direction_from_position(
                        spot, tile_edge_direction
                    )
                    spots.append(free_spot)
        return spots

    def can_append_tile_at_position(
        self, position: Tuple[int, int], tile: Tile
    ) -> bool:
        positions_by_direction = make_adjacent_positions_by_directions(position)
        for direction in positions_by_direction:
            position = positions_by_direction[direction]
            if position in self.tiles:
                tile_edge = tile.edges[direction]
                image_tile_in_direction = self.tiles[position]
                image_tile_edge = image_tile_in_direction.edges[opposite(direction)]
                if tile_edge.edge_data != image_tile_edge.edge_data:
                    return False
        return True

    def append_tile_at_position(self, position: Tuple[int, int], tile: Tile) -> None:
        positions_by_direction = make_adjacent_positions_by_directions(position)
        for direction in positions_by_direction:
            position = positions_by_direction[direction]
            if position in self.tiles:
                tile_edge = tile.edges[direction]
                tile_edge.free = False
                image_tile_in_direction = self.tiles[position]
                image_tile_edge = image_tile_in_direction.edges[opposite(direction)]
                image_tile_edge.free = False

    def undo_append(self, position: Tuple[int, int], tile: Tile) -> None:
        positions_by_direction = make_adjacent_positions_by_directions(position)
        for direction in positions_by_direction:
            position = positions_by_direction[direction]
            if position in self.tiles:
                tile_edge = tile.edges[direction]
                tile_edge.free = True
                image_tile_in_direction = self.tiles[position]
                image_tile_edge = image_tile_in_direction.edges[opposite(direction)]
                image_tile_edge.free = True

    def is_valid(self) -> bool:
        total_free_edges_per_direction: Dict[EdgeDirection, int] = {}
        for position in self.tiles:
            tile = self.tiles[position]
            free_edges_per_direction = tile.number_of_free_edges_per_direction()
            for direction in free_edges_per_direction:
                total_free_edges = total_free_edges_per_direction.get(direction, 0)
                total_free_edges += free_edges_per_direction[direction]
                total_free_edges_per_direction[direction] = total_free_edges
        valid_edges = (
            total_free_edges_per_direction.get(EdgeDirection.UP, 0)
            == total_free_edges_per_direction.get(EdgeDirection.RIGHT, 0)
            == total_free_edges_per_direction.get(EdgeDirection.DOWN, 0)
            == total_free_edges_per_direction.get(EdgeDirection.LEFT, 0)
        )
        corners = self.get_corners()
        return valid_edges and len(corners) == 4

    def is_empty(self) -> bool:
        return len(self.tiles) == 0

    def get_corners(self) -> List[int]:
        corners: List[int] = []
        for position in self.tiles:
            tile = self.tiles[position]
            if tile.number_of_free_edges() == 2:
                corners.append(tile.tile_id)
        return corners


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


def make_tile_variants(tile: Tile) -> List[Tile]:
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

    return tile_variants


def attempt_to_solve(tiles: List[Tile], image: Image) -> Optional[Image]:
    if not tiles:
        if image.is_valid():
            return image
        else:
            return None

    for tile in tiles:
        for tile_variant in make_tile_variants(tile):
            if image.is_empty():
                image_copy = Image(deepcopy(image.tiles))
                tiles_copy = deepcopy(tiles)
                tile_variant_copy = deepcopy(tile_variant)

                image_copy.tiles[(0, 0)] = tile_variant
                tiles_copy.remove(tile)
                result = attempt_to_solve(tiles_copy, image_copy)
                if result:
                    return result
            else:
                for available_spot in image.available_spots():
                    if image.can_append_tile_at_position(available_spot, tile_variant):
                        image.append_tile_at_position(available_spot, tile_variant)

                        image_copy = Image(deepcopy(image.tiles))
                        tiles_copy = deepcopy(tiles)
                        tile_variant_copy = deepcopy(tile_variant)

                        image_copy.tiles[available_spot] = tile_variant
                        tiles_copy.remove(tile)
                        result = attempt_to_solve(tiles_copy, image_copy)
                        if result:
                            return result
                        else:
                            image.undo_append(available_spot, tile_variant)

    return None


def solve() -> str:
    file = open("input.txt", "r")
    tiles: List[Tile] = []
    tile_id: int
    tile_data: List[List[int]] = []
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
            tile_data.append(
                [int(x) for x in line.replace(".", "0").replace("#", "1").strip()]
            )

    # Flip vertical
    # example_tile = tiles[1]
    # example_tile_fvertical = flip_vertical(example_tile)
    # example_tile_fvertical.print_data()

    # Flip vertical + Rotate trice
    # example_tile = tiles[5]
    # example_tile.print_data()
    # print()
    # example_tile_fvertical = flip_vertical(example_tile)
    # example_tile_fvertical.print_data()
    # print()
    # example_tile_fvertical_rotate = rotate(example_tile_fvertical)
    # example_tile_fvertical_rotate = rotate(example_tile_fvertical_rotate)
    # example_tile_fvertical_rotate = rotate(example_tile_fvertical_rotate)
    # example_tile_fvertical_rotate.print_data()
    # print()

    # Flip Horizontal
    # example_tile = tiles[2]
    # example_tile_fhorizontal = flip_horizontal(example_tile)
    # example_tile_fhorizontal.print_data()

    image: Image = Image()
    result = attempt_to_solve(tiles, image)
    if result is None:
        return "Not found"
    result_image: Image = result
    corners = result_image.get_corners()

    product = 1
    for corner in corners:
        product *= corner

    return str(product)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
