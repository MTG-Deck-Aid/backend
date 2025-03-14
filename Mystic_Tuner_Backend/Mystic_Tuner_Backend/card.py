from enum import Enum


class Card:
    """
    Represents a Magic the Gathering (MTG) card within the system.
    """

    class Color(Enum):
        WHITE = "W"
        BLUE = "U"
        BLACK = "B"
        RED = "R"
        GREEN = "G"
        COLORLESS = ""

    def __init__(self, name: str, colors: list[Color]):
        self.name: str = name
        self.colors: list[Card.Color] = colors


    def __str__(self):
        return f"Card: {self.name}\nColors: {self.colors}"

    @classmethod
    def from_json(cls, json_card: dict):
        """
        Alternative constructor for creating a Card object from a JSON object.
        Main Use - API
        """
        card = cls.__new__(cls)
        card._parse_json_card(json_card)

        return card

    def _parse_json_card(self, json_card: dict):
        self.name = json_card["name"]
        self.colors = [Card.Color(color) for color in json_card["colors"]]
        
