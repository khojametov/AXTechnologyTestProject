from config.settings.base import Settings as BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./database.sqlite"
    TEST_DATABASE_URL: str = "sqlite:///./test_database.sqlite"
    SQLALCHEMY_ECHO: bool = True

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 6000
    SECRET_KEY: str = "secret_key"
    ALGORITHM: str = "HS256"
    PASSWORD_HASHING_SCHEME: str = "bcrypt"

    DEBUG: bool = True

    class Config:
        env_file = ".env"
