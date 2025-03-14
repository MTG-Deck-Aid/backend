from django.http import HttpResponse
from django.urls import path
from .views import *

# Full url route example: localhost:8000/api/health-check/
urlpatterns = [
    # General
    path("", lambda request: HttpResponse("Mystic Tuner Backend API"), name="Mystic Tuner Backend"),
    path("health-check/", lambda request: HttpResponse("Mystic Tuner Backend API - OK"), name="health-check"),
    
    # Decks 
    path('new-deck/', create_new_deck),
    path('decks/commander', get_commander, name="commander"),
    path('decks/verify-cards', verify_cards, name="verify_cards"),
    path('decks/<int:deck_id>/', get_deck),
    path('decks/get-image-links', get_image_links, name="get_image_links"),
    path('decks/verify-cards/', verify_cards, name="verify_cards"),

    # Suggestions
    path("suggestions/", suggestions, name="suggestions"),
]