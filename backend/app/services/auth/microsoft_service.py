import requests
import jwt
from jwt.algorithms import RSAAlgorithm
from config import get_settings
from models.token_service_config import TokenServiceConfig
from interfaces.auth_token_service import AuthTokenService
from utilities.microsoft_public_keys_provider import MicrosoftPublicKeysProvider


class MicrosoftService(AuthTokenService):
    def __init__(self):
        settings = get_settings()
        config = TokenServiceConfig(client_id=settings.MICROSOFT_CLIENT_ID, secret=settings.MICROSOFT_SECRET, redirect_url=settings.REDIRECT_URL, auth_url=settings.MICROSOFT_AUTH_URL)
        super().__init__(config)

        self.public_keys_provider = MicrosoftPublicKeysProvider()
        
    def decode_token(self, access_token: str) -> dict:
        rsa_key = self.public_keys_provider.get_rsa_key(access_token)
        public_key = RSAAlgorithm.from_jwk(rsa_key)

        decoded_token = jwt.decode(
            access_token,
            key=public_key,
            algorithms=["RS256"],
            audience=self.CLIENT_ID,
            issuer=rsa_key["issuer"],
        )
        
        return decoded_token

    def fetch_tokens(self, auth_code: str) -> dict:
        data = {
        "code": auth_code,
        "client_id": self.CLIENT_ID,
        "client_secret": self.CLIENT_SECRET,
        "scope": 'openid profile email',
        "redirect_uri": self.REDIRECT_URL,
        "grant_type": 'authorization_code'
        }

        response = requests.post(self.AUTH_URL, data=data)
        return response.json()
    
    def refresh_tokens(self, refresh_token: str):
        data = {
        "client_id": self.CLIENT_ID,
        "client_secret": self.CLIENT_SECRET,
        "refresh_token": refresh_token,
        "grant_type": 'refresh_token'
        }

        response = requests.post(self.AUTH_URL, data=data)
        return response.json()
