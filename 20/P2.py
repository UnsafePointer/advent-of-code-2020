from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum, auto
from os import linesep
from copy import deepcopy
from textwrap import dedent
from math import sqrt
from re import compile


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


def remove_gaps_from_tile(tile: Tile) -> Tile:
    tile_data = [row[1:-1] for row in tile.tile_data[1:-1]]
    return Tile(tile.tile_id, tile_data)


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


def make_position_for_direction_from_position(
    position: Tuple[int, int], direction: Direction
) -> Tuple[int, int]:
    if direction == Direction.UP:
        return (position[0], position[1] + 1)
    elif direction == Direction.RIGHT:
        return (position[0] + 1, position[1])
    elif direction == Direction.DOWN:
        return (position[0], position[1] - 1)
    else:  # elif direction == Direction.LEFT:
        return (position[0] - 1, position[1])


def make_adjacent_positions_by_directions(
    position: Tuple[int, int], ranges: Tuple[range, range]
) -> Dict[Direction, Tuple[int, int]]:
    (x_range, y_range) = ranges
    positions_by_direction: Dict[Direction, Tuple[int, int]] = {}
    for direction in Direction:
        new_position = make_position_for_direction_from_position(position, direction)
        (x, y) = new_position
        if x >= x_range.stop or x < x_range.start:
            continue
        if y >= y_range.stop or y < y_range.start:
            continue
        positions_by_direction[direction] = new_position
    return positions_by_direction


@dataclass
class Image:
    side_length: int
    ranges: Tuple[range, range] = field(init=False)
    tiles: Dict[Tuple[int, int], Tile] = field(default_factory=lambda: {})

    def __post_init__(self) -> None:
        x_min = -int(self.side_length / 2)
        y_min = -int(self.side_length / 2)
        self.ranges = (
            range(x_min, x_min + self.side_length),
            range(y_min, y_min + self.side_length),
        )

    def available_spots(self) -> Set[Tuple[int, int]]:
        spots: Set[Tuple[int, int]] = set()
        (x_range, y_range) = self.ranges
        for spot in self.tiles:
            tile = self.tiles[spot]
            for tile_edge_direction in tile.edges:
                tile_edge = tile.edges[tile_edge_direction]
                if tile_edge.free:
                    free_spot = make_position_for_direction_from_position(
                        spot, tile_edge_direction
                    )
                    (x, y) = free_spot
                    if x >= x_range.stop or x < x_range.start:
                        continue
                    if y >= y_range.stop or y < y_range.start:
                        continue
                    spots.add(free_spot)
        return spots

    def can_append_tile_at_position(
        self, available_position: Tuple[int, int], tile: Tile
    ) -> bool:
        positions_by_direction = make_adjacent_positions_by_directions(
            available_position, self.ranges
        )
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
        positions_by_direction = make_adjacent_positions_by_directions(
            position, self.ranges
        )
        for direction in positions_by_direction:
            position = positions_by_direction[direction]
            if position in self.tiles:
                tile_edge = tile.edges[direction]
                tile_edge.free = False
                image_tile_in_direction = self.tiles[position]
                image_tile_edge = image_tile_in_direction.edges[opposite(direction)]
                image_tile_edge.free = False

    def undo_append(self, position: Tuple[int, int], tile: Tile) -> None:
        positions_by_direction = make_adjacent_positions_by_directions(
            position, self.ranges
        )
        for direction in positions_by_direction:
            position = positions_by_direction[direction]
            if position in self.tiles:
                tile_edge = tile.edges[direction]
                tile_edge.free = True
                image_tile_in_direction = self.tiles[position]
                image_tile_edge = image_tile_in_direction.edges[opposite(direction)]
                image_tile_edge.free = True

    def build_image(self) -> List[List[str]]:
        (x_range, y_range) = self.ranges
        tile_side_size = len(self.tiles[(0, 0)].tile_data)
        tile_side_size -= 2
        image_width = len(x_range) * tile_side_size
        image_height = len(y_range) * tile_side_size
        image_data: List[List[str]] = []
        for _ in range(0, image_height):
            image_data.append(["."] * image_width)

        y_image = self.side_length - 1
        for y in y_range:
            x_image = 0
            for x in x_range:
                position = (x, y)
                tile = remove_gaps_from_tile(self.tiles[position])
                for tile_y, tile_row in enumerate(tile.tile_data):
                    for tile_x, value in enumerate(tile.tile_data[tile_y]):
                        image_data_x = tile_x + x_image * len(tile.tile_data[tile_y])
                        image_data_y = tile_y + y_image * len(tile.tile_data[tile_y])
                        image_data[image_data_y][image_data_x] = value
                x_image += 1
            y_image -= 1
        return image_data


