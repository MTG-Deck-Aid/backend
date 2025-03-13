from Database_Connector.database_connector import DatabaseConnector

class DeckQueries():
    """
    Class for creating queries related to the Deck Table
    """
    def __init__(self):
        self.connection = DatabaseConnector.get_instance()

    #CREATE
    def add_deck(self, user_id, deck_type, deck_name, commander):
        """
        args:
            user_id (int) - user id
            deck_type (String) - type of deck
            deck_name (String) - name for deck (must be unique for the given user)
            commander (String) - name of commander
        return:
            (int) - number of affected rows
        """
        for deck in self.get_user_decks(user_id):
            if(deck_name == deck[2]):
                raise ValueError("DeckName already exists")

        query = "INSERT INTO public.\"Deck\" (\"userId\", \"deckType\", \"deckName\", \"commander\") VALUES (%s, %s, %s, %s);"
        params = (user_id, deck_type, deck_name, commander)

        return self.connection.execute_query(query, params, False)

    #READ
    def get_user_decks(self, user_id):
        """
        args:
            user_id (int) - user id to get decks from
        return:
            (List) - all decks associated with the user
        """
        query = "SELECT * FROM public.\"Deck\" WHERE \"userId\" = %s ORDER BY \"DID\" ASC;"
        params = (user_id,)

        return self.connection.execute_query(query, params)
    
    def get_deck(self, deck_id):
        """
        args:
            deck_id (int) - deck id
        return:
            (List) - the specific deck
        """
        query = "SELECT * FROM public.\"Card\" WHERE \"deckid\" = %s ORDER BY id ASC;"
        params = (deck_id,)

        return self.connection.execute_query(query, params)
    
    #UPDATE
    def update_deck(self, user_id, deck_type, deck_name, deck_id, commander):
        """
        args:
            user_id (int) - user id
            deck_type (String) - type of deck (ex. Standard, Commander)
            deck_name (String) - name of deck 
            decK_id (int) - id of deck to update
            commander (String) - name of commander
        return:
            (int) - number of affected rows

            Overwites existing deck's information with the new data
        """
        query = "UPDATE public.\"Deck\" SET \"userId\" = %s, \"deckType\" = %s, \"deckName\" = %s, \"commander\" = %s WHERE \"DID\" = %s;"
        params = (user_id, deck_type, deck_name, commander, deck_id)
        
        return self.connection.execute_query(query, params, False)

    #DELETE
    def delete_deck(self, user_id, deck_name):
        """
        args:
            user_id (int) - user id
            deck_name (String) - name of deck
        return:
            (int) - number of affected rows

        All asociated cards with the deleted deck are deleted as well
        """
        query = "DELETE FROM public.\"Deck\" WHERE \"userId\" = %s AND \"deckName\" = %s;"
        params = (user_id, deck_name)

        return self.connection.execute_query(query, params, False)