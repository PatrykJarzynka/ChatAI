from unittest.mock import Mock

import pytest
from starlette.testclient import TestClient
from fastapi import status

from app.models.insert_user_dto import InsertLocalUserDTO
from app.tables.user import User
from services.auth.jwt_service import JWTService
from services.auth.google_service import GoogleService
from services.auth.microsoft_service import MicrosoftService
from main import app
from containers import decode_token, get_user_service
from models.token import Token
from models.tenant import Tenant
from models.user_create_dto import UserCreateDTO

MOCKED_TOKEN = Token(access_token="fake_token", token_type="bearer")
MOCKED_TENANT_TOKEN = {"id_token": 'fake_token'}
MOCKED_TENANT_TOKENS = {"id_token": 'fake_token', "refresh_token": "fake_refresh_token"}

@pytest.fixture
def overrite_jwt():
    mock = Mock()
    mock.create_access_token.return_value = MOCKED_TOKEN
    app.dependency_overrides[JWTService] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def overrite_google():
    mock = Mock()
    mock.refresh_tokens.return_value = MOCKED_TENANT_TOKEN
    mock.fetch_tokens.return_value = MOCKED_TENANT_TOKENS
    app.dependency_overrides[GoogleService] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def overrite_microsoft():
    mock = Mock()
    mock.refresh_tokens.return_value = MOCKED_TENANT_TOKEN
    mock.fetch_tokens.return_value = MOCKED_TENANT_TOKENS
    app.dependency_overrides[MicrosoftService] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def overrite_decode():
    mock = Mock()
    mock.return_value = {"sub": 'test_sub'}
    app.dependency_overrides[decode_token] = lambda: mock()
    yield mock
    app.dependency_overrides.clear()

def test_login_success(client: TestClient, overrite_jwt: Mock):
    mock_user = Mock()
    mock_user.id = 123

    mock_user_service = Mock()
    mock_user_service.authenticate_local_user.return_value = mock_user

    app.dependency_overrides[get_user_service] = lambda: mock_user_service

    response = client.post('/auth/login', data={
        "username": "test@test.pl",
        "password": "Test123.",
    })

    assert response.status_code == 200
    assert response.json() == MOCKED_TOKEN.model_dump()

    mock_user_service.authenticate_local_user.assert_called_once_with("test@test.pl", "Test123.")
    overrite_jwt.create_access_token.assert_called_once_with({"sub": "123"})

def test_login_wrong_credentials(client: TestClient, overrite_jwt: Mock):
    mock_user_service = Mock()
    mock_user_service.authenticate_local_user.return_value = False

    app.dependency_overrides[get_user_service] = lambda: mock_user_service

    response = client.post('/auth/login', data={
        "username": 'wrong_username',
        "password": 'wrong_password',
    })

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect username or password"}

    mock_user_service.authenticate_local_user.assert_called_once_with("wrong_username", "wrong_password")
    overrite_jwt.create_access_token.assert_not_called()

def test_register_successfully(client: TestClient, overrite_jwt):
    expected_id = str(1)
    mock_user = InsertLocalUserDTO(email='email@a.pl',password='password', tenant=Tenant.LOCAL, full_name='XYZ', chats=[])

    mock_user_service = Mock()
    mock_user_service.create_user.return_value = mock_user
    mock_user_service.save_user.return_value = None

    app.dependency_overrides[get_user_service] = lambda: mock_user_service

    response = client.post('/auth/register', json={
    "full_name": 'XYZ',
    "email": "test@test.pl",
    "password": "Test123.",
    "tenant": Tenant.LOCAL
    })

    assert response.status_code == 200
    assert response.json() == MOCKED_TOKEN.model_dump()

    mock_user_service.create_user.assert_called_once_with(UserCreateDTO(email="test@test.pl", full_name="XYZ", password="Test123.", tenant=Tenant.LOCAL))

    assert mock_user_service.save_user.call_count == 2

    first_user_call = mock_user_service.save_user.call_args_list[0][0][0]
    assert first_user_call.tenant_id is None

    second_user_call = mock_user_service.save_user.call_args_list[1][0][0]
    assert second_user_call.tenant_id == expected_id

    overrite_jwt.create_access_token.assert_called_once_with({"sub": "123"})

@pytest.mark.parametrize('refresh_token, tenant',[(None,Tenant.LOCAL),('refresh_token',Tenant.GOOGLE),('refresh_token',Tenant.MICROSOFT),('refresh_token',Tenant.LOCAL),('refresh_token','custom_tenant')])
def test_refresh_token(client: TestClient, overrite_jwt, overrite_google, overrite_microsoft, overrite_decode, refresh_token: str | None, tenant: Tenant):

    mock_user_service = Mock()
    mock_user_service.get_user_by_tenant_id.return_value = User(id=123, tenant_id='123', email='email@a.pl',password='password', tenant=tenant, full_name='XYZ')


    app.dependency_overrides[get_user_service] = lambda: mock_user_service


    headers = {"Authorization": "Bearer access_token"}
    body = {"refresh_token": refresh_token}

    response = client.post('/auth/refresh', headers=headers, json=body)

    if not refresh_token:
        assert response.status_code == 400
        assert response.json()['detail'] == 'No refresh token provided!'
            
    elif tenant == Tenant.LOCAL:
        assert response.status_code == 200
        assert response.json() == MOCKED_TOKEN.model_dump()['access_token']
        overrite_jwt.create_access_token.assert_called_once_with({"sub": "123"})

    elif tenant == Tenant.GOOGLE:
        assert response.status_code == 200
        assert response.json() == 'fake_token'
        overrite_google.refresh_tokens.assert_called_once_with(refresh_token)

    elif tenant == Tenant.MICROSOFT:
        assert response.status_code == 200
        assert response.json() == 'fake_token'
        overrite_microsoft.refresh_tokens.assert_called_once_with(refresh_token)

    overrite_decode.assert_called_once()


def test_get_microsoft_tokens(client: TestClient, overrite_microsoft):
    expected_response = {
        'refresh_token': MOCKED_TENANT_TOKENS['refresh_token'],
        'access_token': MOCKED_TENANT_TOKENS['id_token']
    }

    headers = {"Authorization": "Bearer 'access_token"}
    body = {
        "code": 'auth_code'
    }

    response = client.post('/auth/microsoft', headers=headers, json=body)

    assert response.json() == expected_response
    overrite_microsoft.fetch_tokens.assert_called_once_with('auth_code')
    


def test_get_google_tokens(client: TestClient, overrite_google):
    expected_response = {
        'refresh_token': MOCKED_TENANT_TOKENS['refresh_token'],
        'access_token': MOCKED_TENANT_TOKENS['id_token']
    }

    headers = {"Authorization": "Bearer 'access_token"}
    body = {
        "code": 'auth_code'
    }

    response = client.post('/auth/google', headers=headers, json=body)

    assert response.json()  == expected_response
    overrite_google.fetch_tokens.assert_called_once_with('auth_code')
        
        

