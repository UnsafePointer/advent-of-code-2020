from os import linesep
from typing import Set, List


def solve() -> str:
    file = open("input.txt", "r")
    buffer: List[Set[str]] = []
    total = 0
    while True:
        line = file.readline()
        if line == linesep:
            total += len(set.intersection(*buffer))
            buffer.clear()
        elif not line:
            total += len(set.intersection(*buffer))
            break
        else:
            buffer.append(set(line[:-1]))
    return str(total)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
