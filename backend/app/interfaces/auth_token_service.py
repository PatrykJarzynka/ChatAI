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
    def fetch_tokens(auth_code:str):
        pass
    
    @abstractmethod
    def refresh_tokens(refresh_token:str):
        pass
    
    @abstractmethod
    def decode_token(access_token: str):
        pass