import json
import requests
from jose import jwt 
from jose import jwk
import os
from dotenv import load_dotenv

def get_auth0_public_keys():
    #fetch Auth0's public keys from jwks endpoint
    load_dotenv()
    jwks_url = f"https://{os.getenv('AUTH0_DOMAIN')}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()
    return {key["kid"]: key for key in jwks["keys"]}

def validate_auth0_jwt(token):
    #validate auth0 login token
    try:
        unverified_header = jwt.get_unverified_header(token)
        if "kid" not in unverified_header:
            raise ValueError("Invalid Header: Key ID (kid) missing")
        
        keys = get_auth0_public_keys()
        rsa_key = keys.get(unverified_header["kid"])

        if not rsa_key:
            raise ValueError("Invalid Key: No matching public key found")
        
        public_key = jwk.construct(rsa_key)
        decoded_token = jwt.decode(
            token, 
            public_key,
            algorithms = os.getenv('AUTH0_ALGORITHMS'),
            audience = os.getenv('AUTH0_API_AUDIENCE'),
            issuer = f"https://{os.getenv('AUTH0_DOMAIN')}/"
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired.")
    except jwt.JWTClaimsError:
        raise ValueError("Invalid claims, please check the audience and issuer.")
    except Exception as e:
        raise ValueError(f"Token validation error: {str(e)}")