from database_connector import DatabaseConnector 
def main():
    """
    cards = [
    {'cardname': 'Card A', 'sideboard': False, 'cardtype': 'Creature', 'count': 3},
    {'cardname': 'Card B', 'sideboard': True, 'cardtype': 'Sorcery', 'count': 2},
    {'cardname': 'Card C', 'sideboard': False, 'cardtype': 'Creature', 'count': 4},
    {'cardname': 'Card D', 'sideboard': True, 'cardtype': 'Artifact', 'count': 1},
    {'cardname': 'Card E', 'sideboard': False, 'cardtype': 'Instant', 'count': 5},
    {'cardname': 'Card F', 'sideboard': True, 'cardtype': None, 'count': 2}
    ]
    instance = DatabaseConnector()

    result = instance.test_connection()

    if(result):
        print("Database is running, successfully connected to it")
    else:
        print("Error with connection")

    response = instance.get_user_decks(1)
    for item in response:
        print(item)
    
    instance.add_cards_to_deck(cards, 1)

    instance.delete_cards_from_deck(cards, 1)
    """

    instance = DatabaseConnector()

    try:
        instance.add_deck(1, "Commander", "TEST_DECK 1")
    except:
        pass
    instance.delete_deck(1, "TEST_DECK 1")

if __name__ == "__main__":
    main()