"""
Unit Testing File for card_suggestor.py
Decklist used:
- [1] Brendan Smiley. Moxfield. "Marchesa, The Black Rose 🥀🖤" .https://moxfield.com/decks/zGF0eVfcmkqgDDPsKFFu9A

NOTE: To run the unit tests:
    1. Navigate to the deck_suggestion directory.
    2. Run the command 'python -m unittest ./_tests/test_card_suggestor.py'.
"""

import logging
import unittest

from Mystic_Tuner_Backend.card import Card
from Mystic_Tuner_Backend.deck import Deck
from Mystic_Tuner_Backend.deck_suggestions import (
    CardSuggestor,
    DeckSuggestionController,
)


class TestCardSuggestor(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(1, 1)

    def test_suggest_cards_API(self):
        """
        Tests the main API controller for card suggestions.
        The controller should return the proper data structure of
        a list of dictionaries with the keys card_to_replace, card_to_add, and reason.
        card_to_replace and card_to_add should be Card objects, not strings.
        """
        controller = DeckSuggestionController()
        json_str = str(
            {
                "deckName": "Test Deck",
                "gameType": "commander",
                "gameQuantity": 100,
                "commander": "Marchesa, the Black Rose",
                "deckList": [
                    {
                        "name": "Marchesa, the Black Rose",
                        "colors": ["black", "blue", "red"],
                        "quantity": 1,
                    },
                    {"name": "Blood Artist", "colors": ["black"], "quantity": 1},
                    {"name": "Carrion Feeder", "colors": ["black"], "quantity": 1},
                    {
                        "name": "Ashnod's Altar",
                        "colors": ["colorless"],
                        "quantity": 1,
                    },
                    {"name": "Sol Ring", "colors": ["colorless"], "quantity": 1},
                    {"name": "Mana Crypt", "colors": ["colorless"], "quantity": 1},
                ],
            }
        )
        suggestions = controller.get_suggestions(json_str)

        self.assertEqual(type(suggestions), list)
        self.assertEqual(type(suggestions[0]), dict)
        self.assertEqual(
            type(suggestions[0]["card_to_add"]),
            type(Card()),
            "The scryfall search needs to find the full information of the  strings suggested,"
            + "then the API should replace strings with Card objects.",
        )

    def test_suggest_cards_new(self):
        """
        Tests that the generative AI model can suggest new cards
        when given a decklist with less than the format's minimum card count.
        New cards should have the card_to_replace field set to an empty string.
        """
        card_suggestor = CardSuggestor()
        decklist = Deck.from_file("./_tests/incomplete_commander_decklist.json")
        suggestions = card_suggestor.suggest_cards(decklist)
        for suggestion in suggestions:
            self.assertEqual(suggestion["card_to_replace"], "")
            self.assertNotEqual(suggestion["card_to_add"], "")

    def test_suggest_cards_replacement(self):
        """
        Suggestions work correctly when the decklist is at least the minimum card count
        of the format.
        Provides a commander decklist of 100 cards and validates that no empty "" card_to_replace fields are present.
        """
        card_suggestor = CardSuggestor()
        decklist = Deck.from_file("./_tests/commander_decklist.json")
        suggestions = card_suggestor.suggest_cards(decklist)
        for suggestion in suggestions:
            self.assertNotEqual(suggestion["card_to_replace"], "")
            self.assertNotEqual(suggestion["card_to_add"], "")

    def test_suggest_cards_fields_present(self):
        """
        Tests that each suggestion has the correct fields.
        card_to_replace, card_to_add, and reason should all be present.
        """
        card_suggestor = CardSuggestor()
        decklist = Deck.from_file("./_tests/commander_decklist.json")
        suggestions = card_suggestor.suggest_cards(decklist)
        for suggestion in suggestions:
            self.assertIn("card_to_replace", suggestion)
            self.assertIn("card_to_add", suggestion)
            self.assertIn("reason", suggestion)
