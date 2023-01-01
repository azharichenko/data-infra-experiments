import argparse
import json
from enum import Enum, auto
from pathlib import Path
from typing import Dict, List, NamedTuple, Set, Optional

DATA_DIR = Path("..") / "data"
cocktail_data_file = DATA_DIR / "cocktails_raw.json"
ingredient_set_file = DATA_DIR / "ingredient.json"


class IngredientSet(NamedTuple):
    ingredients: Set[str]
    garnishes: Set[str]
    mappings: Dict[str, str]


class PerformOperation(Enum):
    ADD_INGREDIENT = auto()
    ADD_GARNISH = auto()
    ADD_INGREDIENT_AND_RENAME = auto()
    ADD_GARNISH_AND_RENAME = auto()


class Instruction(NamedTuple):
    op: PerformOperation
    data: str
    rename: Optional[str] = None


def read_cocktail_dataset() -> None:
    data: List[Dict]
    if not cocktail_data_file.exists():
        raise RuntimeError("Can't find file")

    with cocktail_data_file.open("r") as f:
        data = json.load(f)
    return data


def write_ingredient_set(data: IngredientSet) -> None:
    with ingredient_set_file.open("w") as f:
        json.dump(
            {
                "ingredients": list(data.ingredients),
                "garnishes": list(data.garnishes),
                "mappings": data.mappings,
            },
            f,
        )


def human_intervention(entry: Dict[str, str]) -> Instruction:
    """
    ai - add ingredient
    ag - add garnish
    ri {:str} - add ingredient but rename to {:str}
    rg {:str} - add garnish but rename to {:str}
    """
    instruction = None

    print("What to do with this ingredient entry?")
    print(entry)

    while instruction is None:
        user_input = input(">>> ")

        if user_input.startswith("ai"):
            instruction = Instruction(
                op=PerformOperation.ADD_INGREDIENT, data=entry["ingredient"]
            )
        elif user_input.startswith("ag"):
            instruction = Instruction(
                op=PerformOperation.ADD_GARNISH, data=entry["ingredient"]
            )
        elif user_input.startswith("ri"):
            ingredient_rename = " ".join(user_input.split(" ")[1:])
            instruction = Instruction(
                op=PerformOperation.ADD_INGREDIENT_AND_RENAME,
                data=entry["ingredient"],
                rename=ingredient_rename,
            )
        elif user_input.startswith("rg"):
            ingredient_rename = " ".join(user_input.split(" ")[1:])
            instruction = Instruction(
                op=PerformOperation.ADD_GARNISH_AND_RENAME,
                data=entry["ingredient"],
                rename=ingredient_rename,
            )
        else:
            print("command not recongized")

    return instruction


def gather_cleaned_ingredient_set() -> IngredientSet:
    recipe_set = read_cocktail_dataset()
    data = IngredientSet(set(), set(), {})

    for recipe in recipe_set:
        for entry in recipe["ingredients"]:
            entry["ingredient"] = entry["ingredient"].lower()

            if entry["ingredient"] in data.mappings:
                entry["ingredient"] = data.mappings[entry["ingredient"]]

            if (
                entry["ingredient"] not in data.ingredients
                and entry["ingredient"] not in data.garnishes
            ):
                instruction = human_intervention(entry)

                if instruction.op == PerformOperation.ADD_INGREDIENT:
                    data.ingredients.add(instruction.data)

                if instruction.op == PerformOperation.ADD_INGREDIENT_AND_RENAME:
                    data.mappings[instruction.data] = instruction.rename
                    data.ingredients.add(instruction.rename)

                if instruction.op == PerformOperation.ADD_GARNISH:
                    data.garnishes.add(instruction.data)

                if instruction.op == PerformOperation.ADD_GARNISH_AND_RENAME:
                    data.mappings[instruction.data] = instruction.rename
                    data.garnishes.add(instruction.rename)
    return data


if __name__ == "__main__":
    # TODO: Add arg for using known ingredient list to avoid redoing everything
    ingredient_set = gather_cleaned_ingredient_set()
    write_ingredient_set(ingredient_set)