def attempt_to_solve(tiles: List[Tile], image: Image) -> Optional[Image]:
    if not tiles:
        return image

    for tile in tiles:
        for tile_variant in make_tile_variants(tile):
            for available_spot in image.available_spots():
                if image.can_append_tile_at_position(available_spot, tile_variant):
                    image.append_tile_at_position(available_spot, tile_variant)

                    image_copy = Image(image.side_length, deepcopy(image.tiles))
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


monster_head_expression = compile(r"(?=..................#.)")
monster_upper_body_expression = compile(r"(#....##....##....###)")
monster_lower_body_expression = compile(r"(.#..#..#..#..#..#...)")


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

    image: Image = Image(side_length=int(sqrt(len(tiles))))
    (image_x_range, image_y_range) = image.ranges
    for tile in tiles:
        possible_append_directions: Set[Direction] = set()
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
                            possible_append_directions.add(tile_edge_direction)
        if len(possible_append_directions) == 2:
            position: Tuple[int, int]
            if (
                Direction.RIGHT in possible_append_directions
                and Direction.DOWN in possible_append_directions
            ):
                position = (image_x_range.start, image_y_range.stop - 1)
            elif (
                Direction.LEFT in possible_append_directions
                and Direction.DOWN in possible_append_directions
            ):
                position = (image_x_range.stop - 1, image_y_range.stop - 1)
            elif (
                Direction.RIGHT in possible_append_directions
                and Direction.UP in possible_append_directions
            ):
                position = (image_x_range.start, image_y_range.start)
            elif (
                Direction.LEFT in possible_append_directions
                and Direction.UP in possible_append_directions
            ):
                position = (image_x_range.stop - 1, image_y_range.start)
            image.tiles[position] = tile
            break

    for image_tile_position in image.tiles:
        image_tile = image.tiles[image_tile_position]
        tiles.remove(image_tile)

    result = attempt_to_solve(tiles, image)
    if result is None:
        return "Not found"
    result_image: Image = result
    result_tile = Tile(0, result_image.build_image())

    found = 0
    result_tile_variant: Tile
    for result_tile_variant in make_tile_variants(result_tile):
        for index, row in enumerate(result_tile_variant.tile_data):
            text_search = "".join(row)
            for text_search_result in monster_head_expression.finditer(text_search):
                if index + 1 >= len(result_tile_variant.tile_data) or index + 2 >= len(
                    result_tile_variant.tile_data
                ):
                    continue
                upper_body_row = "".join(result_tile_variant.tile_data[index + 1])
                lower_body_row = "".join(result_tile_variant.tile_data[index + 2])
                if monster_upper_body_expression.match(
                    upper_body_row, text_search_result.start()
                ) and monster_lower_body_expression.match(
                    lower_body_row, text_search_result.start()
                ):
                    found += 1
        if found != 0:
            break
    all_hash_characters: List[str] = []
    for result_tile_variant_row in result_tile_variant.tile_data:
        all_hash_characters += [
            character for character in result_tile_variant_row if character == "#"
        ]
    return str(len(all_hash_characters) - found * 15)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
