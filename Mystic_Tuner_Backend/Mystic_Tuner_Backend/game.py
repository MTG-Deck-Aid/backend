from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum

from Mystic_Tuner_Backend.card import Card
import Mystic_Tuner_Backend.deck as deck
from Mystic_Tuner_Backend.scryfall_engine.scryfall_engine import ScryFallEngine


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
    def create_game(deck: dict) -> Game:
        game_type = deck.get("gameType", Game.Type.COMMANDER.value)

        if game_type == Game.Type.STANDARD.value:
            return Standard()
        elif game_type == Game.Type.COMMANDER.value:
            # Get the commander card
            commander_name: str = deck["commander"]
            return Commander(ScryFallEngine().validate_commander(commander_name))
        else:
            raise ValueError("Invalid game type provided.")
