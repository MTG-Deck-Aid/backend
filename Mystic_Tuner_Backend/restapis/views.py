from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from restapis.auth0_authentication import Auth0JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.http import JsonResponse
import urllib.parse
import requests

# Create your views here.
# class AuthenticateLoginTokenAPIView(APIView):
#     authentication_classes = [Auth0JSONWebTokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         return Response({"message": "This is a verified user!"})
    
def AuthenticateLogin(request):
    code = request.GET.get('code')
    token_url = f"https://{settings.AUTH0_DOMAIN}/oauth/token"
    headers = {'Content-Type': 'application/json'}
    body = {
        'grant_type': 'authorization_code',
        'client_id': settings.AUTH0_CLIENT_ID,
        'client_secret': settings.AUTH0_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.AUTH0_CALLBACK_URL,
    }
    response = requests.post(token_url, json=body, headers=headers)
    token_data = response.json()

    if 'error' in token_data:
        return JsonResponse({'error': token_data['error_description']}, status=400)
    
    access_token = token_data.get('access_token')
    id_token = token_data.get('id_token')

    user_info_url = f"https://{settings.AUTH0_DOMAIN}/userinfo"
    user_info_response = requests.get(user_info_url, headers={'Authorization': f'Bearer {access_token}'})
    user_info = user_info_response.json()

    return JsonResponse({'access_token': access_token, 'user_info': user_info})