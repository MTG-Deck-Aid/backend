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
from Database_Connector.user_meta_queries import UserMetaQueries

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
    """
    Params:
        List of strings representing a user deck
    Returns:
        List of strings containing any invalid names from the provided list
    """
    try:
        data = request.data
        cardList = data.get("names",[])
        print(f"cardList: {cardList}")
        response_data,all_cards_found = ScryFallEngine.batch_validate(cardList)
        if all_cards_found == 1:
            return Response({"invalidNames" : []}, status = 200)
        else:
            return Response({"invalidNames" : response_data}, status = 422)
    except Exception as e:
        print(f"Error: {e}")
        return Response({"error verifying card names": str(e)}, status = 400)

@ratelimit(key="ip", rate="50/m", method="GET", block=True)
@api_view(["GET"])
def get_image_links(request):
    """
    Params:
        singular card name
    Returns:
        dict of image links associated with the card provided
    """
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
    """
    Params:
        name of a single commander
    Returns:
        dict with card data associated with the requested commander
    """
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
                card: Card = ScryFallEngine.validate_commander(card_name)
                if card != None:
                    filtered_cards.append(card_name)
        else:
            filtered_cards = cards
        print(f"top 3 cards: {filtered_cards[:3]}")
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
        # Display the example deck
        # 
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
            print(f"deck_commander: {deck_commander}")
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

