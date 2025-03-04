from database_connector import database_connector

class card_queries():
    """
    Class for creating queries related to the Card Table
    """
    def __init__(self):
        self.connection = database_connector.get_instance()

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

        for card in cards:
            if card['count'] is None or card['count'] <= 0:
                print(f'card count must be greater than zero For card: {card['cardname']}')
                return False


        query = "SELECT * FROM public.\"Card\" WHERE cardname IN %s;"

        card_names = [card['cardname'] for card in cards]

        params = (tuple(card_names), )
        results = self.connection.execute_query(query, params)

        if(results == False):
            return results

        
        self._update_count(results, cards, deck_id)

        if(len(cards) != 0):
            query = "INSERT INTO public.\"Card\" (deckid, cardname, sideboard, cardtype, count)VALUES %s;"

            params = [(deck_id, card['cardname'], card['sideboard'], card['cardtype'], card['count']) for card in cards]

            return self.connection.execute_long_query(query, params)


    #READ
    def get_card(self, card_name):
        """
        args:
            card_name (String) - name of card
        return: 
            (List) - list of cards matching the name
        """
        query = "SELECT * FROM public.\"Card\" WHERE \"cardname\" = %s ORDER BY id ASC;"
        params = (card_name,)
        return self.connection.execute_query(query, params)
    
    #UPDATE
    def update_card(self, deck_id, card_name, sideboard, type, count):
        """
        args:
            deck_id (int) - deck id card belongs to
            card_name (String) - name of card to update
            sideboard (boolean) - True if card in sideboard
            type (String) - card type (can be None)
            count (int) - number of the card in deck
        return 
            (int) - number of affected rows 

        replaces all values with the inputted values
        """

        if (count <= 0):
            print(f'card count must be greater than zero For card: {card_name}')
            return False

        query = "UPDATE public.\"Card\" SET \"sideboard\" = %s, \"cardtype\" = %s, \"count\" = %s WHERE \"cardname\" = %s AND \"deckid\" = %s;"
        params = (sideboard, type, count, card_name, deck_id)
        return self.connection.execute_query(query, params, False)

    #DELETE
    def delete_cards_from_deck(self, cards, deck_id):
        """
        args:   
            cards (String[]) - names of cards to delete
            deck_id (int)
        return:
            (int) - number of affected rows 
        """
        query =  "DELETE FROM public.\"Card\" WHERE cardname IN %s AND deckid = %s;"
        params = (tuple(cards), deck_id)

        return self.connection.execute_query(query, params, False)


    #Helper function
    def _update_count(self, results, cards, deck_id):
        """
        args:
            results (List) - existing rows
            cards (List) - rows to be addded
            deck_id (int) - deck being added to
        return:
            Nothing
        """
        for existing_row in results:
            for card in cards:
                if(card['cardname'] != existing_row[2]):
                    continue
                query = "UPDATE public.\"Card\" SET count = count + %s WHERE cardname = %s AND deckid = %s;"
                params = (int(card['count']), existing_row[2], deck_id)
                self.connection.execute_query(query, params, False)
                cards.remove(card)
                break



