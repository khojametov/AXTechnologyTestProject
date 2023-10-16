import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from models import User


class TestListUser:
    url = "/users/"

    @staticmethod
    def get_user_data(user: User):
        return {"id": user.id, "email": user.email}

    def test_ok(self, user: User, as_admin: TestClient):
        response = as_admin.get(self.url)

        assert response.status_code == 200
        assert response.json()["items"] == [self.get_user_data(user)]


class TestRetrieveUser:
    url = "/users/{}/"

    def test_ok(
        self,
        user: User,
        as_user: TestClient,
    ):
        response = as_user.get(self.url.format(user.id))

        assert response.status_code == 200
        assert response.json() == {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_admin": user.is_admin,
        }


class TestUpdateUser:
    url = "/users/{}/"

    @pytest.fixture
    def update_data(self):
        return {"full_name": "New full name"}

    def test_ok(self, user: User, as_user: TestClient, update_data: dict):
        response = as_user.patch(self.url.format(user.id), json=update_data)

        assert response.status_code == 204
        assert user.full_name == update_data["full_name"]


class TestDeleteUser:
    url = "/users/{}/"

    def test_ok(
        self,
        user: User,
        as_user: TestClient,
        session: Session,
    ):
        response = as_user.delete(self.url.format(user.id))

        assert response.status_code == 204
        assert (
            session.exec(select(User).where(User.id == user.id)).one_or_none() is None
        )
