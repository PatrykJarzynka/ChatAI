import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool

from app.app_types.token import Token
from app.database import get_session
from app.dependencies import get_jwt_service
from app.main import app
from app.services.auth.jwt_service import JWTService

MOCKED_TOKEN = Token(access_token="fake_token", token_type="bearer")
MOCKED_HASH = 'someHashedPassword'


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
