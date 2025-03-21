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
            include_image : bool - wether or not a image should be retrieved
        returns:
            dict - The card information as a dictionary.
        """
        #ensure requests aren't sent to scryfall too frequently
        time.sleep(0.05)
        #ensure there is a card name passed
        if not card_name:
            return None
        #edit card name to adhere to standard uri conventions
        uriName = encodeURIName(card_name)
        scryfall_url = f"https://api.scryfall.com/cards/named?fuzzy={uriName}"
        headers = {
            'User-Agent': 'MysticTunerApp',
            'Accept': 'application/json'
        }
        #request card information
        response = requests.get(scryfall_url, headers=headers)
        card_data = response.json()
        #check response status
        if response.status_code != 200:
            return None
        card: Card = Card.from_json(card_data)

        #include images if requested
        if include_image:
            card.image_url = self.get_image_links(card_name)

        #return the retrieved card
        return card

    def get_image_links(self, card_name: str) -> dict:
        """
        Get the image links for a card by name.

        params:
            card_name: str - The name of the card to search for.
        returns:
            dict - The image links as a dictionary.
        """
        #ensure requests aren't sent to scryfall too frequently
        time.sleep(0.05)
        #ensure there is a card name passed
        if not card_name:
            return None
        #edit card name to adhere to standard uri conventions
        uriName = encodeURIName(card_name)
        scryfall_url = f"https://api.scryfall.com/cards/named?fuzzy={uriName}"
        headers = {
            'User-Agent': 'MysticTunerApp',
            'Accept': 'application/json'
        }
        #request card image information
        response = requests.get(scryfall_url, headers=headers)
        card_data = response.json()
        #check response status
        if response.status_code != 200:
            return None
        #edit image urls provided
        keys_to_drop = ["png", "border_crop"]
        response_dict = card_data["image_uris"]
        for key in keys_to_drop:
            if key in response_dict:
                del response_dict[key]
        #return retrieved urls
        return response_dict
    
    @staticmethod
    def batch_validate(card_names: list[str]) -> list[list[str],int]:
        """
        Confirms that all cards provided are valid mtg cards.

        params:
            card_name: list[str] - list of card names that need to be validated.
        returns:
           list[list[str],int] - list of card names that were invalid and bool indicating wether or not all cards were validated.
        """
        #ensure that limit of 75 can never be surpassed
        MAXBATCHSIZE = 37
        scryfall_url = "https://api.scryfall.com/cards/collection"
        headers = {
            'User-Agent': 'MysticTunerApp',
            'Accept': 'application/json'
        }
        #break cards up into groups of 37
        card_groups = [card_names[i:i + MAXBATCHSIZE] for i in range(0, len(card_names),MAXBATCHSIZE)]
        invalidNames = []
        potentialInvalidNames = []
        for group in card_groups:
            data = {
                'identifiers': []
            }
            #break up any double cards into their two respsctive halves and format dict correctly
            for card in group:
                if "/" in card:
                    potentialInvalidNames.append(card)
                    split_card = card.split("/")
                    data['identifiers'].append({"name": split_card[0]})
                    data['identifiers'].append({"name": split_card[len(split_card)-1]})
                else:
                    data['identifiers'].append({"name": card})
            #fetch card data for group of cards
            response = requests.post(scryfall_url, json=data, headers=headers)
            response_data = response.json()
            #format returned dict
            if response_data["not_found"] != []:
                for dict in response_data["not_found"]:
                    invalidNames.append(dict["name"])
        if invalidNames != []:
            #return any split double cards to their original state
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
        #ensure a card name is passed
        if not card_name:
            return None
        #alter name to ensure http request compatability
        uriName = encodeURIName(card_name)
        scryfall_url = f"https://api.scryfall.com/cards/named?fuzzy={uriName}"
        headers = {
            'User-Agent': 'MysticTunerApp',
            'Accept': 'application/json'
        }
        #fetch card info
        response = requests.get(scryfall_url, headers=headers)
        card_data = response.json()
        if response.status_code != 200:
            print("Error: Commander Card not found")
            return None
        #ensure requested card is a legal commander card
        if card_data['legalities']['commander'] != 'legal':
            return None
        if ("Legendary Creature" not in card_data['type_line']) and ("can be your commander" not in card_data['oracle_text']):
            return None
        multisided = card_data.get('card_faces', None)
        if multisided and len(multisided) > 1:
            return None
        else:
            return Card.from_json(card_data)
        
    @staticmethod
    def autocomplete(card_name: str) -> list[str]:
        """
        Search for potential cards
        """
        #ensure a cardname is provided
        if not card_name:
            return []
        #encode name to ensiure it is in valid http format
        uriName = encodeURIName(card_name)
        scryfall_url = f"https://api.scryfall.com/cards/autocomplete?q={uriName}"
        headers = {
            'User-Agent': 'MysticTunerApp',
            'Accept': 'application/json'
        }
        #request autocomplete suggestions
        response = requests.get(scryfall_url, headers=headers)
        card_list: list[str] = response.json()["data"]
        if response.status_code != 200:
            return None
        return card_list