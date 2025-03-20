from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from Database_Connector.card_queries import CardQueries
from Database_Connector.deck_queries import DeckQueries
import json
from django_ratelimit.decorators import ratelimit
from Mystic_Tuner_Backend.scryfall_engine.scryfall_engine import ScryFallEngine
from Mystic_Tuner_Backend.card import Card
import json

from Mystic_Tuner_Backend.deck_suggestions.deck_suggestion_controller import CardSuggestionController
from Mystic_Tuner_Backend.security.security_controller import SecurityController

# =========================================== NON-USER ROUTES  =========================================== #
@api_view(["GET","POST", "PUT", "DELETE", "PATCH"])
def ratelimited_error(request, exception):
    """
    How to return a 429 error when the user is ratelimited. (Default is 403 which is the wrong status code)
    Reference: https://django-ratelimit.readthedocs.io/en/stable/cookbook/429.html 
    """
    return Response({"error": "Too many requests"}, status = 429)


@ratelimit(key="ip", rate="50/m", method="POST", block=True)
@api_view(["POST"])
def verify_cards(request):
    try:
        data = request.data
        cardList = data.get("names",[])
        print(f"cardList: {cardList}")
        response_data,all_cards_found = ScryFallEngine.batch_validate(cardList)
        if all_cards_found == 1:
            return Response(status = 200)
        else:
            return Response({"invalidNames" : response_data}, status = 422)
    except Exception as e:
        print(f"Error: {e}")
        return Response({"error verifying card names": str(e)}, status = 400)

@ratelimit(key="ip", rate="50/m", method="GET", block=True)
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

