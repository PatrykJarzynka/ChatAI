from typing import Annotated

from fastapi import Depends

from services.auth.hash_service import HashService
from services.auth.jwt_service import JWTService


def get_jwt_service():
    return JWTService()


def get_hash_service():
    return HashService()


hash_service_dependency = Annotated[HashService, Depends(get_hash_service)]
jwt_service_dependency = Annotated[JWTService, Depends(get_jwt_service)]
