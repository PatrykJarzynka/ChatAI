import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from functools import lru_cache

env_file = ".env.production" if os.getenv("DOCKER_ENV") == "production" else ".env.development"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_path = os.path.join(base_dir, env_file)

load_dotenv(env_path, override=True)

class Settings(BaseSettings):
    REDIRECT_URL: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    MYSQL_DATABASE: str
    OPENAI_API_KEY: str
    SECRET_KEY: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_SECRET: str
    GOOGLE_SEARCH_API_KEY: str
    GOOGLE_ENGINE_ID: str
    MICROSOFT_SECRET: str
    MICROSOFT_CLIENT_ID: str
    SERPER_API_KEY: str
    AIR_API_KEY: str
    MICROSOFT_AUTH_URL: str
    MICROSOFT_OPENID_CONFIG_URL: str
    GOOGLE_AUTH_URL: str
    AIR_API_URL: str

    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding="utf-8")

@lru_cache
def get_settings():
    return Settings()