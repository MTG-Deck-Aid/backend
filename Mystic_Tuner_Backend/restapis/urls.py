from django.urls import path
from .views import *

urlpatterns = [
    path('Authenticate/', AuthenticateLoginTokenAPIView.as_view(), name='Authenticate'),
    path('', HelloWorld.as_view()),
    path('verify-cards/', VerifyCards.as_view())
]