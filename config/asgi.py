from fastapi import FastAPI
from fastapi_pagination import add_pagination

from config import routers
from config.settings import settings


def init_app():
    app = FastAPI(debug=settings.DEBUG)
    routers.init_app(app)
    add_pagination(app)
    return app


app = init_app()

__all__ = ["app"]
