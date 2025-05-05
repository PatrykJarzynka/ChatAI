import pytest
from models.insert_user_dto import InsertLocalUserDTO
from main import app
from starlette.testclient import TestClient
from models.user_create_dto import UserCreateDTO
from models.user_response_dto import UserResponseDTO
from models.tenant import Tenant
from unittest.mock import Mock
from containers import decode_token, get_user_service
from tables.user import User

mock_local_user_get = User(id=123, tenant_id='123', email='email@a.pl',password='password', tenant=Tenant.LOCAL, full_name='XYZ')
mock_local_user_create = InsertLocalUserDTO(email='email@a.pl',password='password', tenant=Tenant.LOCAL, full_name='XYZ', chats=[])

@pytest.fixture
def user_service():
    mock = Mock()
    mock.get_user_by_tenant_id.return_value = mock_local_user_get
    mock.create_user.return_value = mock_local_user_create
    mock.is_tenant_user_in_db.return_value = False
    mock.is_user_with_provided_email_in_db.return_value = False
    app.dependency_overrides[get_user_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def overrite_decode_microsoft():
    mock = Mock()
    mock.return_value = {"sub": 'test_sub', "email":"test@test.pl", "name": 'test_name'}
    app.dependency_overrides[decode_token] = lambda: mock()
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def overrite_decode_google():
    mock = Mock()
    mock.return_value = {"sub": 'test_sub', "email":"test@test.pl", "given_name": 'test', "family_name":"name"}
    app.dependency_overrides[decode_token] = lambda: mock()
    yield mock
    app.dependency_overrides.clear()

def test_get_user_by_tenant_id(client: TestClient, user_service, overrite_decode_microsoft):
    headers = {"Authorization": "Bearer access_token"}
    expected_response = UserResponseDTO(id=mock_local_user_get.id, email=mock_local_user_get.email, full_name=mock_local_user_get.full_name)

    response = client.get('/user/me', headers=headers)

    assert expected_response.model_dump() == response.json()
    overrite_decode_microsoft.assert_called_once()
    user_service.get_user_by_tenant_id.assert_called_once_with('test_sub')

def test_create_new_user_microsoft(client: TestClient, user_service, overrite_decode_microsoft):
    headers = {"Authorization": "Bearer access_token"}
    expected_user = UserCreateDTO(tenant_id='test_sub', email='test@test.pl', password=None, full_name='test_name', tenant=Tenant.MICROSOFT)

    client.post('/user/microsoft', headers=headers, json={})

    overrite_decode_microsoft.assert_called_once()
    user_service.create_user.assert_called_once_with(expected_user)
    user_service.save_user.assert_called_once_with(mock_local_user_create)

def test_create_new_user_google(client: TestClient, user_service, overrite_decode_google):
    headers = {"Authorization": "Bearer access_token"}
    expected_user = UserCreateDTO(tenant_id='test_sub', email='test@test.pl', password=None, full_name='test name', tenant=Tenant.GOOGLE)

    client.post('/user/google', headers=headers, json={})

    overrite_decode_google.assert_called_once()
    user_service.create_user.assert_called_once_with(expected_user)
    user_service.save_user.assert_called_once_with(mock_local_user_create)
