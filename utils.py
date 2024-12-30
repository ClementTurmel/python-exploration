from pokemontcgsdk import *
from markdown_writter import *
from pokemon_cards.card_extended import CardExtented
from typing import List
import json
from dacite import from_dict

pokemon_tcg_data_folder = "pokemon_cards/pokemon-tcg-data-master"

def load_json_cards(set_name:List):
    sets:list[Set] = load_json_sets()
    cards:list[CardExtented] = []
    for set_name in set_name:
        with open(f"{pokemon_tcg_data_folder}/cards/en/{set_name}", mode="r", encoding="utf-8") as file:
                json_data = json.load(file)
                transformed_json_data = [CardExtented.transform(i) for i in json_data]
                
                for item in transformed_json_data:
                    card = from_dict(CardExtented, item)
                    card.set = get_set(card.set_id, sets)
                    cards.append(card)

    return cards

def load_json_sets():
    sets:list = []
    with open(f"{pokemon_tcg_data_folder}/sets/en.json", mode="r", encoding="utf-8") as file:
            json_data = json.load(file)
            sets.extend([from_dict(Set, item) for item in json_data])
    
    return sets

def get_set(set_id:str, sets:List[Set]):
    return [set for set in sets if set.id == set_id][0]
