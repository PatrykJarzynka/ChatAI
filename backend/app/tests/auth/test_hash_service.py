import pytest

from services.auth.hash_service import HashService


@pytest.fixture
def hash_service():
    return HashService()


def test_hash_password(hash_service):
    password = "TestPassword123"

    hashed_password = hash_service.hash_password(password)

    assert hashed_password != password, "Hashed password should not be the same as the original password"

    assert hashed_password.startswith('$2b$'), "Hashed password format should start with $2b$ (bcrypt)"


def test_verify_password(hash_service):
    password = "TestPassword123"

    hashed_password = hash_service.hash_password(password)

    assert hash_service.verify_password(password, hashed_password) == True, "Password verification failed"

    assert hash_service.verify_password("WrongPassword", hashed_password) == False, "Password verification failed"
