from typing import Set, List


def solve() -> str:
    file = open("input.txt", "r")
    preamble_size = 25
    numbers: Set[int] = set()
    insertion_order: List[int] = []
    for _ in range(preamble_size):
        line = file.readline()
        number = int(line)
        numbers.add(number)
        insertion_order.append(number)
    while True:
        line = file.readline()
        if not line:
            return "Unsolved"
        new_number = int(line)
        found = False
        for number in insertion_order:
            to_find = new_number - number
            if to_find in numbers:
                found = True
                break
        if not found:
            return str(new_number)
        oldest = insertion_order.pop(0)
        numbers.remove(oldest)
        insertion_order.append(new_number)
        numbers.add(new_number)
    return "Unsolved"


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
