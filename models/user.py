from typing import Optional

from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from sqlmodel import Field

from config.settings import settings
from models.base import BaseModel


class User(BaseModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    email: str = Field(sa_column_kwargs={"unique": True})
    full_name: Optional[str]
    password: Optional[str]
    is_admin: bool = Field(default=False)

    def __str__(self) -> str:
        return f"User #{self.id} - {self.email}"

    def __repr__(self) -> str:
        return f"<User {self.id}>"

    @staticmethod
    def _get_crypto_context() -> CryptContext:
        return CryptContext(schemes=settings.PASSWORD_HASHING_SCHEME)

    @staticmethod
    def hash_password(password_string: str) -> str:
        ctx = User._get_crypto_context()
        return ctx.hash(password_string)

    def set_password(self, password_string):
        self.password = self.hash_password(password_string)

    def check_password(self, password_string: str) -> bool:
        ctx = self._get_crypto_context()
        try:
            return ctx.verify(password_string, self.password)
        except UnknownHashError:
            return False
