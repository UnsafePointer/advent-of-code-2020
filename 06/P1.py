from os import linesep
from typing import Set


def solve() -> str:
    file = open("input.txt", "r")
    buffer: Set[str] = set()
    total = 0
    while True:
        line = file.readline()
        if line == linesep:
            total += len(buffer)
            buffer.clear()
        elif not line:
            total += len(buffer)
            break
        else:
            buffer = buffer.union(set(line[:-1]))
    return str(total)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
