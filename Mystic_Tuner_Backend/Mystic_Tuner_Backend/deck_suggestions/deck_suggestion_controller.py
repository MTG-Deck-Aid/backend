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
        returns:
            list[dict] - A list of suggested cards. Where each dictionary contains:
                {
                    "card_to_replace": Card - The card to replace in the decklist.
                    "card_to_add": Card - The card to replace the card with.
                    "reason": str - The reason for the suggestion.
                }
        """

        # Get suggestions
        decklist = Deck.from_json(json_str)
        suggestions = CardSuggestor().suggest_cards(decklist)
        # Find cards needed, replace cards in suggestions with card objects
        scryfall = ScryFallEngine()
        for suggestion in suggestions:
            suggestion["card_to_replace"] = scryfall.search_card(
                suggestion["card_to_replace"]
            )
            suggestion["card_to_add"] = scryfall.search_card(suggestion["card_to_add"])
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
