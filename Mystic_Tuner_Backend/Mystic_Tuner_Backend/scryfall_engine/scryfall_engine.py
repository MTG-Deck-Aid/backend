from backend.Mystic_Tuner_Backend.Mystic_Tuner_Backend.card import Card
from django.http import JsonResponse
import requests
import time

class ScryFallEngine:
    """
    Uses Scryfall API to find Magic The Gathering (MTG) card information
    """

    def __init__(self):
        self
        

    def search_card(self, card_name: str) -> Card:
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
        scryfall_url = f"https://api.scryfall.com/cards/named?fuzzy={card_name}"
        headers = {
            'User-Agent': 'MysticTunerApp',
            'Accept': 'application/json'
        }
        response = requests.get(scryfall_url, headers=headers)
        card_data = response.json()
        if response.status_code != 200:
            return None
        return Card.from_json(card_data)
    
if __name__ == "__main__":
    # Example Usage
    engine = ScryFallEngine()
    card = engine.search_card('Black Lotus')
    print(card.__str__())
    
        
