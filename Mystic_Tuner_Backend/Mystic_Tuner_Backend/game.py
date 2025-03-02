from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum

from backend.Mystic_Tuner_Backend.Mystic_Tuner_Backend.card import Card
import backend.Mystic_Tuner_Backend.Mystic_Tuner_Backend.deck as deck


class Game(ABC):
    class Type(Enum):
        STANDARD = "standard"
        COMMANDER = "commander"

    @abstractmethod
    def __init__(self, card_quantity: int):
        self.card_quantity = card_quantity

    @abstractmethod
    def __str__(self):
        pass


class Commander(Game):
    def __init__(self, commander: Card):
        super().__init__(100)
        self.commander: Card = commander

    def __str__(self):
        return f"{Game.Type.COMMANDER.value}"


class Standard(Game):
    def __init__(self):
        super().__init__(60)

    def __str__(self):
        return f"{Game.Type.STANDARD.value}"


class GameFactory:

    @staticmethod
    def create_game(game_json: dict) -> Game:
        game_type = game_json["gameType"]

        if game_type == Game.Type.STANDARD.value:
            return Standard()
        elif game_type == Game.Type.COMMANDER.value:
            # Find the commander card in the decklist
            commander_card_json = {}
            for card in game_json["deckList"]:
                if card["name"] == game_json["commander"]:
                    commander_card_json = card
                    break
            return Commander(Card.from_json(commander_card_json))
        else:
            raise ValueError("Invalid game type provided.")
