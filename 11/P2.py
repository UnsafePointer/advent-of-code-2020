from typing import List, Dict, Tuple
from copy import deepcopy
from enum import Enum, auto
from functools import lru_cache


class Direction(Enum):
    N = auto()
    NE = auto()
    E = auto()
    SE = auto()
    S = auto()
    SW = auto()
    W = auto()
    NW = auto()


def solve() -> str:
    file = open("input.txt", "r")
    seats: List[List[str]] = []
    for line in file:
        line_seats = list(line[:-1])
        seats.append(line_seats)

    @lru_cache(maxsize=None)
    def is_adjecent_occupied_in_direction(
        column_index: int, row_index: int, direction: Direction
    ) -> bool:
        if direction == Direction.N:
            column_index -= 1
        elif direction == Direction.NE:
            column_index -= 1
            row_index += 1
        elif direction == Direction.E:
            row_index += 1
        elif direction == Direction.SE:
            row_index += 1
            column_index += 1
        elif direction == Direction.S:
            column_index += 1
        elif direction == Direction.SW:
            row_index -= 1
            column_index += 1
        elif direction == Direction.W:
            row_index -= 1
        elif direction == Direction.NW:
            row_index -= 1
            column_index -= 1

        if (
            column_index < 0
            or column_index >= len(seats)
            or row_index < 0
            or row_index >= len(seats[column_index])
        ):
            return False

        if seats[column_index][row_index] == "L":
            return False
        elif seats[column_index][row_index] == "#":
            return True
        elif seats[column_index][row_index] == ".":
            result = is_adjecent_occupied_in_direction(
                column_index, row_index, direction
            )
            return result

        return False

    def occupied_adjacent(column_index: int, row_index: int) -> int:
        occupied = 0
        for direction in list(Direction):
            if is_adjecent_occupied_in_direction(column_index, row_index, direction):
                occupied += 1
        return occupied

    def transform(column_index: int, row_index: int) -> bool:
        if seats[column_index][row_index] == "L" and not occupied_adjacent(
            column_index, row_index
        ):
            return True
        elif (
            seats[column_index][row_index] == "#"
            and occupied_adjacent(column_index, row_index) >= 5
        ):
            return True
        return False

    has_transformed = True
    while has_transformed:
        has_transformed = False
        is_adjecent_occupied_in_direction.cache_clear()
        new_seats = deepcopy(seats.copy())
        for column_index in range(len(seats)):
            for row_index in range(len(seats[column_index])):
                if transform(column_index, row_index):
                    has_transformed = True
                    if seats[column_index][row_index] == "L":
                        new_seats[column_index][row_index] = "#"
                    elif seats[column_index][row_index] == "#":
                        new_seats[column_index][row_index] = "L"
        seats = new_seats

    total_occupied = 0
    for column in range(len(seats)):
        for row in range(len(seats[column])):
            if seats[column][row] == "#":
                total_occupied += 1

    return str(total_occupied)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
