import requests
import jwt
from jwt.types import JWKDict
from typing import Dict, Any, List
from config import get_settings


class MicrosoftPublicKeysProvider:
    def __init__(self):
        self.openid_config_url = get_settings().MICROSOFT_OPENID_CONFIG_URL

    def get_openid_config(self) -> Dict[str, Any]:
        response = requests.get(self.openid_config_url)
        return response.json()
    
    def get_jwks_by_config(self, openid_config) -> List[Dict[str, str]]:
        jwks_uri = openid_config["jwks_uri"]
        response = requests.get(jwks_uri)
        return response.json()["keys"]
    
    def get_rsa_key_from_jwks(self, access_token: str, jwks: List[Dict[str, str]]) -> JWKDict | None:
        unverified_header = jwt.get_unverified_header(access_token)
        kid = unverified_header["kid"]

        for key in jwks:
            if key["kid"] == kid:
                return key
        return None
    
    def get_rsa_key(self, access_token: str) -> JWKDict:
        openid_config = self.get_openid_config()
        jwks = self.get_jwks_by_config(openid_config)

        rsa_key = self.get_rsa_key_from_jwks(access_token, jwks)

        if not rsa_key:
            raise ValueError('Invalid public key!')
        
        return rsa_key
    