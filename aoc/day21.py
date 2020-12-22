from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from typing import Optional, List, Set, Tuple

from aoc.utils import load_input


@dataclass(frozen=True)
class Food:
    ingredients: Tuple[str]
    allergens: Tuple[str]


def load_data():
    foods = []
    for line in load_input():
        ingredients_str, allergens_str = line.split("(contains")
        ingredients = tuple(ingredients_str.strip().split(" "))
        allergens = tuple(map(str.strip, allergens_str.replace(")", "").split(",")))
        food = Food(ingredients=ingredients, allergens=allergens)
        foods.append(food)
    return tuple(foods)


def part1():
    foods = load_data()
    allergen_to_ingredients = get_allergen_to_ingredients(foods)
    ingredients_that_might_contain_allergen = reduce(set.union, allergen_to_ingredients.values())
    return len([ingredient for food in foods for ingredient in food.ingredients if ingredient not in ingredients_that_might_contain_allergen])


def get_allergen_to_ingredients(foods):
    allergen_to_ingredients = {}
    allergen_to_foods = defaultdict(list)
    for food in foods:
        for allergen in food.allergens:
            allergen_to_foods[allergen].append(food)
    for allergen, foods_ in allergen_to_foods.items():
        allergen_to_ingredients[allergen] = reduce(set.intersection, [set(food.ingredients) for food in foods if
                                                                      allergen in food.allergens])
    any_changes = True
    while any_changes:
        any_changes = False
        for allergen, ingredients in allergen_to_ingredients.items():
            if len(ingredients) == 1:
                [ingredient] = ingredients
                for allergen_, ingredients_ in allergen_to_ingredients.items():
                    if allergen_ != allergen:
                        if ingredient in ingredients_:
                            any_changes = True
                            ingredients_.discard(ingredient)
    for food in foods:
        for allergen in food.allergens:
            ingredients = allergen_to_ingredients[allergen]
            assert any(ingredient in food.ingredients for ingredient in ingredients)

    return allergen_to_ingredients


def part2():
    foods = load_data()
    allergen_to_ingredients = get_allergen_to_ingredients(foods)
    definite_allergen_ingredients = [(allergen, list(ingredients)[0]) for allergen, ingredients in
                              allergen_to_ingredients.items() if len(ingredients) == 1]
    string = ",".join(map(lambda x: x[1], sorted(definite_allergen_ingredients, key=lambda x: x[0])))
    assert " " not in string
    return string



def main():
    print("part1", part1())
    print("part2", part2())


if __name__ == "__main__":
    main()
