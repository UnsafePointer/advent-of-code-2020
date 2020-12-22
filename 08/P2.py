from typing import List, Set


def attempt_to_solve(
    program: List[str], pc: int, acc: int, executed: Set[int], can_modify: bool
) -> int:
    if pc == len(program):
        return acc
    if pc in executed:
        return -1

    line = program[pc]
    splitted = line.strip().split()
    opcode = splitted[0]
    arg = int(splitted[1])

    if opcode == "nop":
        if can_modify:
            program[pc] = " ".join(["jmp", str(arg)])
            previous_executed = executed.copy()
            result = attempt_to_solve(program, pc, acc, executed, False)
            if result > 0:
                return result
            else:
                executed = previous_executed
                program[pc] = " ".join(splitted)
        executed.add(pc)
        pc += 1
    elif opcode == "acc":
        acc += arg
        executed.add(pc)
        pc += 1
    elif opcode == "jmp":
        if can_modify:
            program[pc] = " ".join(["nop", str(arg)])
            previous_executed = executed.copy()
            result = attempt_to_solve(program, pc, acc, executed, False)
            if result > 0:
                return result
            else:
                executed = previous_executed
                program[pc] = " ".join(splitted)
        executed.add(pc)
        pc += arg

    return attempt_to_solve(program, pc, acc, executed, can_modify)


def solve() -> str:
    file = open("input.txt", "r")
    program = file.readlines()
    pc = 0
    acc = 0
    executed: Set[int] = set()
    result = attempt_to_solve(program, pc, acc, executed, True)
    return str(result)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
