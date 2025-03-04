from database_queries import deck_queries, card_queries
from database_connector import DatabaseConnector
import pytest

@pytest.fixture
def setup_and_teardown():
    query_generator = deck_queries()
    cards = [
        {'cardname': 'Card A', 'sideboard': False, 'cardtype': 'Creature', 'count': 3},
        {'cardname': 'Card B', 'sideboard': True, 'cardtype': 'Sorcery', 'count': 2},
        {'cardname': 'Card C', 'sideboard': False, 'cardtype': 'Instant', 'count': 4},
        {'cardname': 'Card D', 'sideboard': True, 'cardtype': 'Enchantment', 'count': 1}
        ]
    
    decks = [
        [10, "Commander", "Deck1"],
        [10, "Commander", "Deck2"],
        [10, "Standard", "Deck3"],
        [20, "Commander", "Deck4"],
        [20, "Modern", "Deck5"]
    ]

    try:
        query_generator.add_deck(decks[0][0], decks[0][1], decks[0][2])
        query_generator.add_deck(decks[1][0], decks[1][1], decks[1][2])
        query_generator.add_deck(decks[2][0], decks[2][1], decks[2][2])
        query_generator.add_deck(decks[3][0], decks[3][1], decks[3][2])
        query_generator.add_deck(decks[4][0], decks[4][1], decks[4][2])

    except ValueError as e:
        pass #Decks already exist/ not an issue

    user_decks = query_generator.get_user_decks(10)
    deck_id = None
    for deck in user_decks:
        if deck[2] == "Deck1":
            deck_id = deck[3]

    if deck_id == None:
        raise Exception()

    query_generator = card_queries()
    cards = [
        {'cardname': 'Card A', 'sideboard': False, 'cardtype': 'Creature', 'count': 3},
        {'cardname': 'Card B', 'sideboard': True, 'cardtype': 'Sorcery', 'count': 2},
        {'cardname': 'Card C', 'sideboard': False, 'cardtype': 'Instant', 'count': 4},
        {'cardname': 'Card D', 'sideboard': True, 'cardtype': 'Enchantment', 'count': 1}
        ]

    query_generator.add_cards_to_deck(cards, deck_id)

    yield deck_id

    cards = ['Card A', 'Card B', 'Card C', 'Card D']

    query_generator.delete_cards_from_deck(cards, deck_id)

    query_generator = deck_queries()

    query_generator.delete_deck(10, "Deck1")
    query_generator.delete_deck(10, "Deck2")
    query_generator.delete_deck(10, "Deck3")
    query_generator.delete_deck(20, "Deck4")
    query_generator.delete_deck(20, "Deck5")

    query_generator.delete_deck(10, "Test_deck")
    query_generator.delete_deck(11, "Test_deck")


#
#CREATE TESTS
#
def test_create_deck(setup_and_teardown):
    query_generator = deck_queries()

    deck_to_add = [10, "Standard", "Test_deck"]

    query_generator.add_deck(deck_to_add[0], deck_to_add[1], deck_to_add[2])

    tested_decks = query_generator.get_user_decks(deck_to_add[0])

    correct = False

    for deck in tested_decks:
        if deck[1] == deck_to_add[1] and deck[2] == deck_to_add[2]:
            correct = True
            break
    
    assert correct == True

def test_create_deck_none_name(setup_and_teardown):
    query_generator = deck_queries()

    deck_to_add = [10, "Standard", None]

    result = query_generator.add_deck(deck_to_add[0], deck_to_add[1], deck_to_add[2])

    assert result == False

def test_create_deck_none_type(setup_and_teardown):
    query_generator = deck_queries()

    deck_to_add = [10, None, "Test_deck"]

    result = query_generator.add_deck(deck_to_add[0], deck_to_add[1], deck_to_add[2])

    assert result == False

def test_create_deck_none_user(setup_and_teardown):
    query_generator = deck_queries()

    deck_to_add = [None, "Standard", "Test_deck"]

    result = query_generator.add_deck(deck_to_add[0], deck_to_add[1], deck_to_add[2])

    assert result == False

def test_create_existing_deck(setup_and_teardown):
    query_generator = deck_queries()

    deck_to_add = [10, "Standard", "Deck1"]

    with pytest.raises(ValueError):
        query_generator.add_deck(deck_to_add[0], deck_to_add[1], deck_to_add[2])


#
#READ TESTS
#
def test_get_all_user_decks(setup_and_teardown):
    query_generator = deck_queries()

    decks = query_generator.get_user_decks(10)

    correct_values = [        
        ["Commander", "Deck1"],
        ["Commander", "Deck2"],
        ["Standard", "Deck3"]]
    correct = True
    for deck in decks:
        correct = False
        for value in correct_values:
            if(value[0] == deck[1] and value[1] == deck[2]):
                correct = True
                break
        assert correct == True

def test_get_all_user_decks_none_user(setup_and_teardown):
    query_generator = deck_queries()
    decks = query_generator.get_user_decks(100)

    assert len(decks) == 0

def test_get_deck(setup_and_teardown):
    query_generator = deck_queries()
    deck = query_generator.get_deck(setup_and_teardown)

    assert len(deck) == 4

def test_get_empty_deck(setup_and_teardown):
    query_generator = deck_queries()
    deck = query_generator.get_deck(setup_and_teardown + 1)

    assert len(deck) == 0
#
#UPDATE TESTS
#

def test_update_deck(setup_and_teardown):
    query_generator = deck_queries()

    query_generator.update_deck(11, "Pauper", "Test_deck", setup_and_teardown)

    decks = query_generator.get_user_decks(11)

    assert decks[0][0] == 11

    assert decks[0][1] == "Pauper"

    assert decks[0][2] == "Test_deck"

def test_update_deck_invalid_user(setup_and_teardown):
    query_generator = deck_queries()
    
    result = query_generator.update_deck(None, "Pauper", "Test_deck", setup_and_teardown)

    assert result == False

def test_update_deck_invalid_type(setup_and_teardown):
    query_generator = deck_queries()
    
    result = query_generator.update_deck(11, None, "Test_deck", setup_and_teardown)

    assert result == False

def test_update_deck_invalid_name(setup_and_teardown):
    query_generator = deck_queries()
    
    result = query_generator.update_deck(11, "Pauper", None, setup_and_teardown)

    assert result == False
#
#DELETE TESTS
#

def test_delete_deck(setup_and_teardown):
    query_generator = deck_queries()

    rows_affected = query_generator.delete_deck(10, "Deck1")

    assert rows_affected == 1

    results = query_generator.get_user_decks(10)

    correct = True
    
    for deck in results:
        if deck[2] == "Deck1":
            correct = False
            break

    assert correct == True


def test_delete_nonexistant_deck(setup_and_teardown):
    query_generator = deck_queries()

    rows_affected = query_generator.delete_deck(10, "Nonexistant_Deck")

    assert rows_affected == 0

def test_delete_deck_wrong_user(setup_and_teardown):
    query_generator = deck_queries()

    rows_affected = query_generator.delete_deck(11, "Deck1")

    assert rows_affected == 0

    results = query_generator.get_user_decks(10)

    correct = False
    
    for deck in results:
        if deck[2] == "Deck1":
            correct = True
            break

    assert correct == True