import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from models import User


class TestRegister:
    url = "/auth/register/"

    @pytest.fixture
    def post_data(self):
        return {"email": "qwe@test.com", "password": "qwerty123"}

    def test_ok(
        self,
        session: Session,
        client: TestClient,
        post_data: dict,
    ):
        response = client.post(self.url, json=post_data)

        assert response.status_code == 201
        user = session.execute(
            select(User).where(User.email == post_data["email"])
        ).first()
        assert user


class TestLoginUser:
    url = "/auth/login/"

    @pytest.fixture
    def user__password(self):
        return "some_random_password"

    @pytest.fixture
    def post_data(self, user: User, user__password):
        return {"email": user.email, "password": user__password}

    def test_ok(self, as_user: TestClient, post_data: dict):
        response = as_user.post(self.url, json=post_data)

        assert response.status_code == 200

    def test_invalid_credentials(self, as_user: TestClient, post_data: dict):
        post_data["email"] = "wrong@test.com"
        response = as_user.post(self.url, json=post_data)

        assert response.status_code == 401
