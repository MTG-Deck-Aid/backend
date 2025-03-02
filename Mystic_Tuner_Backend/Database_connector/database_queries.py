from database_connector import DatabaseConnector
import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values
class card_queries():
    def __init__(self):
        self.connection = DatabaseConnector.get_instance()

    #CREATE
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
        results = self.connection.execute_query(query, params)

        print(results)
        
        self.update_count(results, cards, deck_id)

        if(len(cards) != 0):
            query = "INSERT INTO public.\"Card\" (deckid, cardname, sideboard, cardtype, count)VALUES %s;"

            params = [(deck_id, card['cardname'], card['sideboard'], card['cardtype'], card['count']) for card in cards]

            return self.connection.execute_long_query(query, params)


    #READ
    def get_card(self, card_name):
        query = "SELECT * FROM public.\"Card\" WHERE \"cardname\" = %s ORDER BY id ASC;"
        params = (card_name,)
        return self.connection.execute_query(query, params)
    
    #UPDATE
    def update_count(self, results, cards, deck_id):
        for existing_row in results:
            for card in cards:
                if(card['cardname'] != existing_row[2]):
                    continue
                query = "UPDATE public.\"Card\" SET count = count + %s WHERE cardname = %s AND deckid = %s;"
                params = (int(card['count']), existing_row[2], deck_id)
                self.connection.execute_query(query, params, False)
                cards.remove(card)
                break
            
    #DELETE
    def delete_cards_from_deck(self, cards, deck_id):
        """
        args:   cards (String[]) - names of cards to delete
                deck_id (int)
        
        """
        query =  "DELETE FROM public.\"Card\" WHERE cardname IN %s AND deckid = %s;"
        params = (tuple(cards), deck_id)

        return self.connection.execute_query(query, params, False)



class deck_queries():
    def __init__(self):
        self.connection = DatabaseConnector.get_instance()

    #CREATE
    def add_deck(self, user_id, deck_type, deck_name):

        for deck in self.get_user_decks(user_id):
            if(deck_name == deck[2]):
                raise ValueError("DeckName already exists")

        query = "INSERT INTO public.\"Deck\" (\"userId\", \"deckType\", \"deckName\") VALUES (%s, %s, %s);"
        params = (user_id, deck_type, deck_name)

        return self.connection.execute_query(query, params, False)

    #READ
    def get_user_decks(self, user_id):
        query = "SELECT * FROM public.\"Deck\" WHERE \"userId\" = %s ORDER BY \"DID\" ASC;"
        params = (user_id,)
        return self.connection.execute_query(query, params)
    
    def get_deck(self, deck_id):
        query = "SELECT * FROM public.\"Card\" WHERE \"deckid\" = %s ORDER BY id ASC;"
        params = (deck_id,)
        return self.connection.execute_query(query, params)
    
    #UPDATE
    def update_deck(self, user_id, deck_type, deck_name, deck_id):
        query = "UPDATE public.\"Deck\" SET \"userId\" = %s, \"decktype\" = %s, \"deckName\" = %s WHERE DID = %s;"
        params = (user_id, deck_type, deck_name, deck_id)
        return self.connection.execute_query(query, params, False)

    #DELETE
    def delete_deck(self, user_id, deck_name):

        query = "DELETE FROM public.\"Deck\" WHERE \"userId\" = %s AND \"deckName\" = %s;"
        params = (user_id, deck_name)

        return self.connection.execute_query(query, params, False)


class card_repository_queries():
    def __init__(self):
        self.connection = DatabaseConnector.get_instance()

    def validate_card(self, card_name):
        query = "SELECT * FROM public.\"CardNames\" where \"name\" = %s;"
        params = (card_name,)
        result = self.connection.execute_query(query, params)

        if len(result) > 0:
            #Card exists in card repository
            return True
        else:
            return False

    def update_card_repository(self, cards):

        query = "INSERT INTO public.\"CardNames\" (name) VALUES %s ON CONFLICT DO NOTHING;"

        params = [(card,) for card in cards]

        return self.connection.excute_long_query(query, params)

    def clear_card_repository(self):

        query = "DELETE FROM public.\"CardNames\""

        return self.connection.execute_query(query, None, False)