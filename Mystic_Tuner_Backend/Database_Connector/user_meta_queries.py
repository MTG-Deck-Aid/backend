from Database_Connector.database_connector import DatabaseConnector
from Database_Connector.deck_queries import DeckQueries

class UserMetaQueries():
    """
    Class for creating queries related to the USER_META Table
    """
    def __init__(self):
        self.connection = DatabaseConnector.get_instance()

    # CREATE
    def create_user(self, user_id: str):
        """
        Creates a new user in the user_meta table.
        Sets the seen_example to false for a new user, and generates them an
        example deck to get started. The example deck's id is stored in the user_meta table.

        args:
            user_id (String) - the user's id
        """
        query = "INSERT INTO \"user_meta\" (id, seen_example, example_did) VALUES (%s, %s, %s);"

        deck_queries = DeckQueries()
        did = deck_queries.generate_example_deck(user_id)

        params = (user_id, False, did)
        return self.connection.execute_query(query, params, False)
    
    # READ
    def user_exists(self, user_id: str):
        """
        args:
            user_id (String) - the user's id
        """
        query = "SELECT * FROM \"user_meta\" WHERE id = %s;"
        params = (user_id,)
        response = self.connection.execute_query(query, params)
        if response:
            return True
        return False
    
    # READ
    def seen_example(self, user_id: str):
        """
        args:
            user_id (String) - the user's id
        """
        query = "SELECT seen_example FROM \"user_meta\" WHERE id = %s;"
        params = (user_id,)
        return self.connection.execute_query(query, params)
    
    # READ
    def get_example_deck(self, user_id: str):
        """
        args:
            user_id (String) - the user's id
        """
        query = "SELECT example_did FROM \"user_meta\" WHERE id = %s;"
        params = (user_id,)
        return self.connection.execute_query(query, params)
    
    def set_example_seen(self, user_id: str):
        """
        args:
            user_id (String) - the user's id
        """
        query = "UPDATE \"user_meta\" SET seen_example = %s WHERE id = %s;"
        params = (True, user_id)
        return self.connection.execute_query(query, params, False)