@ratelimit(key="ip", rate="30/m", method="DELETE", block=True)
@api_view(["DELETE"])
def delete_deck(request):
    """
    Deletes the deck from the database

    https://localhost:8000/api/decks/delete/?deckId=1
    """
    print(" ========== DELETE DECK BY DECK ID & USER ID ========== ")
    try:
        deck_id = int(request.GET.get("deckId", None))
    except Exception as e:
        return Response({"error": "deckId must be an integer"}, status = 400)

    user_id, invalid_response =  _check_auth(request)
    if invalid_response != None:
        return invalid_response

    if(deck_id == None):
        return Response({"No Deck ID provided"}, status = status.HTTP_400_BAD_REQUEST)

    deck_queries = DeckQueries()
    user_decks = deck_queries.get_user_decks(user_id)
    if user_decks == None:
        return Response({"Error" : "couldn't retrieve data"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    try:
        # Check that the deck belongs to the user, and that the deck id is correct
        for usr_deck in user_decks:
            usr_deck_user_id: int = usr_deck[4]
            usr_deck_id:int = usr_deck[2]
            if ((usr_deck_id == deck_id) and (usr_deck_user_id == user_id)):
                deck_queries.delete_deck(user_id, deck_id)
            
        # Delete all cards from the deck
        card_queries = CardQueries()
        cards = card_queries.get_all_cards(deck_id)
        card_queries.delete_cards_from_deck(deck_id = deck_id, cards = [card[2] for card in cards])
            
        # Clean up check
        _handle_deck_example(user_id, deck_id)
        return Response({"message": "Successfully deleted deck"}, status = 200)
    except Exception as e:
        return Response({"Error" : "Deck not found"}, status = status.HTTP_404_NOT_FOUND)

@ratelimit(key="ip", rate="30/m", method="PATCH", block=True)
@api_view(["PATCH"])
def update_deck(request):
    """
    Updates the entire deck with the new decklist
    http://localhost:8000/api/decks/update/
    request.data = {
        "deckId": 1,
        "deckName": "new deck name",
        "commander": "new commander name"
        "deckList": [
            {
                "name": "cardname",
                "quantity": 3
            }
        ]
    }
    """
    print(" ========== UPDATE DECK BY DECK ID & USER ID ========== ")
    # Validate user input
    try:
        deck_id = int(request.data.get("deckId", None))
        deck_name = request.data.get("deckName", None)
        commander = request.data.get("commander", None)
        decklist: list[dict] = request.data.get("deckList", None)
        print(f"deck_id: {deck_id}, deck_name: {deck_name}, commander: {commander}, decklist: {decklist}")

        if(deck_id == None or deck_name == None or commander == None or decklist == None):
            return Response({"Please provide all the deck information"}, status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "deck_id must be an integer"}, status = status.HTTP_400_BAD_REQUEST)

    # Validate user is authenticated
    user_id, invalid_response =  _check_auth(request)
    if invalid_response != None:
        return invalid_response


    deck_queries = DeckQueries()
    card_queries = CardQueries()
    user_decks = deck_queries.get_user_decks(user_id)
    if user_decks == None:
        return Response({"Error" : "couldn't retrieve data"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Check that the deck belongs to the user, and that the deck id is correct
    for usr_deck in user_decks:
        usr_deck_user_id: int = usr_deck[4]
        usr_deck_id:int = usr_deck[2]
        found_the_deck = (usr_deck_id == deck_id) and (usr_deck_user_id == user_id)
        if (found_the_deck):
            deck_queries.update_deck(user_id, usr_deck[0], deck_name, deck_id, commander)
            # Get the current deck list from the database
            current_deck_list: list[tuple] = deck_queries.get_deck(deck_id)
            
            # Remove the current deck list from the database
            for card in current_deck_list:
                card_queries.delete_cards_from_deck([card[2]], deck_id)
                
            # Add the new deck list to the database
            for card in decklist:
                card_queries.add_cards_to_deck([{'cardname': card['cardName'], 'sideboard': False, 'cardtype': None, 'count': card['quantity']}], deck_id)
            return Response({"message": "Successfully updated deck"}, status = 200)
        
    return Response({"Error" : "Deck not found"}, status = status.HTTP_404_NOT_FOUND)



@ratelimit(key="ip", rate="30/m", method="PATCH", block=True)
@api_view(["PATCH"])
def add_remove_cards(request):
    """
    Appends and pops cards from the deck in the database

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
    print(" ========== UPDATE CARDS IN A DECK ========== ")
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
        cardQueries.remove_cards_from_deck(cards_removed, deck_id)
    return Response({"message": "Successfully updated deck"}, status = 200)


    



@ratelimit(key="ip", rate="10/m", method="POST", block=True)
@api_view(["POST"])
def create_new_deck(request):
    print(" ========== CREATE NEW DECK ========== ")
    data = request.data
    print(f"frontend data: {data}")
    deck_name = data['deckName']
    commander = data['commander']
    cards = data['deckList']
    
    user_id = SecurityController().get_user_id(request.headers.get("Authorization").split(" ")[1])

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
        formatted_list.append({'cardname': card['cardName'], 'sideboard': False, 'cardtype': None, 'count': card['quantity']})
    
    print(f"Adding cards to {deck_name}: {formatted_list}")

    card_queries = CardQueries()

    result = card_queries.add_cards_to_deck(formatted_list, deck[2])
    print(f"Adding cards result: {result}")

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
        elif type(user_id) == str:
            _handle_new_user(user_id)
            return user_id, None
        return user_id, None
    except Exception as e:
        return -1, Response({"Failed to Authenticate User": str(e)}, status = 401)


def _handle_new_user(user_id: str) -> None:
    """
    Helper function to check if the user is new, if they are, add them to the database
    """
    user_meta_queries = UserMetaQueries()
    result = user_meta_queries.user_exists(user_id)
    if result == False:
        print("User does not exist, creating new user.")
        user_meta_queries.create_user(user_id)

def _handle_deck_example(user_id: str, did: int) -> None:
    """
    Helper function to check if the user has deleted the example deck, if they have permanently
    mark they're user meta as seen
    """
    user_meta_queries = UserMetaQueries()
    response = user_meta_queries.get_example_deck(user_id)
    example_did = response[0][0]
    if int(example_did) == int(did):
        print("User has deleted the example deck, marking user as seen.")
        user_meta_queries.set_example_seen(user_id)

