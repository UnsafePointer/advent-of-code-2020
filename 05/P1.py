from sys import maxsize


def solve() -> str:
    file = open("input.txt", "r")
    highest_seat_id = -maxsize
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
        if seat_id > highest_seat_id:
            highest_seat_id = seat_id
    return str(highest_seat_id)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
