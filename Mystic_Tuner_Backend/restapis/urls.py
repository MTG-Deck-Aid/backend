from django.http import HttpResponse
from django.urls import path

from Mystic_Tuner_Backend import settings
from .views import *

# Full url route example: localhost:8000/api/health-check/
urlpatterns = [
    # General
    path("", lambda request: HttpResponse("Mystic Tuner Backend API"), name="Mystic Tuner Backend"),
    path("health-check/", lambda request: HttpResponse("Mystic Tuner Backend API - OK"), name="health-check"),
    
    # Decks 
    path('decks/new-deck/', create_new_deck),
    path('decks/commander', get_commander, name="commander"),
    path('decks/verify-cards/', verify_cards, name="verify_cards"),
    path('decks/deck', get_deck),
    path('decks/update/', update_deck),
    path('decks/delete/', delete_deck),
    path('decks/add_remove_cards/', add_remove_cards),
    path('decks/user-decks', get_user_decks),
    path('decks/get-image-links', get_image_links, name="get_image_links"),
    #path('decks/verify-cards/', verify_cards, name="verify_cards"),
    path("decks/autocomplete/", autocomplete_search, name="autocomplete_search"),

    # Suggestions
    path("suggestions/", suggestions, name="suggestions"),
]

# TEST ROUTES
if settings.DEBUG:
    # print in red
    print("\033[91m " + "DEBUG MODE ENABLED")
    print("THESE ROUTES ARE FOR TESTING PURPOSES ONLY. IF YOU SEE THIS MESSAGE IN PRODUCTION, DEBUG IS ENABLED.")
    print("\033[0m")
    test_routes = [path("test/get-user-id/", get_user_id, name="get_user_id"),]
    urlpatterns.extend(test_routes)
