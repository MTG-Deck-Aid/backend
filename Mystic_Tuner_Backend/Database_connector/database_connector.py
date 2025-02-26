import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

class DatabaseConnector():
    __instance = None

    def __new__(cls, *args, **kwargs):
        if (cls.__instance is None):
            cls.__instance = super().__new__(cls)
        return cls.__instance



    def __init__(self):
        # Database connection parameters
        self.host = "localhost"  # Example: localhost or an IP address
        self.dbname = "Mystic_Tuner_Application"  # Your database name
        self.user = "MT_Admin"  # Your database username
        self.password = "admin"  # Your database password
        self.port = "5433"  # Default PostgreSQL port

        try:
            self.connection = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print("Connection successful")

        except Exception as e:
            print(f"Error: {e}")

    def execute_query(self, query, params = None, is_select = True):
        try:

            cursor = self.connection.cursor()

            if(params == None):
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            


            print(f"Rows affected: {cursor.rowcount}")
            if(is_select):
                return cursor.fetchall()
            else:
                self.connection.commit()
        except Exception as e:
            print(f"With query: {query}\nWith params: {params}\nHas error: {e}")
            return False


    def test_connection(self):
        """
        params: self
        returns: boolean
        
        attempts to establish connection to the Mystic_Tuner_Application database server
        main purpose is for troubleshooting.  Returns true if the connection was successful
        """

        result = self.execute_query("SELECT version();")

        if(result != False):
            print(F"Connection successfully established: {result}")
            return True
        else:
            print("Failled to connect to database")
            return False

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
        
        query =  "DELETE FROM public.\"Card\" WHERE cardname IN %s AND deckid = %s;"
        cardnames = [card['cardname'] for card in cards]
        params = (tuple(cardnames), deck_id)

        print(cardnames)
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