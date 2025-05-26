import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer
from fastapi.testclient import TestClient

from DesafioInfog2.database import get_session
from DesafioInfog2.main import app
from DesafioInfog2.models import table_registry
from DesafioInfog2.security import hash_password
from tests.factories import UserFactory


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client
    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())
        yield _engine


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)
    with Session(engine) as _session:
        yield _session
    table_registry.metadata.drop_all(engine)

@pytest.fixture
def user(session):
    password = "test_password"
    user = UserFactory(password=hash_password(password))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user