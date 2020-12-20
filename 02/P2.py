from typing import List
from dataclasses import dataclass


@dataclass
class Password:
    first: int
    second: int
    letter: str
    value: str

    def valid(self) -> bool:
        is_valid: bool = False
        if self.value[self.first - 1] == self.letter:
            is_valid = True
        if self.value[self.second - 1] == self.letter:
            if is_valid:
                is_valid = False
            else:
                is_valid = True
        return is_valid


def solve() -> str:
    file = open("input.txt", "r")

    passwords: List[Password] = []
    for line in file:
        splitted = line.split(" ")
        ranges = splitted[0].split("-")
        first = int(ranges[0])
        second = int(ranges[1])
        letter = splitted[1].split(":")[0]
        value = splitted[2]
        password = Password(first, second, letter, value)
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
