from os import linesep
from typing import Dict, List, Tuple, Set
from copy import deepcopy


def is_number_valid_in_ranges(number: int, ranges: List[range]) -> bool:
    for field_range in ranges:
        if number in field_range:
            return True
    return False


cache: Dict[Tuple[int, str], bool] = {}


def are_tickets_valid_for_ranges_at_position(
    tickets: List[List[int]], position: int, field_name: str, ranges: List[range]
) -> bool:
    key = (position, field_name)
    if key in cache:
        return cache[key]
    for ticket in tickets:
        field_number = ticket[position]
        if not is_number_valid_in_ranges(field_number, ranges):
            cache[key] = False
            return False
    cache[key] = True
    return True


def sorted_fields(
    fields: Dict[str, List[range]], tickets: List[List[int]]
) -> List[str]:

    positions_for_field_names: Dict[str, List[int]] = {}
    for position in range(len(fields)):
        for field_name in fields:
            if are_tickets_valid_for_ranges_at_position(
                tickets, position, field_name, fields[field_name]
            ):
                positions = positions_for_field_names.get(field_name, [])
                positions.append(position)
                positions_for_field_names[field_name] = positions

    number_of_positions_for_field_names = {
        (key, len(value)) for (key, value) in positions_for_field_names.items()
    }

    fields_sorted_by_number_of_positions = sorted(
        number_of_positions_for_field_names, key=lambda tuple: tuple[1]
    )

    final_positions: List[str] = [""] * 20
    positions_so_far: Set[int] = set()
    for (field, _) in fields_sorted_by_number_of_positions:
        positions_for_field = positions_for_field_names[field]
        position_for_field = list(
            set(positions_for_field).difference(positions_so_far)
        )[0]
        final_positions[position_for_field] = field
        positions_so_far.add(position_for_field)

    return final_positions


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

    def validate_tiket(ticket: List[int]) -> bool:
        for number in ticket:
            if not validate_number(number):
                return False
        return True

    valid_tickets: List[List[int]] = []
    for nearby_ticket in nearby_tickets:
        if validate_tiket(nearby_ticket):
            valid_tickets.append(nearby_ticket)

    valid_tickets.append(ticket_numbers)
    fields_order = sorted_fields(ranges, valid_tickets)

    solution = 1
    for index, value in enumerate(fields_order):
        if value.startswith("departure"):
            solution *= ticket_numbers[index]
    return str(solution)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
