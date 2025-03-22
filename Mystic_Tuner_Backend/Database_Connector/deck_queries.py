from Database_Connector.database_connector import DatabaseConnector
from Database_Connector.card_queries import CardQueries
class DeckQueries():
    """
    Class for creating queries related to the Deck Table
    """
    def __init__(self):
        self.connection = DatabaseConnector.get_instance()

    def generate_example_deck(self, user_id: str) -> int:
        """
        Generates an example deck for the user.

        args:
            user_id (String) - the user's id
        """
        deck_queries = DeckQueries()
        card_queries = CardQueries()
        deck_queries.add_deck(user_id, "commander", "Example Deck", "Marchesa, The Black Rose")
        decks = deck_queries.get_user_decks(user_id)
        did = decks[-1][2]
        print("Example Deck ID: ", did)
        
        cards = [
        {'cardname': 'Marchesa, The Black Rose', 'sideboard': False, 'cardtype': None, 'count': 1},
        {'cardname': 'Demonic Tutor', 'sideboard': False, 'cardtype': None, 'count': 1},
        {'cardname': 'Counterspell', 'sideboard': False, 'cardtype': None, 'count': 1},
        {'cardname': 'Negate', 'sideboard': False, 'cardtype': None, 'count': 1},
        {'cardname': 'Chaos Warp', 'sideboard': False, 'cardtype': None, 'count': 1},
        {'cardname': 'Swiftfoot Boots', 'sideboard': False, 'cardtype': None, 'count': 1},
        {'cardname': 'Sol Ring', 'sideboard': False, 'cardtype': None, 'count': 1},
        {'cardname': 'Talisman of Creativity', 'sideboard': False, 'cardtype': None, 'count': 1},
        {'cardname': 'Talisman of Dominance', 'sideboard': False, 'cardtype': None, 'count': 1},
        {'cardname': 'Talisman of Indulgence', 'sideboard': False, 'cardtype': None, 'count': 1},
        {'cardname': 'Dauthi Voidwalker', 'sideboard': False, 'cardtype': None, 'count': 1},
        {'cardname': 'Spark Double', 'sideboard': False, 'cardtype': None, 'count': 1},
        {'cardname': 'Skullclamp', 'sideboard': False, 'cardtype': None, 'count': 1},
        {'cardname': 'Swamp', 'sideboard': False, 'cardtype': None, 'count': 12},
        {'cardname': 'Island', 'sideboard': False, 'cardtype': None, 'count': 12},
        {'cardname': 'Mountain', 'sideboard': False, 'cardtype': None, 'count': 12},
        ]

        card_queries.add_cards_to_deck(cards, did)
        print("Example Deck Created for new user.")
        return did

    #CREATE
    def add_deck(self, user_id, deck_type, deck_name, commander):
        """
        args:
            user_id (String) - user id
            deck_type (String) - type of deck
            deck_name (String) - name for deck (must be unique for the given user)
            commander (String) - name of commander
        return:
            (int) - number of affected rows
        """
        for deck in self.get_user_decks(user_id):
            if(deck_name == deck[1]):
                raise ValueError("DeckName already exists")

        query = "INSERT INTO \"deck\" (\"userId\", \"deckType\", \"deckName\", \"commander\") VALUES (%s, %s, %s, %s);"
        params = (user_id, deck_type, deck_name, commander)

        return self.connection.execute_query(query, params, False)

    #READ
    def get_user_decks(self, user_id):
        """
        args:
            user_id (String) - user id to get decks from
        return:
            (List) - all decks associated with the user
        """
        query = "SELECT * FROM \"deck\" WHERE \"userId\" = %s ORDER BY \"DID\" ASC;"
        params = (user_id,)

        return self.connection.execute_query(query, params)
    
    def get_deck(self, deck_id):
        """
        args:
            deck_id (int) - deck id
        return:
            (List) - the specific deck
        """
        query = "SELECT * FROM \"card\" WHERE \"deckid\" = %s ORDER BY id ASC;"
        params = (deck_id,)

        return self.connection.execute_query(query, params)
    
    #UPDATE
    def update_deck(self, user_id, deck_type, deck_name, deck_id, commander):
        """
        args:
            user_id (String) - user id
            deck_type (String) - type of deck (ex. Standard, Commander)
            deck_name (String) - name of deck 
            decK_id (int) - id of deck to update
            commander (String) - name of commander
        return:
            (int) - number of affected rows

            Overwites existing deck's information with the new data
        """
        query = "UPDATE \"deck\" SET \"userId\" = %s, \"deckType\" = %s, \"deckName\" = %s, \"commander\" = %s WHERE \"DID\" = %s;"
        params = (user_id, deck_type, deck_name, commander, deck_id)
        
        return self.connection.execute_query(query, params, False)

    #DELETE
    def delete_deck(self, user_id, DID):
        """
        args:
            user_id (String) - user id
            deck_name (String) - name of deck
        return:
            (int) - number of affected rows

        All asociated cards with the deleted deck are deleted as well
        """
        query = "DELETE FROM \"deck\" WHERE \"userId\" = %s AND \"DID\" = %s;"
        params = (user_id, DID)

        return self.connection.execute_query(query, params, False)