from typing import List


def solve() -> str:
    file = open("input.txt", "r")
    adapters: List[int] = []
    for line in file:
        adapters.append(int(line))
    adapters.sort()
    adapters.append(adapters[-1] + 3)
    differences = 0
    previous_adapter = 0
    difference_of_1 = 0
    difference_of_3 = 0
    for adapter in adapters:
        difference = adapter - previous_adapter
        if difference == 1:
            difference_of_1 += 1
        elif difference == 3:
            difference_of_3 += 1
        differences += difference
        previous_adapter = adapter
    return str(difference_of_1 * difference_of_3)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
