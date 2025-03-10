import json
from unittest.mock import patch

import pytest
from sqlmodel import Session, select
from starlette.testclient import TestClient
from fastapi import HTTPException

from db_models.user_model import User
from services.auth.hash_service import HashService
from services.auth.jwt_service import JWTService
from services.user_service import UserService
from main import app
from dependencies import get_jwt_service
from app_types.token import Token
from app_types.tenant import Tenant

MOCKED_TOKEN = Token(access_token="fake_token", token_type="bearer")

@pytest.fixture
def jwt_service():
    return JWTService()

@pytest.fixture
def hash_service():
    return HashService()


@pytest.fixture
def user_service(session: Session, hash_service):
    return UserService(session, hash_service)

def override_jwt_service():
    jwt_service = JWTService()
    jwt_service.create_access_token = lambda x: MOCKED_TOKEN
    return jwt_service


def test_register_successfully(session: Session, client: TestClient):
    app.dependency_overrides[get_jwt_service] = override_jwt_service
   
    response = client.post('/auth/register', json={
    "full_name": 'XYZ',
    "email": "test@test.pl",
    "password": "Test123.",
    "tenant": Tenant.LOCAL
    })

    data = response.json()

    assert response.status_code == 200
    assert json.dumps(data) == json.dumps(MOCKED_TOKEN.model_dump())

    statement = select(User).where(User.email == 'test@test.pl')
    created_user = session.exec(statement).first()
    assert created_user is not None
    assert created_user.email == 'test@test.pl'
    assert created_user.full_name == 'XYZ'
    assert created_user.password != 'Test123.'
    assert created_user.tenant == Tenant.LOCAL


def test_register_existing_email(user_service: UserService, client: TestClient):
    app.dependency_overrides[get_jwt_service] = override_jwt_service

    registered_user = User(email='test@test.pl', full_name='XYZ', password='someHashedPassword', tenant=Tenant.LOCAL)
    user_service.save_user(registered_user)

    response = client.post('/auth/register', json={
    "full_name": 'TestName',
    "email": "test@test.pl",
    "password": "Test123.",
    "tenant": Tenant.LOCAL
    })

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}


def test_login_successfully(user_service: UserService, client: TestClient):
    app.dependency_overrides[get_jwt_service] = override_jwt_service

    client.post('/auth/register', json={  # Create user with hashed password
        "full_name": 'TestName',
        "email": "test@test.pl",
        "password": "Test123.",
        "tenant": Tenant.LOCAL
    })

    response = client.post('/auth/login', data={
        "username": "test@test.pl",
        "password": "Test123.",
    })

    data = response.json()

    assert response.status_code == 200
    assert json.dumps(data) == json.dumps(MOCKED_TOKEN.model_dump())


def test_login_wrong_credentials(user_service: UserService, client: TestClient):
    app.dependency_overrides[get_jwt_service] = override_jwt_service
    
    client.post('/auth/register', json={  # Create user with hashed password
        "full_name": 'TestName',
        "email": "test@test.pl",
        "password": "Test123.",
        "tenant": Tenant.LOCAL
    })

    response_wrong_username = client.post('/auth/login', data={
        "username": "Test@test.pl",
        "password": "Test123.",
    })

    response_wrong_password = client.post('/auth/login', data={
        "username": "test@test.pl",
        "password": "Test123,",
    })

    assert response_wrong_username.status_code == 401
    assert response_wrong_username.json() == {"detail": "Incorrect username or password"}

    assert response_wrong_password.status_code == 401
    assert response_wrong_password.json() == {"detail": "Incorrect username or password"}

def test_refresh_token(client: TestClient, jwt_service: JWTService):
    test_token = jwt_service.create_access_token({"sub": '1'})
    headers = {"Authorization": f"Bearer {test_token.access_token}"}

    with  patch.object(JWTService, 'decode_access_token', return_value={"sub": "1"}) as mock_decode, \
          patch.object(JWTService, 'create_access_token', return_value=Token(access_token='xyz', token_type='bearer')) as mock_token_create:
        
            response = client.get('/auth/refresh', headers=headers)

            assert response.status_code == 200
            mock_decode.assert_called_once_with(test_token.access_token)
            mock_token_create.assert_called_once_with({"sub": "1"})

def test_verify_token(client: TestClient, jwt_service: JWTService):
    test_token = jwt_service.create_access_token({"sub": '1'})
    headers = {"Authorization": f"Bearer {test_token.access_token}"}

    with  patch.object(JWTService, 'decode_access_token', return_value={"sub": "1"}) as mock_decode:
        response = client.get('/auth/verify', headers=headers)
        data = response.json()

        assert response.status_code == 200
        assert data == test_token.access_token
        mock_decode.assert_called_once_with(test_token.access_token)

def test_verify_token_invalid(client: TestClient, jwt_service: JWTService):
    invalid_token = 'test.token'
    headersTokenInvalid = {"Authorization": f"Bearer {invalid_token}"}

    with  patch.object(JWTService, 'decode_access_token', side_effect=HTTPException(detail="Token error", status_code=401)) as mock_decode:
        responseInvalid = client.get('/auth/verify', headers=headersTokenInvalid)

        mock_decode.assert_called_with(invalid_token)

        assert responseInvalid.status_code == 401

        assert responseInvalid.json() == {'detail': 'Token error'}
        
        

