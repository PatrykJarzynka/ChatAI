import pytest
from unittest.mock import Mock
from enums.role import Role
from enums.tenant import Tenant
from tables.user import User
from utilities.token_validator import TokenValidator
from services.role_service import RoleService
from main import app
from services.auth.google_service import GoogleService
from services.auth.microsoft_service import MicrosoftService
from services.auth.jwt_service import JWTService
from containers import authorize
from fastapi import Request, HTTPException, status

mock_token = {'sub': 'mockTenant'}

@pytest.fixture
def request_mock():
    mock = Mock(spec=Request)
    return mock

@pytest.fixture
def override_jwt_service():
    mock = Mock()
    mock.decode_local_token.return_value = mock_token
    app.dependency_overrides[JWTService] = mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def override_google_service():
    mock = Mock()
    mock.decode_token.return_value = mock_token
    app.dependency_overrides[GoogleService] = mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def override_microsoft_service():
    mock = Mock()
    mock.decode_token.return_value = mock_token
    app.dependency_overrides[MicrosoftService] = mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def override_role_service():
    mock = Mock()
    app.dependency_overrides[RoleService] = mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def overrride_user_service():
    mock = Mock()
    mock.get_user_by_tenant_id.return_value = User(id=123, tenant_id='123', email='email@a.pl',password='password', tenant=Tenant.LOCAL, full_name='XYZ')
    app.dependency_overrides[TokenValidator] = mock
    yield mock
    app.dependency_overrides.clear()

@pytest.fixture
def overrride_token_validator():
    mock = Mock()
    mock.validate_token.return_value = mock_token
    app.dependency_overrides[TokenValidator] = mock
    yield mock
    app.dependency_overrides.clear()
    
@pytest.mark.asyncio
async def test_authorize_missing_authorization_header(override_role_service, overrride_token_validator, overrride_user_service):

    dependency_function = authorize(role=None)
    
    with pytest.raises(HTTPException) as no_auth_header_exec:
        await dependency_function(
            authorization = "",
            role_service = override_role_service,
            token_validator = overrride_token_validator,
            user_service = overrride_user_service
        )

    
    assert no_auth_header_exec.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert no_auth_header_exec.value.detail == "Authorization header missing"

@pytest.mark.asyncio
async def test_authorize_no_role_check(override_role_service, overrride_token_validator, overrride_user_service):
    # override_jwt_service.get_token_issuer.return_value=issuer
    # overrride_token_validator.autorize_role.return_value = True
    mock_auth_header = f"Bearer mock_token"
    dependency_function = authorize(role=None)
    
    result = await dependency_function(
            authorization = mock_auth_header,
            role_service = override_role_service,
            token_validator = overrride_token_validator,
            user_service = overrride_user_service
        )
    
    overrride_token_validator.validate_token.assert_called_once_with(mock_auth_header)
    assert result == mock_token

@pytest.mark.asyncio
async def test_authorize_invalid_role(override_role_service, overrride_token_validator, overrride_user_service):

    mock_auth_header = f"Bearer mock_token"
    dependency_function = authorize(role=Role.ADMIN)

    override_role_service.autorize_role.return_value = False
    
    with pytest.raises(HTTPException) as invalide_role_exec:
        await dependency_function(
            authorization = mock_auth_header,
            role_service = override_role_service,
            token_validator = overrride_token_validator,
            user_service = overrride_user_service
        )
    
    assert invalide_role_exec.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert invalide_role_exec.value.detail == "Permission role restricted."
    overrride_token_validator.validate_token.assert_called_once_with(mock_auth_header)
    overrride_user_service.get_user_by_tenant_id.assert_called_once_with('mockTenant')

@pytest.mark.asyncio
async def test_authorize_valid(override_role_service, overrride_token_validator, overrride_user_service):
    mock_auth_header = f"Bearer mock_token"
    dependency_function = authorize(role=Role.ADMIN)

    override_role_service.autorize_role.return_value = True
    
   
    result = await dependency_function(
        authorization = mock_auth_header,
        role_service = override_role_service,
        token_validator = overrride_token_validator,
        user_service = overrride_user_service
    )

    overrride_token_validator.validate_token.assert_called_once_with(mock_auth_header)
    overrride_user_service.get_user_by_tenant_id.assert_called_once_with('mockTenant')
    assert result == mock_token
    
    






