import pytest
from typing import cast
from pydantic import EmailStr
from sqlmodel import Session
from starlette.testclient import TestClient
from services.auth.jwt_service import JWTService
from services.auth.hash_service import HashService
from services.user_service import UserService
from app_types.user_create_dto import UserCreateDTO
from app_types.user_response_dto import UserResponseDTO
from app_types.auth_provider import AuthProvider

@pytest.fixture()
def jwt_service():
    return JWTService()

@pytest.fixture
def hash_service():
    return HashService()

@pytest.fixture
def user_service(session: Session, hash_service):
    return UserService(session, hash_service)

def test_get_user_by_id_with_valid_token(session: Session, client: TestClient, jwt_service: JWTService, user_service: UserService):
    create_user_data = UserCreateDTO(email=cast(EmailStr, 'test@test.pl'), password='Test123.', full_name='TestName', provider=AuthProvider.LOCAL)
    testUser = user_service.create_user(create_user_data)
    user_service.save_user(testUser)

    test_token = jwt_service.create_access_token({"sub": str(testUser.id)})
    headers = {"Authorization": f"Bearer {test_token.access_token}"}

    response = client.get('/user/me', headers=headers)
    data = response.json()

    assert response.status_code == 200
    assert data == UserResponseDTO(id=testUser.id, full_name=testUser.full_name, email=testUser.email).model_dump()

def test_get_user_by_id_with_invalid_token(session: Session, client: TestClient):
    response = client.get('/user/me')
    data = response.json()

    assert response.status_code == 401
    assert data == {"detail": "Not authenticated"}
