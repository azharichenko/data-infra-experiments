import json
from string import ascii_lowercase
from typing import Dict, List, NamedTuple, Generator
from pathlib import Path

import requests
from tqdm import tqdm

DATA_DIR = Path() / "data"
BASE_URL = "https://www.thecocktaildb.com/api/json/v2/9973533/search.php?f={}"


def _parse_cocktaildb_drink(data: Dict) -> Dict:
    ingredients = [
        {
            "ingredient": data["strIngredient{}".format(i)],
            "measurement": data["strMeasure{}".format(i)],
        }
        for i in range(1, 16)
        if data["strIngredient{}".format(i)] is not None
    ]
    return {
        "name": data["strDrink"],
        "category": data["strCategory"],
        "glass": data["strGlass"],
        "ingredients": ingredients,
    }


def get_cockails() -> Generator[None, None, None]:
    cocktail_data_file = DATA_DIR / "cocktails.json"
    with cocktail_data_file.open("w", encoding="utf-8") as f:
        f.write("[")
        for i, letter in tqdm(enumerate(ascii_lowercase), total=26):
            resp = requests.get(BASE_URL.format(letter))
            assert resp.status_code == 200
            data = resp.json()
            parsed_data: List[Dict]
            if data["drinks"] is None:
                continue
            if i != 0:
                f.write(",")
            parsed_data = [_parse_cocktaildb_drink(drink) for drink in data["drinks"] if drink["strAlcoholic"] == "Alcoholic"]
            parsed_data = json.dumps(parsed_data, indent=4, ensure_ascii=False)[1:-1]
            f.write(parsed_data)
        f.write("]")

if __name__ == "__main__":
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()
    get_cockails()
