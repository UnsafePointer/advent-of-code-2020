from typing import List
from copy import deepcopy


def occupied_adjacent(
    matrix: List[List[str]], column_index: int, row_index: int
) -> int:
    occupied = 0
    for column in range(max(column_index - 1, 0), min(column_index + 2, len(matrix))):
        for row in range(
            max(row_index - 1, 0), min(row_index + 2, len(matrix[column]))
        ):
            if column == column_index and row == row_index:
                continue
            if matrix[column][row] == "#":
                occupied += 1
    return occupied


def transform(matrix: List[List[str]], column_index: int, row_index: int) -> bool:
    if matrix[column_index][row_index] == "L" and not occupied_adjacent(
        matrix, column_index, row_index
    ):
        return True
    elif (
        matrix[column_index][row_index] == "#"
        and occupied_adjacent(matrix, column_index, row_index) >= 4
    ):
        return True
    return False


def solve() -> str:
    file = open("input.txt", "r")
    seats: List[List[str]] = []
    for line in file:
        line_seats = list(line[:-1])
        seats.append(line_seats)

    has_transformed = True
    while has_transformed:
        has_transformed = False
        new_seats = deepcopy(seats.copy())
        for column_index in range(len(seats)):
            for row_index in range(len(seats[column_index])):
                if transform(seats, column_index, row_index):
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
