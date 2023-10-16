import pytest
from sqlmodel import Session

from config.asgi import init_app
from config.db import get_session


@pytest.fixture
def app(session: Session):
    app = init_app()

    app.dependency_overrides[get_session] = lambda: session

    return app
