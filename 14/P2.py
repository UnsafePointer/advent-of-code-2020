from dataclasses import dataclass, field
from re import search
from typing import Dict, List


@dataclass
class Bitmask:
    mask: str

    def mask_address(self, address: int) -> List[int]:
        mask_value = list(self.mask)
        address_value = list(bin(address)[2:])
        masked_value: List[str] = []
        indices = []
        while mask_value:
            mask_bit = mask_value.pop()
            address_bit = "0"
            if address_value:
                address_bit = address_value.pop()
            masked_bit: str
            if mask_bit == "0":
                masked_bit = address_bit
            elif mask_bit == "1":
                masked_bit = "1"
            elif mask_bit == "X":
                masked_bit = "X"
                indices.append(len(mask_value))
            masked_value.insert(0, masked_bit)

        addresses: List[int] = []
        if len(indices) == 0:
            addresses.append(int("".join(masked_value), base=2))
            return addresses

        for number in range(0, pow(2, len(indices))):
            binary_number = bin(number)[2:]
            preleading = len(indices) - len(binary_number)
            binary_number_w_preleading = ["0"] * preleading
            binary_number_w_preleading.extend(binary_number)
            masked_value_copy = masked_value.copy()
            indices_copy = indices.copy()
            while binary_number_w_preleading:
                index = indices_copy.pop()
                masked_value_copy[index] = binary_number_w_preleading.pop()
            addresses.append(int("".join(masked_value_copy), base=2))
        return addresses


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
                memory_addresses: List[int] = current_mask.mask_address(
                    int(memory_address)
                )
                for address in memory_addresses:
                    memory[address] = int(argument)
    total = 0
    for key in memory:
        total += memory[key]
    return str(total)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
