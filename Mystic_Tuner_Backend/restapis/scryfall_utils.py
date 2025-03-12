import requests
import json

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