import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from core.token import Token
from models import User


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


def _make_api_client(client: TestClient, user: User) -> TestClient:
    token = Token.generate_token_for_user(user)
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest.fixture
def as_user(client: TestClient, user: User) -> TestClient:
    return _make_api_client(client, user)


@pytest.fixture
def as_admin(client: TestClient, user: User) -> TestClient:
    user.is_admin = True
    return _make_api_client(client, user)
