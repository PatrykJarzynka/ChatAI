import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
from functools import lru_cache

env_file = ".env.production" if os.getenv("DOCKER_ENV") == "production" else ".env.development"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env_path = os.path.join(base_dir, env_file)

load_dotenv(env_path, override=True)

class Settings(BaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    MYSQL_DATABASE: str

    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding="utf-8")

@lru_cache
def get_settings():
    return Settings()