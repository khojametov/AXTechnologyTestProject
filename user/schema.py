from typing import Optional

from pydantic import BaseModel


class ListUserSchema(BaseModel):
    id: int
    email: str


class RetrieveUserSchema(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    is_admin: bool


class UpdateUserSchema(BaseModel):
    full_name: str
