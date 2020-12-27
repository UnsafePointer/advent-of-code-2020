from typing import Dict, Tuple, List
from copy import deepcopy


def active_neighbors(
    state: Dict[Tuple[int, int, int], str], point: Tuple[int, int, int]
) -> int:
    (point_x_index, point_y_index, point_z_index) = point
    total_active_neighbors = 0
    for x_index in range(point_x_index - 1, point_x_index + 2):
        for y_index in range(point_y_index - 1, point_y_index + 2):
            for z_index in range(point_z_index - 1, point_z_index + 2):
                key = (x_index, y_index, z_index)
                if point == key:
                    continue
                current_state = state.get(key, ".")
                if current_state == "#":
                    total_active_neighbors += 1
    return total_active_neighbors


def get_neighbors(point: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    (point_x_index, point_y_index, point_z_index) = point
    neighbors: List[Tuple[int, int, int]] = []
    for x_index in range(point_x_index - 1, point_x_index + 2):
        for y_index in range(point_y_index - 1, point_y_index + 2):
            for z_index in range(point_z_index - 1, point_z_index + 2):
                neighbor = (x_index, y_index, z_index)
                if point == neighbor:
                    continue
                neighbors.append(neighbor)
    return neighbors


def transition_state(
    initial_state: Dict[Tuple[int, int, int], str]
) -> Dict[Tuple[int, int, int], str]:
    new_state = initial_state.copy()
    for point in initial_state:
        point_active_neighbors = active_neighbors(initial_state, point)
        if initial_state[point] == "#":
            if point_active_neighbors == 2 or point_active_neighbors == 3:
                pass
            else:
                new_state[point] = "."
            neighbors = get_neighbors(point)
            for neighbor in neighbors:
                if neighbor not in initial_state:
                    neighbor_active_neighbors = active_neighbors(
                        initial_state, neighbor
                    )
                    if neighbor_active_neighbors == 3:
                        new_state[neighbor] = "#"
        else:
            if point_active_neighbors == 3:
                new_state[point] = "#"
    return new_state


def solve() -> str:
    state: Dict[Tuple[int, int, int], str] = {}

    file = open("input.txt", "r")
    y_index = 0
    for line in file:
        characters = list(line[:-1])
        for x_index, character in enumerate(characters):
            state[(x_index, y_index, 0)] = character
        y_index += 1

    for _ in range(0, 6):
        state = transition_state(state)

    total_active = 0
    for point in state:
        if state[point] == "#":
            total_active += 1
    return str(total_active)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
