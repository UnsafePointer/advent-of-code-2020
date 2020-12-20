from typing import List
from dataclasses import dataclass


@dataclass
class Password:
    lowest: int
    highest: int
    letter: str
    value: str

    def valid(self) -> bool:
        count: int = list(self.value).count(self.letter)
        return count <= self.highest and count >= self.lowest


def solve() -> str:
    file = open("input.txt", "r")

    passwords: List[Password] = []
    for line in file:
        splitted = line.split(" ")
        ranges = splitted[0].split("-")
        lowest = int(ranges[0])
        highest = int(ranges[1])
        letter = splitted[1].split(":")[0]
        value = splitted[2]
        password = Password(lowest, highest, letter, value)
        passwords.append(password)

    valid_passwords: int = 0
    for password in passwords:
        if password.valid():
            valid_passwords += 1

    return valid_passwords


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
