from dataclasses import dataclass
from math import cos, sin, radians


@dataclass
class Position:
    x: int
    y: int

    def rotate(self, angle: int) -> None:
        x = int(self.x * cos(radians(angle)) - self.y * sin(radians(angle)))
        y = int(self.x * sin(radians(angle)) + self.y * cos(radians(angle)))
        self.x = x
        self.y = y
        pass


@dataclass
class Ship:
    position: Position
    direction: Position

    def move(self, instruction: str, param: int) -> None:
        if instruction == "N":
            self.position.y += param
        elif instruction == "S":
            self.position.y -= param
        elif instruction == "E":
            self.position.x += param
        elif instruction == "W":
            self.position.x -= param
        elif instruction == "L":
            self.direction.rotate(param)
        elif instruction == "R":
            self.direction.rotate(360 - param)
        elif instruction == "F":
            self.position.x += self.direction.x * param
            self.position.y += self.direction.y * param

    def manhattan_distance(self) -> int:
        return abs(self.position.x) + abs(self.position.y)


def solve() -> str:
    ship: Ship = Ship(Position(0, 0), Position(1, 0))

    file = open("input.txt", "r")
    for line in file:
        instruction = line[0]
        param = int(line[1:-1])
        ship.move(instruction, param)

    return str(ship.manhattan_distance())


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
