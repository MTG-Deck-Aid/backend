import requests
import json
from Mystic_Tuner_Backend.card import Card

def batch_validate(card_names: list[str]) -> list[list[str],int]:
    MAXBATCHSIZE = 75
    scryfall_url = "https://api.scryfall.com/cards/collection"
    headers = {
        'User-Agent': 'MysticTunerApp',
        'Accept': 'application/json'
    }
    card_groups = [card_names[i:i + MAXBATCHSIZE] for i in range(0, len(card_names),MAXBATCHSIZE)]
    for group in card_groups:
        data = {
            'identifiers': []
        }
        for card in card_names:
            data['identifiers'].append({"name": card})
        response = requests.post(scryfall_url, json=data, headers=headers)
        response_data = response.json()
        if response_data["not_found"] != []:
            return response_data["not_found"],0
    return [],1

def validate_commander(card_name: str) -> Card:
    if not card_name:
        return None
    scryfall_url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
    headers = {
        'User-Agent': 'MysticTunerApp',
        'Accept': 'application/json'
    }
    response = requests.get(scryfall_url, headers=headers)
    card_data = response.json()
    if response.status_code != 200:
        return None
    if card_data['legalities']['commander'] != 'legal':
        return None
    if ("Legendary Creature" not in card_data['type_line']) and ("can be your commander" not in card_data['oracle_text']):
        return None
    else:
        return Card.from_json(card_data)