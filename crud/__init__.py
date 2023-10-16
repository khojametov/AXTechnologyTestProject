from crud.base import BaseCRUDService
from models.user import User

user = BaseCRUDService(User)

__all__ = [
    "user",
]
