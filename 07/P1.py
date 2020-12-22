from typing import Dict, List, Set


def find_all_containers(graph: Dict[str, List[str]], to_find: str) -> Set[str]:
    if to_find not in graph:
        return set()
    containers = graph[to_find]
    parent_containers: Set[str] = set()
    for container in containers:
        parent_containers = parent_containers.union(
            find_all_containers(graph, container)
        )
    return set(containers).union(parent_containers)


def solve() -> str:
    file = open("input.txt", "r")

    # contained_by -> container
    graph: Dict[str, List[str]] = {}
    for line in file:
        sentences = line[:-2].split("contain ")
        container = " ".join(sentences[0].split()[:-1])
        contained_by = sentences[1].split(", ")
        if contained_by[0] == "no other bags":
            continue
        for bag in contained_by:
            key = " ".join(bag.split(" ", 1)[1].split()[:-1])
            containers = graph.get(key, [])
            containers.append(container)
            graph[key] = containers

    result = find_all_containers(graph, "shiny gold")
    return str(len(result))


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
