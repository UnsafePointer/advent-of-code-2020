from typing import List


def solve() -> str:
    file = open("input.txt", "r")

    expenses: List[int] = []
    for line in file:
        expenses.append(int(line))

    expenses.sort()
    for expense in expenses:
        if expense > 2020:
            continue
        to_find = 2020 - expense
        if to_find in expenses:
            return str(to_find * expense)

    return "Not found"


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
