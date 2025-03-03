from typing import cast

import pytest
from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import Session

from app_types.user_create_dto import UserCreateDTO
from db_models.user_model import User
from services.auth.hash_service import HashService
from app_types.auth_provider import AuthProvider
from services.user_service import UserService


@pytest.fixture
def hash_service():
    return HashService()


@pytest.fixture
def user_service(session: Session, hash_service: HashService):
    return UserService(session, hash_service)


def test_create_user_successfully(user_service: UserService):
    create_user_data = UserCreateDTO(email=cast(EmailStr, 'test@test.pl'), password='Test123.', full_name='TestName', provider=AuthProvider.LOCAL)
    new_user = user_service.create_user(create_user_data)

    assert isinstance(new_user, User)
    assert new_user.email == 'test@test.pl'
    assert new_user.full_name == 'TestName'
    assert new_user.password != 'Test123.'


def test_create_user_existing_email(user_service: UserService):
    user_service.save_user(User(email='test@test.pl', full_name='TestName', password='SomeHashedPassword',provider=AuthProvider.LOCAL))

    create_user_data = UserCreateDTO(email=cast(EmailStr, 'test@test.pl'), password='Test123.', full_name='TestName2', provider=AuthProvider.LOCAL)

    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(create_user_data)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == 'Email already registered'


def test_authenticate_local_user_successfully(user_service: UserService):
    create_user_data = UserCreateDTO(email=cast(EmailStr, 'test@test.pl'), password='Test123.', full_name='TestName2', provider=AuthProvider.LOCAL)
    user = user_service.create_user(create_user_data)  # create new user with hashed password
    user_service.save_user(user)

    authenticated_user = user_service.authenticate_local_user(email='test@test.pl', password='Test123.')

    assert authenticated_user is not False


def test_authenticate_local_user_wrong_password(user_service: UserService):
    create_user_data = UserCreateDTO(email=cast(EmailStr, 'test@test.pl'), password='Test123.', full_name='TestName2', provider=AuthProvider.LOCAL)
    user = user_service.create_user(create_user_data)  # create new user with hashed password
    user_service.save_user(user)

    authenticated_user = user_service.authenticate_local_user(email='test@test.pl', password='Test1234.')

    assert authenticated_user is False


def test_authenticate_local_user_not_existing_user(user_service: UserService):
    authenticated_user = user_service.authenticate_local_user(email='test@test.pl', password='Test123.')

    assert authenticated_user is False

def test_authenticate_local_user_google_provider(user_service: UserService):
    google_user_data = UserCreateDTO(email=cast(EmailStr, 'test@test.pl'), password='Test123.', full_name='TestName2', provider=AuthProvider.GOOGLE)
    user = user_service.create_user(google_user_data)
    user_service.save_user(user)

    authenticated_user = user_service.authenticate_local_user(email='test@test.pl', password='Test123.')

    assert authenticated_user is False

def test_get_user_by_id_successfully(user_service: UserService):
    create_user_data = UserCreateDTO(email=cast(EmailStr, 'test@test.pl'), password='Test123.', full_name='TestName2', provider=AuthProvider.LOCAL)
    user = user_service.create_user(create_user_data)  # create new user with hashed password
    user_service.save_user(user)

    found_user = user_service.get_user_by_id(user.id)
    
    assert found_user == user

def test_get_user_by_id_failed(user_service: UserService):

    with pytest.raises(HTTPException) as getting_error:
        user_service.get_user_by_id(1)
    
    assert getting_error.value.detail == 'User not found'

def test_get_user_by_email_successfully(user_service: UserService):
    create_user_data = UserCreateDTO(email=cast(EmailStr, 'test@test.pl'), password='Test123.', full_name='TestName2', provider=AuthProvider.LOCAL)
    user = user_service.create_user(create_user_data)  # create new user with hashed password
    user_service.save_user(user)

    found_user = user_service.get_user_by_email(user.email)
    
    assert found_user == user

def test_get_user_by_email_failed(user_service: UserService):

    with pytest.raises(HTTPException) as getting_error:
        user_service.get_user_by_email('test@test.pl')
    
    assert getting_error.value.detail == 'User not found'

def test_is_user_with_provided_email_in_db_successfully(user_service: UserService):
    create_user_data = UserCreateDTO(email=cast(EmailStr, 'test@test.pl'), password='Test123.', full_name='TestName2', provider=AuthProvider.LOCAL)
    user = user_service.create_user(create_user_data)  # create new user with hashed password
    user_service.save_user(user)

    isExisting = user_service.is_user_with_provided_email_in_db(user.email)
    assert isExisting == True

def test_is_user_with_provided_email_in_db_failed(user_service: UserService):
    isExisting = user_service.is_user_with_provided_email_in_db('test@test.pl')
    assert isExisting == False

