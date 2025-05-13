from google.oauth2 import id_token
import google.auth.transport.requests
import requests
from config import get_settings
from interfaces.auth_token_service import AuthTokenService
from models.token_service_config import TokenServiceConfig

class GoogleService(AuthTokenService):

    def __init__(self):
        settings = get_settings()
        config = TokenServiceConfig(client_id=settings.GOOGLE_CLIENT_ID, secret=settings.GOOGLE_SECRET, redirect_url=settings.REDIRECT_URL, auth_url=settings.GOOGLE_AUTH_URL)
        super().__init__(config)

    def decode_token(self, access_token: str) -> dict:
        return id_token.verify_oauth2_token(access_token, google.auth.transport.requests.Request(), audience=self.CLIENT_ID)
        
    def fetch_tokens(self, auth_code: str) -> dict:
        data = {
        "code": auth_code,
        "client_id": self.CLIENT_ID,
        "client_secret": self.CLIENT_SECRET,
        "redirect_uri": self.REDIRECT_URL,
        "grant_type": 'authorization_code',
        }

        response = requests.post(self.AUTH_URL, data=data)
        return response.json()

    def refresh_tokens(self, refresh_token: str) -> dict:
        data = {
        "client_id": self.CLIENT_ID,
        "client_secret": self.CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": 'refresh_token'
        }

        response = requests.post(self.AUTH_URL, data=data)
        return response.json()

    