@ratelimit(key="ip", rate="3/m", method="POST", block=True)
@api_view(["POST"])
def suggestions(request):
    """
    Googel Gemini has a Rate Limit of 15 requests per minute, so we will limit the requests to 3 per minute.
    This allows us to have 5 active users at a time.
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


@ratelimit(key="ip", rate="50/m", method="POST", block=True)
@api_view(["POST"])
def get_commander(request):
    print(" ========== GET COMMANDER ========== ")
    try:
        commander = request.data.get('commander')
        # "commander" is from the JSON file
    except ParseError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    valid_commander = ScryFallEngine.validate_commander(commander)
    if(valid_commander == None):
        return Response({'error': 'commander name not recognized'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)
    engine = ScryFallEngine()
    return Response({'commander': valid_commander.name, 'images': engine.get_image_links(valid_commander.name)}, status=status.HTTP_200_OK)

@ratelimit(key="ip", rate="50/m", method="GET", block=True)
@api_view(["GET"])
def autocomplete_search(request):
    """
    Returns 
    """
    print(" ========== AUTOCOMPLETE SEARCH ========== ")
    try:
        query = request.GET.get("q", "")
        commander_only  = request.GET.get("commander", "false")
        print(f"query: {query}, commander_only: {commander_only}")
        cards: list[str] = ScryFallEngine().autocomplete(query)

        filtered_cards = []
        if commander_only == "true":
            for card_name in cards:
                print(f"card_name: {card_name}")
                card: Card = ScryFallEngine.validate_commander(card_name)
                if card != None:
                    filtered_cards.append(card_name)
        else:
            filtered_cards = cards
        return Response(filtered_cards, status = 200)
    except Exception as e:
        return Response({"error getting autocomplete suggestions": str(e)}, status = 400)

# =========================================== USER ROUTES  =========================================== #
@ratelimit(key="ip", rate="50/m", method="GET", block=True)
@api_view(["GET"])
def get_user_decks(request):
    """
    Get the decks for the user by user id
    """
    print(" ========== GET USER DECKS BY USER ID ========== ")
    user_id, invalid_response = _check_auth(request)
    if invalid_response != None:
        return invalid_response
    
    deck_queries = DeckQueries()
    user_decks = deck_queries.get_user_decks(user_id)
    print(f"user_decks: {user_decks}")
    if user_decks == None:
        return Response({"decks": []}, status = 200)
    
    decks = []
    engine = ScryFallEngine()
    for decklist in user_decks:
        deck_name = decklist[1]
        deck_id = decklist[2]
        
        deck = {
            'name': deck_name,
            'id': deck_id,
        }
        
        if decklist[0] == 'commander':
            deck_commander = decklist[3]    
            imageLinks = engine.get_image_links(deck_commander)
            deck['image_url'] = imageLinks['art_crop']
        print(deck)
        decks.append(deck)
        
    return Response({ 'message': 'success', 'status': '200', 'decks': decks}, status = 200)

@ratelimit(key="ip", rate="30/m", method="GET", block=True)
@api_view(["GET"])
def get_deck(request):
    """
    request.data = {
        "deck_id": 1,
    }
    """
    print(" ========== GET DECK BY DECK ID & USER ID ========== ")
    try:
        deck_id = int(request.GET.get("deck_id", None))
    except Exception as e:
        return Response({"error": "deck_id must be an integer"}, status = 400)

    user_id, invalid_response =  _check_auth(request)
    if invalid_response != None:
        return invalid_response

    if(deck_id == None):
        return Response({"No Deck ID provided"}, status = status.HTTP_400_BAD_REQUEST)

    deck_queries = DeckQueries()
    card_list: list[tuple] = deck_queries.get_deck(deck_id)
    user_decks: list[tuple] = deck_queries.get_user_decks(user_id)
    print(f"card_list: {card_list}")
    print(f"user_decks: {user_decks}")
    if card_list == None or user_decks == None:
        return Response({"Error" : "couldn't retrieve data"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Same deck id, and belongs to the user id
    the_deck:dict = None
    # Check that the deck belongs to the user, and that the deck id is correct
    for usr_deck in user_decks:
        usr_deck_user_id: int = usr_deck[4]
        usr_deck_id:int = usr_deck[2]
        if ((usr_deck_id == deck_id) and (usr_deck_user_id == user_id)):
            game_type: str = usr_deck[0]
            deck_name: str = usr_deck[1]
            commander: str = None
            if game_type == "commander":
                commander = usr_deck[3]
            the_deck = {
                "game_type": game_type,
                "deck_name": deck_name,
                "deck_id": usr_deck_id,
                "commander": commander
            }
            break

    if the_deck == None:
        return Response({"Error" : "Deck not found"}, status = status.HTTP_404_NOT_FOUND)

    cards = []
    for card in card_list:
        cards.append({'name':card[2], 'quantity': card[5], 'sideboard': card[3], 'cardtype': card[4]})# Currently only name and quantity are supported
    the_deck['cards'] = cards
    print(f"response: {cards}")  
    return Response({"deck" : the_deck}, status = status.HTTP_200_OK)

@ratelimit(key="ip", rate="30/m", method="POST", block=True)
@api_view(["PATCH"])
def update_deck(request):
    """
    request.data = {
        "deck_id": 1,
        "cardsAdded": [
            {
                "name": "cardname",
                "quantity": 3
            }
        ],
        "cardsRemoved": [
            {
                "name": "cardname",
                "quantity": 3
            }
        ]
    """
    print(" ========== UPDATE DECK ========== ")
    data: dict = request.data
    deck_id: int = data.get("deck_id", None)
    if deck_id == None:
        return Response({"No Deck ID provided"}, status = 401)
    
    cards_added: list[dict] = data.get("cardsAdded", None)
    cards_removed: list[dict] = data.get("cardsRemoved", None)

    user_id, invalid_response =  _check_auth(request)
    if invalid_response != None:
        return invalid_response

    # Format the cards for the canned transaction    
    for card in cards_added:
        card['count'] = card['quantity']
        del card['quantity']
        card['cardname'] = card['name']
        del card['name']
        card['sideboard'] = False
        card['cardtype'] = ""

    # Format the cards for the canned transaction
    for card in cards_removed:
        card['count'] = card['quantity']
        del card['quantity']
        card['cardname'] = card['name']
        del card['name']
        card['sideboard'] = False
        card['cardtype'] = ""

    # Call the canned transaction
    cardQueries = CardQueries()
    if cards_added != None:
        cardQueries.add_cards_to_deck(cards_added, deck_id)

    if cards_removed != None:
        cardQueries.remove_cards_from_deck(cards_removed, deck_id) # TODO fix remove cards from deck
    return Response({"message": "Successfully updated deck"}, status = 200)


    



@ratelimit(key="ip", rate="10/m", method="POST", block=True)
@api_view(["POST"])
def create_new_deck(request):
    print(" ========== CREATE NEW DECK ========== ")
    deck = request.data
    print(f"deck: {deck}")
    commander = deck['commander']
    deck_name = deck['deckName']
    
    user_id = SecurityController().get_user_id(request.headers.get("Authorization").split(" ")[1])
    cards = json.loads(deck['deckList'])

    deck_queries = DeckQueries()

    result = deck_queries.add_deck(user_id, 'commander', deck_name, commander)

    if result == False:
        return Response({'error' : 'Deck name already exists'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

    decks = deck_queries.get_user_decks(user_id)
    deck = None

    for item in decks:
        if item[1] == deck_name:
            deck = item
            break
    print(f"new deck created: {deck}")

    if deck == None:
        return Response({'error' : 'couldn\'t create deck'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    formatted_list = []
    for card in cards:
        formatted_list.append({'cardname': card['name'], 'sideboard': False, 'cardtype': None, 'count': card['quantity']})
    
    print(f"cards to add: {formatted_list}")

    card_queries = CardQueries()

    result = card_queries.add_cards_to_deck(formatted_list, deck[2])
    print(f"result: {result}")

    if result == False:
        deck_queries.delete_deck(user_id, deck_name)
        return Response({'error' : 'Could not populate deck'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)


    return Response({"message": "Successfully built deck", 'deckId' : deck[3]}, status = status.HTTP_200_OK)





# =========================================== TEST ROUTES  =========================================== #
@api_view(["GET"])
def get_user_id(request):
    """
    NOTE: THIS IS A TEST ROUTE AND SHOULD NOT BE USED IN PRODUCTION
    """
    access_token = request.headers.get("Authorization")
    access_token = access_token.split(" ")[1]
    print(f"access token: {access_token}")
    return Response({"userId": SecurityController().get_user_id(access_token)}, status = status.HTTP_200_OK)

# =========================================== HELPERS  =========================================== #
def _check_auth(request) -> tuple[int, Response]:
    """
    Helper function to check if the user is authenticated
    """
    try:
        user_id: str = SecurityController().get_user_id(request.headers.get("Authorization").split(" ")[1])
        if user_id == -1:
            return user_id, Response({"error": "Invalid user token"}, status = 401)
        return user_id, None
    except Exception as e:
        return -1, Response({"Failed to Authenticate User": str(e)}, status = 401)


