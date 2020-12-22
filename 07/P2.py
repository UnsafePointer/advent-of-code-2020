from typing import Dict, List, Set, Tuple


def find_all_within(graph: Dict[str, List[Tuple[str, int]]], to_find: str) -> int:
    if to_find not in graph:
        return 0
    contained = graph[to_find]
    children_contained = 0
    for container in contained:
        container_total = container[1] * find_all_within(graph, container[0])
        children_contained += container[1] + container_total
    return children_contained


def solve() -> str:
    file = open("input.txt", "r")

    # container -> [contained, num]
    graph: Dict[str, List[Tuple[str, int]]] = {}
    for line in file:
        sentences = line[:-2].split("contain ")
        container = " ".join(sentences[0].split()[:-1])
        contained = sentences[1].split(", ")
        if contained[0] == "no other bags":
            continue
        for bag in contained:
            splitted = bag.split(" ", 1)
            num = splitted[0]
            color = " ".join(splitted[1].split()[:-1])
            containers = graph.get(container, [])
            containers.append((color, int(num)))
            graph[container] = containers

    result = find_all_within(graph, "shiny gold")
    return str(result)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
