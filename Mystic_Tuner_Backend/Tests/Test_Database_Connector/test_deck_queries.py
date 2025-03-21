from Database_Connector.deck_queries import DeckQueries
from Database_Connector.card_queries import CardQueries
import pytest

@pytest.fixture
def setup_and_teardown():
    query_generator = DeckQueries()
    cards = [
        {'cardname': 'Card A', 'sideboard': False, 'cardtype': 'Creature', 'count': 3},
        {'cardname': 'Card B', 'sideboard': True, 'cardtype': 'Sorcery', 'count': 2},
        {'cardname': 'Card C', 'sideboard': False, 'cardtype': 'Instant', 'count': 4},
        {'cardname': 'Card D', 'sideboard': True, 'cardtype': 'Enchantment', 'count': 1}
        ]
    
    decks = [
        ["10", "Commander", "Deck1", "Card A"],
        ["10", "Commander", "Deck2", None],
        ["10", "Standard", "Deck3", None],
        ["20", "Commander", "Deck4", None],
        ["20", "Modern", "Deck5", None]
    ]

    try:
        query_generator.add_deck(decks[0][0], decks[0][1], decks[0][2], decks[0][3])
        query_generator.add_deck(decks[1][0], decks[1][1], decks[1][2], decks[1][3])
        query_generator.add_deck(decks[2][0], decks[2][1], decks[2][2], decks[2][3])
        query_generator.add_deck(decks[3][0], decks[3][1], decks[3][2], decks[3][3])
        query_generator.add_deck(decks[4][0], decks[4][1], decks[4][2], decks[4][3])

    except ValueError as e:
        pass #Decks already exist/ not an issue

    user_decks = query_generator.get_user_decks("10")
    deck_id = None
    for deck in user_decks:
        if deck[1] == "Deck1":
            deck_id = deck[2]

    if deck_id == None:
        raise Exception()

    query_generator = CardQueries()
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

    query_generator = DeckQueries()

    query_generator.delete_deck("10", "Deck1")
    query_generator.delete_deck("10", "Deck2")
    query_generator.delete_deck("10", "Deck3")
    query_generator.delete_deck("20", "Deck4")
    query_generator.delete_deck("20", "Deck5")

    query_generator.delete_deck("10", "Test_deck")
    query_generator.delete_deck("11", "Test_deck")


#
#CREATE TESTS
#

#TC-DQ01
def test_create_deck(setup_and_teardown):
    query_generator = DeckQueries()

    deck_to_add = ["10", "Standard", "Test_deck", None]

    query_generator.add_deck(deck_to_add[0], deck_to_add[1], deck_to_add[2], deck_to_add[3])

    tested_decks = query_generator.get_user_decks(deck_to_add[0])

    correct = False

    for deck in tested_decks:
        if deck[0] == deck_to_add[1] and deck[1] == deck_to_add[2]:
            correct = True
            break
    
    assert correct == True

#TC-DQ02
def test_create_deck_none_name(setup_and_teardown):
    query_generator = DeckQueries()

    deck_to_add = ["10", "Standard", None, None]

    result = query_generator.add_deck(deck_to_add[0], deck_to_add[1], deck_to_add[2], deck_to_add[3])

    assert result == False

#TC-DQ03
def test_create_deck_none_type(setup_and_teardown):
    query_generator = DeckQueries()

    deck_to_add = ["10", None, "Test_deck", None]

    result = query_generator.add_deck(deck_to_add[0], deck_to_add[1], deck_to_add[2], deck_to_add[3])

    assert result == False

#TC-DQ04
def test_create_deck_none_user(setup_and_teardown):
    query_generator = DeckQueries()

    deck_to_add = [None, "Standard", "Test_deck", None]

    result = query_generator.add_deck(deck_to_add[0], deck_to_add[1], deck_to_add[2], deck_to_add[3])

    assert result == False

#TC-DQ05
def test_create_existing_deck(setup_and_teardown):
    query_generator = DeckQueries()

    deck_to_add = ["10", "Standard", "Deck1", None]

    with pytest.raises(ValueError):
        query_generator.add_deck(deck_to_add[0], deck_to_add[1], deck_to_add[2], deck_to_add[3])


#
#READ TESTS
#

#TC-DQ06
def test_get_all_user_decks(setup_and_teardown):
    query_generator = DeckQueries()

    decks = query_generator.get_user_decks("10")

    correct_values = [        
        ["Commander", "Deck1"],
        ["Commander", "Deck2"],
        ["Standard", "Deck3"]]
    correct = True
    for deck in decks:
        correct = False
        for value in correct_values:
            if(value[0] == deck[0] and value[1] == deck[1]):
                correct = True
                break
        assert correct == True

#TC-DQ07
def test_get_all_user_decks_none_user(setup_and_teardown):
    query_generator = DeckQueries()
    decks = query_generator.get_user_decks("-1")

    assert len(decks) == 0

#TC-DQ08
def test_get_deck(setup_and_teardown):
    query_generator = DeckQueries()
    deck = query_generator.get_deck(setup_and_teardown)

    assert len(deck) == 4

#TC-DQ09
def test_get_empty_deck(setup_and_teardown):
    query_generator = DeckQueries()
    deck = query_generator.get_deck(setup_and_teardown + 1)

    assert len(deck) == 0
#
#UPDATE TESTS
#

#TC-DQ10
def test_update_deck(setup_and_teardown):
    query_generator = DeckQueries()

    query_generator.update_deck("11", "Pauper", "Test_deck", setup_and_teardown, None)

    decks = query_generator.get_user_decks("11")

    assert decks[0][4] == "11"

    assert decks[0][0] == "Pauper"

    assert decks[0][1] == "Test_deck"

    assert decks[0][3] == None

#TC-DQ11
def test_update_deck_invalid_user(setup_and_teardown):
    query_generator = DeckQueries()
    
    result = query_generator.update_deck(None, "Pauper", "Test_deck", setup_and_teardown, None)

    assert result == False

#TC-DQ12
def test_update_deck_invalid_type(setup_and_teardown):
    query_generator = DeckQueries()
    
    result = query_generator.update_deck("11", None, "Test_deck", setup_and_teardown, None)

    assert result == False

#TC-DQ13
def test_update_deck_invalid_name(setup_and_teardown):
    query_generator = DeckQueries()
    
    result = query_generator.update_deck("11", "Pauper", None, setup_and_teardown, None)

    assert result == False
#
#DELETE TESTS
#

#TC-DQ14
def test_delete_deck(setup_and_teardown):
    query_generator = DeckQueries()

    rows_affected = query_generator.delete_deck("10", "Deck1")

    assert rows_affected == 1

    results = query_generator.get_user_decks("10")

    correct = True
    
    for deck in results:
        if deck[1] == "Deck1":
            correct = False
            break

    assert correct == True


#TC-DQ15
def test_delete_nonexistant_deck(setup_and_teardown):
    query_generator = DeckQueries()

    rows_affected = query_generator.delete_deck("10", "Nonexistant_Deck")

    assert rows_affected == 0

#TC-DQ16
def test_delete_deck_wrong_user(setup_and_teardown):
    query_generator = DeckQueries()

    rows_affected = query_generator.delete_deck("11", "Deck1")

    assert rows_affected == 0

    results = query_generator.get_user_decks("10")

    correct = False
    
    for deck in results:
        if deck[1] == "Deck1":
            correct = True
            break

    assert correct == True


