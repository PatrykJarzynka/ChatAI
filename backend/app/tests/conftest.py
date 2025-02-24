import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_types.token import Token
from database import get_session
from dependencies import get_jwt_service
from main import app
from services.auth.jwt_service import JWTService

MOCKED_TOKEN = Token(access_token="fake_token", token_type="bearer")


@pytest.fixture(name='session')
def session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="jwt_service")
def jwt_service_fixture():
    def get_jwt_service_override():
        jwt_service = JWTService()
        jwt_service.create_access_token = lambda x: MOCKED_TOKEN
        return jwt_service

    app.dependency_overrides[get_jwt_service] = get_jwt_service_override
    yield
    app.dependency_overrides.clear()
