from os import linesep
from typing import Dict, List
from dataclasses import dataclass, field
import re


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
    year_pattern: str = r"^[0-9]{4}$"
    height_pattern: str = r"^([0-9]+)(cm|in)$"
    hair_color_pattern: str = r"^#[0-9a-f]{6}$"
    eye_color_pattern: str = r"\b(amb|blu|brn|gry|grn|hzl|oth)\b"
    passport_id_pattern: str = r"^[0-9]{9}$"

    def valid(self) -> bool:
        for field in self.required_fields:
            if not field in self.data:
                return False
            else:
                field_data = self.data[field]
                if field == "byr":
                    result = re.search(self.year_pattern, field_data)
                    if not result:
                        return False
                    year = int(field_data)
                    if year < 1920 or year > 2002:
                        return False
                elif field == "iyr":
                    result = re.search(self.year_pattern, field_data)
                    if not result:
                        return False
                    year = int(field_data)
                    if year < 2010 or year > 2020:
                        return False
                elif field == "eyr":
                    result = re.search(self.year_pattern, field_data)
                    if not result:
                        return False
                    year = int(field_data)
                    if year < 2020 or year > 2030:
                        return False
                elif field == "hgt":
                    result = re.search(self.height_pattern, field_data)
                    if not result:
                        return False
                    value = int(result.group(1))
                    unit = result.group(2)
                    if unit == "cm":
                        if value < 150 or value > 193:
                            return False
                    elif unit == "in":
                        if value < 59 or value > 76:
                            return False
                elif field == "hcl":
                    result = re.search(self.hair_color_pattern, field_data)
                    if not result:
                        return False
                elif field == "ecl":
                    result = re.search(self.eye_color_pattern, field_data)
                    if not result:
                        return False
                elif field == "pid":
                    result = re.search(self.passport_id_pattern, field_data)
                    if not result:
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
            splitted = line[:-1].split(" ")
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
