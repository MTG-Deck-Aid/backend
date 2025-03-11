from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
import json

from Mystic_Tuner_Backend.scryfall_engine.scryfall_engine import ScryFallEngine

# Create your views here.
class AuthenticateLoginTokenAPIView(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "This is a verified user!"})
    
class HelloWorld(APIView):
    def get(self, request):
        return Response ({"HELLO! from Django"})
    
class VerifyCards(APIView):
    def post(self, request):
        try:
            cards = unpack_file(request)['deckList']
        except ParseError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        engine = ScryFallEngine()
        invalid_cards = []
        for card in cards:
            print(card)
            result = engine.search_card(card['name'])
            if result is None:
                invalid_cards.append(card['name'])

        if len(invalid_cards) > 0:
            return Response({'message': 'Unrecognized cards found', 'data': invalid_cards}, status=status.HTTP_206_PARTIAL_CONTENT)

        return Response({'message': 'All cards identified'}, status=status.HTTP_200_OK)
    
class GetUserDecks(APIView):
    def post(self, request):
        return Response({"TODO"}, status = status.HTTP_418_IM_A_TEAPOT)

class GetDeck(APIView):
    def get(self, request, deck_id = None):

        if(deck_id == None):
            return Response({"TODO"}, status = status.HTTP_418_IM_A_TEAPOT)

        return Response({"TODO"}, status = status.HTTP_418_IM_A_TEAPOT)
    
    def patch(self, request, deck_id = None):
        return Response({"TODO"}, status = status.HTTP_418_IM_A_TEAPOT)


class GetCommander(APIView):
    def get(self, request):
        try:
            commander = unpack_file(request)
        except ParseError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        engine = ScryFallEngine()
        print(commander)
        valid_commander = engine.search_card(commander['commander'])

        # TODO call scryfall engine commander validation command

        if(valid_commander == None):
            return Response({'error': 'commander name not recognized'}, status = status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response({'commander': valid_commander.name}, status=status.HTTP_200_OK)

class CreateNewDeck(APIView):
    def get(self, request):
        return Response({"TODO"}, status = status.HTTP_418_IM_A_TEAPOT)

class GetSuggestions(APIView):
    def get(self, request):
        return Response({"TODO"}, status = status.HTTP_418_IM_A_TEAPOT)


def unpack_file(request):
    file = request.FILES.get('file')

    if not file:
        raise ParseError('No file uploaded')

    try:
        file_data = file.read().decode('utf-8')
        json_data = json.loads(file_data)
        return json_data
    except json.JSONDecodeError:
        raise ParseError('Invalid JSON file')