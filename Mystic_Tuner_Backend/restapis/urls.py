from django.urls import path
from .views import verify_cards

urlpatterns = [
    path('decks/verify-cards', verify_cards, name="verify_cards"),
]