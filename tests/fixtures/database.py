import pytest
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from sqlalchemy.engine.base import Engine
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel import SQLModel

from config.settings import settings
from tests.session import TestSession


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        "sqlite:///./test_db.sqlite",
        echo=settings.SQLALCHEMY_ECHO,
        connect_args={"check_same_thread": False},
    )
    return engine


@pytest.fixture(scope="session")
def _create_database(db_engine: Engine):
    if database_exists(db_engine.url):
        drop_database(db_engine.url)
    create_database(db_engine.url)


@pytest.fixture(scope="session")
def _create_tables(db_engine: Engine, _create_database):
    SQLModel.metadata.create_all(db_engine)
    yield
    SQLModel.metadata.drop_all(db_engine)


@pytest.fixture(scope="session")
def connection(db_engine: Engine, _create_tables):
    with db_engine.connect() as _connection:
        yield _connection


@pytest.fixture(autouse=True)
def session(connection: Connection):
    transaction = connection.begin()

    session = TestSession(bind=connection)

    try:
        yield session
    finally:
        TestSession.remove()
        transaction.rollback()
