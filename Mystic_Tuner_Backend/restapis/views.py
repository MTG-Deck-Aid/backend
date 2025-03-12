from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from Mystic_Tuner_Backend.deck_suggestions.deck_suggestion_controller import CardSuggestionController

# Create your views here.
class AuthenticateLoginTokenAPIView(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "This is a verified user!"})
    

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