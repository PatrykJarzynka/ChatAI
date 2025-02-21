from typing import cast

import pytest
from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import Session

from app_types.user_create_dto import UserCreateDTO
from db_models.user_model import User
from services.auth.hash_service import HashService
from services.user_service import UserService


@pytest.fixture
def hash_service():
    return HashService()


@pytest.fixture
def user_service(session: Session, hash_service):
    return UserService(session, hash_service)


def test_create_user_successfully(user_service):
    create_user_data = UserCreateDTO(email=cast(EmailStr, 'test@test.pl'), password='Test123.', full_name='TestName')
    new_user = user_service.create_user(create_user_data)

    assert isinstance(new_user, User)
    assert new_user.email == 'test@test.pl'
    assert new_user.full_name == 'TestName'
    assert new_user.password != 'Test123.'


def test_create_user_existing_email(user_service):
    user_service.save_user(User(email='test@test.pl', full_name='TestName', password='SomeHashedPassword'))

    create_user_data = UserCreateDTO(email=cast(EmailStr, 'test@test.pl'), password='Test123.', full_name='TestName2')

    with pytest.raises(HTTPException) as exc_info:
        user_service.create_user(create_user_data)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == 'Email already registered'


def test_authenticate_user_successfully(user_service):
    create_user_data = UserCreateDTO(email=cast(EmailStr, 'test@test.pl'), password='Test123.', full_name='TestName2')
    user = user_service.create_user(create_user_data)  # create new user with hashed password
    user_service.save_user(user)

    authenticated_user = user_service.authenticate_user(email='test@test.pl', password='Test123.')

    assert authenticated_user is not False


def test_authenticate_user_wrong_password(user_service):
    create_user_data = UserCreateDTO(email=cast(EmailStr, 'test@test.pl'), password='Test123.', full_name='TestName2')
    user = user_service.create_user(create_user_data)  # create new user with hashed password
    user_service.save_user(user)

    authenticated_user = user_service.authenticate_user(email='test@test.pl', password='Test1234.')

    assert authenticated_user is False


def test_authenticate_not_existing_user(user_service):
    authenticated_user = user_service.authenticate_user(email='test@test.pl', password='Test123.')

    assert authenticated_user is False
