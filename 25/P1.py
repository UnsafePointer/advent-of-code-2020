def find_secret_loop_size(public_key: int) -> int:
    loop = 0
    subject_number = 7
    value = subject_number
    while True:
        loop += 1
        value *= subject_number
        value %= 20201227
        if value == public_key:
            break
    return loop


def get_encryption_key(public_key: int, loop_size: int) -> int:
    subject_number = public_key
    value = subject_number
    for _ in range(0, loop_size):
        value *= subject_number
        value %= 20201227
    return value


def solve() -> str:
    file = open("input.txt", "r")
    card_public_key = 0
    door_public_key = 0
    for line in file:
        if card_public_key == 0:
            card_public_key = int(line.strip())
        else:
            door_public_key = int(line.strip())
    loop_size = find_secret_loop_size(card_public_key)
    encryption_key = get_encryption_key(door_public_key, loop_size)
    return str(encryption_key)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
