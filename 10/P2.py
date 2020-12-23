from typing import List, Dict
from functools import lru_cache


def solve() -> str:
    file = open("input.txt", "r")
    adapters: List[int] = []
    adapters.append(0)
    for line in file:
        adapters.append(int(line))
    adapters.sort()
    device = adapters[-1] + 3
    adapters.append(device)

    @lru_cache(maxsize=None)
    def attempt_to_solve(
        current_index: int,
    ) -> int:
        if current_index == len(adapters) - 1:
            return 1
        result = 0
        for index in range(current_index + 1, len(adapters)):
            if adapters[index] - adapters[current_index] <= 3:
                result += attempt_to_solve(index)
        return result

    result = attempt_to_solve(0)

    return str(result)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
