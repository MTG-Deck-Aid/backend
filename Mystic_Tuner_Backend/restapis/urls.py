from django.http import HttpResponse
from django.urls import path
from .views import AuthenticateLoginTokenAPIView, SuggestionsAPIView

urlpatterns = [
    path('Authenticate/', AuthenticateLoginTokenAPIView.as_view(), name='Authenticate'),
    path("health-check/", lambda request: HttpResponse("OK"), name="health-check"),
    path("", lambda request: HttpResponse("Mystic Tuner Backend API"), name="Mystic Tuner Backend"),
    path("suggestions/", SuggestionsAPIView.as_view(), name="suggestions"),
]