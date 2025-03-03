from database_queries import card_queries
from database_connector import DatabaseConnector
import pytest


@pytest.fixture
def setup_and_teardown():


    yield




def test_create():
    instance = card_queries()
    cards = [
        {'cardname': 'Card A', 'sideboard': False, 'cardtype': 'Creature', 'count': 3},
        {'cardname': 'Card B', 'sideboard': True, 'cardtype': 'Sorcery', 'count': 2}
        ]
    instance.add_cards_to_deck(cards, 1)
    assert len(instance.get_card('Card A')) != 0

    assert len(instance.get_card('Card B')) != 0

    cards_to_delete = ['Card A', 'Card B']

    instance.delete_cards_from_deck(cards_to_delete, 1)

    

def test_read():
    pass

def test_delete():
    pass




