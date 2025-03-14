from abc import ABC, abstractmethod
import json
import os
from Mystic_Tuner_Backend.deck import Deck
from google import genai
from dotenv import load_dotenv

from Mystic_Tuner_Backend.game import Commander, Game


class CardSuggestor:
    """
    Suggests MTG cards for a provided decklist.

    Utilizes Strategy Pattern to allow different Machine Learning models to be used for card suggestions.
    The default model is a Google Gemini Model, see that strategy for more information.
    """

    def __init__(self):
        try:
            with open("prompt.txt", "r") as f:
                self.prompt = f.read()
        except Exception as e:
            print("An error occured when reading the prompt file: ", e)
            raise e

        self.model_strategy: DeckListTuner = GeminiDeckListTuner()

    def set_model_strategy(self, model_strategy):
        self.model_strategy = model_strategy

    def suggest_cards(self, decklist: Deck) -> list[dict]:
        """
        Suggests cards for a provided decklist.

        params:
            decklist: Deck - The decklist to suggest cards for.
        returns:
            list[dict] - two lists of cards, one set to replace and one set to add. Only contains the names, and reasons.
        """
        return self.model_strategy.generate(self.prompt, decklist)


class DeckListTuner(ABC):
    """
    Abstract base class for the Strategy Pattern.
    Future Models used for card suggestions should inherit from this class.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def _format_prompt(self, deck: Deck) -> str:
        """
        Formats the prompt with the deck information. See the prompt.txt file for the format.
        """
        pass

    @abstractmethod
    def _clean_response(self, response: dict) -> list[dict]:
        """
        Cleans the response from the model to a list of suggestions.
        """
        pass

    @abstractmethod
    def generate(self, prompt: str, decklist: Deck) -> list[dict]:
        """
        Suggests cards for a provided deck.
        ---
        params:
            deck: Deck - The deck to suggest cards for.
        returns:
            list[dict] - A list of suggested cards. Where each dictionary contains:
                {
                    "card_to_replace": str - The card to replace in the deck.
                    "card_to_add": str - The card to replace the card with.
                    "reason": str - The reason for the suggestion.
                }
        """
        pass


class GeminiDeckListTuner(DeckListTuner):
    """
    Uses Google's Gemini API to suggest cards for a provided decklist.
    Handles all API requests and responses to this external REST API.
    """

    def __init__(self):
        load_dotenv()
        self.client: genai.Client = genai.Client(
            api_key=os.environ.get("GEMINI_API_KEY")
        )

    def _format_prompt(self, deck: Deck) -> str:
        # Include only the necessary information for the API request
        game_type = f"{deck.game}"

        # Generate a list of cards with their quantities
        card_json_list = []
        for card in deck.card_list:
            card_json = {
                "name": card.name,
                "quantity": deck.card_list.count(card),
                "colors": [color.value for color in card.colors],
            }
            if card_json not in card_json_list:
                card_json_list.append(card_json)
            else:
                for card in card_json_list:
                    if card["name"] == card_json["name"]:
                        card["quantity"] += card_json["quantity"]

        deck_json = {
            "deckName": deck.name,
            "gameType": f"{deck.game}",
            "gameQuantity": deck.game.card_quantity,
            "cards": card_json_list,
        }

        if game_type == Game.Type.COMMANDER.value:
            game: Commander = deck.game
            deck_json["commander"] = game.commander.name
        return str(deck_json)

    def _clean_response(self, response_text: str) -> list[dict]:
        """
        params:
            response_text: str - The response from the Gemini API.
                ```python
                [
                    {
                        "card_to_replace": "",
                        "card_to_add": "Grave Pact",
                        "reason": "More sacrifice synergy with Marchesa and token generation for board control."
                    },
                ]
                ```

        returns:
            dict - A list of dictionaries containing the suggestions.
        """
        # Remove the extra characters from the response
        response_text = response_text.replace("```python", "")
        response_text = response_text.replace("```", "")
        return json.loads(response_text)

    def generate(self, prompt: str, deck: Deck) -> list[dict]:
        """
        Returns a list of card suggestions for a provided deck.

        - If the card_to_replace is an empty string, then the card_to_add
        is a new card to add to the deck, as the deck is under the minimum card count.
        """
        prompt = prompt.replace("[INSERT_CARD_LIST_HERE]", self._format_prompt(deck))
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        return self._clean_response(response.text)


if __name__ == "__main__":
    # Example Usage
    card_suggestor = CardSuggestor()
    decklist = Deck.from_file("./_tests/decklist.json")
    suggestions = card_suggestor.suggest_cards(decklist)
    print(type(suggestions))
    print(suggestions)
