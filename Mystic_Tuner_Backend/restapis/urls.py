from django.urls import path
from .views import *

urlpatterns = [
    path('Authenticate/', AuthenticateLoginTokenAPIView.as_view(), name='Authenticate'),
    path('', HelloWorld.as_view()),
    path('verify-cards/', VerifyCards.as_view()),
    path('decks/<int:deck_id>/', GetDeck.as_view()),
    path('commander/', GetCommander.as_view()),
    path('new-deck/', CreateNewDeck.as_view()),
    path('suggestions/', GetSuggestions.as_view())
]