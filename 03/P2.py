from typing import List
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Map:
    data: List[List[str]]

    def get_width(self) -> int:
        return len(self.data[0])

    def get_height(self) -> int:
        return len(self.data)

    def get_at_position(self, position: Position) -> str:
        return self.data[position.y][position.x % self.get_width()]

    def num_of_trees_for(self, right: int, down: int) -> int:
        position: Position = Position(0, 0)
        num_of_trees: int = 0
        while True:
            position.y += down
            position.x += right
            if position.y >= self.get_height():
                break
            square: str = self.get_at_position(position)
            if square == "#":
                num_of_trees += 1

        return num_of_trees


def solve() -> str:
    file = open("input.txt", "r")

    map_data: List[List[str]] = []
    for line in file:
        map_line = list(line)
        del map_line[-1]
        map_data.append(map_line)
    map: Map = Map(map_data)
    solution: int = map.num_of_trees_for(1, 1)
    solution *= map.num_of_trees_for(3, 1)
    solution *= map.num_of_trees_for(5, 1)
    solution *= map.num_of_trees_for(7, 1)
    solution *= map.num_of_trees_for(1, 2)
    return str(solution)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
