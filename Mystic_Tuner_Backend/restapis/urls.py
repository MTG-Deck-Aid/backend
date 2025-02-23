from django.urls import path
from .views import AuthenticateLoginTokenAPIView

urlpatterns = [
    path('Authenticate/', AuthenticateLoginTokenAPIView.as_view(), name='Authenticate'),
]