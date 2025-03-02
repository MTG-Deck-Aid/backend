from backend.Mystic_Tuner_Backend.Mystic_Tuner_Backend.card import Card
import backend.Mystic_Tuner_Backend.Mystic_Tuner_Backend.game as game
import json


class Deck:
    """
    Represents a Magic the Gathering (MTG) deck within the system.
    """

    def __init__(
        self,
        name: str,
        card_list: list[Card] = None,
        game_type: game.Game = None,
    ):
        """
        Different ways to create a Deck object.
        For alternative constructors see "from_..." methods.
        """
        self.name: str = name
        self.game: game.Game = game_type
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
        deck = cls.__new__(cls)
        deck._parse_json_deck(json_deck)
        return deck

    @classmethod
    def from_file(cls, file_path: str):
        """
        Alternative constructor for creating a Deck object from a file.
        Main Use - Unit Testing
        """
        deck = cls.__new__(cls)
        deck._load_deck_from_file(file_path)
        return deck

    def _parse_json_deck(self, json_deck: dict):
        self.name = json_deck["deckName"]
        self.game = game.GameFactory.create_game(json_deck)
        self.card_list = []
        for deck_card in json_deck["deckList"]:
            quantity = deck_card["quantity"]
            for _ in range(quantity):
                card = deck_card.copy()
                card.pop("quantity")
                self.card_list.append(Card.from_json(card))

    def _load_deck_from_file(self, file_path: str):
        try:
            with open(file_path, "r") as f:
                self._parse_json_deck(json.load(f))
        except Exception as e:
            print("An error occured when reading the decklist file: ", e)
            raise e


if __name__ == "__main__":

    def example():
        # Constructor 1
        deck = Deck(
            "My Deck",
            game_type=game.GameFactory.create_game(
                {"gameType": "standard", "deckList": []}
            ),
        )

        # Constructor 2
        deck = Deck.from_json(
            {
                "deckName": "My Deck",
                "gameType": "standard",
                "deckList": [],
            }
        )
        # Constructor 3
        deck = Deck.from_file("./deck_suggestions/_tests/decklist.json")

    example()
