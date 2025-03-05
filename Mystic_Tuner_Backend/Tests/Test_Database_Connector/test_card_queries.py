from Database_Connector.card_queries import card_queries

import pytest


@pytest.fixture
def setup_and_teardown():
    query_generator = card_queries()
    cards = [
        {'cardname': 'Card A', 'sideboard': False, 'cardtype': 'Creature', 'count': 3},
        {'cardname': 'Card B', 'sideboard': True, 'cardtype': 'Sorcery', 'count': 2},
        {'cardname': 'Card C', 'sideboard': False, 'cardtype': 'Instant', 'count': 4},
        {'cardname': 'Card D', 'sideboard': True, 'cardtype': 'Enchantment', 'count': 1}
        ]
    deck_id = 1
    query_generator.add_cards_to_deck(cards, deck_id)


    yield deck_id
    
    cards_to_delete = ['Card A', 'Card B', 'Card C', 'Card D', 'Card E']
    query_generator.delete_cards_from_deck(cards_to_delete, deck_id)

#
#CREATION TESTS
#

def test_create_valid(setup_and_teardown):
    query_generator = card_queries()

    new_card = [{
        'cardname': 'Card E', 'sideboard': False, 'cardtype': 'Creature', 'count': 1
    }]

    rows_affected = query_generator.add_cards_to_deck(new_card, setup_and_teardown)

    assert rows_affected == 1

    results = query_generator.get_card('Card E')

    found_card = False

    for result in results:
        if result[1] == setup_and_teardown and result[2] == 'Card E':
            found_card = True
            break
    
    assert found_card == True

def test_create_none_cardtype(setup_and_teardown):
    query_generator = card_queries()

    new_card = [{
        'cardname': 'Card E', 'sideboard': False, 'cardtype': None, 'count': 1
    }]

    rows_affected = query_generator.add_cards_to_deck(new_card, setup_and_teardown)

    assert rows_affected != False
    assert rows_affected == 1

    result = query_generator.get_card(new_card[0]['cardname'])

    assert result[0][4] == None

def test_create_invalid_name(setup_and_teardown):
    query_generator = card_queries()

    new_card = [{
        'cardname': None, 'sideboard': False, 'cardtype': 'Creature', 'count': 1
    }]
    
    rows_affected = query_generator.add_cards_to_deck(new_card, setup_and_teardown)

    assert rows_affected == False

def test_create_invalid_sideboard(setup_and_teardown):
    query_generator = card_queries()

    new_card = [{
        'cardname': 'Card E', 'sideboard': None, 'cardtype': 'Creature', 'count': 1
    }]
    
    rows_affected = query_generator.add_cards_to_deck(new_card, setup_and_teardown)

    assert rows_affected == False


def test_create_none_count(setup_and_teardown):
    query_generator = card_queries()

    new_card = [{
        'cardname': 'Card E', 'sideboard': True, 'cardtype': 'Creature', 'count': None
    }]
    
    rows_affected = query_generator.add_cards_to_deck(new_card, setup_and_teardown)

    assert rows_affected == False

def test_create_negative_count(setup_and_teardown):
    query_generator = card_queries()

    new_card = [{
        'cardname': 'Card E', 'sideboard': True, 'cardtype': 'Creature', 'count': -1
    }]
    
    rows_affected = query_generator.add_cards_to_deck(new_card, setup_and_teardown)

    assert rows_affected == False

def test_create_zero_count(setup_and_teardown):
    query_generator = card_queries()

    new_card = [{
        'cardname': 'Card E', 'sideboard': True, 'cardtype': 'Creature', 'count': 0
    }]
    
    rows_affected = query_generator.add_cards_to_deck(new_card, setup_and_teardown)

    assert rows_affected == False

#
#READ TESTS
#

def test_read(setup_and_teardown):
    query_generator = card_queries()

    target_card = 'Card A'

    result = query_generator.get_card(target_card)

    assert result[0][1] == setup_and_teardown

    assert result[0][2] == 'Card A'

    assert result[0][3] == False

    assert result[0][4] == 'Creature'

    assert result[0][5] == 3

def test_read_nonexistant_card(setup_and_teardown):
    query_generator = card_queries()

    target_card = 'Card F'

    result = query_generator.get_card(target_card)

    assert len(result) == 0

#
#UPDATE TESTS
#

def test_update(setup_and_teardown):
    query_generator = card_queries()

    rows_updated = query_generator.update_card(setup_and_teardown, 'Card A', True, 'Enchantment', 1)

    assert rows_updated == 1

    result = query_generator.get_card('Card A')

    assert result[0][1] == setup_and_teardown

    assert result[0][2] == 'Card A'

    assert result[0][3] == True

    assert result[0][4] == 'Enchantment'

    assert result[0][5] == 1

def test_update_nonexistant_card(setup_and_teardown):
    query_generator = card_queries()

    result = query_generator.update_card(setup_and_teardown, 'Card F', True, 'Enchantment', 1)

    assert result == 0

def test_update_invalid_name(setup_and_teardown):
    query_generator = card_queries()

    result = query_generator.update_card(setup_and_teardown, None, True, 'Enchantment', 1)

    assert result == 0

def test_update_invalid_sideboard(setup_and_teardown):
    query_generator = card_queries()

    result = query_generator.update_card(setup_and_teardown, 'Card A', None, 'Enchantment', 1)

    assert result == False

def test_update_none_type(setup_and_teardown):
    query_generator = card_queries()

    result = query_generator.update_card(setup_and_teardown, 'Card A', False, None, 1)

    assert result == 1

def test_update_negative_count(setup_and_teardown):
    query_generator = card_queries()

    result = query_generator.update_card(setup_and_teardown, 'Card A', False, 'Enchantment', -1)

    assert result == False

def test_update_zero_count(setup_and_teardown):
    query_generator = card_queries()

    result = query_generator.update_card(setup_and_teardown, 'Card A', False, 'Enchantment', 0)

    assert result == False
#
#DELETE TESTS
#

def test_delete(setup_and_teardown):
    query_generator = card_queries()

    target_card = ['Card A']

    query_generator.delete_cards_from_deck(target_card, setup_and_teardown)

    result = query_generator.get_card(target_card[0])

    assert len(result) == 0

def test_delete_nonexistant_card(setup_and_teardown):
    query_generator = card_queries()

    target_card = ['Card F']
    
    rows_affected = query_generator.delete_cards_from_deck(target_card, setup_and_teardown)

    assert rows_affected == 0

def test_delete_card_wrong_deck(setup_and_teardown):
    query_generator = card_queries()

    target_card = ['Card A']
    
    rows_affected = query_generator.delete_cards_from_deck(target_card, setup_and_teardown + 1)

    assert rows_affected == 0

    result = query_generator.get_card(target_card[0])

    assert result[0][1] == setup_and_teardown

    assert result[0][2] == 'Card A'

    assert result[0][3] == False

    assert result[0][4] == 'Creature'

    assert result[0][5] == 3

def main():
    test_update_invalid_name(1)

if __name__ == "__main__":
    main()


