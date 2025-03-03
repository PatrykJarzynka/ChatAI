from google.oauth2 import id_token
import google.auth.transport.requests
from dotenv import load_dotenv
import os
import time

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
        
    def validate_iss(self, id_info: dict) -> bool:
        iss = id_info.get('iss')

        if iss != "https://accounts.google.com":
           raise ValueError('Invalid issuer token!')
        else:
            return True
    
    def validate_exp_time(self, id_info: dict) -> bool:
        exp = id_info.get('exp')
        current_time = time.time()

        if exp < current_time:
           raise ValueError('Google token expired!')
        else:
            return True


