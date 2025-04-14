import os
import requests
import jwt
from jwt.algorithms import RSAAlgorithm
from jwt.types import JWKDict
from config import get_settings


class MicrosoftService:
    def __init__(self):
        self.client_id = get_settings().MICROSOFT_CLIENT_ID
        self.authority = "https://login.microsoftonline.com/common/v2.0"

    def get_openid_config(self):
        openid_config_url = f"{self.authority}/.well-known/openid-configuration"
        response = requests.get(openid_config_url)
        return response.json()
    
    def get_jwks(self, openid_config):
        jwks_uri = openid_config["jwks_uri"]
        response = requests.get(jwks_uri)
        return response.json()["keys"]
    
    def get_rsa_key(self, access_token, jwks) -> JWKDict | None:
        unverified_header = jwt.get_unverified_header(access_token)
        kid = unverified_header["kid"]

        for key in jwks:
            if key["kid"] == kid:
                return key
        return None
    
    def convert_jwk_to_pem(self, jwk: JWKDict):
        return RSAAlgorithm.from_jwk(jwk)

    
    def verify_and_decode_token(self, access_token, rsa_key):
        public_key = self.convert_jwk_to_pem(rsa_key)

        decoded_token = jwt.decode(
            access_token,
            key=public_key,
            algorithms=["RS256"],
            audience=self.client_id,
            issuer=rsa_key["issuer"],
        )
        
        return decoded_token

        
    def validate_token(self, access_token):
        openid_config = self.get_openid_config()
        jwks = self.get_jwks(openid_config)
        rsa_key = self.get_rsa_key(access_token, jwks)

        if not rsa_key:
            raise ValueError('Invalid public key!')

        return self.verify_and_decode_token(access_token, rsa_key)

    def fetch_tokens(self, code: str) -> dict:
        settings = get_settings()
        SECRET = settings.MICROSOFT_SECRET
        REDIRECT_URL = settings.REDIRECT_URL
        AUTH_URL= settings.MICROSOFT_AUTH_URL

        data = {
        "code": code,
        "client_id": self.client_id,
        "client_secret": SECRET,
        "scope": 'openid profile email',
        "redirect_uri": REDIRECT_URL,
        "grant_type": 'authorization_code'
        }

        response = requests.post(AUTH_URL, data=data)
        return response.json()
    
    def refresh_id_token(self, refresh_token: str):
        settings = get_settings()
        SECRET = settings.MICROSOFT_SECRET
        AUTH_URL= settings.MICROSOFT_AUTH_URL

        data = {
        "client_id": self.client_id,
        "client_secret": SECRET,
        "refresh_token": refresh_token,
        "grant_type": 'refresh_token'
        }

        response = requests.post(AUTH_URL, data=data)
        return response.json()
