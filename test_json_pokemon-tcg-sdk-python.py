import pytest
from pokemontcgsdk import *
from markdown_writter import *
from pokemon_cards.card_extended import CardExtented
import os
from datetime import datetime

from utils import *

pokemon_tcg_data_folder = "pokemon_cards/pokemon-tcg-data-master"

@pytest.fixture(scope="module")
def all_cards():
    cards:list[CardExtented] = load_json_cards(os.listdir(f"{pokemon_tcg_data_folder}/cards/en"))
    yield cards

@pytest.fixture(scope="module")
def cards_base123():
    cards:list[CardExtented] = load_json_cards(["base1.json", "base2.json", "base3.json"])
    yield cards

@pytest.fixture(scope="module")
def sets():
    sets:list[Set] = load_json_sets()
    yield sets



def test_print_pokemons_that_can_elvolve_or_are_evolded(doc, cards_base123):
    cards = cards_base123
    
    evolvings_cards = [card for card in cards 
        if card.supertype == "Pokémon" and (
        card.evolvesFrom is not None 
        or card.name in [poké.evolvesFrom for poké in cards])
    ]
    sorted_evolvings_cards:list[CardExtented] = sorted(
        evolvings_cards, 
        key=lambda x : (x.nationalPokedexNumbers[0]), 
        reverse=False
    )

    doc.log(f"Limit to 9 first cards")
    for i in range(0,9):
            card = sorted_evolvings_cards[i]
            doc.log("<br/>", "\n") if "Basic" in card.subtypes else None
            doc.log(doc.img(card.images.small)," ")


def test_cardExtended_object_contain_level_attribute(doc, cards_base123):
    card = cards_base123[0]
    doc.log(f"{card.name} with id '{card.id}' is level '{card.level}'")
    assert card.level == "42"

def test_cardExtended_object_must_contain_set_id_attribute(doc, cards_base123):
    card = cards_base123[0]
    doc.log(f"{card.name} with id '{card.id}' have  set_id '{card.set_id}'")
    assert card.set_id == "base1"


def test_cardExtended_object_must_contain_set_object_with_values(doc, cards_base123):
    card = cards_base123[0]

    doc.log(doc.img(card.images.small))
    doc.log(f"Release date of {card.name} from set '{card.set.name}' is {card.set.releaseDate}")
    assert card.set.releaseDate == "1999/01/09"


def test_given_ponytas_sorted_by_counting_same_attacks_then_the_3_first_ponytas_should_have_same_attacks(all_cards, sets:list[Set], doc):
    filtered_cards:list[CardExtented] = [card for card in all_cards if "ponyta" in card.name.lower()]

    sorted_filtered_cards:list[CardExtented] = sorted(
            filtered_cards, 
            key=lambda x : (
                [card.attacks for card in filtered_cards].count(x.attacks),
                [attack.name for attack in x.attacks],
            ), 
            reverse=True
        )
    
    doc.log(" ".join([doc.img(card.images.small) for card in sorted_filtered_cards]))


    assert sorted_filtered_cards[0].attacks \
        == sorted_filtered_cards[1].attacks \
        == sorted_filtered_cards[2].attacks

def test_print_card_with_no_attack(all_cards, doc):

    creature_cards_without_attacks = [
        card for card in all_cards 
        if card.supertype == "Pokémon" 
        and len(card.attacks) == 0
    ]
    print (f"Number of creature cards without attacks: {len(creature_cards_without_attacks)}")
    doc_log_cards(doc, creature_cards_without_attacks)


def test_print_all_cards_with_the_maximal_number_of_attacks(all_cards, doc):
    doc.log("V union cards are not included")
    non_v_union_cards = [card for card in all_cards if "V-UNION" not in card.subtypes]
    max_attacks_count = max([len(card.attacks) for card in non_v_union_cards])
    cards_with_max_attacks = [card for card in non_v_union_cards if len(card.attacks) == max_attacks_count]
    
    doc_log_cards(doc, cards_with_max_attacks)


def test_print_all_V_UNION_cards(all_cards, doc):
    v_union_cards = [card for card in all_cards if "V-UNION" in card.subtypes]

    v_union_dict = {}
    for card in v_union_cards:
        if card.name not in v_union_dict:
            v_union_dict[card.name] = []
        v_union_dict[card.name].append(card)

    for name, cards in v_union_dict.items():
        doc.log(f"V-Union Name: {name}")
        for i, card in enumerate(cards):
            doc.log(doc.img(card.images.small), '\n\n' if i % 2 == 0 else '')


def test_print_all_pikachu_cards(all_cards, doc):
    pikachu_cards = [card for card in all_cards if "pikachu" in card.name.lower()]
    
    sorted_pikachu_cards = sorted(
        pikachu_cards, 
        key=lambda x : datetime.strptime(x.set.releaseDate, "%Y/%m/%d")
    )

    doc.log(f"There is %s pikachu cards" % len(sorted_pikachu_cards))
    doc.log("First one is")
    doc_log_card(doc, sorted_pikachu_cards[0])
    doc.log("release the %s" % sorted_pikachu_cards[0].set.releaseDate," ")
    doc.log("Last one is ")
    doc_log_card(doc, sorted_pikachu_cards[-1])
    doc.log("release the %s" % sorted_pikachu_cards[-1].set.releaseDate," ")


def test_print_all_EX_V_GX_cards(all_cards, doc):
    ex_cards = [card for card in all_cards if any(elem in ["EX", "V", "GX"] for elem in card.subtypes) and len(card.nationalPokedexNumbers) ==1]
    sorted_ex_cards = sorted(
        ex_cards, 
        key=lambda x : x.nationalPokedexNumbers[0]
    )
    doc_log_cards(doc, sorted_ex_cards[:10])

def test_print_all_artist_Yuka_Morii_cards(all_cards, doc):
    artist_cards = [card for card in all_cards if card.artist == "Yuka Morii"]
    sorted_artist_cards = sorted(
        artist_cards, 
        key=lambda x : x.nationalPokedexNumbers[0]
    )
    doc_log_cards(doc, sorted_artist_cards)

@pytest.mark.skip(reason="to much cards")
def test_print_first_card_of_each_national_pokedex_number(all_cards, doc):
    cards_with_national_pokedex_numbers = [card for card in all_cards if card.nationalPokedexNumbers is not None and len(card.nationalPokedexNumbers) == 1]
    cards_sorted_by_national_pokedex_numbers = sorted(
        cards_with_national_pokedex_numbers, 
        key=lambda x : x.nationalPokedexNumbers[0]
    )

    one_of_each_dict = {}
    for card in cards_sorted_by_national_pokedex_numbers:
        if card.nationalPokedexNumbers[0] not in one_of_each_dict:
            one_of_each_dict[card.nationalPokedexNumbers[0]] = card

    for national_pokedex_number, card in one_of_each_dict.items():
        #doc.log(f"National Pokedex Number: {national_pokedex_number}")
        doc_log_card(doc, card)

############## UTILITIES ##############

def doc_log_cards(doc, cards):
    doc.log("")
    for card in cards:
        doc_log_card(doc, card)

def doc_log_card(doc, card):
    doc.log(doc.img(card.images.small)," ")