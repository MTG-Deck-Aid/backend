from django.urls import path
from . import views

urlpatterns = [
    path('Authenticate/', views.AuthenticateLogin, name='Authenticate'),
    #path('api/', include('restapis.urls')),  # Ensure this line is present
    path('getMagicImage/', views.getMagicImage, name='getMagicImage'),
]