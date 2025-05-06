from math import e
from typing import cast, Optional

import pytest
from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import Session

from app.models.local_user_data import LocalUserData
from tables.user import User
from services.auth.hash_service import HashService
from models.tenant import Tenant
from services.user_service import UserService
from typing import cast
from unittest.mock import patch


@pytest.fixture
def hash_service():
    return HashService()


@pytest.fixture
def user_service(session: Session, hash_service: HashService):
    return UserService(session, hash_service)

@pytest.fixture
def local_user_fixture(user_service: UserService) -> User:
    hashed_user = user_service.hash_user_password(LocalUserData(email='test@test.pl',password='somePassword',full_name='XYZ'))
    new_user = User(email=hashed_user.email, password=hashed_user.password,full_name=hashed_user.full_name, tenant=Tenant.LOCAL)

    user_service.save_user(new_user)
    new_user.tenant_id = str(new_user.id)
    user_service.save_user(new_user)
    return new_user


def test_hash_password(user_service: UserService):
    initial_user_data = LocalUserData(email='test@test.pl',password='passwordToHash',full_name='XYZ')
    hashed_user = user_service.hash_user_password(initial_user_data)
    
    assert hashed_user.email == initial_user_data.email
    assert hashed_user.full_name == initial_user_data.full_name
    assert hashed_user.password != initial_user_data.password


def test_authenticate_local_user_successfully(user_service: UserService, local_user_fixture: User):
    authenticated_user = user_service.authenticate_local_user(email='test@test.pl', password='some_password')

    assert authenticated_user is not False


def test_authenticate_local_user_wrong_password(user_service: UserService, local_user_fixture: User):
    authenticated_user = user_service.authenticate_local_user(email='test@test.pl', password='Test1234.')

    assert authenticated_user is None


def test_authenticate_local_user_not_existing_user(user_service: UserService):
    authenticated_user = user_service.authenticate_local_user(email='test@test.pl', password='Test123.')

    assert authenticated_user is None

@pytest.mark.parametrize('tenant',[Tenant.GOOGLE, Tenant.MICROSOFT])
def test_authenticate_local_user_no_local_tenant(user_service: UserService, tenant: Tenant):
    new_user = User(email='tenant@email.com', password=None,full_name='XYZ', tenant=tenant, tenant_id='123')
    user_service.save_user(new_user)

    authenticated_user = user_service.authenticate_local_user(email='test@test.pl', password='Test123.')

    assert authenticated_user is None

def test_get_user_by_id_successfully(user_service: UserService, local_user_fixture: User):
    found_user = user_service.get_user_by_id(local_user_fixture.id)
    
    assert found_user == local_user_fixture

def test_get_user_by_id_failed(user_service: UserService):

    with pytest.raises(HTTPException) as getting_error:
        user_service.get_user_by_id(1)
    
    assert getting_error.value.detail == 'User not found'

def test_get_user_by_email_successfully(user_service: UserService, local_user_fixture: User):
    found_user = user_service.get_user_by_email(local_user_fixture.email)
    
    assert found_user == local_user_fixture

def test_get_user_by_email_failed(user_service: UserService):

    with pytest.raises(HTTPException) as getting_error:
        user_service.get_user_by_email('test@test.pl')
    
    assert getting_error.value.detail == 'User not found'

@pytest.mark.parametrize('tenant',[Tenant.GOOGLE, Tenant.MICROSOFT])
def test_get_user_by_tenant_id_successfully(user_service: UserService, tenant: Tenant):
    new_user = User(email='tenant@email.com', password=None,full_name='XYZ', tenant=tenant, tenant_id='123')
    user_service.save_user(new_user)
    
    found_user = user_service.get_user_by_tenant_id(new_user.tenant_id)
    
    assert found_user == new_user

def test_get_user_by_tenant_id_failed(user_service: UserService):

    with pytest.raises(HTTPException) as getting_error:
        user_service.get_user_by_tenant_id('123')
    
    assert getting_error.value.detail == 'User not found'

def test_is_user_with_provided_email_in_db_successfully(user_service: UserService, local_user_fixture: User):
    isExisting = user_service.is_user_with_provided_email_in_db(local_user_fixture.email)
    assert isExisting == True

def test_is_user_with_provided_email_in_db_failed(user_service: UserService):
    isExisting = user_service.is_user_with_provided_email_in_db('test@test.pl')
    assert isExisting == False

