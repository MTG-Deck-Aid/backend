from django.http import HttpResponse
from django.urls import path
from .views import *
from .views import verify_cards
from .views import get_image_links
from .views import AuthenticateLoginTokenAPIView, SuggestionsAPIView

urlpatterns = [
    path('Authenticate/', AuthenticateLoginTokenAPIView.as_view(), name='Authenticate'),
    path('verify-cards/', VerifyCards.as_view()),
    path('decks/<int:deck_id>/', GetDeck.as_view()),
    path('commander/', GetCommander.as_view()),
    path('new-deck/', CreateNewDeck.as_view()),
    path("health-check/", lambda request: HttpResponse("OK"), name="health-check"),
    path("", lambda request: HttpResponse("Mystic Tuner Backend API"), name="Mystic Tuner Backend"),
    path("suggestions/", SuggestionsAPIView.as_view(), name="suggestions"),
    path('decks/verify-cards', verify_cards, name="verify_cards"),
    path('decks/get-image-links', get_image_links, name="get_image_links"),
]