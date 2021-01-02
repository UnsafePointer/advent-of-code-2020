from typing import Dict, List


class Node:
    value = None
    next_node = None


def solve() -> str:
    file = open("input.txt", "r")
    line = file.readline()

    first_node = None
    previous_node = None
    search: Dict[int, Node] = {}
    for character in list(line.strip()):
        number = int(character)
        node = Node()
        node.value = number
        search[number] = node
        if not first_node:
            first_node = node
        else:
            previous_node.next_node = node
        previous_node = node
    for input_number in range(10, 1_000_000 + 1):
        node = Node()
        node.value = input_number
        search[input_number] = node
        previous_node.next_node = node
        previous_node = node
    previous_node.next_node = first_node
    max_number = 1_000_000

    turns = 10000000
    current_node = first_node
    while turns > 0:
        removed_numbers: List[int] = []
        next_three_nodes_iter_start = current_node.next_node
        next_three_nodes_iter = current_node.next_node
        next_three_nodes_iter_end: Node
        for index in range(0, 3):
            removed_numbers.append(next_three_nodes_iter.value)
            if index == 2:
                next_three_nodes_iter_end = next_three_nodes_iter
            next_three_nodes_iter = next_three_nodes_iter.next_node
        current_node.next_node = next_three_nodes_iter
        destination_number = current_node.value
        while True:
            destination_number -= 1
            if destination_number <= 0:
                destination_number = max_number
            if destination_number not in removed_numbers:
                break
        destination_node = search[destination_number]
        destination_node_old_next_node = destination_node.next_node
        destination_node.next_node = next_three_nodes_iter_start
        next_three_nodes_iter_end.next_node = destination_node_old_next_node
        current_node = current_node.next_node
        turns -= 1
    node_1 = search[1]
    solution = node_1.next_node.value * node_1.next_node.next_node.value
    return str(solution)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
