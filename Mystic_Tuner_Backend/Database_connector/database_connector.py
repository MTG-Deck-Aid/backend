import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

class DatabaseConnector():
    """
    Singleton connector class that excutes queries passed to it
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if (cls._instance is None):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host, database_name, user, password, port):
        """
        args:
            host (String) - host IP 
            database_name (String) - name of database
            user (String) - database user username
            password (String) - database user password
            port (int) - port of the database
        return:
            nothing
        """
        try:
            self.connection = psycopg2.connect(
                host = host,
                dbname = database_name,
                user = user,
                password = password,
                port = port
            )
            print("Connection successfully established with database")

        except Exception as e:
            print(f"Could not establish connection to database: {e}")

    @staticmethod
    def get_instance(self):
        """
        args:
            Nothing
        return:
            (DatabaseConnector) - singleton instance of the database connector
        """
        if self._instance == None:
            self._instance = DatabaseConnector()
        return self._instance

    def execute_query(self, query, params = None, is_select = True):
        """
        args:
            query (String) - base SQL query
            params (tuple) - tuple of values for the query
            is_select (boolean) - true if the query is a select query
        return:
            results of query
                - list of rows for select queries (List)
                - number of rows affected for all other (int)
        
        designed for majority of possible SQL queries
        """
        try:

            cursor = self.connection.cursor()

            if(params == None):
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            
            row_count = cursor.rowcount

            print(f"Rows affected: {row_count}")
            if(is_select):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return row_count
        except Exception as e:
            print(f"With query: {query}\nWith params: {params}\nHas error: {e}")
            return False

    def execute_long_query(self, query, params):
        """
        args:
            query (String) - base SQL query
            params (tuple) - tuple of values for the query
            is_select (boolean) - true if the query is a select query
        return:
            (int) number of rows affected 
        
        designed for the few more complex SQL queries; typically queries involving inserting 
        a bulk of rows at once
        """
        try:
            cursor = self.connection.cursor()

            execute_values(cursor, query, params)

            self.connection.commit()

            row_count = cursor.rowcount
            print(f"Rows affected: {row_count}")
            return row_count

        except Exception as e:
            print(f"With query: {query}\nWith params: {params}\nHas error: {e}")
            return False





















#DELETE after testing
    def get_deck(self, deck_id):
        query = "SELECT * FROM public.\"Card\" WHERE \"deckid\" = %s ORDER BY id ASC;"
        params = (deck_id,)
        return self.execute_query(query, params)

    def get_card(self, card_name):
        query = "SELECT * FROM public.\"Card\" WHERE \"cardname\" = %s ORDER BY id ASC;"
        params = (card_name,)
        return self.execute_query(query, params)
    
    def get_user_decks(self, user_id):
        query = "SELECT * FROM public.\"Deck\" WHERE \"userId\" = %s ORDER BY \"DID\" ASC;"
        params = (user_id,)
        return self.execute_query(query, params)

    def validate_card(self, card_name):
        query = "SELECT * FROM public.\"CardNames\" where \"name\" = %s;"
        params = (card_name,)
        result = self.execute_query(query, params)

        if len(result) > 0:
            #Card exists in card repository
            return True
        else:
            return False
    
    def add_cards_to_deck(self, cards, deck_id):
        """
        arguments:
        cards: a list of dictionaries with the format of each dictionary being:
        cardname: string
        sideboard: boolean
        cardtype: string (can be None)
        count: integer
        deckid: the deck to insert the cards into

        EXAMPLE:
        cards = [
        {'cardname': 'Card A', 'sideboard': False, 'cardtype': 'Creature', 'count': 3},
        {'cardname': 'Card B', 'sideboard': True, 'cardtype': 'Sorcery', 'count': 2}
        ]

        If an inputted card already exists within the deck, instead the count of that row is incremented by the
        value passed in by the list.
        """
        cards = cards.copy()
        query = "SELECT * FROM public.\"Card\" WHERE cardname IN %s;"

        card_names = [card['cardname'] for card in cards]

        print(card_names)
        params = (tuple(card_names), )
        results = self.execute_query(query, params)

        print(results)

        for existing_row in results:
            for card in cards:
                if(card['cardname'] != existing_row[2]):
                    continue
                   
                print(f"Cardname: {card['cardname']}, existing count: {existing_row[5]}, added count: {card['count']}")

                print(existing_row[2])
                query = "UPDATE public.\"Card\" SET count = count + %s WHERE cardname = %s AND deckid = %s;"
                params = (int(card['count']), existing_row[2], deck_id)
                self.execute_query(query, params, False)
                cards.remove(card)
                break
            
        
        if(len(cards) != 0):
            query = "INSERT INTO public.\"Card\" (deckid, cardname, sideboard, cardtype, count)VALUES %s;"

            params = [(deck_id, card['cardname'], card['sideboard'], card['cardtype'], card['count']) for card in cards]
            print(params)
            execute_values(self.connection.cursor(), query, params)

            self.connection.commit()

    def delete_cards_from_deck(self, cards, deck_id):
        """
        args:   cards (String[]) - names of cards to delete
                deck_id (int)
        
        """
        query =  "DELETE FROM public.\"Card\" WHERE cardname IN %s AND deckid = %s;"
        params = (tuple(cards), deck_id)

        self.execute_query(query, params, False)

    def add_deck(self, user_id, deck_type, deck_name):

        for deck in self.get_user_decks(user_id):
            if(deck_name == deck[2]):
                raise ValueError("DeckName already exists")

        query = "INSERT INTO public.\"Deck\" (\"userId\", \"deckType\", \"deckName\") VALUES (%s, %s, %s);"
        params = (user_id, deck_type, deck_name)

        self.execute_query(query, params, False)

    def delete_deck(self, user_id, deck_name):

        query = "DELETE FROM public.\"Deck\" WHERE \"userId\" = %s AND \"deckName\" = %s;"
        params = (user_id, deck_name)

        self.execute_query(query, params, False)

    def update_card_repository(self, cards):

        query = "INSERT INTO public.\"CardNames\" (name) VALUES %s ON CONFLICT DO NOTHING;"

        params = [(card,) for card in cards]
        execute_values(self.connection.cursor(), query, params)

        self.connection.commit()

    def clear_card_repository(self):

        query = "DELETE FROM public.\"CardNames\""

        self.execute_query(query, None, False)