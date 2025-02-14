from typing import Annotated

from fastapi import Depends

from app.services.auth.hash_service import HashService
from app.services.auth.jwt_service import JWTService


def get_jwt_service():
    return JWTService()


hash_service_dependency = Annotated[HashService, Depends(HashService)]
jwt_service_dependency = Annotated[JWTService, Depends(get_jwt_service)]
