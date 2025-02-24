from django.urls import path
from . import views

urlpatterns = [
    path('Authenticate/', views.AuthenticateLogin, name='Authenticate'),
]