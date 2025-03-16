import os
import requests
import jose.jwt as jws
class SecurityController:
    """
    Validates that the user is authorized to access the requested endpoint.
    Provides multiple utility functions for security purposes.

    References: 
    [0] - microapis. "Validate JWTs issued by Auth0 in FastAPI" .Youtube. https://www.youtube.com/watch?v=AtmyC945_no&list=PLZGraXskpvb8JX17hMZoYQRmMr0fo97G6&index=3
    """
    jws_well_knowns = f"{os.environ.get('AUTH0_DOMAIN')}/.well-known/jwks.json"
    jws_keys = requests.get(jws_well_knowns).json()["keys"]

    def __init__(self):
        pass

    def _find_public_key(self, kid: str) -> str:
        """
        Finds the public key from the well known jwks.json endpoint.
        Parameters:
            kid: str - The key id of the public key to find.
        """
        for key in self.jws_keys:
            if key["kid"] == kid:
                return key
        return None

    def _validate_jwt_token(self, access_token: str) -> None:
        """
        Validates the access token with asymmetric encrpytion using the public key that signed it from the Auth0 servers.
        Parameters:
            access_token: str - The access token to validate, must be a valid JWT token signed by Auth0 servers.
        """
        unverified_token = jws.get_unverified_header(access_token)
        public_key = self._find_public_key(unverified_token["kid"])
        if not public_key:
            return False
        try:
            jws.decode(token=access_token, key=public_key, audience=os.environ.get("AUTH0_AUDIENCE"), algorithms=["RS256"])
            print("User access token validated.")
        except Exception as e:
            raise Exception(f"Error validating JWT token: {e}")

    def get_user_id(self, access_token: str) -> int:
        """
        Validates the access token and returns the assiocated user id.
        Once verified that the access token is valid we can use the sub claim to get the user id.
        """
        if not access_token:
            return -1
        
        self._validate_jwt_token(access_token)
        return jws.get_unverified_claims(access_token)["sub"] 