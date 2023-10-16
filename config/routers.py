from fastapi import FastAPI

from auth.routes import router as auth_router
from user.routes import router as user_router


def init_app(app: FastAPI):
    app.include_router(auth_router, prefix="/auth")
    app.include_router(user_router, prefix="/users")
