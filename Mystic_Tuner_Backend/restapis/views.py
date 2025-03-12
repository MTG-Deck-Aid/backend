from rest_framework.decorators import api_view
from rest_framework.response import Response
from .scryfall_utils import batch_validate
import json

from Mystic_Tuner_Backend.deck_suggestions.deck_suggestion_controller import CardSuggestionController

# Create your views here.

@api_view(["POST"])
def verify_cards(request):
    try:
        data = request.data
        cardList = data.get("names",[])
        response_data,all_cards_found = batch_validate(cardList)
        if all_cards_found == 1:
            return Response(status = 200)
        else:
            return Response(json.dumps(response_data), status = 422)
    except Exception as e:
        return Response({"error verifying card names": str(e)}, status = 400)
      
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
