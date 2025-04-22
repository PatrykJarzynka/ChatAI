import requests
import jwt
from jwt.algorithms import RSAAlgorithm
from jwt.types import JWKDict


class MicrosoftPublicKeysProvider:
    def __init__(self):
        self.authority = "https://login.microsoftonline.com/common/v2.0"

    def get_openid_config(self):
        openid_config_url = f"{self.authority}/.well-known/openid-configuration"
        response = requests.get(openid_config_url)
        return response.json()
    
    def get_jwks_by_config(self, openid_config):
        jwks_uri = openid_config["jwks_uri"]
        response = requests.get(jwks_uri)
        return response.json()["keys"]
    
    def get_rsa_key_from_jwks(self, access_token, jwks) -> JWKDict | None:
        unverified_header = jwt.get_unverified_header(access_token)
        kid = unverified_header["kid"]

        for key in jwks:
            if key["kid"] == kid:
                return key
        return None
    
    def convert_jwk_to_pem(self, jwk: JWKDict):
        return RSAAlgorithm.from_jwk(jwk)
    
    def get_rsa_key(self, access_token: str):
        openid_config = self.get_openid_config()
        jwks = self.get_jwks_by_config(openid_config)

        rsa_key = self.get_rsa_key_from_jwks(access_token, jwks)

        if not rsa_key:
            raise ValueError('Invalid public key!')
        
        return rsa_key
    