import pytest
from main import app
from starlette.testclient import TestClient
from models.user_response_dto import UserResponseDTO
from enums.tenant import Tenant
from unittest.mock import Mock
from containers import get_user_service, authorize_no_role
from tables.user import User

mock_local_user_get = User(id=123, external_user_id='123', email='email@a.pl',password='password', tenant=Tenant.LOCAL, full_name='XYZ')

@pytest.fixture
def user_service():
    mock = Mock()
    mock.get_user_by_external_user_id.return_value = mock_local_user_get
    mock.is_tenant_user_in_db.return_value = False
    mock.is_user_with_provided_email_in_db.return_value = False
    app.dependency_overrides[get_user_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def overrite_decode_microsoft():
    mock = Mock()
    mock.return_value = {"sub": 'test_sub', "email":"test@test.pl", "name": 'test_name'}
    app.dependency_overrides[authorize_no_role] = lambda: mock()
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def overrite_decode_google():
    mock = Mock()
    mock.return_value = {"sub": 'test_sub', "email":"test@test.pl", "given_name": 'test', "family_name":"name"}
    app.dependency_overrides[authorize_no_role] = lambda: mock()
    yield mock
    app.dependency_overrides.clear()

def test_get_user_by_external_user_id(client: TestClient, user_service, overrite_decode_microsoft):
    headers = {"Authorization": "Bearer access_token"}
    expected_response = UserResponseDTO(id=mock_local_user_get.id, email=mock_local_user_get.email, full_name=mock_local_user_get.full_name)

    response = client.get('/user/me', headers=headers)

    assert expected_response.model_dump() == response.json()
    overrite_decode_microsoft.assert_called_once()
    user_service.get_user_by_external_user_id.assert_called_once_with('test_sub')

def test_create_new_user_microsoft(client: TestClient, user_service, overrite_decode_microsoft):
    headers = {"Authorization": "Bearer access_token"}
    decoded = overrite_decode_microsoft.return_value
    
    expected_user = User(email=decoded['email'],password=None, external_user_id=decoded['sub'], full_name=decoded['name'], tenant=Tenant.MICROSOFT)

    client.post('/user/microsoft', headers=headers, json={})

    overrite_decode_microsoft.assert_called_once()
    user_service.save_user.assert_called_once_with(expected_user)

def test_create_new_user_google(client: TestClient, user_service, overrite_decode_google):
    headers = {"Authorization": "Bearer access_token"}
    decoded = overrite_decode_google.return_value
    expected_full_name = f"{decoded['given_name']} {decoded['family_name']}"
    

    expected_user = User(email=decoded['email'], password=None, external_user_id=decoded['sub'], full_name=expected_full_name, tenant=Tenant.GOOGLE)

    client.post('/user/google', headers=headers, json={})

    overrite_decode_google.assert_called_once()
    user_service.save_user.assert_called_once_with(expected_user)
