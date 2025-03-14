from Mystic_Tuner_Backend.deck import Deck
from Mystic_Tuner_Backend.deck_suggestions.card_suggestor import (
    CardSuggestor,
)
from Mystic_Tuner_Backend.scryfall_engine.scryfall_engine import (
    ScryFallEngine,
)


class CardSuggestionController:
    """
    Controller to commuinicate with the frontend.
    Acts as a portion of the Mystic Tuner API.
    """
    @staticmethod
    def validate_request(request: dict) -> None:
        """
        Validate the request from the frontend.
        Ensure that the request is a JSON string.

        params:
            request: dict - The request from the frontend.
        returns:
            None
        """
        if not isinstance(request, dict):
            raise TypeError("Request must be a dictionary.")
        if "decklist" not in request:
            raise ValueError("Request must contain a decklist.")
        if not isinstance(request["decklist"], dict):
            raise TypeError("Decklist must be a dictionary containing the commander and mainboard.")
        if  "commander" not in request["decklist"]:
            raise ValueError("Decklist must contain a commander.")
        if "mainboard" not in request["decklist"]:
            raise ValueError("Decklist must contain a mainboard.")
       

    @staticmethod
    def get_suggestions(json_str: str) -> list[dict]:
        """
        From the provided JSON string, get suggestions for a decklist.
        Calls the deck suggestion routine and then finds the cards needed via Scryfall API
        Converts the list of dictionaries from the subrountine into a JSON string and returns it.

        params:
            json_str: str - The JSON string containing the decklist.
            {
                num_to_add: int - The number of cards to add to the decklist.
                num_to_remove: int - The number of cards to remove from the decklist.
                decklist: dict - The decklist to suggest cards for.
                {
                    commander: str - The commander of the deck.
                    mainboard: list[dict] - The mainboard of the deck.
                    [
                        {
                            name: str - The name of the card.
                            quantity: int - The quantity of the card in the deck.
                        }
                    ]
                }
            }
        returns:
            dict - A list of suggested cards to add and a list of cards to remove stored in a dict. 
            {
                cards_to_add: list[Card] - A list of cards to add to the deck.
                cards_to_remove: list[Card] - A list of cards to remove from the deck.
            }

        """
        # Get suggestions
        decklist = Deck.from_json(json_str["decklist"])
        suggestions: dict = {
            "cards_to_add": [],
            "cards_to_remove": [],
        }

        # Only get suggestions for the requested number of cards, return the first n suggestions
        if json_str["num_to_add"] > 0:
            suggestions["cards_to_add"] = CardSuggestor(CardSuggestor.OperationStrategy.ADD).suggest_cards(decklist)[:json_str["num_to_add"]]

        if json_str["num_to_remove"] > 0:
            suggestions["cards_to_remove"] = CardSuggestor(CardSuggestor.OperationStrategy.REMOVE).suggest_cards(decklist)[:json_str["num_to_remove"]]

        # Find cards needed, replace cards in suggestions with card objects
        scryfall = ScryFallEngine()
        for suggestion in suggestions["cards_to_add"]:
            suggestion["card"] = scryfall.search_card(suggestion["card"], include_image=True) 
        
        for suggestion in suggestions["cards_to_remove"]:
            suggestion["card"] = scryfall.search_card(suggestion["card"], include_image=True)

        return suggestions


if __name__ == "__main__":

    def suggestions():
        """
        EXAMPLE USE ONLY
        REST API CALL FROM FRONTEND --> JSON STRING IN ROUTE /suggestion
        """
        # json_str = request.get_json()
        #suggestions = CardSuggestionController:.get_suggestions({})
        return {
            "status": "success",
            "code": 200,
            "data": suggestions,
        }

    suggestions()
