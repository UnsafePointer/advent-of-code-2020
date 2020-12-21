from os import linesep
from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class Passport:
    data: Dict[str, str]
    required_fields: List[str] = field(
        default_factory=lambda: [
            "byr",
            "iyr",
            "eyr",
            "hgt",
            "hcl",
            "ecl",
            "pid",
            # "cid",
        ]
    )

    def valid(self) -> bool:
        for field in self.required_fields:
            if not field in self.data:
                return False
        return True


def solve() -> str:
    file = open("input.txt", "r")

    buffer: Dict[str, str] = {}
    passports: List[Passport] = []
    while True:
        line = file.readline()
        if line == linesep:
            passport = Passport(buffer)
            passports.append(passport)
            buffer = {}
        elif not line:
            passport = Passport(buffer)
            passports.append(passport)
            break
        else:
            splitted = line.split(" ")
            for item in splitted:
                key_value = item.split(":")
                buffer[key_value[0]] = key_value[1]

    valid_passwords = 0
    for passport in passports:
        if passport.valid():
            valid_passwords += 1
    return str(valid_passwords)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
