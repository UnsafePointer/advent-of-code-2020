from typing import Set, List


def find_sequence_for(numbers: List[int], to_find: int) -> int:
    front: int = 0
    total: int = 0
    size: int = len(numbers)
    for back in range(size):
        while front < size and total + numbers[front] <= to_find:
            total += numbers[front]
            front += 1
        if total == to_find:
            sequence = numbers[back:front]
            return min(sequence) + max(sequence)
        total -= numbers[back]
    return 0


def solve() -> str:
    file = open("input.txt", "r")
    input_numbers = []
    for line in file:
        input_numbers.append(int(line))

    preamble_size = 25
    numbers: Set[int] = set()
    insertion_order: List[int] = []
    for index in range(preamble_size):
        number = input_numbers[index]
        numbers.add(number)
        insertion_order.append(number)

    invalid_number: int
    for index in range(preamble_size, len(input_numbers)):
        new_number = input_numbers[index]
        found = False
        for number in insertion_order:
            to_find = new_number - number
            if to_find in numbers:
                found = True
                break
        if not found:
            invalid_number = new_number
            break
        oldest = insertion_order.pop(0)
        numbers.remove(oldest)
        insertion_order.append(new_number)
        numbers.add(new_number)

    result = find_sequence_for(input_numbers, invalid_number)

    return str(result)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
