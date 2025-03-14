from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from Database_Connector.card_queries import CardQueries
from Database_Connector.deck_queries import DeckQueries
import json

from Mystic_Tuner_Backend.scryfall_engine.scryfall_engine import ScryFallEngine
from .scryfall_utils import batch_validate, validate_commander
from Mystic_Tuner_Backend.card import Card
import json

from Mystic_Tuner_Backend.deck_suggestions.deck_suggestion_controller import CardSuggestionController

# Create your views here.

@api_view(["POST"])
def verify_cards(request):
    try:
        data = request.data
        cardList = data.get("names",[])
        response_data,all_cards_found = batch_validate(cardList)
        if all_cards_found == 1:
            return Response(status = 200)
        else:
            return Response(json.dumps(response_data), status = 422)
    except Exception as e:
        return Response({"error verifying card names": str(e)}, status = 400)
    
@api_view(["GET"])
def get_image_links(request):
    try:
        card_name = request.data.get("name")
        if not card_name:
            return Response({"error": "No card name provided"}, status = 400)
        engine = ScryFallEngine()
        image_links = engine.get_image_links(card_name)
        if not image_links:
            return Response({"error": "No image links found"}, status = 404)
        return Response(image_links, status = 200)
    except Exception as e:
        return Response({"error getting image links": str(e)}, status = 400)
      
class AuthenticateLoginTokenAPIView(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "This is a verified user!"})
    

class VerifyCards(APIView):
    def post(self, request):
        try:
            cards = unpack_file(request)['deckList']
        except ParseError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        engine = ScryFallEngine()
        invalid_cards = []
        for card in cards:
            print(card)
            result = engine.search_card(card['name'])
            if result is None:
                invalid_cards.append(card['name'])

        if len(invalid_cards) > 0:
            return Response({'message': 'Unrecognized cards found', 'data': invalid_cards}, status=status.HTTP_206_PARTIAL_CONTENT)

        return Response({'message': 'All cards identified'}, status=status.HTTP_200_OK)
    
class GetUserDecks(APIView):
    def post(self, request):
        return Response({"TODO"}, status = status.HTTP_418_IM_A_TEAPOT)

class GetDeck(APIView):
    def get(self, request, deck_id = None):

        if(deck_id == None):
            return Response({"TODO"}, status = status.HTTP_418_IM_A_TEAPOT)

        deck_queries = DeckQueries()

        results = deck_queries.get_deck(deck_id)


        user_decks = deck_queries.get_user_decks(100) # TODO fix to use user id token return from auth0

        if results == None or user_decks == None:
            return Response({"Error" : "couldn't retrieve data"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        deck = None
        for item in user_decks:
            if item[3] == deck_id:
                deck = item
                break

        response = []

        for result in results:
            if result[2] == deck[4]:
                response.append({'commander' : result[2]})
            response.append({'cardname':result[2], 'sideboard': result[3], 'cardtype': result[4], 'count': result[5]})


        return Response({"deck" : response}, status = status.HTTP_200_OK)
    
    def patch(self, request, deck_id = None):
        return Response({"TODO"}, status = status.HTTP_418_IM_A_TEAPOT)


class GetCommander(APIView):
    def get(self, request):
        try:
            commander = unpack_file(request)
        except ParseError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        print(commander)
        valid_commander = validate_commander(commander)

        if(valid_commander == None):
            return Response({'error': 'commander name not recognized'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)
        engine = ScryFallEngine
        return Response({'commander': valid_commander.name, 'images': engine.get_image_links(valid_commander.name)}, status=status.HTTP_200_OK)

class CreateNewDeck(APIView):
    def post(self, request):
        try:
            deck = unpack_file(request)
        except ParseError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
        commander = deck['commander']
        deck_name = deck['deckName']
        
        user_id = deck['userId']
        cards = deck['deckList']

        deck_queries = DeckQueries()

        result = deck_queries.add_deck(user_id, 'commander', deck_name, commander)

        if result == False:
            return Response({'error' : 'Deck name already exists'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

        decks = deck_queries.get_user_decks(user_id)

        deck = None

        for item in decks:
            if item[2] == deck_name:
                deck = item
                break

        print(f"deck: {deck}")
        if deck == None:
            return Response({'error' : 'couldn\'t create deck'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

        formatted_list = []
        for card in cards:
            formatted_list.append({'cardname': card['name'], 'sideboard': False, 'cardtype': None, 'count': card['quantity']})
        
        print(f"formatted_list: {formatted_list}")

        card_queries = CardQueries()

        result = card_queries.add_cards_to_deck(formatted_list, deck[3])

        if result == False:
            deck_queries.delete_deck(user_id, deck_name)
            return Response({'error' : 'Could not populate deck'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)


        return Response({"message": "Successfully built deck", 'deckId' : deck[3]}, status = status.HTTP_200_OK)

def unpack_file(request):
    file = request.FILES.get('file')

    if not file:
        raise ParseError('No file uploaded')

    try:
        file_data = file.read().decode('utf-8')
        json_data = json.loads(file_data)
        return json_data
    except json.JSONDecodeError:
        raise ParseError('Invalid JSON file')

class SuggestionsAPIView(APIView):
    authentication_classes = []
    permission_classes = [] # Guest or Authenticated User
    
    def post(self, request: dict):
        """
        Creates a CardSuggestionController object and returns the suggestions
        """
        
        print(request.data)
        CardSuggestionController.validate_request(request)
        return Response({"message": "Gemini Suggestions Coming Soon!"})

        # TODO suggestions = CardSuggestionController.get_suggestions(request.data)
