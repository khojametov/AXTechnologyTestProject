from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi_pagination import add_pagination

from config import routers
from config.settings import settings


def init_app():
    app = FastAPI(debug=settings.DEBUG)
    routers.init_app(app)
    add_pagination(app)
    return app


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = init_app()
app.openapi = custom_openapi

__all__ = ["app"]
