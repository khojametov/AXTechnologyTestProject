from pydantic import BaseModel


class BaseAuthSchema(BaseModel):
    email: str
    password: str


class UserLoginSchema(BaseAuthSchema):
    pass


class UserRegisterSchema(BaseAuthSchema):
    pass
