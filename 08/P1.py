from typing import Set


def solve() -> str:
    file = open("input.txt", "r")
    lines = file.readlines()
    pc = 0
    acc = 0
    executed: Set[int] = set()
    while True:
        if pc in executed:
            break
        line = lines[pc]
        executed.add(pc)
        splitted = line[:-1].split()
        opcode = splitted[0]
        arg = int(splitted[1])
        if opcode == "nop":
            pc += 1
        elif opcode == "acc":
            acc += arg
            pc += 1
        elif opcode == "jmp":
            pc += arg
    return str(acc)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
