from dataclasses import dataclass, field
from re import search
from typing import Dict


@dataclass
class Bitmask:
    mask: str
    and_mask: int = field(init=False)
    or_mask: int = field(init=False)

    def __post_init__(self) -> None:
        and_mask_str = self.mask.replace("1", "0").replace("X", "1")
        or_mask_str = self.mask.replace("X", "0")
        self.and_mask = int(and_mask_str, base=2)
        self.or_mask = int(or_mask_str, base=2)

    def mask_value(self, value: int) -> int:
        to_keep = value & self.and_mask
        new_value = to_keep | self.or_mask
        return new_value


def solve() -> str:
    file = open("input.txt")
    current_mask: Bitmask
    memory_address_pattern = r"^mem\[([0-9]+)\]$"
    memory: Dict[int, int] = {}
    for line in file:
        splitted = line[:-1].split(" = ")
        operation = splitted[0]
        argument = splitted[1]
        if operation == "mask":
            current_mask = Bitmask(argument)
        else:
            result = search(memory_address_pattern, operation)
            if result:
                memory_address = result.group(1)
                memory[int(memory_address)] = current_mask.mask_value(int(argument))
    total = 0
    for key in memory:
        total += memory[key]
    return str(total)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
