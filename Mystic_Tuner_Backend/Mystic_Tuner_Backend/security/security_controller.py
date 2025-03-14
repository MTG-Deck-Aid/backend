import json
import os
from dotenv import load_dotenv
import requests
import http.client

class SecurityController:
    """
    Validates that the user is authorized to access the requested endpoint.
    Provides multiple utility functions for security purposes.
    """

    def __init__(self):
        pass

    def get_user_id(self, access_token: str) -> int:
        """
        Call the Auth0 API to get the user ID from the token.
        """
        if not access_token:
            return -1
        
        conn = http.client.HTTPSConnection(os.environ.get("AUTH0_DOMAIN").split("//")[1])
        headers = { 'authorization': f"Bearer {access_token}" }
        conn.request("GET", "/userinfo", headers=headers)
        res = conn.getresponse()
        data = res.read()
        print(data)
        data = json.loads(data.decode("utf-8"))
        print(data)
        return data["sub"]
    
    

def test():
        load_dotenv()


        conn = http.client.HTTPSConnection(os.environ.get("AUTH0_DOMAIN").split("//")[1])
        payload = {
            "client_id": os.environ.get("AUTH0_CLIENT_ID"),
            "client_secret": os.environ.get("AUTH0_CLIENT_SECRET"),
            "audience": f"{os.environ.get('AUTH0_DOMAIN')}/api/v2/",
            "grant_type": "client_credentials"
        }
        payload = json.dumps(payload)
            

        headers = { 'content-type': "application/json" }

        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))

        access_token = data["access_token"]
        print(access_token)

        headers = { 'authorization': f"Bearer {access_token}" }

        conn.request("GET", "/userinfo", headers=headers)

        res = conn.getresponse()
        data = res.read()

        print(data.decode("utf-8"))


# test()