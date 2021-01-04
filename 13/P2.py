from typing import List, Tuple


def solve() -> str:
    file = open("input.txt", "r")
    busses: List[Tuple[int, int]] = []
    time = 0
    for bid in file.readline()[:-1].split(","):
        time += 1
        if bid == "x":
            continue
        busses.append((int(bid), time - 1))
    timestamp = 0
    (step, _) = busses.pop(0)
    while busses:
        (next_bus, time) = busses[0]
        if (timestamp + time) % next_bus == 0:
            step *= next_bus  # this works because they're prime
            busses.pop(0)
        else:
            timestamp += step
    return str(timestamp)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
