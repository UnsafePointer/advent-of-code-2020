from typing import Dict, Set, List, Tuple


def attempt_to_solve(
    alergens: Dict[str, Set[str]], single_out_alergens: List[Tuple[str, Set[str]]]
) -> List[Tuple[str, Set[str]]]:
    if len(alergens) == len(single_out_alergens):
        return single_out_alergens

    for alergen in alergens:
        ingredients_for_alergen = alergens[alergen]
        ingredients_for_alergen_difference = ingredients_for_alergen
        for single_out_alergen in single_out_alergens:
            ingredients_for_alergen_difference = (
                ingredients_for_alergen_difference.difference(single_out_alergen[1])
            )
            if len(ingredients_for_alergen_difference) == 1 and alergen not in [
                x[0] for x in single_out_alergens
            ]:
                single_out_alergens.append(
                    (alergen, ingredients_for_alergen_difference)
                )
                return attempt_to_solve(alergens, single_out_alergens)

    assert False
    return []


def solve() -> str:
    file = open("input.txt", "r")
    alergens: Dict[str, Set[str]] = {}
    for line in file:
        splitted = line.strip().split("(contains")
        alergen_names = splitted[1][:-1].split(",")
        ingredients_for_food = set(splitted[0].strip().split(" "))
        for alergen_name in alergen_names:
            current_ingredients = alergens.get(alergen_name.strip(), set())
            if not current_ingredients:
                current_ingredients = ingredients_for_food
            else:
                current_ingredients = current_ingredients.intersection(
                    ingredients_for_food
                )
            alergens[alergen_name.strip()] = current_ingredients
    single_out_alergens: List[Tuple[str, Set[str]]] = []
    for alergen in alergens:
        ingredients_for_alergen = alergens[alergen]
        if len(ingredients_for_alergen) == 1:
            single_out_alergens.append((alergen, alergens[alergen]))
    result = attempt_to_solve(alergens, single_out_alergens)
    result.sort(key=lambda x: x[0])
    ingredients = [next(iter(x[1])) for x in result]
    return ",".join(ingredients)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
