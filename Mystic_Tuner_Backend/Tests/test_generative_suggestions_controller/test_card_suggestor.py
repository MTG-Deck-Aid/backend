"""
Unit Testing File for card_suggestor.py
Decklist used:
- [1] Brendan Smiley. Moxfield. "Marchesa, The Black Rose 🥀🖤" .https://moxfield.com/decks/zGF0eVfcmkqgDDPsKFFu9A

NOTE: To run the unit tests:
    1. pytest must be installed
    2. Navigate to the backend/Mystic_Tuner_Backend directory
    3. Run the command `pytest` for all
    4. You can run just this file by running the command `pytest ./Tests/test_generative_suggestions_controller/test_card_suggestor.py`
"""

import pytest

from Mystic_Tuner_Backend.card import Card
from Mystic_Tuner_Backend.deck import Deck
from Mystic_Tuner_Backend.deck_suggestions.deck_suggestion_controller import CardSuggestionController

@pytest.fixture
def setup_and_teardown():
    decklist ={
    "num_to_add": 1,
    "num_to_remove": 2,
    "decklist": {
        "commander": "Marchesha The Black Rose",
        "mainboard": [
        {
            "name": "Ashnod's Al",
            "quantity": 1
        },
        {
            "name": "Demonic Tut",
            "quantity": 1
        },
        {
            "name": "Counterspell",
            "quantity": 1
        },
        {
            "name": "Sol Ring",
            "quantity": 1
        },
        {
            "name": "Swamp",
            "quantity": 9
        },
        {
            "name": "Island",
            "quantity": 9
        },
        {
            "name": "Mountain",
            "quantity": 12
        }
        ]
    }
    }
    yield decklist
    

def test_validate_request(setup_and_teardown):
    """
    Tests the validation of the request from the frontend.
    Should raise an error if the request is not the correct format
    """
    with pytest.raises(ValueError):
        CardSuggestionController.validate_request({
            "decklist": {
                "commander": "Marchesa, the Black Rose",
                "mainturd": [
                    {
                        "name": "Blood Crypt",
                        "quantity": 1
                    }
                ]
            }
        })

def test_add_suggestions(setup_and_teardown):
    """
    Tests the creation of a new card suggestion.
    Should only suggest a card once.
    """
    suggestions = CardSuggestionController.get_suggestions({
        "num_to_add": 5,
        "num_to_remove": 0,
        "decklist": {
            "commander": "Marchesa, the Black Rose",
            "mainboard": [
                {
                    "name": "Blood Crypt",
                    "quantity": 1
                },
                {
                    "name": "Sol Ring",
                    "quantity": 1
                },
            ]
        }
    })
    already_suggested = []
    for suggestion in suggestions["cards_to_add"]:
        if suggestion["card"].name in already_suggested:
            assert False
        already_suggested.append(suggestion["card"].name)
    assert True
        


def test_remove_suggestions_invalid_card_amount(setup_and_teardown):
    """
    Tests the removal of a card suggestion.
    Should only suggest a card once.
    Should add an "issue"
    """
    suggestions = CardSuggestionController.get_suggestions({
        "num_to_add": 0,
        "num_to_remove": 5,
        "decklist": {
            "commander": "Marchesa, the Black Rose",
            "mainboard": [
                {
                    "name": "Blood Crypt",
                    "quantity": 1
                },
                {
                    "name": "Sol Ring",
                    "quantity": 1
                },
            ]
        }
    })
    assert len(suggestions["issues"]) > 0

def test_remove_suggestions_valid_card_amount(setup_and_teardown):
    """
    Tests the removal of a card suggestion.
    Should only suggest a card once.
    """
    suggestions = CardSuggestionController.get_suggestions(setup_and_teardown)
    already_suggested = []
    for suggestion in suggestions["cards_to_remove"]:
        if suggestion["card"].name in already_suggested:
            assert False
        already_suggested.append(suggestion["card"].name)
    assert True


def test_reason_present(setup_and_teardown):
    """
    Tests the presence of a reason in the card suggestion.
    """
    suggestions = CardSuggestionController.get_suggestions(setup_and_teardown)
    for suggestion in suggestions["cards_to_add"]:
        assert suggestion["reason"] != ""
    for suggestion in suggestions["cards_to_remove"]:
        assert suggestion["reason"] != ""

def test_image_present(setup_and_teardown):
    """
    Tests the presence of an image in the card suggestion.
    """
    suggestions = CardSuggestionController.get_suggestions(setup_and_teardown)
    for suggestion in suggestions["cards_to_add"]:
        assert suggestion["card"].image_url != ""
    for suggestion in suggestions["cards_to_remove"]:
        assert suggestion["card"].image_url != ""