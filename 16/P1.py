from os import linesep
from typing import Dict, List


def solve() -> str:
    file = open("input.txt", "r")

    ranges: Dict[str, List[range]] = {}

    line = file.readline()
    while line != linesep:
        splitted = line.split(":")
        ranges_splitted = splitted[1].strip().split(" or ")
        ranges_for_fields: List[range] = []
        for range_splitted in ranges_splitted:
            numbers = range_splitted.split("-")
            field_range = range(int(numbers[0]), int(numbers[1]) + 1)
            ranges_for_fields.append(field_range)
        ranges[splitted[0]] = ranges_for_fields
        line = file.readline()

    ticket_numbers: List[int]
    line = file.readline()
    while line != linesep:
        if line.strip() == "your ticket:":
            line = file.readline()
            continue
        ticket_numbers = [int(x) for x in line.strip().split(",")]
        line = file.readline()

    nearby_tickets: List[List[int]] = []
    line = file.readline()
    while line != linesep:
        if line.strip() == "nearby tickets:":
            line = file.readline()
            continue
        if line == "":
            break
        nearby_ticket = [int(x) for x in line.strip().split(",")]
        nearby_tickets.append(nearby_ticket)
        line = file.readline()

    def validate_number(number: int) -> bool:
        for field in ranges:
            field_ranges = ranges[field]
            for field_range in field_ranges:
                if number in field_range:
                    return True
        return False

    invalid_numbers_sum = 0
    for nearby_ticket in nearby_tickets:
        for number in nearby_ticket:
            if not validate_number(number):
                invalid_numbers_sum += number
    return str(invalid_numbers_sum)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
