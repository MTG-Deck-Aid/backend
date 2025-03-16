import pytest

from Mystic_Tuner_Backend.scryfall_engine.scryfall_engine import ScryFallEngine

@pytest.fixture
def setup_and_teardown():
    pass

def test_autocomplete(setup_and_teardown):
    list_of_cards: list = ScryFallEngine.autocomplete("Demonic")
    assert len(list_of_cards) > 3 # Domain Knowledge, there are more than 3 cards with "Demonic"
    for card_name in list_of_cards:
        assert "Demonic" in card_name

def test_autocomplete_empty_string(setup_and_teardown):
    list_of_cards: list = ScryFallEngine.autocomplete("")
    assert type(list_of_cards) == list
    assert len(list_of_cards) == 0