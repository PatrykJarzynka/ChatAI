from google.oauth2 import id_token
import google.auth.transport.requests
import os
import requests

class GoogleService:

    def verify_and_decode_token(self, token: str) -> dict:
        client_id = os.getenv("GOOGLE_CLIENT_ID")

        return id_token.verify_oauth2_token(token, google.auth.transport.requests.Request(), audience=client_id)
        
    def fetch_tokens(self, code: str) -> dict:
        CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        SECRET = os.getenv("GOOGLE_SECRET")
        REDIRECT_URL = os.getenv('REDIRECT_URL')
        AUTH_URL=os.getenv('GOOGLE_AUTH_URL')

        data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": SECRET,
        "redirect_uri": REDIRECT_URL,
        "grant_type": 'authorization_code',
        }

        response = requests.post(AUTH_URL, data=data)
        return response.json()

    def refresh_id_token(self, refresh_token: str) -> dict:
        CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        SECRET = os.getenv("GOOGLE_SECRET")
        AUTH_URL=os.getenv('GOOGLE_AUTH_URL')

        data = {
        "client_id": CLIENT_ID,
        "client_secret": SECRET,
        "refresh_token": refresh_token,
        "grant_type": 'refresh_token'
        }

        response = requests.post(AUTH_URL, data=data)
        return response.json()

    

