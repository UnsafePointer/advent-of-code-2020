from typing import List
from sys import maxsize
from math import floor


def solve() -> str:
    file = open("input.txt", "r")
    target = int(file.readline())
    busses: List[int] = []
    for bid in file.readline()[:-1].split(","):
        if bid == "x":
            continue
        busses.append(int(bid))

    bus_id_departure = maxsize
    found_bus_id = 0
    for bus_id in busses:
        next_bus = ((floor(target / bus_id)) + 1) * bus_id
        if next_bus < bus_id_departure:
            bus_id_departure = next_bus
            found_bus_id = bus_id
    return str((bus_id_departure - target) * found_bus_id)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
