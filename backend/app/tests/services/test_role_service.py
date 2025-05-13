from unittest.mock import Mock, patch
from fastapi import HTTPException, status
import pytest
import requests

from config import get_settings
from enums.role import Role
from services.role_service import RoleService

role_service_url = get_settings().ROLE_SERVICE_URL

@pytest.fixture
def role_service() -> RoleService:
    return RoleService()

def test_save_user_default_role(role_service: RoleService):
    user_id = 1

    with patch('requests.post', return_value=None) as mock_post:
        role_service.save_user_default_role(user_id)

    mock_post.assert_called_once_with(role_service_url + '/role/default', json={user_id})

def test_autorize_role_success(role_service: RoleService):
    role = Role.ADMIN
    user_id = 1
    expected_body = {"role": role, "user_id": user_id}

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = True

    with patch('requests.post', return_value=mock_response) as mock_post:
        result = role_service.autorize_role(role=role, user_id=user_id)

    mock_post.assert_called_once_with(role_service_url + '/role/authorize', json=expected_body)
    assert result == True

def test_autorize_role_exception(role_service: RoleService):
    role = Role.ADMIN
    user_id = 1
    expected_body = {"role": role, "user_id": user_id}

    error_response = Mock()
    error_response.status_code = status.HTTP_400_BAD_REQUEST
    error_response.json.return_value = {"detail": "Access denied"}

    mock_http_error = requests.HTTPError(response=error_response)

    with patch('requests.post', side_effect=mock_http_error) as mock_post:
        with pytest.raises(HTTPException) as exc:
            role_service.autorize_role(role=role, user_id=user_id)

    mock_post.assert_called_once_with(role_service_url + '/role/authorize', json=expected_body)
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == 'Access denied'