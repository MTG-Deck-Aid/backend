from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import restapis.auth0_utils

class Auth0JSONWebTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        pass