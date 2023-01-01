from typing import Dict, List, Set, NamedTuple

class RawRecipe(NamedTuple):
    name: str
    ingredients: List[Dict[str, str]]
    garnishs: List[str]


class Ingredient(NamedTuple):
    name: str
    unit: int

class Recipe(NamedTuple):
    name: str
    ingredients: List[Ingredient]
    garnishs: List[str]
        
        
class IngredientSet(NamedTuple):
    ingredients: Set[str]
    garnishes: Set[str]
    mappings: Dict[str, str]