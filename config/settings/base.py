from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SQLALCHEMY_ECHO: bool = True

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    PASSWORD_HASHING_SCHEME: str = "bcrypt"

    DEBUG: bool = True

    class Config:
        env_file = ".env"
