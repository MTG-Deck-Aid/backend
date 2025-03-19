from Mystic_Tuner_Backend.card import Card
from django.http import JsonResponse
import requests
import time
import json
import urllib.parse

def encodeURIName(card_name: str) -> str:
    return urllib.parse.quote(card_name)

class ScryFallEngine:
    """
    Uses Scryfall API to find Magic The Gathering (MTG) card information
    """

    def __init__(self):
        self
        

    def search_card(self, card_name: str, include_image = False) -> Card:
        """
        Search for a card by name.

        params:
            card_name: str - The name of the card to search for.
        returns:
            dict - The card information as a dictionary.
        """
        time.sleep(0.05)
        if not card_name:
            return None
        uriName = encodeURIName(card_name)
        scryfall_url = f"https://api.scryfall.com/cards/named?fuzzy={uriName}"
        headers = {
            'User-Agent': 'MysticTunerApp',
            'Accept': 'application/json'
        }
        response = requests.get(scryfall_url, headers=headers)
        card_data = response.json()
        if response.status_code != 200:
            return None
        card: Card = Card.from_json(card_data)

        if include_image:
            card.image_url = self.get_image_links(card_name)

        return card

    def get_image_links(self, card_name: str) -> dict:
        """
        Get the image links for a card by name.

        params:
            card_name: str - The name of the card to search for.
        returns:
            dict - The image links as a dictionary.
        """
        time.sleep(0.05)
        if not card_name:
            return None
        uriName = encodeURIName(card_name)
        scryfall_url = f"https://api.scryfall.com/cards/named?fuzzy={uriName}"
        headers = {
            'User-Agent': 'MysticTunerApp',
            'Accept': 'application/json'
        }
        response = requests.get(scryfall_url, headers=headers)
        card_data = response.json()
        if response.status_code != 200:
            return None
        keys_to_drop = ["png", "border_crop"]
        response_dict = card_data["image_uris"]
        for key in keys_to_drop:
            if key in response_dict:
                del response_dict[key]
        return response_dict
    
    @staticmethod
    def batch_validate(card_names: list[str]) -> list[list[str],int]:
        MAXBATCHSIZE = 37
        scryfall_url = "https://api.scryfall.com/cards/collection"
        headers = {
            'User-Agent': 'MysticTunerApp',
            'Accept': 'application/json'
        }
        card_groups = [card_names[i:i + MAXBATCHSIZE] for i in range(0, len(card_names),MAXBATCHSIZE)]
        invalidNames = []
        potentialInvalidNames = []
        for group in card_groups:
            data = {
                'identifiers': []
            }
            for card in group:
                if "/" in card:
                    potentialInvalidNames.append(card)
                    split_card = card.split("/")
                    data['identifiers'].append({"name": split_card[0]})
                    data['identifiers'].append({"name": split_card[len(split_card)-1]})
                else:
                    data['identifiers'].append({"name"})
            response = requests.post(scryfall_url, json=data, headers=headers)
            response_data = response.json()
            if response_data["not_found"] != []:
                for dict in response_data["not_found"]:
                    invalidNames.append(dict["name"])
        if invalidNames != []:
            for name in invalidNames:
                for match in potentialInvalidNames:
                    if match.find(name) != -1:
                        invalidNames.remove(name)
                        invalidNames.append(match)
            return invalidNames,0
        else:
            return invalidNames,1

    @staticmethod
    def validate_commander(card_name: str) -> Card:
        if not card_name:
            return None
        uriName = encodeURIName(card_name)
        scryfall_url = f"https://api.scryfall.com/cards/named?fuzzy={uriName}"
        headers = {
            'User-Agent': 'MysticTunerApp',
            'Accept': 'application/json'
        }
        response = requests.get(scryfall_url, headers=headers)
        card_data = response.json()
        if response.status_code != 200:
            print("Error: Commander Card not found")
            return None
        if card_data['legalities']['commander'] != 'legal':
            return None
        if ("Legendary Creature" not in card_data['type_line']) and ("can be your commander" not in card_data['oracle_text']):
            return None
        multisided = card_data.get('card_faces', None)
        if multisided and len(multisided) > 1:
            return None
        else:
            if card_data['name'] == "Invasion of Fiora // Marchesa, Resolute Monarch":
                print(card_data)
            return Card.from_json(card_data)
        
    @staticmethod
    def autocomplete(card_name: str) -> list[str]:
        """
        Search for potential cards
        """

        if not card_name:
            return []
        uriName = encodeURIName(card_name)
        scryfall_url = f"https://api.scryfall.com/cards/autocomplete?q={uriName}"
        headers = {
            'User-Agent': 'MysticTunerApp',
            'Accept': 'application/json'
        }
        response = requests.get(scryfall_url, headers=headers)
        card_list: list[str] = response.json()["data"]
        if response.status_code != 200:
            return None
        return card_list
    


    
    
if __name__ == "__main__":
    # Example Usage
    engine = ScryFallEngine()
    card = engine.search_card('Black Lotus')
    print(card.__str__())
    
        
