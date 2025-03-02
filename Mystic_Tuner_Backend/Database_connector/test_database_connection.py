from database_connector import DatabaseConnector 
"""
        self.host = "localhost"  # Example: localhost or an IP address
        self.dbname = "Mystic_Tuner_Application"  # Your database name
        self.user = "MT_Admin"  # Your database username
        self.password = "admin"  # Your database password
        self.port = "5433"  # Default PostgreSQL port
"""

def main():
    
    cards = [
    {'cardname': 'Card A', 'sideboard': False, 'cardtype': 'Creature', 'count': 3},
    {'cardname': 'Card B', 'sideboard': True, 'cardtype': 'Sorcery', 'count': 2},
    {'cardname': 'Card C', 'sideboard': False, 'cardtype': 'Creature', 'count': 4},
    {'cardname': 'Card D', 'sideboard': True, 'cardtype': 'Artifact', 'count': 1},
    {'cardname': 'Card E', 'sideboard': False, 'cardtype': 'Instant', 'count': 5},
    {'cardname': 'Card F', 'sideboard': True, 'cardtype': None, 'count': 2}
    ]

    cards_list = ['Card A', 'Card B', 'Card C', 'Card D', 'Card E', 'Card F']
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

    instance.delete_cards_from_deck(cards_list, 1)
    
    cards = ["Card A", "Card B", "Card C"]
    instance = DatabaseConnector()

    instance.update_card_repository(cards)
    instance.clear_card_repository()

if __name__ == "__main__":
    main()