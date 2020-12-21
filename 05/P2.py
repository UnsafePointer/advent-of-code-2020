from typing import List


def solve() -> str:
    file = open("input.txt", "r")
    seat_ids: List[int] = []
    for line in file:
        row_bsp = line[:7]
        row_bsp = row_bsp.replace("F", "0")
        row_bsp = row_bsp.replace("B", "1")
        row = int(row_bsp, 2)
        column_bsp = line[7:10]
        column_bsp = column_bsp.replace("L", "0")
        column_bsp = column_bsp.replace("R", "1")
        column = int(column_bsp, 2)
        seat_id = row * 8 + column
        seat_ids.append(seat_id)
    seat_ids.sort()
    for index, seat_id in enumerate(seat_ids):
        if seat_id + 1 != seat_ids[index + 1]:
            return str(seat_id + 1)
    return "Not found"


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
