from typing import List


def solve() -> str:
    file = open("input.txt", "r")
    line = file.readline()
    input_numbers: List[int] = []
    for character in list(line.strip()):
        number = int(character)
        input_numbers.append(number)
    max_number = len(input_numbers)
    moves = 100
    current_index = 0
    removed_numbers: List[int] = []
    while moves > 0:
        current_number = input_numbers[current_index]
        current_index += 1
        for _ in range(0, 3):
            if current_index >= len(input_numbers):
                current_index = 0
            removed_numbers.append(input_numbers[current_index])
            current_index += 1
        for removed_number in removed_numbers:
            input_numbers.remove(removed_number)
        destination_number = current_number
        while True:
            destination_number -= 1
            if destination_number < 0:
                destination_number = max_number
            try:
                destination_index = input_numbers.index(destination_number)
                destination_index += 1
                for removed_number in removed_numbers:
                    input_numbers.insert(destination_index, removed_number)
                    destination_index += 1
                removed_numbers.clear()
                break
            except ValueError as _:
                continue
        # end
        current_index = input_numbers.index(current_number)
        current_index += 1
        if current_index >= len(input_numbers):
            current_index = 0
        moves -= 1

    solution = ""
    index_of_1 = input_numbers.index(1)
    for x in range(0, len(input_numbers) - 1):
        index_of_1 += 1
        if index_of_1 >= len(input_numbers):
            index_of_1 = 0
        solution += str(input_numbers[index_of_1])
    return solution


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
