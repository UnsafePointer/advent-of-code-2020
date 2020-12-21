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


def solve() -> str:
    file = open("input.txt", "r")

    map_data: List[List[str]] = []
    for line in file:
        map_line = list(line)
        del map_line[-1]
        map_data.append(map_line)
    map: Map = Map(map_data)
    position: Position = Position(0, 0)
    num_of_trees: int = 0
    while True:
        position.y += 1
        position.x += 3
        if position.y >= map.get_height():
            break
        square: str = map.get_at_position(position)
        if square == "#":
            num_of_trees += 1

    return str(num_of_trees)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
