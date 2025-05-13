from abc import ABC, abstractmethod
from models.token_service_config import TokenServiceConfig

class AuthTokenService(ABC):

    @abstractmethod
    def __init__(self, config: TokenServiceConfig):
        self.CLIENT_ID = config.client_id
        self.CLIENT_SECRET = config.secret
        self.REDIRECT_URL = config.redirect_url
        self.AUTH_URL = config.auth_url

    @abstractmethod
    def fetch_tokens(self, auth_code:str) -> dict:
        pass
    
    @abstractmethod
    def refresh_tokens(self, refresh_token:str) -> dict:
        pass
    
    @abstractmethod
    def decode_token(self, access_token: str) -> dict:
        pass