from Mystic_Tuner_Backend.card import Card
import Mystic_Tuner_Backend.game as mtg_games
import json

from Mystic_Tuner_Backend.scryfall_engine.scryfall_engine import ScryFallEngine


class Deck:
    """
    Represents a Magic the Gathering (MTG) deck within the system.
    """

    def __init__(
        self,
        name: str,
        card_list: list[Card] = None,
        game: mtg_games.Game = None,
    ):
        """
        Different ways to create a Deck object.
        For alternative constructors see "from_..." methods.
        """
        self.name: str = name
        self.game: mtg_games.Game = game
        self.card_list: list[Card] = card_list

    def __str__(self):
        res = f"Deck: {self.name}\nGame Type: {self.game}\nCard List:"
        for card in self.card_list:
            res += f"\n{card}"
        return res

    @classmethod
    def from_json(cls, json_deck: dict):
        """
        Alternative constructor for creating a Deck object from a JSON object.
        Main Use - API
        """
        try:
            deck = cls.__new__(cls)
            deck._parse_json_deck(json_deck)
            return deck
        except Exception as e:
            print("An error occured when parsing the deck JSON: ", e)
        

    @classmethod
    def from_file(cls, file_path: str):
        """
        Alternative constructor for creating a Deck object from a file.
        Main Use - Unit Testing
        """
        deck = cls.__new__(cls)
        deck._load_deck_from_file(file_path)
        return deck

    def _parse_json_deck(self, deck: dict):
        self.name = deck.get("deckName", "Unnamed Deck")
        self.game = mtg_games.GameFactory.create_game(deck)
        self.card_list = []
        engine = ScryFallEngine()
        for deck_card in deck["decklist"]["mainboard"]:
            quantity = deck_card["quantity"]
            for _ in range(quantity):
                card = deck_card.copy()
                card.pop("quantity")
                self.card_list.append(engine.search_card(card["name"]))

    def _load_deck_from_file(self, file_path: str):
        try:
            with open(file_path, "r") as f:
                self._parse_json_deck(json.load(f))
        except Exception as e:
            print("An error occured when reading the decklist file: ", e)
            raise e


