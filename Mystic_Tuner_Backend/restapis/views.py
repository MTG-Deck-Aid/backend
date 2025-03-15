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
from Mystic_Tuner_Backend.card import Card
import json

from Mystic_Tuner_Backend.deck_suggestions.deck_suggestion_controller import CardSuggestionController
from Mystic_Tuner_Backend.security.security_controller import SecurityController

@api_view(["POST"])
def verify_cards(request):
    try:
        data = request.data
        cardList = data.get("names",[])
        response_data,all_cards_found = ScryFallEngine.batch_validate(cardList)
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
      
@api_view(["POST"])
def suggestions(request):
    """
    Returns: 
    {
        "cards_to_add":[
        {
        "name": "...",
        "reason": "...",
        "image-url": "..."
        }
        ],
        "cards_to_remove":[
        <SAME>
        ],
        "issues":["Not enough cards to remove. Please add more cards to the deck."]
    }
    """
    try:
        CardSuggestionController.validate_request(request.data)
        print("Request validated.")
        suggestions: dict[list] = CardSuggestionController.get_suggestions(request.data)
        print(f"Suggestions generated. \n{suggestions}")

        # Return only required data from the Card objects ()
        cards_to_add = []
        for card_info in suggestions["cards_to_add"]:
            card: Card = card_info["card"]  
            cards_to_add.append({
                "name": card.name,
                "reason": card_info["reason"],
                "imageURL": card.image_url
            })

        cards_to_remove = []
        for card_info in suggestions["cards_to_remove"]:
            card: Card = card_info["card"]
            cards_to_remove.append({
                "name": card.name,
                "reason": card_info["reason"],
                "imageURL": card.image_url
            })
        return Response({"cardsToAdd": cards_to_add, "cardsToRemove": cards_to_remove, "issues": suggestions["issues"]}, status = 200)
    except Exception as e:
        return Response({"error getting suggestions from gemini": str(e)}, status = 400)

@api_view(["POST"])
def get_user_decks(request):
    return Response({"TODO"}, status = status.HTTP_418_IM_A_TEAPOT)

@api_view(["GET"])
def get_deck(request, deck_id = None):
    if(deck_id == None):
            return Response({"TODO"}, status = status.HTTP_418_IM_A_TEAPOT)

    deck_queries = DeckQueries()

    results = deck_queries.get_deck(deck_id)
    try:
        user_id = SecurityController.get_user_id(_unpack_file(request)["auth0Token"])
    except Exception as e:
        return Response({"error authenticating user" : str(e)}, status = 403)
    user_decks = deck_queries.get_user_decks(user_id)

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


@api_view(["PATCH"])
def update_deck(request, deck_id = None):
    return Response({"TODO"}, status = status.HTTP_418_IM_A_TEAPOT)


@api_view(["POST"])
def get_commander(request):
    try:
        commander = _unpack_file(request)["commander"]
    except ParseError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    valid_commander = ScryFallEngine.validate_commander(commander)
    if(valid_commander == None):
        return Response({'error': 'commander name not recognized'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)
    engine = ScryFallEngine()
    return Response({'commander': valid_commander.name, 'images': engine.get_image_links(valid_commander.name)}, status=status.HTTP_200_OK)


@api_view(["POST"])
def create_new_deck(request):
    try:
        deck = _unpack_file(request)
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

@api_view(["GET"])
def get_user_id(request):
    access_token = request.headers.get("Authorization")
    print(f"access token: {access_token}")
    return Response({"userId": SecurityController().get_user_id(access_token)}, status = status.HTTP_200_OK)


@api_view(["GET"])
def autocomplete_search(request):
    try:
        query = request.GET.get("q", "")
        print(f"query: {query}")
        cards: list[str] = ScryFallEngine().autocomplete(query)
        return Response(cards, status = 200)
    except Exception as e:
        return Response({"error getting autocomplete suggestions": str(e)}, status = 400)


def _unpack_file(request):
    print(request)
    file = request.FILES.get('file')

    if not file:
        raise ParseError('No file uploaded')

    try:
        file_data = file.read().decode('utf-8')
        json_data = json.loads(file_data)
        return json_data
    except json.JSONDecodeError:
        raise ParseError('Invalid JSON file')



