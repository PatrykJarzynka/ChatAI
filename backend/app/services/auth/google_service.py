from google.oauth2 import id_token
import google.auth.transport.requests
from app_types.google_tokens import GoogleTokens
from dotenv import load_dotenv
import os
import requests

env_file = ".env.production" if os.getenv("DOCKER_ENV") == "production" else ".env.development"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_path = os.path.join(base_dir, env_file)

load_dotenv(env_path)

class GoogleService:

    def verify_and_decode_token(self, token: str) -> dict:
        client_id = os.getenv("GOOGLE_CLIENT_ID")

        try:
            return id_token.verify_oauth2_token(token, google.auth.transport.requests.Request(), audience=client_id)
        except:
            raise ValueError('Not authenicated!')
        
    def fetch_tokens(self, code: str) -> dict:
        CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        SECRET = os.getenv("GOOGLE_SECRET")

        data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": SECRET,
        "redirect_uri": 'postmessage',
        "grant_type": 'authorization_code'
        }

        response = requests.post('https://oauth2.googleapis.com/token', data=data)
        return response.json()

    def refresh_id_token(self, refresh_token: str) -> dict:
        CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        SECRET = os.getenv("GOOGLE_SECRET")

        data = {
        "client_id": CLIENT_ID,
        "client_secret": SECRET,
        "refresh_token": refresh_token,
        "grant_type": 'refresh_token'
        }

        response = requests.post('https://oauth2.googleapis.com/token', data=data)
        return response.json()

    

