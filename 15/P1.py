from typing import List, Dict


def solve() -> str:
    file = open("input.txt", "r")
    line = file.readline()
    starting_number: List[int] = []
    for number in line[:-1].split(","):
        starting_number.append(int(number))

    last_turns: Dict[int, List[int]] = {}
    for index in range(len(starting_number)):
        last_turns[starting_number[index]] = [index + 1]

    last_spoken_number = starting_number[-1]

    def add_turns_for_last_spoken_number() -> None:
        if last_spoken_number in last_turns:
            turns_for_last_spoken_number = last_turns[last_spoken_number]
            turns_for_last_spoken_number.append(turn)
            if len(turns_for_last_spoken_number) > 2:
                turns_for_last_spoken_number.pop(0)
        else:
            turns_for_last_spoken_number = [turn]
            last_turns[last_spoken_number] = turns_for_last_spoken_number

    for turn in range(len(starting_number) + 1, 2021):
        turns_for_last_spoken_number = last_turns[last_spoken_number]
        if len(turns_for_last_spoken_number) < 2:
            last_spoken_number = 0
            add_turns_for_last_spoken_number()
        else:
            last_spoken_number = (
                turns_for_last_spoken_number[1] - turns_for_last_spoken_number[0]
            )
            add_turns_for_last_spoken_number()

    return str(last_spoken_number)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
