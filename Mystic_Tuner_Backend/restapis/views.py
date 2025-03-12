from rest_framework.decorators import api_view
from rest_framework.response import Response
from .scryfall_utils import batch_validate
import json

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