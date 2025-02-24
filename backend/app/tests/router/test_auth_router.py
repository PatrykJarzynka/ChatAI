import json
from unittest.mock import patch

import pytest
from sqlmodel import Session, select
from starlette.testclient import TestClient

from db_models.user_model import User
from services.auth.hash_service import HashService
from services.auth.jwt_service import JWTService
from services.user_service import UserService
from main import app
from dependencies import get_jwt_service
from app_types.token import Token

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
    print("override_jwt_service called!")
    return jwt_service


def test_register_successfully(session: Session, client: TestClient):
    app.dependency_overrides[get_jwt_service] = override_jwt_service
   
    response = client.post('/auth/register', json={
    "full_name": 'XYZ',
    "email": "test@test.pl",
    "password": "Test123.",
    })

    data = response.json()
    print(data)

    assert response.status_code == 200
    assert json.dumps(data) == json.dumps(MOCKED_TOKEN.model_dump())

    statement = select(User).where(User.email == 'test@test.pl')
    created_user = session.exec(statement).first()
    assert created_user is not None
    assert created_user.email == 'test@test.pl'
    assert created_user.full_name == 'XYZ'
    assert created_user.password != 'Test123.'


def test_register_existing_email(user_service: UserService, client: TestClient):
    app.dependency_overrides[get_jwt_service] = override_jwt_service

    registered_user = User(email='test@test.pl', full_name='XYZ', password='someHashedPassword')
    user_service.save_user(registered_user)

    response = client.post('/auth/register', json={
    "full_name": 'TestName',
    "email": "test@test.pl",
    "password": "Test123.",
    })

    assert response.status_code == 409
    assert response.json() == {"detail": "Email already registered"}


def test_login_successfully(user_service: UserService, client: TestClient):
    app.dependency_overrides[get_jwt_service] = override_jwt_service

    client.post('/auth/register', json={  # Create user with hashed password
        "full_name": 'TestName',
        "email": "test@test.pl",
        "password": "Test123.",
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
    response = client.get('/auth/refresh', headers=headers)
    data = response.json()
    print(data)

    assert response.status_code == 200

