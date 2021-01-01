from typing import Dict, Set


def solve() -> str:
    file = open("input.txt", "r")
    alergens: Dict[str, Set[str]] = {}
    ingredients: Set[str] = set()
    ingredients_ocurrences: Dict[str, int] = {}
    for line in file:
        splitted = line.strip().split("(contains")
        alergen_names = splitted[1][:-1].split(",")
        ingredients_for_food = set(splitted[0].strip().split(" "))
        for ingredient in ingredients_for_food:
            ocurrences = ingredients_ocurrences.get(ingredient, 0)
            ocurrences += 1
            ingredients_ocurrences[ingredient] = ocurrences
        ingredients.update(ingredients_for_food)
        for alergen_name in alergen_names:
            current_ingredients = alergens.get(alergen_name.strip(), set())
            if not current_ingredients:
                current_ingredients = ingredients_for_food
            else:
                current_ingredients = current_ingredients.intersection(
                    ingredients_for_food
                )
            alergens[alergen_name.strip()] = current_ingredients
    ingredients_with_alergens: Set[str] = set()
    for alergen in alergens:
        ingredients_with_alergens.update(alergens[alergen])
    total = 0
    for ingredient in ingredients.difference(ingredients_with_alergens):
        total += ingredients_ocurrences[ingredient]
    return str(total)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
