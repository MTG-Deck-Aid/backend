from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import restapis.auth0_utils

class Auth0JSONWebTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        try:
            decoded_token = auth0_utils.validate_auth0_jwt(token)
            return (decoded_token, None)
        except ValueError as e:
            raise AuthenticationFailed(str(e))