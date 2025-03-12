from Database_Connector.database_connector import DatabaseConnector

class CardQueries():
    """
    Class for creating queries related to the Card Table
    """
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

        *Note, due to the complexity of how the function does the updating, the returned row_count may not be accurate
        """
        cards = cards.copy()

        for card in cards:
            if card['count'] is None or card['count'] <= 0:
                print(f'card count must be greater than zero For card: {card['cardname']}')
                return False


        results = self._get_cards(cards, deck_id)

        if(results == False):
            return results

        
        rows_affected = self._update_count(results, cards, deck_id)

        if(len(cards) != 0):
            query = "INSERT INTO public.\"Card\" (deckid, cardname, sideboard, cardtype, count)VALUES %s;"

            params = [(deck_id, card['cardname'], card['sideboard'], card['cardtype'], card['count']) for card in cards]

            result = self.connection.execute_long_query(query, params)

            if (result == False):
                return result
            else:
                return result + rows_affected
        return rows_affected


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

    def remove_cards_from_deck(self, cards, deck_id):
        cards = cards.copy()

        for card in cards:
            if card['count'] is None or card['count'] > 0:
                print(f'card count to remove must be less than 0: {card['cardname']}')
                return False


        results = self._get_cards(cards, deck_id)

        if(results == False):
            return results
        
        rows_affected = self._update_count(results, cards, deck_id)

        return rows_affected

    def delete_cards_from_deck(self, cards, deck_id):
        """
        args:   
            cards (String[]) - names of cards to delete
            deck_id (int)
        return:
            (int) - number of affected rows 
        """
        query =  "DELETE FROM public.\"Card\" WHERE cardname IN %s AND deckid = %s;"
        print(cards)
        params = (tuple(cards), deck_id)
        
        return self.connection.execute_query(query, params, False)


    #Helper functions
    def _update_count(self, results, cards, deck_id):
        """
        args:
            results (List) - existing rows
            cards (List) - rows to be addded
            deck_id (int) - deck being added to
        return:
            Nothing
        """
        updated_rows = 0
        for existing_row in results:
            for card in cards:
                if(card['cardname'] != existing_row[2]):
                    continue
                if(existing_row[5] + int(card['count']) <= 0):
                    cards_to_delete = []
                    cards_to_delete.append(card['cardname'])
                    self.delete_cards_from_deck(cards_to_delete, deck_id)
                    break

                query = "UPDATE public.\"Card\" SET count = count + %s WHERE cardname = %s AND deckid = %s;"
                params = (int(card['count']), existing_row[2], deck_id)
                self.connection.execute_query(query, params, False)
                cards.remove(card)
                break
            updated_rows += 1

        
        return updated_rows

    def _get_cards(self, cards, deck_id):


        query = "SELECT * FROM public.\"Card\" WHERE cardname IN %s AND deckid = %s;"

        card_names = [card['cardname'] for card in cards]

        params = (tuple(card_names), deck_id)
        return self.connection.execute_query(query, params)
