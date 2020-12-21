from typing import List
from itertools import islice


def solve() -> str:
    file = open("input.txt", "r")

    expenses: List[int] = []
    for line in file:
        expenses.append(int(line))

    expenses.sort()

    for index, expense1 in enumerate(islice(expenses, 0, len(expenses) - 1)):
        for expense2 in islice(expenses, index + 1, len(expenses)):
            expense_so_far = expense1 + expense2
            if expense_so_far > 2020:
                continue
            to_find = 2020 - expense_so_far
            if to_find in expenses:
                return str(to_find * expense1 * expense2)

    return "Not found"


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
